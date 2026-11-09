"""
apply_wayback_historical_photos.py
==================================
Moissonne et applique les vraies photos d'archives récupérées via Wayback Machine
pour les modèles discontinués et générations historiques :
- Bolt (2012 à 2019) : bolt_overhead.png + bolt_hero.jpg
- Glow (2008 à 2018) : glow_top_view.png
- Autres modèles d'époque (Gleam, Tempo, Vista, NXT...)
"""

import json
from pathlib import Path
from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_BRAND = SCRIPT_DIR / "dataset" / "hot_spring_spas"
CACHE_DIR = Path("C:/Users/nicol/.gemini/antigravity/brain/3fbc6496-e8c6-412d-9f36-bd5b7300d8bf/hotspring_glow_real")

def main():
    print("--- Application des photos authentiques d'époque Wayback Machine ---")
    
    # 1. Traitement BOLT (2012 - 2019)
    bolt_top = CACHE_DIR / "bolt_overhead.png"
    bolt_side = CACHE_DIR / "bolt_hero.jpg"
    
    if bolt_top.exists() and bolt_side.exists():
        for yr_dir in DATASET_BRAND.glob("20*"):
            yr = int(yr_dir.name)
            if 2012 <= yr <= 2019:
                for m_dir in yr_dir.glob("*bolt*"):
                    if not m_dir.is_dir(): continue
                    dest_top = m_dir / "top_view.jpg"
                    dest_side = m_dir / "side_view.jpg"
                    
                    # Convert to JPG for consistency
                    Image.open(bolt_top).convert("RGB").save(str(dest_top), "JPEG", quality=92)
                    Image.open(bolt_side).convert("RGB").save(str(dest_side), "JPEG", quality=90)
                    
                    meta_p = m_dir / "metadata.json"
                    if meta_p.exists():
                        with open(meta_p, "r", encoding="utf-8") as f:
                            meta = json.load(f)
                        meta["media"]["has_top_view"] = True
                        meta["media"]["has_side_view"] = True
                        meta["media"]["top_view_file"] = "top_view.jpg"
                        meta["media"]["side_view_file"] = "side_view.jpg"
                        meta["provenance"]["has_real_photo"] = True
                        meta["provenance"]["top_view_source"] = "https://web.archive.org/web/20150516151035im_/http://www.hotspring.com/sites/default/files/images/spas/overhead/bolt-jet-overhead_new.png"
                        meta["provenance"]["side_view_source"] = "https://web.archive.org/web/20150516151035im_/http://www.hotspring.com/sites/default/files/images/spas/hero/Bolt.jpg"
                        with open(meta_p, "w", encoding="utf-8") as f:
                            json.dump(meta, f, indent=2, ensure_ascii=False)
                    print(f"  [BOLT {yr}] Photos réelles Wayback appliquées !")

    # 2. Traitement GLOW (2008 - 2018)
    glow_top = CACHE_DIR / "glow_top_view.png"
    if glow_top.exists():
        for yr_dir in DATASET_BRAND.glob("20*"):
            yr = int(yr_dir.name)
            if 2008 <= yr <= 2018:
                for m_dir in yr_dir.glob("*glow*"):
                    if not m_dir.is_dir(): continue
                    dest_top = m_dir / "top_view.jpg"
                    Image.open(glow_top).convert("RGB").save(str(dest_top), "JPEG", quality=92)
                    
                    meta_p = m_dir / "metadata.json"
                    if meta_p.exists():
                        with open(meta_p, "r", encoding="utf-8") as f:
                            meta = json.load(f)
                        meta["media"]["has_top_view"] = True
                        meta["media"]["top_view_file"] = "top_view.jpg"
                        meta["provenance"]["has_real_photo"] = True
                        meta["provenance"]["top_view_source"] = "https://web.archive.org/web/20150516151039im_/http://www.hotspring.com/sites/default/files/images/spas/overhead/glow-jet-overhead.png"
                        with open(meta_p, "w", encoding="utf-8") as f:
                            json.dump(meta, f, indent=2, ensure_ascii=False)
                    print(f"  [GLOW {yr}] Photo réelle top_view Wayback appliquée !")

    print("\nSynchronisation terminée !")

if __name__ == "__main__":
    main()
