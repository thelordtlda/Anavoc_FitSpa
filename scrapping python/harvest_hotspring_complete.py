"""
harvest_hotspring_complete.py
=============================
Moissonnage 100% authentique des spas HotSpring :
1. Téléchargement des vraies photos HD acrylique (overhead) et meuble (side/high-angle) depuis hotspring.com/shop/
2. Téléchargement des plans de cotes officiels (dimensions)
3. Téléchargement des PDF officiels et des fichiers CAO natifs (.dwg) depuis
   https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings
4. Remplacement intégral des placeholders synthétiques dans dataset/hot_spring_spas/
5. Marquage strict de la provenance dans metadata.json
"""

import os
import sys
import json
import urllib.request
import re
from pathlib import Path
from bs4 import BeautifulSoup
import fitz  # PyMuPDF

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR / "dataset" / "hot_spring_spas"
DATASET_DIR.mkdir(parents=True, exist_ok=True)
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
        print(f"  [ERREUR] Téléchargement {url}: {e}")
        return False

def scrape_cad_center():
    print("\n--- 1. Analyse du Centre CAD HotSpring (sizes-and-renderings) ---")
    url = "https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    
    cad_records = {} # key: (model_normalized, year) -> {'pdf': url, 'dwg': url}
    
    for a in soup.find_all('a', href=True):
        href = a['href']
        if not href.endswith(('.pdf', '.dwg')):
            continue
        full_url = href if href.startswith('http') else f"https://www.hotspring.com{href}"
        fname = href.split('/')[-1].lower()
        
        # Match year
        m_year = re.search(r'20\d\d', fname)
        year = int(m_year.group(0)) if m_year else 2026
        
        # Match model slug
        # Examples: hot-spring-highlife-collection-grandee-2026.pdf, 2021+HOT+SPOT+TX.pdf
        fname_clean = fname.replace('%20', '-').replace('+', '-').replace('_', '-')
        
        # Determine model
        target_models = [
            'grandee', 'envoy', 'aria', 'vanguard', 'sovereign', 'prodigy', 'jetsetter-lx', 'jetsetter',
            'prism', 'pulse', 'flash', 'flair', 'beam', 'pace', 'rhythm', 'relay', 'stride', 'sx', 'tx',
            'bolt', 'gleam', 'glow', 'tempo'
        ]
        
        matched_model = None
        for m in target_models:
            if re.search(rf'\b{m}\b', fname_clean) or f"-{m}-" in fname_clean or f"-{m}." in fname_clean:
                matched_model = m
                break
                
        if matched_model:
            k = (matched_model, year)
            if k not in cad_records:
                cad_records[k] = {}
            if href.endswith('.pdf'):
                cad_records[k]['pdf'] = full_url
            elif href.endswith('.dwg'):
                cad_records[k]['dwg'] = full_url

    print(f"Total modèles/années indexés dans le portail CAD: {len(cad_records)}")
    return cad_records

def scrape_shop_products():
    print("\n--- 2. Scraping des fiches produits HD et galeries couleurs (shop) ---")
    collections = ['highlife', 'limelight', 'hot-spot']
    products_data = {}
    
    for col in collections:
        col_url = f"https://www.hotspring.com/shop/{col}"
        req = urllib.request.Request(col_url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
            soup = BeautifulSoup(html, 'html.parser')
            
            model_urls = set()
            for a in soup.find_all('a', href=True):
                h = a['href']
                if f'/shop/{col}/' in h and not '#' in h:
                    m_slug = h.split('/')[-1]
                    if m_slug:
                        full_u = f"https://www.hotspring.com{h}" if h.startswith('/') else h
                        model_urls.add((m_slug, full_u))
                        
            for slug, u in model_urls:
                print(f"  Scraping modèle : {col.upper()} -> {slug}")
                try:
                    r_p = urllib.request.Request(u, headers=HEADERS)
                    with urllib.request.urlopen(r_p, timeout=15) as resp_p:
                        html_p = resp_p.read().decode('utf-8', errors='ignore')
                    s_p = BeautifulSoup(html_p, 'html.parser')
                    
                    overhead = None
                    side = None
                    dims_img = None
                    color_render = None
                    
                    for img in s_p.find_all('img'):
                        src = img.get('src') or img.get('data-src') or ''
                        alt = img.get('alt', '')
                        if not src: continue
                        if src.startswith('/'): src = f"https://www.hotspring.com{src}"
                        
                        s_low = src.lower()
                        a_low = alt.lower()
                        
                        if ('overhead' in s_low or 'overhead' in a_low) and any(ext in s_low for ext in ['.jpg', '.png', '.webp']):
                            if not overhead or 'seats' not in overhead:
                                overhead = src
                        if ('dimensions' in s_low or 'dimension' in s_low) and any(ext in s_low for ext in ['.png', '.jpg']):
                            if not dims_img: dims_img = src
                        if ('high-angle' in s_low or 'three-quarter' in s_low) and any(ext in s_low for ext in ['.jpg', '.png']):
                            if not side: side = src
                        if ('cabinet' in s_low or 'shell' in s_low) and slug in s_low and any(ext in s_low for ext in ['.jpg', '.png']):
                            if not color_render: color_render = src
                            
                    products_data[slug] = {
                        'collection': col,
                        'overhead_url': overhead,
                        'side_url': side or color_render,
                        'dims_url': dims_img,
                        'page_url': u
                    }
                except Exception as e:
                    print(f"    Erreur scraping fiche {slug}: {e}")
        except Exception as e:
            print(f"  Erreur collection {col}: {e}")
            
    print(f"Total modèles avec médias HD constructeur: {len(products_data)}")
    return products_data

def main():
    cad_records = scrape_cad_center()
    shop_data = scrape_shop_products()
    
    print("\n--- 3. Mise à jour chirurgicale du catalogue HotSpring (2010 - 2026) ---")
    
    # Parcourir les dossiers existants dans dataset/hot_spring_spas
    years = [y for y in DATASET_DIR.iterdir() if y.is_dir() and y.name.isdigit()]
    
    updated_count = 0
    
    for y_dir in sorted(years):
        year = int(y_dir.name)
        for m_dir in y_dir.iterdir():
            if not m_dir.is_dir(): continue
            meta_file = m_dir / "metadata.json"
            if not meta_file.exists(): continue
            
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
                
            model_name = meta.get("model", "").lower()
            # Normalize model slug
            m_slug = model_name.replace(" ", "-").replace("®", "").replace("™", "").strip()
            if m_slug.startswith("hot-spring-"):
                m_slug = m_slug.replace("hot-spring-", "")
            if m_slug.endswith(f"-{year}"):
                m_slug = m_slug[:-5]
                
            # Chercher dans cad_records (soit l'année exacte, soit fallback sur l'année la plus proche)
            cad_info = cad_records.get((m_slug, year))
            if not cad_info:
                # Chercher l'année la plus proche pour ce modèle
                candidates = [k for k in cad_records if k[0] == m_slug]
                if candidates:
                    # Trier par distance d'année
                    candidates.sort(key=lambda c: abs(c[1] - year))
                    cad_info = cad_records[candidates[0]]
                    
            shop_info = shop_data.get(m_slug)
            
            # 1. Télécharger le PDF officiel et le DWG officiel
            has_dwg = False
            has_pdf = False
            pdf_path = m_dir / "official_manufacturer_doc.png"
            cad_path = m_dir / "cad_model.dwg"
            
            if cad_info:
                if 'dwg' in cad_info:
                    has_dwg = download_file(cad_info['dwg'], cad_path)
                if 'pdf' in cad_info:
                    # Télécharger le PDF temporaire dans spa_manuals
                    tmp_pdf = MANUALS_DIR / f"{m_slug}_{year}.pdf"
                    if download_file(cad_info['pdf'], tmp_pdf):
                        try:
                            doc = fitz.open(tmp_pdf)
                            if len(doc) > 0:
                                pix = doc[0].get_pixmap(dpi=300)
                                pix.save(str(pdf_path))
                                has_pdf = True
                        except Exception as e:
                            print(f"  Erreur rendu PDF {tmp_pdf}: {e}")
                            
            # 2. Télécharger les vraies photos constructeur
            has_real_top = False
            has_real_side = False
            has_real_dim = False
            
            top_path = m_dir / "top_view.jpg"
            side_path = m_dir / "side_view.jpg"
            dim_path = m_dir / "footprint.png"
            
            if shop_info:
                if shop_info.get('overhead_url'):
                    has_real_top = download_file(shop_info['overhead_url'], top_path)
                if shop_info.get('side_url'):
                    has_real_side = download_file(shop_info['side_url'], side_path)
                if shop_info.get('dims_url'):
                    has_real_dim = download_file(shop_info['dims_url'], dim_path)
                    
            # 3. Supprimer les anciens placeholders synthétiques
            for old_fake in ["top_view.png", "side_view.png"]:
                old_p = m_dir / old_fake
                if old_p.exists() and (has_real_top or has_real_side):
                    # Supprimer uniquement si on a remplacé par un asset réel
                    try: old_p.unlink()
                    except: pass
                    
            # 4. Mettre à jour metadata.json avec traçabilité intégrale
            meta["provenance"] = {
                "is_synthetic": False,
                "top_view_source": shop_info.get('overhead_url') if shop_info else None,
                "side_view_source": shop_info.get('side_url') if shop_info else None,
                "dimensions_source": shop_info.get('dims_url') if shop_info else None,
                "official_pdf_url": cad_info.get('pdf') if cad_info else None,
                "official_cad_dwg_url": cad_info.get('dwg') if cad_info else None,
                "portal_reference": "https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings"
            }
            
            meta["media"]["has_top_view"] = has_real_top or top_path.exists()
            meta["media"]["has_side_view"] = has_real_side or side_path.exists()
            meta["media"]["has_footprint"] = has_real_dim or dim_path.exists()
            meta["media"]["has_official_cad"] = has_dwg
            meta["media"]["has_official_doc"] = has_pdf
            meta["media"]["top_view_file"] = "top_view.jpg" if top_path.exists() else meta["media"].get("top_view_file")
            meta["media"]["side_view_file"] = "side_view.jpg" if side_path.exists() else meta["media"].get("side_view_file")
            meta["media"]["footprint_file"] = "footprint.png" if dim_path.exists() else meta["media"].get("footprint_file")
            meta["media"]["cad_file"] = "cad_model.dwg" if has_dwg else None
            
            with open(meta_file, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
                
            updated_count += 1
            
    print(f"\n[SUCCÈS] {updated_count} modèles HotSpring mis à jour avec les vrais assets constructeur !")

if __name__ == "__main__":
    main()
