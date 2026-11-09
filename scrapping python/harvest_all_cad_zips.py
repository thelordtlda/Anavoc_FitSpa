"""
harvest_all_cad_zips.py
=======================
Télécharge et extrait l'INTÉGRALITÉ des fichiers CAO natifs (.dwg/.dxf)
depuis les 301 archives .ZIP du portail HotSpring :
https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings

Pour chaque modèle et millésime (2002 à 2021) :
- Télécharge l'archive .zip officielle depuis AWS S3
- Extrait le fichier natif AutoCAD (.dwg ou .dxf)
- Le sauvegarde sous `cad_model.dwg` dans le dossier du modèle
- Met à jour metadata.json (has_official_cad = True)
"""

import os
import sys
import json
import urllib.request
import re
import zipfile
import io
from pathlib import Path
from bs4 import BeautifulSoup

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_BRAND = SCRIPT_DIR / "dataset" / "hot_spring_spas"
ZIPS_CACHE = SCRIPT_DIR / "spa_manuals" / "hotspring_zips"
ZIPS_CACHE.mkdir(parents=True, exist_ok=True)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

def clean_model_name(raw_name: str) -> str:
    name = raw_name.replace("®", "").replace("™", "").strip()
    name = re.sub(r'\s+(Classic|Endurol|LE|DL|NXT)$', '', name, flags=re.IGNORECASE)
    return name

def main():
    print("--- 1. Analyse exhaustive des liens CAD ZIP et DWG sur HotSpring ---")
    url = "https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')

    tabs = soup.find_all('div', class_='elementor-tab-desktop-title')
    print(f"Sections d'années trouvées : {len(tabs)}")

    cad_items = [] # (year, model, zip_or_dwg_url)

    for t in tabs:
        tab_text = t.get_text(strip=True)
        m_year = re.search(r'20\d\d', tab_text)
        if not m_year: continue
        year = int(m_year.group(0))
        
        tab_id = t.get('data-tab')
        content = soup.find('div', attrs={'data-tab': tab_id, 'class': lambda c: c and 'elementor-tab-content' in c})
        if not content: continue

        current_model = ""
        for el in content.find_all(['h3', 'a']):
            if el.name == 'h3':
                current_model = clean_model_name(el.get_text(strip=True))
            elif el.name == 'a' and el.get('href'):
                href = el['href'].strip()
                if '.zip' in href.lower() or href.lower().endswith(('.dwg', '.dxf')):
                    full_url = href if href.startswith('http') else f"https://www.hotspring.com{href}"
                    cad_items.append({
                        'year': year,
                        'model': current_model,
                        'url': full_url,
                        'filename': href.split('/')[-1]
                    })

    print(f"Total fichiers CAO (ZIP + DWG) répertoriés : {len(cad_items)}")

    # Téléchargement et extraction pour chaque modèle
    extracted_count = 0
    errors_count = 0

    known_models = [
        'grandee', 'envoy', 'aria', 'vanguard', 'sovereign', 'prodigy', 'jetsetter',
        'prism', 'pulse', 'flash', 'flair', 'beam', 'pace', 'rhythm', 'relay', 'stride', 'sx', 'tx',
        'bolt', 'gleam', 'glow', 'tempo', 'triumph', 'vista', 'landmark', 'accolade', 'highlife'
    ]

    for item in cad_items:
        yr = item['year']
        mod = item['model']
        fn = item['filename'].lower()
        
        # Deduce model slug if missing
        if not mod:
            for k in known_models:
                if k in fn:
                    mod = k.capitalize()
                    break
        if not mod: continue

        mod_slug = mod.lower().replace(" ", "_").replace("-", "_")
        target_dir = DATASET_BRAND / str(yr) / f"hot_spring_{mod_slug}_{yr}"
        if not target_dir.exists():
            # Chercher un dossier existant qui matche
            yr_dir = DATASET_BRAND / str(yr)
            if yr_dir.exists():
                candidates = [d for d in yr_dir.iterdir() if d.is_dir() and mod_slug in d.name]
                if candidates:
                    target_dir = candidates[0]
                else:
                    target_dir.mkdir(parents=True, exist_ok=True)
            else:
                target_dir.mkdir(parents=True, exist_ok=True)

        dwg_target = target_dir / "cad_model.dwg"
        dxf_target = target_dir / "cad_model.dxf"

        # Si le fichier CAD existe déjà avec une bonne taille (>50KB), on passe
        if (dwg_target.exists() and dwg_target.stat().st_size > 10000) or (dxf_target.exists() and dxf_target.stat().st_size > 10000):
            continue

        cad_url = item['url']
        print(f"[{yr} {mod}] Traitement {cad_url.split('/')[-1]}...")

        try:
            req_c = urllib.request.Request(cad_url, headers=HEADERS)
            with urllib.request.urlopen(req_c, timeout=25) as resp:
                data = resp.read()

            if cad_url.lower().endswith('.zip'):
                # Décompresser le ZIP en mémoire
                with zipfile.ZipFile(io.BytesIO(data)) as z:
                    dwg_files = [f for f in z.infolist() if f.filename.lower().endswith(('.dwg', '.dxf'))]
                    if dwg_files:
                        chosen = dwg_files[0]
                        out_ext = ".dwg" if chosen.filename.lower().endswith('.dwg') else ".dxf"
                        out_file = target_dir / f"cad_model{out_ext}"
                        with z.open(chosen) as zf, open(out_file, "wb") as f_out:
                            f_out.write(zf.read())
                        print(f"  -> Extrait : {out_file.name} ({out_file.stat().st_size} octets)")
                        extracted_count += 1
                    else:
                        print(f"  -> Aucun .dwg/.dxf trouvé dans le ZIP {cad_url}")
            else:
                # Fichier DWG direct
                with open(dwg_target, "wb") as f_out:
                    f_out.write(data)
                print(f"  -> Sauvegardé DWG direct ({dwg_target.stat().st_size} octets)")
                extracted_count += 1

            # Mettre à jour metadata.json
            meta_p = target_dir / "metadata.json"
            meta = {}
            if meta_p.exists():
                try:
                    with open(meta_p, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                except: pass

            if "media" not in meta: meta["media"] = {}
            meta["media"]["has_official_cad"] = True
            meta["media"]["cad_file"] = "cad_model.dwg" if dwg_target.exists() else "cad_model.dxf"

            if "provenance" not in meta: meta["provenance"] = {}
            meta["provenance"]["has_official_cad_dwg"] = True
            meta["provenance"]["official_cad_dwg_url"] = cad_url

            with open(meta_p, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)

        except Exception as e:
            print(f"  [ERREUR] {cad_url}: {e}")
            errors_count += 1

    print(f"\n[RÉSULTAT] {extracted_count} fichiers AutoCAD (.dwg/.dxf) extraits et sauvegardés sur disque !")
    print(f"Erreurs : {errors_count}")

if __name__ == "__main__":
    main()
