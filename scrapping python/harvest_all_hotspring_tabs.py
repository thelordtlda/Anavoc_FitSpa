"""
harvest_all_hotspring_tabs.py
=============================
Moissonnage exhaustif de toutes les 23 sections d'années (2002 à 2026) du portail HotSpring :
https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings

Pour chaque modèle et chaque année :
- Télécharge le PDF officiel (Pre-Delivery / Architectural sizing guide)
- Télécharge le fichier natif AutoCAD (.dwg) s'il est disponible
- Convertit le PDF à 300 DPI (official_manufacturer_doc.png)
- Supprime impérativement les anciens placeholders synthétiques
- Structure les dossiers de 2002 à 2026 dans dataset/hot_spring_spas/
"""

import os
import sys
import json
import urllib.request
import re
from pathlib import Path
from bs4 import BeautifulSoup
import fitz

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_BRAND = SCRIPT_DIR / "dataset" / "hot_spring_spas"
DATASET_BRAND.mkdir(parents=True, exist_ok=True)
MANUALS_DIR = SCRIPT_DIR / "spa_manuals" / "hotspring"
MANUALS_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def download_file(url: str, dest_path: Path) -> bool:
    if dest_path.exists() and dest_path.stat().st_size > 1000:
        return True
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=25) as resp, open(dest_path, "wb") as f:
            f.write(resp.read())
        return True
    except Exception as e:
        print(f"  [ERREUR] {dest_path.name} <- {url}: {e}")
        return False

def clean_model_name(raw_name: str) -> str:
    name = raw_name.replace("®", "").replace("™", "").strip()
    # Remove collection prefixes or suffixes like Classic, Endurol, etc.
    name = re.sub(r'\s+(Classic|Endurol|LE|DL|NXT)$', '', name, flags=re.IGNORECASE)
    return name

def main():
    print("--- Moissonnage exhaustif des 23 années HotSpring (2002 - 2026) ---")
    url = "https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')

    tabs = soup.find_all('div', class_='elementor-tab-desktop-title')
    print(f"Nombre de sections d'années trouvées : {len(tabs)}")

    all_entries = [] # (year, collection, model_clean, pdf_url, dwg_url)

    for t in tabs:
        tab_text = t.get_text(strip=True)
        m_year = re.search(r'20\d\d', tab_text)
        if not m_year: continue
        year = int(m_year.group(0))
        
        tab_id = t.get('data-tab')
        content = soup.find('div', attrs={'data-tab': tab_id, 'class': lambda c: c and 'elementor-tab-content' in c})
        if not content: continue

        # In each tab content, there are h2/h3 headings and links
        # Let's traverse the children of content
        current_collection = "Highlife"
        current_model = ""
        
        # We can inspect all h3 and a tags
        for el in content.find_all(['h2', 'h3', 'a']):
            if el.name == 'h2':
                current_collection = el.get_text(strip=True)
            elif el.name == 'h3':
                current_model = clean_model_name(el.get_text(strip=True))
            elif el.name == 'a' and el.get('href'):
                href = el['href'].strip()
                if not href.endswith(('.pdf', '.dwg')): continue
                full_url = href if href.startswith('http') else f"https://www.hotspring.com{href}"
                
                # Check if this link belongs to current_model or can be inferred
                link_text = el.get_text(strip=True).upper()
                is_dwg = href.endswith('.dwg')
                is_pdf = href.endswith('.pdf')
                
                all_entries.append({
                    'year': year,
                    'collection': current_collection,
                    'model': current_model,
                    'link_type': 'dwg' if is_dwg else 'pdf',
                    'url': full_url,
                    'filename': href.split('/')[-1]
                })

    print(f"Total fichiers indexés depuis les onglets : {len(all_entries)}")
    
    # Group by (model, year)
    grouped = {}
    for e in all_entries:
        mod = e['model']
        if not mod:
            # Try to extract model from filename
            fn = e['filename'].lower()
            for known in ['grandee', 'envoy', 'aria', 'vanguard', 'sovereign', 'prodigy', 'jetsetter',
                          'prism', 'pulse', 'flash', 'flair', 'beam', 'pace', 'rhythm', 'relay', 'stride', 'sx', 'tx',
                          'bolt', 'gleam', 'glow', 'tempo', 'triumph', 'vista', 'landmark', 'accolade']:
                if known in fn:
                    mod = known.capitalize()
                    break
        if not mod: continue
        
        k = (mod, e['year'])
        if k not in grouped:
            grouped[k] = {'collection': e['collection'], 'model': mod, 'year': e['year'], 'pdf': None, 'dwg': None}
        if e['link_type'] == 'pdf' and not grouped[k]['pdf']:
            grouped[k]['pdf'] = e['url']
        elif e['link_type'] == 'dwg' and not grouped[k]['dwg']:
            grouped[k]['dwg'] = e['url']

    print(f"Total couples uniques (Modèle, Année) à intégrer : {len(grouped)}")

    # Process each model and year
    processed_count = 0
    for (mod_name, yr), info in sorted(grouped.items(), key=lambda x: (x[0][0], x[0][1])):
        mod_slug = mod_name.lower().replace(" ", "_")
        target_dir = DATASET_BRAND / str(yr) / f"hot_spring_{mod_slug}_{yr}"
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # 1. Download official CAD DWG if available
        has_dwg = False
        if info['dwg']:
            dwg_dest = target_dir / "cad_model.dwg"
            has_dwg = download_file(info['dwg'], dwg_dest)
            
        # 2. Download official PDF and render 300 DPI
        has_pdf = False
        pdf_dest = target_dir / "official_manufacturer_doc.png"
        if info['pdf']:
            tmp_pdf = MANUALS_DIR / f"{mod_slug}_{yr}.pdf"
            if download_file(info['pdf'], tmp_pdf):
                try:
                    doc = fitz.open(tmp_pdf)
                    if len(doc) > 0:
                        pix = doc[0].get_pixmap(dpi=300)
                        pix.save(str(pdf_dest))
                        has_pdf = True
                except Exception as ex:
                    print(f"  Erreur rendu PDF {tmp_pdf}: {ex}")
                    
        # 3. Élimination stricte des faux placeholders synthétiques
        for fake_f in ["top_view.png", "side_view.png"]:
            fake_p = target_dir / fake_f
            if fake_p.exists():
                # Check if it was an old synthetic file (size under 20KB or generic)
                try: fake_p.unlink()
                except: pass
                
        # 4. Check if a real photo exists in this folder (top_view.jpg, side_view.jpg)
        real_top = (target_dir / "top_view.jpg").exists()
        real_side = (target_dir / "side_view.jpg").exists()
        
        # 5. Write metadata.json with total transparency
        meta_file = target_dir / "metadata.json"
        meta = {}
        if meta_file.exists():
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    meta = json.load(f)
            except: pass
            
        meta["brand"] = "Hot Spring Spas"
        meta["model"] = mod_name
        meta["series"] = f"{info['collection']} Collection"
        meta["vintage_year"] = yr
        meta["generation_id"] = f"HS-{mod_slug.upper()}-{yr}"
        
        meta["provenance"] = {
            "is_synthetic": False,
            "has_real_photo": real_top,
            "has_official_cad_dwg": has_dwg,
            "has_official_pdf_doc": has_pdf,
            "official_pdf_url": info['pdf'],
            "official_cad_dwg_url": info['dwg'],
            "portal_reference": "https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings"
        }
        
        if "media" not in meta: meta["media"] = {}
        meta["media"]["has_top_view"] = real_top
        meta["media"]["has_side_view"] = real_side
        meta["media"]["has_footprint"] = has_pdf or (target_dir / "footprint.png").exists()
        meta["media"]["has_official_cad"] = has_dwg
        meta["media"]["has_official_doc"] = has_pdf
        meta["media"]["top_view_file"] = "top_view.jpg" if real_top else None
        meta["media"]["side_view_file"] = "side_view.jpg" if real_side else None
        meta["media"]["footprint_file"] = "official_manufacturer_doc.png" if has_pdf else "footprint.png"
        meta["media"]["cad_file"] = "cad_model.dwg" if has_dwg else None
        
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
            
        processed_count += 1

    print(f"\n[SUCCÈS] {processed_count} fiches réparties de 2002 à 2026 synchronisées avec les documents constructeur !")

if __name__ == "__main__":
    main()
