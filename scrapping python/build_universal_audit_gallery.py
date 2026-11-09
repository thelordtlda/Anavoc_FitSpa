import json
import os
import re
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR / "dataset"
OUTPUT_HTML = SCRIPT_DIR / "universal_audit_gallery.html"
OUTPUT_HTML_DATASET = DATASET_DIR / "universal_audit_gallery.html"

def to_ft_in(val):
    if not val: return '0\'0"'
    feet = int(val // 12)
    rem = round(val - feet * 12, 1)
    if rem == 12.0:
        feet += 1
        rem = 0.0
    if rem == int(rem):
        return f"{feet}'{int(rem)}\""
    return f"{feet}'{rem}\""

def format_dims_4_units(length_in, width_in, height_in, radius_in=None):
    if not length_in or not width_in or not height_in:
        return {"in": "N/A", "ft": "N/A", "cm": "N/A", "mm": "N/A"}
        
    in_str = f"{length_in:.1f}\" × {width_in:.1f}\" × {height_in:.1f}\""
    ft_str = f"{to_ft_in(length_in)} × {to_ft_in(width_in)} × {to_ft_in(height_in)}"
    cm_str = f"{round(length_in*2.54, 1)} × {round(width_in*2.54, 1)} × {round(height_in*2.54, 1)} cm"
    mm_str = f"{round(length_in*25.4)} × {round(width_in*25.4)} × {round(height_in*25.4)} mm"
    
    if radius_in:
        in_str += f" (R: {radius_in:.1f}\")"
        ft_str += f" (R: {to_ft_in(radius_in)})"
        cm_str += f" (R: {round(radius_in*2.54, 1)} cm)"
        mm_str += f" (R: {round(radius_in*25.4)} mm)"
        
    return {
        "in": in_str,
        "ft": ft_str,
        "cm": cm_str,
        "mm": mm_str
    }

def main():
    print("--- Génération de la Galerie d'Audit avec Groupement Automatique (Marque -> Modèle -> Année) ---")
    
    cards = []
    verified_brands = [
        ("hot_spring_spas", "Hot Spring Spas", "https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings"),
        ("bullfrog_spas", "Bullfrog Spas", "https://www.bullfrogspas.com/manuals/"),
        ("jacuzzi", "Jacuzzi", "https://www.jacuzzi.com/en-us/hot-tubs/owners-manuals.html"),
        ("sundance_spas", "Sundance Spas", "https://www.sundancespas.com/en-us/owner-resources/manuals/"),
        ("american_whirlpool", "American Whirlpool", "https://americanwhirlpool.com/"),
        ("maax_spas", "MAAX Spas", "https://maaxspas.com/"),
    ]

    for b_slug, default_brand, default_portal in verified_brands:
        b_dir = DATASET_DIR / b_slug
        if not b_dir.exists():
            continue
        for yr_dir in sorted(list(b_dir.glob("20*"))):
            if not yr_dir.is_dir():
                continue
            year = int(yr_dir.name)
            for m_dir in sorted(list(yr_dir.iterdir())):
                if not m_dir.is_dir():
                    continue
                meta_p = m_dir / "metadata.json"
                if not meta_p.exists():
                    continue
                try:
                    with open(meta_p, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                except Exception:
                    continue

                brand = meta.get("brand", default_brand)
                model = meta.get("model", m_dir.name)
                series = meta.get("series", "Standard")
                dims = meta.get("dimensions", {})
                prov = meta.get("provenance", {})

                l_in = float(dims.get("length_in", 0) or 0)
                w_in = float(dims.get("width_in", 0) or 0)
                h_in = float(dims.get("height_in", 0) or 0)
                r_in = float(dims.get("corner_radius_in", 0) or 0)
                dims_4u = format_dims_4_units(l_in, w_in, h_in, r_in)

                top_p = m_dir / "top_view.jpg"
                if not top_p.exists(): top_p = m_dir / "top_view.png"
                if not top_p.exists(): top_p = m_dir / "top_view.webp"

                side_p = m_dir / "side_view.jpg"
                if not side_p.exists(): side_p = m_dir / "side_view.png"
                if not side_p.exists(): side_p = m_dir / "side_view.webp"

                doc_p = m_dir / "official_manufacturer_doc.png"
                cad_p = m_dir / "cad_model.dwg"
                dxf_p = m_dir / "cad_model.dxf"

                has_real_photo = bool(prov.get("has_real_photo", False)) and top_p.exists() and top_p.stat().st_size > 4000
                has_side_photo = side_p.exists() and side_p.stat().st_size > 4000
                has_dwg = cad_p.exists() and cad_p.stat().st_size > 4000
                has_dxf = dxf_p.exists() and dxf_p.stat().st_size > 4000
                has_pdf_doc = bool(prov.get("has_official_pdf_doc", False)) and doc_p.exists() and doc_p.stat().st_size > 4000

                top_rel = top_p.relative_to(SCRIPT_DIR).as_posix() if has_real_photo else ""
                side_rel = side_p.relative_to(SCRIPT_DIR).as_posix() if has_side_photo else ""
                doc_rel = doc_p.relative_to(SCRIPT_DIR).as_posix() if has_pdf_doc else ""

                dwg_size = round(cad_p.stat().st_size / (1024*1024), 2) if has_dwg else 0
                dxf_size = round(dxf_p.stat().st_size / (1024*1024), 2) if has_dxf else 0

                top_src = prov.get("top_view_source") or ""
                side_src = prov.get("side_view_source") or ""
                pdf_src = prov.get("official_pdf_url") or ""
                dwg_src = prov.get("official_cad_dwg_url") or ""
                portal_ref = prov.get("portal_reference") or default_portal

                cards.append({
                    "brand": brand,
                    "model": model,
                    "year": year,
                    "series": series,
                    "dims_4u": dims_4u,
                    "top_img": top_rel,
                    "side_img": side_rel,
                    "doc_img": doc_rel,
                    "has_real_photo": has_real_photo,
                    "has_side_photo": has_side_photo,
                    "has_dwg": has_dwg,
                    "dwg_size": dwg_size,
                    "has_dxf": has_dxf,
                    "dxf_size": dxf_size,
                    "has_pdf": has_pdf_doc,
                    "has_bim": False,
                    "top_src": top_src,
                    "side_src": side_src,
                    "pdf_src": pdf_src,
                    "dwg_src": dwg_src,
                    "dxf_src": "",
                    "bim_src": "",
                    "portal_ref": portal_ref,
                    "seats": meta.get("seating_capacity", ""),
                    "shape": dims.get("corner_type", "Square / Rectangular")
                })

    print(f"Total fiches indexées : {len(cards)}")
    
    # Structure hiérarchique : Brand -> Model -> [Cards triées par année croissante]
    # et structure d'options pour les dropdowns
    hierarchy = defaultdict(lambda: defaultdict(list))
    for c in cards:
        hierarchy[c["brand"]][c["model"]].append(c)
        
    for b in hierarchy:
        for m in hierarchy[b]:
            hierarchy[b][m].sort(key=lambda x: x["year"])
            
    # Hiérarchie simple pour les menus
    dropdown_map = {}
    for b in sorted(hierarchy.keys()):
        dropdown_map[b] = {}
        for m in sorted(hierarchy[b].keys()):
            years = [card["year"] for card in hierarchy[b][m]]
            dropdown_map[b][m] = sorted(list(set(years)))

    cards_json = json.dumps(cards, ensure_ascii=False)
    dropdown_map_json = json.dumps(dropdown_map, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SpaFit Cover Sizer - Galerie d'Audit Hiérarchique (Marque &bull; Modèle &bull; Année)</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --bg-dark: #0b1120;
            --card-bg: #1e293b;
            --card-border: #334155;
            --accent: #38bdf8;
            --accent-hover: #0284c7;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --badge-dwg: #059669;
            --badge-dxf: #0d9488;
            --badge-pdf: #d97706;
            --badge-bim: #7c3aed;
            --badge-photo: #2563eb;
            --badge-missing: #475569;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg-dark);
            color: var(--text-main);
            padding: 24px;
            line-height: 1.5;
        }}
        header {{
            margin-bottom: 24px;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 20px;
        }}
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        h1 {{
            font-size: 26px;
            color: var(--accent);
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        h1 i {{ color: #f59e0b; }}
        p.subtitle {{
            color: var(--text-muted);
            font-size: 14px;
            margin-top: 6px;
        }}
        
        /* Stats Ribbon */
        .stats-ribbon {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 12px;
            margin: 20px 0;
        }}
        .stat-card {{
            background: #131d31;
            border: 1px solid var(--card-border);
            border-radius: 8px;
            padding: 12px 16px;
        }}
        .stat-card .val {{
            font-size: 22px;
            font-weight: bold;
            color: var(--accent);
        }}
        .stat-card .lbl {{
            font-size: 11px;
            text-transform: uppercase;
            color: var(--text-muted);
            letter-spacing: 0.5px;
        }}

        /* Cascading Dropdowns & Control Bar */
        .controls-panel {{
            background: #131d31;
            border: 1px solid var(--card-border);
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 28px;
            display: flex;
            flex-direction: column;
            gap: 14px;
            position: sticky;
            top: 12px;
            z-index: 100;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }}
        .dropdowns-row {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 12px;
        }}
        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .filter-group label {{
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        select, input[type="text"] {{
            background: #0b1120;
            border: 1px solid var(--card-border);
            color: #f1f5f9;
            padding: 10px 14px;
            border-radius: 6px;
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
            width: 100%;
        }}
        select:focus, input[type="text"]:focus {{
            border-color: var(--accent);
        }}
        
        .toggles-row {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            align-items: center;
            padding-top: 10px;
            border-top: 1px solid rgba(255,255,255,0.08);
        }}
        .toggle-btn {{
            background: #1e293b;
            border: 1px solid var(--card-border);
            color: var(--text-muted);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            user-select: none;
            transition: all 0.2s;
        }}
        .toggle-btn.active {{
            background: #0284c7;
            color: white;
            border-color: var(--accent);
        }}
        .reset-btn {{
            margin-left: auto;
            background: #334155;
            color: #f1f5f9;
            border: none;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 12px;
            cursor: pointer;
        }}
        .reset-btn:hover {{ background: #475569; }}

        /* Hierarchical Grouping Layout */
        .brand-section {{
            margin-bottom: 40px;
            background: rgba(19, 29, 49, 0.4);
            border: 1px solid rgba(51, 65, 85, 0.6);
            border-radius: 12px;
            padding: 24px;
        }}
        .brand-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            border-bottom: 2px solid var(--accent);
            padding-bottom: 12px;
            margin-bottom: 24px;
        }}
        .brand-title {{
            font-size: 22px;
            color: #f8fafc;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .brand-title i {{ color: var(--accent); }}
        .brand-meta {{
            font-size: 13px;
            color: var(--text-muted);
            background: #090e1a;
            padding: 4px 12px;
            border-radius: 20px;
            border: 1px solid var(--card-border);
        }}

        .model-section {{
            margin-bottom: 30px;
            background: #101827;
            border: 1px solid var(--card-border);
            border-radius: 10px;
            padding: 18px;
        }}
        .model-section:last-child {{ margin-bottom: 0; }}
        .model-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px dashed #334155;
        }}
        .model-title {{
            font-size: 18px;
            color: #38bdf8;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .model-meta {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        .years-cards-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(430px, 1fr));
            gap: 18px;
        }}
        
        /* Card Styling */
        .spa-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 10px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            transition: transform 0.2s, border-color 0.2s;
        }}
        .spa-card:hover {{
            transform: translateY(-3px);
            border-color: var(--accent);
        }}
        .card-header {{
            padding: 10px 14px;
            background: #090e1a;
            border-bottom: 1px solid var(--card-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .card-title-box {{
            display: flex;
            flex-direction: column;
        }}
        .card-model {{
            font-size: 15px;
            font-weight: bold;
            color: #f8fafc;
        }}
        .card-sub {{
            font-size: 11px;
            color: var(--text-muted);
        }}
        .year-pill {{
            background: #0284c7;
            color: white;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }}

        .card-body {{
            padding: 14px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            flex: 1;
        }}

        /* 3 Image Viewports with Source Action */
        .viewports-row {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 8px;
        }}
        .viewport-container {{
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .viewport {{
            background: #000;
            border-radius: 6px;
            height: 115px;
            position: relative;
            overflow: hidden;
            border: 1px solid #1e293b;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }}
        .viewport img {{
            max-width: 100%;
            max-height: 100%;
            object-fit: contain;
        }}
        .viewport-placeholder {{
            background: #141e30;
            color: #64748b;
            font-size: 10px;
            text-align: center;
            padding: 6px;
            line-height: 1.2;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 4px;
            height: 115px;
            border-radius: 6px;
            border: 1px solid #1e293b;
        }}
        .viewport-placeholder i {{ font-size: 16px; color: #475569; }}
        .viewport-lbl {{
            position: absolute;
            bottom: 3px;
            left: 4px;
            font-size: 9px;
            background: rgba(0,0,0,0.8);
            color: #cbd5e1;
            padding: 1px 5px;
            border-radius: 3px;
            font-weight: 500;
        }}
        
        /* Direct Source Link Button under viewport */
        .src-btn {{
            font-size: 10px;
            background: #0b1120;
            border: 1px solid #334155;
            color: #38bdf8;
            padding: 3px 6px;
            border-radius: 4px;
            text-decoration: none;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            text-overflow: ellipsis;
            white-space: nowrap;
            overflow: hidden;
            transition: all 0.2s;
        }}
        .src-btn:hover {{
            background: #0284c7;
            color: white;
            border-color: #38bdf8;
        }}
        .src-btn.disabled {{
            color: #64748b;
            border-color: #1e293b;
            pointer-events: none;
            background: #0a0f1d;
        }}

        /* 4-Unit Dimensions Box */
        .dims-box {{
            background: #0b1120;
            border: 1px solid #243248;
            border-radius: 6px;
            padding: 8px 10px;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        .dims-header {{
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--accent);
            font-weight: bold;
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 2px;
        }}
        .dim-row {{
            display: flex;
            font-size: 11px;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px dashed rgba(255,255,255,0.06);
            padding-bottom: 2px;
        }}
        .dim-row:last-child {{ border-bottom: none; padding-bottom: 0; }}
        .dim-unit {{
            color: var(--text-muted);
            font-weight: 600;
            width: 70px;
        }}
        .dim-val {{
            color: #f1f5f9;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 11px;
        }}

        /* Technical Badges Row with Source Links */
        .tech-badges-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: auto;
            padding-top: 8px;
            border-top: 1px solid var(--card-border);
        }}
        .tech-badge {{
            font-size: 11px;
            font-weight: 600;
            padding: 3px 8px;
            border-radius: 4px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            transition: opacity 0.2s;
        }}
        .tech-badge:hover {{ opacity: 0.85; }}
        .badge-dwg {{ background: var(--badge-dwg); color: white; }}
        .badge-dxf {{ background: var(--badge-dxf); color: white; }}
        .badge-pdf {{ background: var(--badge-pdf); color: white; }}
        .badge-bim {{ background: var(--badge-bim); color: white; }}
        .badge-photo {{ background: var(--badge-photo); color: white; }}
        .badge-portal {{ background: #334155; color: #cbd5e1; }}
        .badge-missing {{ background: var(--badge-missing); color: #cbd5e1; font-style: italic; }}

        /* Modal for full image zoom */
        .modal {{
            display: none;
            position: fixed;
            z-index: 9999;
            left: 0; top: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.92);
            align-items: center;
            justify-content: center;
            flex-direction: column;
            gap: 12px;
        }}
        .modal.open {{ display: flex; }}
        .modal-content {{
            max-width: 90%;
            max-height: 82%;
            object-fit: contain;
            border: 2px solid #334155;
            border-radius: 8px;
        }}
        .modal-src-link {{
            color: var(--accent);
            background: #1e293b;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 13px;
            border: 1px solid var(--card-border);
        }}
        .modal-close {{
            position: absolute;
            top: 20px;
            right: 30px;
            color: white;
            font-size: 34px;
            cursor: pointer;
        }}
    </style>
</head>
<body>

    <header>
        <div class="header-top">
            <div>
                <h1><i class="fa-solid fa-layer-group"></i> SpaFit Cover Sizer &bull; Galerie d'Audit Hiérarchique</h1>
                <p class="subtitle">Groupement automatique par <strong>Marque ➔ Modèle ➔ Année</strong> &bull; Liens sources certifiés pour chaque fichier (Top View, Side View, PDF, DWG, DXF, BIM) &bull; Dimensions quadruples (po, pi, cm, mm).</p>
            </div>
        </div>

        <div class="stats-ribbon">
            <div class="stat-card">
                <div class="val" id="stat-total">{len(cards)}</div>
                <div class="lbl">Fiches Modèle / Année</div>
            </div>
            <div class="stat-card">
                <div class="val" id="stat-brands">{len(hierarchy)}</div>
                <div class="lbl">Marques Représentées</div>
            </div>
            <div class="stat-card">
                <div class="val" id="stat-dwg">{sum(1 for c in cards if c["has_dwg"])}</div>
                <div class="lbl">Fichiers AutoCAD .DWG</div>
            </div>
            <div class="stat-card">
                <div class="val" id="stat-photos">{sum(1 for c in cards if c["has_real_photo"])}</div>
                <div class="lbl">Photos Réelles Validées</div>
            </div>
        </div>
    </header>

    <!-- Panneau de Contrôle & 3 Listes Déroulantes en Cascade -->
    <div class="controls-panel">
        <div class="dropdowns-row">
            <div class="filter-group">
                <label><i class="fa-solid fa-industry"></i> 1. Marque (Brand)</label>
                <select id="select-brand">
                    <option value="ALL">-- Toutes les marques --</option>
                </select>
            </div>
            <div class="filter-group">
                <label><i class="fa-solid fa-bath"></i> 2. Modèle (Model)</label>
                <select id="select-model" disabled>
                    <option value="ALL">-- Tous les modèles --</option>
                </select>
            </div>
            <div class="filter-group">
                <label><i class="fa-solid fa-calendar"></i> 3. Année (Year)</label>
                <select id="select-year" disabled>
                    <option value="ALL">-- Toutes les années --</option>
                </select>
            </div>
            <div class="filter-group">
                <label><i class="fa-solid fa-magnifying-glass"></i> Recherche instantanée</label>
                <input type="text" id="search-box" placeholder="Ex: Glow, Grandee, 84x76, TX...">
            </div>
        </div>

        <div class="toggles-row">
            <span style="font-size:12px; color:var(--text-muted); font-weight:600;">Filtres techniques :</span>
            <div class="toggle-btn" id="filter-dwg" onclick="toggleTechFilter('dwg')">
                <i class="fa-solid fa-drafting-compass"></i> Avec DWG / DXF
            </div>
            <div class="toggle-btn" id="filter-pdf" onclick="toggleTechFilter('pdf')">
                <i class="fa-solid fa-file-pdf"></i> Avec Plan 300 DPI
            </div>
            <div class="toggle-btn" id="filter-photo" onclick="toggleTechFilter('photo')">
                <i class="fa-solid fa-camera"></i> Avec Photo Réelle
            </div>
            <button class="reset-btn" onclick="resetFilters()"><i class="fa-solid fa-rotate-left"></i> Réinitialiser</button>
        </div>
    </div>

    <div style="margin-bottom: 20px; font-size: 14px; color: var(--text-muted);">
        Affichage de <strong id="visible-count" style="color:var(--accent); font-size:16px;">0</strong> fiche(s) groupée(s) hiérarchiquement
    </div>

    <!-- Conteneur Hiérarchique : Marque -> Modèle -> Années -->
    <div id="hierarchy-container"></div>

    <!-- Modal zoom image avec lien source -->
    <div class="modal" id="image-modal" onclick="closeModal(event)">
        <span class="modal-close" onclick="closeModal(event)">&times;</span>
        <img class="modal-content" id="modal-img" src="" alt="Zoom">
        <a class="modal-src-link" id="modal-src-btn" href="#" target="_blank" onclick="event.stopPropagation()">
            <i class="fa-solid fa-arrow-up-right-from-square"></i> Ouvrir le fichier original sur le serveur fabricant
        </a>
    </div>

    <script>
        const cardsData = {cards_json};
        const dropdownMap = {dropdown_map_json};

        let filterState = {{
            brand: "ALL",
            model: "ALL",
            year: "ALL",
            search: "",
            onlyDwg: false,
            onlyPdf: false,
            onlyPhoto: false
        }};

        function initApp() {{
            const brandSelect = document.getElementById('select-brand');
            brandSelect.innerHTML = '<option value="ALL">-- Toutes les marques (' + Object.keys(dropdownMap).length + ') --</option>';
            
            for (const b of Object.keys(dropdownMap).sort()) {{
                const opt = document.createElement('option');
                opt.value = b;
                opt.textContent = b + ' (' + Object.keys(dropdownMap[b]).length + ' modèles)';
                brandSelect.appendChild(opt);
            }}

            brandSelect.addEventListener('change', onBrandChange);
            document.getElementById('select-model').addEventListener('change', onModelChange);
            document.getElementById('select-year').addEventListener('change', onYearChange);
            document.getElementById('search-box').addEventListener('input', onSearchInput);
            
            // Pré-sélectionner Hot Spring Spas par défaut
            if (dropdownMap["Hot Spring Spas"]) {{
                brandSelect.value = "Hot Spring Spas";
                onBrandChange();
            }} else {{
                renderHierarchicalView();
            }}
        }}

        function onBrandChange() {{
            const brand = document.getElementById('select-brand').value;
            filterState.brand = brand;
            filterState.model = "ALL";
            filterState.year = "ALL";
            
            const modelSelect = document.getElementById('select-model');
            const yearSelect = document.getElementById('select-year');
            
            if (brand === "ALL") {{
                modelSelect.innerHTML = '<option value="ALL">-- Tous les modèles --</option>';
                modelSelect.disabled = true;
                yearSelect.innerHTML = '<option value="ALL">-- Toutes les années --</option>';
                yearSelect.disabled = true;
            }} else {{
                modelSelect.disabled = false;
                modelSelect.innerHTML = '<option value="ALL">-- Tous les modèles (' + Object.keys(dropdownMap[brand]).length + ') --</option>';
                for (const m of Object.keys(dropdownMap[brand]).sort()) {{
                    const opt = document.createElement('option');
                    opt.value = m;
                    opt.textContent = m + ' (' + dropdownMap[brand][m].length + ' millésimes)';
                    modelSelect.appendChild(opt);
                }}
                yearSelect.innerHTML = '<option value="ALL">-- Toutes les années --</option>';
                yearSelect.disabled = true;
            }}
            renderHierarchicalView();
        }}

        function onModelChange() {{
            const brand = filterState.brand;
            const model = document.getElementById('select-model').value;
            filterState.model = model;
            filterState.year = "ALL";
            
            const yearSelect = document.getElementById('select-year');
            if (model === "ALL" || !brand || !dropdownMap[brand][model]) {{
                yearSelect.innerHTML = '<option value="ALL">-- Toutes les années --</option>';
                yearSelect.disabled = true;
            }} else {{
                yearSelect.disabled = false;
                const years = dropdownMap[brand][model];
                yearSelect.innerHTML = '<option value="ALL">-- Toutes les années (' + years.length + ') --</option>';
                for (const y of years) {{
                    const opt = document.createElement('option');
                    opt.value = y;
                    opt.textContent = y;
                    yearSelect.appendChild(opt);
                }}
            }}
            renderHierarchicalView();
        }}

        function onYearChange() {{
            filterState.year = document.getElementById('select-year').value;
            renderHierarchicalView();
        }}

        function onSearchInput(e) {{
            filterState.search = e.target.value.toLowerCase().trim();
            renderHierarchicalView();
        }}

        function toggleTechFilter(type) {{
            if (type === 'dwg') {{
                filterState.onlyDwg = !filterState.onlyDwg;
                document.getElementById('filter-dwg').classList.toggle('active', filterState.onlyDwg);
            }} else if (type === 'pdf') {{
                filterState.onlyPdf = !filterState.onlyPdf;
                document.getElementById('filter-pdf').classList.toggle('active', filterState.onlyPdf);
            }} else if (type === 'photo') {{
                filterState.onlyPhoto = !filterState.onlyPhoto;
                document.getElementById('filter-photo').classList.toggle('active', filterState.onlyPhoto);
            }}
            renderHierarchicalView();
        }}

        function resetFilters() {{
            document.getElementById('select-brand').value = "ALL";
            document.getElementById('search-box').value = "";
            filterState = {{
                brand: "ALL",
                model: "ALL",
                year: "ALL",
                search: "",
                onlyDwg: false,
                onlyPdf: false,
                onlyPhoto: false
            }};
            document.getElementById('filter-dwg').classList.remove('active');
            document.getElementById('filter-pdf').classList.remove('active');
            document.getElementById('filter-photo').classList.remove('active');
            onBrandChange();
        }}

        function openModal(imgSrc, originalUrl) {{
            document.getElementById('modal-img').src = imgSrc;
            const srcBtn = document.getElementById('modal-src-btn');
            if (originalUrl) {{
                srcBtn.href = originalUrl;
                srcBtn.style.display = "inline-flex";
            }} else {{
                srcBtn.style.display = "none";
            }}
            document.getElementById('image-modal').classList.add('open');
        }}

        function closeModal(event) {{
            if (event.target.id === 'modal-src-btn') return;
            document.getElementById('image-modal').classList.remove('open');
        }}

        // Génération automatique du DOM groupé par Marque -> Modèle -> Année
        function renderHierarchicalView() {{
            const root = document.getElementById('hierarchy-container');
            root.innerHTML = "";

            // 1. Filtrer les cartes
            const filteredCards = cardsData.filter(c => {{
                if (filterState.brand !== "ALL" && c.brand !== filterState.brand) return false;
                if (filterState.model !== "ALL" && c.model !== filterState.model) return false;
                if (filterState.year !== "ALL" && c.year.toString() !== filterState.year) return false;
                if (filterState.onlyDwg && !c.has_dwg && !c.has_dxf) return false;
                if (filterState.onlyPdf && !c.has_pdf) return false;
                if (filterState.onlyPhoto && !c.has_real_photo) return false;
                
                if (filterState.search) {{
                    const s = filterState.search;
                    const matchModel = c.model.toLowerCase().includes(s);
                    const matchBrand = c.brand.toLowerCase().includes(s);
                    const matchSeries = c.series.toLowerCase().includes(s);
                    const matchYear = c.year.toString().includes(s);
                    const matchDims = c.dims_4u.in.toLowerCase().includes(s) || c.dims_4u.mm.toLowerCase().includes(s);
                    if (!matchModel && !matchBrand && !matchSeries && !matchYear && !matchDims) return false;
                }}
                return true;
            }});

            document.getElementById('visible-count').textContent = filteredCards.length;

            if (filteredCards.length === 0) {{
                root.innerHTML = '<div style="text-align:center; padding:50px; color:#64748b; font-size:16px;">Aucun spa ne correspond aux filtres sélectionnés.</div>';
                return;
            }}

            // 2. Structurer hiérarchiquement : Brand -> Model -> [Cards]
            const groups = {{}};
            for (const c of filteredCards) {{
                if (!groups[c.brand]) groups[c.brand] = {{}};
                if (!groups[c.brand][c.model]) groups[c.brand][c.model] = [];
                groups[c.brand][c.model].push(c);
            }}

            // 3. Rendu par Marque
            for (const brand of Object.keys(groups).sort()) {{
                const brandSection = document.createElement('div');
                brandSection.className = 'brand-section';
                
                let totalBrandSpas = 0;
                for (const m of Object.keys(groups[brand])) {{
                    totalBrandSpas += groups[brand][m].length;
                }}

                brandSection.innerHTML = `
                    <div class="brand-header">
                        <h2 class="brand-title"><i class="fa-solid fa-industry"></i> ${{brand}}</h2>
                        <span class="brand-meta">${{Object.keys(groups[brand]).length}} modèles &bull; ${{totalBrandSpas}} millésimes</span>
                    </div>
                `;

                // 4. Rendu par Modèle
                for (const model of Object.keys(groups[brand]).sort()) {{
                    const modelCards = groups[brand][model];
                    modelCards.sort((a, b) => a.year - b.year); // Ordre chronologique

                    const firstYr = modelCards[0].year;
                    const lastYr = modelCards[modelCards.length - 1].year;
                    const seriesName = modelCards[modelCards.length - 1].series;

                    const modelSection = document.createElement('div');
                    modelSection.className = 'model-section';
                    modelSection.innerHTML = `
                        <div class="model-header">
                            <h3 class="model-title"><i class="fa-solid fa-bath"></i> ${{model}}</h3>
                            <span class="model-meta">${{seriesName}} &bull; Historique ${{firstYr}} à ${{lastYr}} (${{modelCards.length}} fiches)</span>
                        </div>
                    `;

                    const cardsGrid = document.createElement('div');
                    cardsGrid.className = 'years-cards-grid';

                    // 5. Rendu des cartes par Année
                    for (const c of modelCards) {{
                        const cardEl = document.createElement('div');
                        cardEl.className = 'spa-card';

                        // Viewport Top (Acrylique) + bouton source
                        const topBox = c.has_real_photo && c.top_img
                            ? `
                            <div class="viewport-container">
                                <div class="viewport" onclick="openModal('${{c.top_img}}', '${{c.top_src}}')">
                                    <img src="${{c.top_img}}" alt="Top" loading="lazy">
                                    <span class="viewport-lbl">Acrylique</span>
                                </div>
                                ${{c.top_src ? `<a href="${{c.top_src}}" target="_blank" class="src-btn" title="Lien original constructeur"><i class="fa-solid fa-arrow-up-right-from-square"></i> Source Web</a>` : `<span class="src-btn disabled">Source locale</span>`}}
                            </div>`
                            : `
                            <div class="viewport-container">
                                <div class="viewport-placeholder"><i class="fa-solid fa-camera"></i><span>Photo d'époque<br>en recherche</span></div>
                                <span class="src-btn disabled">Non archivée</span>
                            </div>`;

                        // Viewport Side (Meuble) + bouton source
                        const sideBox = c.has_side_photo && c.side_img
                            ? `
                            <div class="viewport-container">
                                <div class="viewport" onclick="openModal('${{c.side_img}}', '${{c.side_src}}')">
                                    <img src="${{c.side_img}}" alt="Side" loading="lazy">
                                    <span class="viewport-lbl">Meuble</span>
                                </div>
                                ${{c.side_src ? `<a href="${{c.side_src}}" target="_blank" class="src-btn" title="Lien original constructeur"><i class="fa-solid fa-arrow-up-right-from-square"></i> Source Web</a>` : `<span class="src-btn disabled">Source locale</span>`}}
                            </div>`
                            : `
                            <div class="viewport-container">
                                <div class="viewport-placeholder"><i class="fa-solid fa-image"></i><span>Vue meuble<br>en recherche</span></div>
                                <span class="src-btn disabled">Non archivée</span>
                            </div>`;

                        // Viewport Plan 300 DPI + bouton source
                        const docBox = c.has_pdf && c.doc_img
                            ? `
                            <div class="viewport-container">
                                <div class="viewport" onclick="openModal('${{c.doc_img}}', '${{c.pdf_src}}')">
                                    <img src="${{c.doc_img}}" alt="Doc" loading="lazy">
                                    <span class="viewport-lbl">Plan 300 DPI</span>
                                </div>
                                ${{c.pdf_src ? `<a href="${{c.pdf_src}}" target="_blank" class="src-btn" title="Télécharger le PDF officiel"><i class="fa-solid fa-file-pdf"></i> Source PDF</a>` : `<span class="src-btn disabled">Plan local</span>`}}
                            </div>`
                            : `
                            <div class="viewport-container">
                                <div class="viewport-placeholder"><i class="fa-solid fa-file-pdf"></i><span>Plan technique<br>en cours</span></div>
                                <span class="src-btn disabled">Non disponible</span>
                            </div>`;

                        // Badges techniques avec liens sources directs
                        const photoBadge = c.has_real_photo
                            ? `<span class="tech-badge badge-photo"><i class="fa-solid fa-circle-check"></i> Photo Réelle</span>`
                            : `<span class="tech-badge badge-missing">Photo Manquante</span>`;

                        const dwgBadge = c.has_dwg
                            ? `<a class="tech-badge badge-dwg" href="${{c.dwg_src || '#'}}" target="_blank" title="Télécharger le fichier CAO natif (.dwg)"><i class="fa-solid fa-cube"></i> DWG (${{c.dwg_size}} MB) <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:9px;"></i></a>`
                            : `<span class="tech-badge badge-missing">DWG non publié</span>`;

                        const dxfBadge = c.has_dxf
                            ? `<a class="tech-badge badge-dxf" href="${{c.dxf_src || '#'}}" target="_blank"><i class="fa-solid fa-vector-square"></i> DXF <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:9px;"></i></a>`
                            : ``;

                        const pdfBadge = c.has_pdf
                            ? `<a class="tech-badge badge-pdf" href="${{c.pdf_src || '#'}}" target="_blank" title="Ouvrir le document d'ingénierie d'origine"><i class="fa-solid fa-file-pdf"></i> PDF Officiel <i class="fa-solid fa-arrow-up-right-from-square" style="font-size:9px;"></i></a>`
                            : ``;

                        const portalBadge = c.portal_ref
                            ? `<a class="tech-badge badge-portal" href="${{c.portal_ref}}" target="_blank" title="Accéder au portail constructeur"><i class="fa-solid fa-globe"></i> Portail</a>`
                            : ``;

                        cardEl.innerHTML = `
                            <div class="card-header">
                                <div class="card-title-box">
                                    <span class="card-model">${{c.model}}</span>
                                    <span class="card-sub">${{c.brand}} &bull; ${{c.series}}</span>
                                </div>
                                <span class="year-pill">${{c.year}}</span>
                            </div>
                            <div class="card-body">
                                <div class="viewports-row">
                                    ${{topBox}}
                                    ${{sideBox}}
                                    ${{docBox}}
                                </div>

                                <!-- 4 Mesures Simultanées -->
                                <div class="dims-box">
                                    <div class="dims-header"><i class="fa-solid fa-ruler-combined"></i> Dimensions Certifiées Constructeur</div>
                                    <div class="dim-row">
                                        <span class="dim-unit">Pouces (po)</span>
                                        <span class="dim-val">${{c.dims_4u.in}}</span>
                                    </div>
                                    <div class="dim-row">
                                        <span class="dim-unit">Pieds (pi)</span>
                                        <span class="dim-val">${{c.dims_4u.ft}}</span>
                                    </div>
                                    <div class="dim-row">
                                        <span class="dim-unit">Centim. (cm)</span>
                                        <span class="dim-val">${{c.dims_4u.cm}}</span>
                                    </div>
                                    <div class="dim-row">
                                        <span class="dim-unit">Millim. (mm)</span>
                                        <span class="dim-val">${{c.dims_4u.mm}}</span>
                                    </div>
                                </div>

                                <div class="tech-badges-row">
                                    ${{photoBadge}}
                                    ${{dwgBadge}}
                                    ${{dxfBadge}}
                                    ${{pdfBadge}}
                                    ${{portalBadge}}
                                </div>
                            </div>
                        `;
                        cardsGrid.appendChild(cardEl);
                    }}

                    modelSection.appendChild(cardsGrid);
                    brandSection.appendChild(modelSection);
                }}

                root.appendChild(brandSection);
            }}
        }}

        window.addEventListener('DOMContentLoaded', initApp);
    </script>
</body>
</html>
"""

    OUTPUT_HTML.write_text(html, encoding="utf-8")
    OUTPUT_HTML_DATASET.write_text(html, encoding="utf-8")
    print(f"Galerie générée : {OUTPUT_HTML} ({round(OUTPUT_HTML.stat().st_size / 1024, 1)} KB)")
    print(f"Copie dataset : {OUTPUT_HTML_DATASET}")

if __name__ == "__main__":
    main()
