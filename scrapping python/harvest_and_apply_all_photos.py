import json
import urllib.request
from pathlib import Path
from PIL import Image
import fitz # PyMuPDF

base_dir = Path(__file__).resolve().parent
hs_dir = base_dir / "dataset" / "hot_spring_spas"
cache_dir = base_dir / "images" / "hotspring_shop_harvest"
cache_dir.mkdir(parents=True, exist_ok=True)

with open(base_dir / "hotspring_current_shop_images.json", "r", encoding="utf-8") as f:
    shop_data = json.load(f)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

print("--- 1. Téléchargement des photos réelles officielles depuis HotSpring.com ---")
downloaded_assets = {}

for model, info in shop_data.items():
    overhead_url = info.get("overhead")
    side_url = info.get("side")
    
    top_cached = None
    side_cached = None
    
    if overhead_url:
        top_dest = cache_dir / f"{model}_overhead.jpg"
        if not top_dest.exists() or top_dest.stat().st_size < 5000:
            try:
                print(f"Téléchargement overhead {model}: {overhead_url.split('/')[-1]}...")
                req = urllib.request.Request(overhead_url, headers=headers)
                with urllib.request.urlopen(req, timeout=20) as resp:
                    top_dest.write_bytes(resp.read())
            except Exception as e:
                print(f"  Erreur overhead {model}: {e}")
        if top_dest.exists() and top_dest.stat().st_size > 5000:
            top_cached = top_dest

    if side_url:
        side_dest = cache_dir / f"{model}_side.jpg"
        if not side_dest.exists() or side_dest.stat().st_size < 5000:
            try:
                print(f"Téléchargement side {model}: {side_url.split('/')[-1]}...")
                req = urllib.request.Request(side_url, headers=headers)
                with urllib.request.urlopen(req, timeout=20) as resp:
                    side_dest.write_bytes(resp.read())
            except Exception as e:
                print(f"  Erreur side {model}: {e}")
        if side_dest.exists() and side_dest.stat().st_size > 5000:
            side_cached = side_dest
            
    downloaded_assets[model] = {
        "top": top_cached,
        "side": side_cached,
        "overhead_url": overhead_url,
        "side_url": side_url
    }

print("\n--- 2. Application rigoureuse des photos réelles par millésime ---")
applied_count = 0

for yr_dir in hs_dir.glob("20*"):
    if not yr_dir.is_dir(): continue
    yr = int(yr_dir.name)
    
    for m_dir in yr_dir.iterdir():
        if not m_dir.is_dir(): continue
        meta_p = m_dir / "metadata.json"
        if not meta_p.exists(): continue
        
        with open(meta_p, "r", encoding="utf-8") as f:
            meta = json.load(f)
            
        model_name = meta.get("model", "").lower().strip()
        series = meta.get("series", "")
        
        # Identifier le modèle correspondant dans shop_data
        matched_model = None
        for sm in shop_data.keys():
            # match model name
            if sm in model_name or model_name.replace(" ", "_") == sm or model_name.replace("-", "_") == sm:
                matched_model = sm
                break
                
        if not matched_model: continue
        asset_info = downloaded_assets.get(matched_model, {})
        
        # Pour les millésimes 2024 à 2026 : génération actuelle -> photo 100% exacte
        # Pour la gamme Hot Spot (Rhythm, Relay, Pace, Stride, SX, TX) : cuve acrylique identique depuis 2010 !
        is_current_gen = yr in [2024, 2025, 2026]
        is_hot_spot_historic = ("hot spot" in series.lower() or matched_model in ["rhythm", "relay", "stride", "sx", "tx"]) and 2010 <= yr <= 2023
        
        if is_current_gen or is_hot_spot_historic:
            top_file = asset_info.get("top")
            side_file = asset_info.get("side")
            
            if top_file and top_file.exists():
                dest_top = m_dir / "top_view.jpg"
                Image.open(top_file).convert("RGB").save(str(dest_top), "JPEG", quality=92)
                meta["media"]["has_top_view"] = True
                meta["media"]["top_view_file"] = "top_view.jpg"
                meta["provenance"]["has_real_photo"] = True
                meta["provenance"]["top_view_source"] = asset_info.get("overhead_url", "")
                applied_count += 1
                
            if side_file and side_file.exists() and is_current_gen:
                dest_side = m_dir / "side_view.jpg"
                Image.open(side_file).convert("RGB").save(str(dest_side), "JPEG", quality=90)
                meta["media"]["has_side_view"] = True
                meta["media"]["side_view_file"] = "side_view.jpg"
                meta["provenance"]["side_view_source"] = asset_info.get("side_url", "")

        # Si aucune vraie photo n'a été validée pour ce modèle historique, s'assurer que has_real_photo = False
        top_dest = m_dir / "top_view.jpg"
        if not top_dest.exists() or not meta.get("provenance", {}).get("has_real_photo"):
            meta["provenance"]["has_real_photo"] = False
            meta["media"]["has_top_view"] = False
            
        with open(meta_p, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

print(f"Total photos réelles appliquées : {applied_count}")
print("Mise à jour terminée avec succès !")
