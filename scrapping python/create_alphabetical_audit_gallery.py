"""
create_alphabetical_audit_gallery.py
====================================
Génère la galerie d'audit classée par ORDRE ALPHABÉTIQUE DES MODÈLES :
- Regroupement de toutes les années (2002 à 2026) pour un modèle donné (ex. Grandee 2002 -> 2026)
- Permet de voir l'évolution historique du modèle et ses plans techniques
- Distinction stricte et honnête entre vraie photo, plan officiel et photo d'époque manquante
- Barres de navigation rapide par modèle
"""

import json
from pathlib import Path
from collections import defaultdict

DATASET_BRAND = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/hot_spring_spas")
OUTPUT_HTML = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/audit_gallery_hotspring_alphabetical.html")

def main():
    models_dict = defaultdict(list)
    
    # Parcourir tous les dossiers d'années
    years = [y for y in DATASET_BRAND.iterdir() if y.is_dir() and y.name.isdigit()]
    
    total_models_count = 0
    total_dwg_count = 0
    total_pdf_count = 0
    total_real_photo_count = 0
    
    for y_dir in sorted(years, key=lambda x: int(x.name)):
        year = int(y_dir.name)
        for m_dir in sorted(y_dir.iterdir()):
            if not m_dir.is_dir(): continue
            meta_file = m_dir / "metadata.json"
            if not meta_file.exists(): continue
            
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
                
            model = meta.get("model", "Inconnu").strip()
            series = meta.get("series", "")
            dims = meta.get("dimensions", {})
            prov = meta.get("provenance", {})
            media = meta.get("media", {})
            
            # Paths relative to OUTPUT_HTML
            top_p = m_dir / "top_view.jpg"
            side_p = m_dir / "side_view.jpg"
            doc_p = m_dir / "official_manufacturer_doc.png"
            cad_p = m_dir / "cad_model.dwg"
            
            # Strict verification of real photo: must exist and not be an old synthetic file
            has_real_top = top_p.exists() and top_p.stat().st_size > 15000
            has_real_side = side_p.exists() and side_p.stat().st_size > 15000
            has_pdf_doc = doc_p.exists() and doc_p.stat().st_size > 5000
            has_dwg = cad_p.exists() and cad_p.stat().st_size > 1000
            
            top_rel = top_p.relative_to(OUTPUT_HTML.parent).as_posix() if has_real_top else ""
            side_rel = side_p.relative_to(OUTPUT_HTML.parent).as_posix() if has_real_side else ""
            doc_rel = doc_p.relative_to(OUTPUT_HTML.parent).as_posix() if has_pdf_doc else ""
            
            dwg_size_mb = round(cad_p.stat().st_size / (1024*1024), 2) if has_dwg else 0
            
            if has_dwg: total_dwg_count += 1
            if has_pdf_doc: total_pdf_count += 1
            if has_real_top: total_real_photo_count += 1
            total_models_count += 1
            
            models_dict[model].append({
                "year": year,
                "model": model,
                "series": series,
                "dims": f"{dims.get('length_in', 0)}\" x {dims.get('width_in', 0)}\" x {dims.get('height_in', 0)}\" (R: {dims.get('corner_radius_in', 0)}\")",
                "top_img": top_rel,
                "side_img": side_rel,
                "doc_img": doc_rel,
                "has_real_top": has_real_top,
                "has_real_side": has_real_side,
                "has_dwg": has_dwg,
                "dwg_size": dwg_size_mb,
                "dwg_url": prov.get("official_cad_dwg_url", ""),
                "pdf_url": prov.get("official_pdf_url", ""),
                "has_pdf_doc": has_pdf_doc
            })
            
    # Sort models alphabetically
    sorted_model_names = sorted(models_dict.keys())
    
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Audit Qualité Officiel par Modèle - HotSpring Spas (2002 - 2026)</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #0b1120; color: #f8fafc; margin: 0; padding: 24px; }}
        h1 {{ margin: 0 0 8px 0; font-size: 28px; color: #38bdf8; }}
        p.subtitle {{ margin: 0 0 20px 0; color: #94a3b8; font-size: 15px; }}
        .nav-models {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 24px; background: #1e293b; padding: 12px 16px; border-radius: 8px; border: 1px solid #334155; position: sticky; top: 12px; z-index: 100; }}
        .nav-btn {{ color: #38bdf8; text-decoration: none; font-size: 13px; font-weight: 600; padding: 4px 10px; background: #0f172a; border-radius: 6px; border: 1px solid #334155; transition: all 0.2s; }}
        .nav-btn:hover {{ background: #38bdf8; color: #0f172a; border-color: #38bdf8; }}
        .stats-bar {{ display: flex; gap: 16px; margin-bottom: 24px; background: #1e293b; padding: 16px; border-radius: 8px; border: 1px solid #334155; }}
        .stat-item {{ flex: 1; }}
        .stat-val {{ font-size: 24px; font-weight: bold; color: #38bdf8; }}
        .stat-lbl {{ font-size: 12px; color: #94a3b8; text-transform: uppercase; }}
        .model-section {{ margin-bottom: 40px; background: #0f172a; border: 1px solid #334155; border-radius: 12px; padding: 20px; }}
        .model-header {{ display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 16px; border-bottom: 1px solid #1e293b; padding-bottom: 8px; }}
        .model-title {{ font-size: 22px; font-weight: bold; color: #f1f5f9; }}
        .model-meta {{ color: #94a3b8; font-size: 14px; }}
        .cards-row {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 16px; }}
        .card {{ background: #1e293b; border-radius: 10px; border: 1px solid #334155; overflow: hidden; display: flex; flex-direction: column; }}
        .card-header {{ padding: 10px 14px; background: #090e1a; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }}
        .card-year {{ font-size: 16px; font-weight: bold; color: #38bdf8; }}
        .card-series {{ font-size: 12px; color: #94a3b8; }}
        .card-body {{ padding: 14px; display: flex; flex-direction: column; gap: 10px; flex: 1; }}
        .img-grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 6px; }}
        .img-box {{ background: #000; border-radius: 6px; overflow: hidden; height: 110px; display: flex; align-items: center; justify-content: center; position: relative; border: 1px solid #1e293b; }}
        .img-box img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
        .img-box.placeholder {{ background: #182234; color: #64748b; font-size: 10px; text-align: center; padding: 6px; line-height: 1.2; display: flex; align-items: center; justify-content: center; }}
        .img-lbl {{ position: absolute; bottom: 2px; left: 4px; font-size: 8px; background: rgba(0,0,0,0.75); color: #cbd5e1; padding: 1px 4px; border-radius: 3px; }}
        .badges-row {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: auto; padding-top: 8px; border-top: 1px solid #334155; }}
        .badge {{ font-size: 10px; padding: 3px 6px; border-radius: 4px; font-weight: 600; text-decoration: none; display: inline-flex; align-items: center; }}
        .badge-cad {{ background: #059669; color: white; }}
        .badge-pdf {{ background: #d97706; color: white; }}
        .badge-photo {{ background: #2563eb; color: white; }}
        .badge-missing {{ background: #475569; color: #cbd5e1; font-style: italic; }}
    </style>
</head>
<body>
    <h1>Audit Qualité Constructeur par Modèle - HotSpring Spas</h1>
    <p class="subtitle">Classement alphabétique de chaque modèle sur l'historique complet 2002 - 2026. Comparaison directe des évolutions de cuve, plans d'ingénierie officiels et fichiers AutoCAD natifs.</p>
    
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-val">{len(sorted_model_names)}</div>
            <div class="stat-lbl">Modèles Uniques</div>
        </div>
        <div class="stat-item">
            <div class="stat-val">{total_models_count}</div>
            <div class="stat-lbl">Fiches Modèle / Année</div>
        </div>
        <div class="stat-item">
            <div class="stat-val">{total_dwg_count}</div>
            <div class="stat-lbl">Fichiers AutoCAD .DWG</div>
        </div>
        <div class="stat-item">
            <div class="stat-val">{total_pdf_count}</div>
            <div class="stat-lbl">Plans Officiels 300 DPI</div>
        </div>
        <div class="stat-item">
            <div class="stat-val">{total_real_photo_count}</div>
            <div class="stat-lbl">Photos Réelles Acrylique</div>
        </div>
    </div>

    <!-- Navigation rapide par modèle -->
    <div class="nav-models">
        <span style="font-size: 13px; color: #94a3b8; align-self: center; margin-right: 6px;">Accès rapide :</span>
"""
    for m in sorted_model_names:
        html_content += f'<a class="nav-btn" href="#model-{m.lower().replace(" ", "_")}">{m}</a>\n'
        
    html_content += "</div>\n"

    # Affichage groupé par modèle
    for m in sorted_model_names:
        year_list = models_dict[m]
        # Trier par année croissante (2002 -> 2026)
        year_list.sort(key=lambda x: x['year'])
        first_yr = year_list[0]['year']
        last_yr = year_list[-1]['year']
        coll = year_list[-1]['series']
        
        html_content += f"""
    <div class="model-section" id="model-{m.lower().replace(" ", "_")}">
        <div class="model-header">
            <span class="model-title">{m}</span>
            <span class="model-meta">{coll} &bull; Historique de {first_yr} à {last_yr} ({len(year_list)} millésimes)</span>
        </div>
        <div class="cards-row">
"""
        for card in year_list:
            top_block = f'<div class="img-box"><img src="{card["top_img"]}" alt="Acrylique" loading="lazy"><span class="img-lbl">Acrylique</span></div>' if card["has_real_top"] else '<div class="img-box placeholder"><span>Photo d\'époque<br>en recherche</span></div>'
            side_block = f'<div class="img-box"><img src="{card["side_img"]}" alt="Meuble" loading="lazy"><span class="img-lbl">Meuble</span></div>' if card["has_real_side"] else '<div class="img-box placeholder"><span>Vue meuble<br>en recherche</span></div>'
            doc_block = f'<div class="img-box"><img src="{card["doc_img"]}" alt="Plan 300 DPI" loading="lazy"><span class="img-lbl">Plan 300 DPI</span></div>' if card["has_pdf_doc"] else '<div class="img-box placeholder"><span>Plan en cours</span></div>'
            
            photo_badge = '<span class="badge badge-photo">Photo Réelle ✓</span>' if card["has_real_top"] else '<span class="badge badge-missing">Photo Archive Manquante</span>'
            dwg_badge = f'<a class="badge badge-cad" href="{card["dwg_url"]}" target="_blank">DWG ({card["dwg_size"]} MB)</a>' if card["has_dwg"] else '<span class="badge badge-missing">DWG non publié</span>'
            pdf_badge = f'<a class="badge badge-pdf" href="{card["pdf_url"]}" target="_blank">PDF Officiel</a>' if card["pdf_url"] else ''
            
            html_content += f"""
            <div class="card">
                <div class="card-header">
                    <span class="card-year">{card['year']}</span>
                    <span class="card-series">{m} ({card['series']})</span>
                </div>
                <div class="card-body">
                    <div class="img-grid">
                        {top_block}
                        {side_block}
                        {doc_block}
                    </div>
                    <div style="font-size: 12px; color: #cbd5e1; margin-top: 4px;">
                        {card['dims']}
                    </div>
                    <div class="badges-row">
                        {photo_badge}
                        {dwg_badge}
                        {pdf_badge}
                    </div>
                </div>
            </div>
"""
        html_content += """
        </div>
    </div>
"""

    html_content += """
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"[SUCCÈS] Galerie d'audit alphabétique générée : {OUTPUT_HTML}")

if __name__ == "__main__":
    main()
