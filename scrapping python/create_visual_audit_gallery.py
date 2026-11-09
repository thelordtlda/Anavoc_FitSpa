"""
create_visual_audit_gallery.py
==============================
Génère une galerie HTML interactive locale pour auditer visuellement la qualité
des assets récoltés pour HotSpring (ou toute autre marque).
Permet à l'utilisateur de comparer côte à côte :
- La vraie photo zénithale acrylique
- La vraie photo latérale / 3D du meuble
- Le plan officiel constructeur (PDF / dimensions)
- Le statut du fichier CAO natif (.dwg)
"""

import json
from pathlib import Path

DATASET_BRAND = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/hot_spring_spas")
OUTPUT_HTML = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/audit_gallery_hotspring.html")

def main():
    years = sorted([y for y in DATASET_BRAND.iterdir() if y.is_dir() and y.name.isdigit()], key=lambda x: int(x.name), reverse=True)
    
    cards = []
    
    for y_dir in years:
        year = y_dir.name
        for m_dir in sorted(y_dir.iterdir()):
            if not m_dir.is_dir(): continue
            meta_file = m_dir / "metadata.json"
            if not meta_file.exists(): continue
            
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
                
            model = meta.get("model", m_dir.name)
            series = meta.get("series", "")
            dims = meta.get("dimensions", {})
            prov = meta.get("provenance", {})
            media = meta.get("media", {})
            
            # Paths relative to OUTPUT_HTML
            top_p = m_dir / "top_view.jpg"
            if not top_p.exists(): top_p = m_dir / "top_view.png"
            
            side_p = m_dir / "side_view.jpg"
            if not side_p.exists(): side_p = m_dir / "side_view.png"
            
            doc_p = m_dir / "official_manufacturer_doc.png"
            cad_p = m_dir / "cad_model.dwg"
            
            top_rel = top_p.relative_to(OUTPUT_HTML.parent).as_posix() if top_p.exists() else ""
            side_rel = side_p.relative_to(OUTPUT_HTML.parent).as_posix() if side_p.exists() else ""
            doc_rel = doc_p.relative_to(OUTPUT_HTML.parent).as_posix() if doc_p.exists() else ""
            
            has_dwg = cad_p.exists()
            dwg_size_mb = round(cad_p.stat().st_size / (1024*1024), 2) if has_dwg else 0
            
            cards.append({
                "year": year,
                "model": model,
                "series": series,
                "dims": f"{dims.get('length_in', 0)}\" x {dims.get('width_in', 0)}\" x {dims.get('height_in', 0)}\" (R: {dims.get('corner_radius_in', 0)}\")",
                "top_img": top_rel,
                "side_img": side_rel,
                "doc_img": doc_rel,
                "has_dwg": has_dwg,
                "dwg_size": dwg_size_mb,
                "dwg_url": prov.get("official_cad_dwg_url", ""),
                "pdf_url": prov.get("official_pdf_url", ""),
                "source_ref": prov.get("portal_reference", "")
            })
            
    # Generate HTML
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Galerie d'Audit Qualité - HotSpring Spas (100% Officiel)</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #0f172a; color: #f8fafc; margin: 0; padding: 24px; }}
        h1 {{ margin: 0 0 8px 0; font-size: 28px; color: #38bdf8; }}
        p.subtitle {{ margin: 0 0 24px 0; color: #94a3b8; font-size: 15px; }}
        .stats-bar {{ display: flex; gap: 16px; margin-bottom: 24px; background: #1e293b; padding: 16px; border-radius: 8px; border: 1px solid #334155; }}
        .stat-item {{ flex: 1; }}
        .stat-val {{ font-size: 24px; font-weight: bold; color: #38bdf8; }}
        .stat-lbl {{ font-size: 12px; color: #94a3b8; text-transform: uppercase; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 20px; }}
        .card {{ background: #1e293b; border-radius: 12px; border: 1px solid #334155; overflow: hidden; display: flex; flex-direction: column; transition: transform 0.2s; }}
        .card:hover {{ transform: translateY(-4px); border-color: #38bdf8; }}
        .card-header {{ padding: 12px 16px; background: #0f172a; border-bottom: 1px solid #334155; display: flex; justify-content: space-between; align-items: center; }}
        .card-title {{ font-weight: bold; font-size: 16px; color: #f1f5f9; }}
        .badge-year {{ background: #0284c7; color: white; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold; }}
        .card-body {{ padding: 16px; display: flex; flex-direction: column; gap: 12px; flex: 1; }}
        .img-row {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }}
        .img-box {{ background: #000; border-radius: 6px; overflow: hidden; height: 110px; display: flex; align-items: center; justify-content: center; position: relative; }}
        .img-box img {{ max-width: 100%; max-height: 100%; object-fit: contain; }}
        .img-lbl {{ position: absolute; bottom: 2px; left: 4px; font-size: 9px; background: rgba(0,0,0,0.7); color: #cbd5e1; padding: 1px 4px; border-radius: 3px; }}
        .specs {{ font-size: 13px; color: #cbd5e1; line-height: 1.4; }}
        .badges-row {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: auto; padding-top: 8px; border-top: 1px solid #334155; }}
        .badge {{ font-size: 11px; padding: 3px 8px; border-radius: 4px; font-weight: 600; text-decoration: none; display: inline-flex; align-items: center; }}
        .badge-cad {{ background: #059669; color: white; }}
        .badge-pdf {{ background: #d97706; color: white; }}
        .badge-photo {{ background: #2563eb; color: white; }}
        .badge-none {{ background: #475569; color: #94a3b8; }}
    </style>
</head>
<body>
    <h1>Galerie d'Assurance Qualité Constructeur - HotSpring Spas</h1>
    <p class="subtitle">Vérification visuelle intégrale des assets 100% officiels (Photos réelles, Plans vectoriels d'ingénierie, Fichiers natifs AutoCAD .dwg).</p>
    
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-val">{len(cards)}</div>
            <div class="stat-lbl">Modèles indexés</div>
        </div>
        <div class="stat-item">
            <div class="stat-val">{sum(1 for c in cards if c['has_dwg'])}</div>
            <div class="stat-lbl">Fichiers AutoCAD .dwg</div>
        </div>
        <div class="stat-item">
            <div class="stat-val">{sum(1 for c in cards if c['doc_img'])}</div>
            <div class="stat-lbl">Plans Officiels 300 DPI</div>
        </div>
        <div class="stat-item">
            <div class="stat-val">{sum(1 for c in cards if c['top_img'])}</div>
            <div class="stat-lbl">Photos Acrylique Réelles</div>
        </div>
    </div>

    <div class="grid">
"""

    for c in cards:
        dwg_badge = f'<a class="badge badge-cad" href="{c["dwg_url"]}" target="_blank">DWG CAD ({c["dwg_size"]} MB)</a>' if c['has_dwg'] else '<span class="badge badge-none">Pas de DWG</span>'
        pdf_badge = f'<a class="badge badge-pdf" href="{c["pdf_url"]}" target="_blank">PDF Officiel</a>' if c['pdf_url'] else '<span class="badge badge-none">Pas de PDF</span>'
        
        html_content += f"""
        <div class="card">
            <div class="card-header">
                <span class="card-title">{c['model']} <small style="color:#94a3b8; font-weight:normal;">({c['series']})</small></span>
                <span class="badge-year">{c['year']}</span>
            </div>
            <div class="card-body">
                <div class="img-row">
                    <div class="img-box">
                        <img src="{c['top_img']}" alt="Top View" loading="lazy">
                        <span class="img-lbl">Acrylique</span>
                    </div>
                    <div class="img-box">
                        <img src="{c['side_img']}" alt="Side View" loading="lazy">
                        <span class="img-lbl">Meuble</span>
                    </div>
                    <div class="img-box">
                        <img src="{c['doc_img']}" alt="Footprint" loading="lazy">
                        <span class="img-lbl">Plan 300 DPI</span>
                    </div>
                </div>
                <div class="specs">
                    <strong>Dimensions :</strong> {c['dims']}<br>
                </div>
                <div class="badges-row">
                    <span class="badge badge-photo">Photo Réelle ✓</span>
                    {dwg_badge}
                    {pdf_badge}
                </div>
            </div>
        </div>
"""

    html_content += """
    </div>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"[SUCCÈS] Galerie d'audit générée : {OUTPUT_HTML} ({len(cards)} fiches)")

if __name__ == "__main__":
    main()
