#!/usr/bin/env python3
"""
scripts/generate_catalog_json.py

Refactored Compatibility Engine (Phase 3):
1. Swim Spa Radius Sentinel Handling:
   Safely parses corner_radius_in; assigns internal tolerance radius (6.0")
   for swim spas when radius is non-numeric or 'N/A (Swim Spa)'.
2. Dynamic Height & Radius Bounds:
   Reads h_min, h_max, s_r_min, s_r_max directly from models.json without hardcoded clamps.
   Enables swim spas (height 50"-55") to evaluate cleanly against Legend and Endless Pools.
3. Strict Entry Orientation Constraint:
   Enforces orientation_entree (short_side, long_side, any) to prevent unrealistic inverted evaluations.
4. Point-to-Curve Distance for Circular Spas:
   Computes exact Euclidean clearance from circular perimeter to Cover corner posts.
5. Emits cad_svg_contour for models with CAD vector contours.
6. Compiles data/spas_catalog_data.json and data/spas_catalog_data.js.
"""

import os
import csv
import json
import math
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT_DIR / 'data' / 'spas_master_database.csv'
COVER_MODELS_PATH = ROOT_DIR / 'data' / 'models.json'
OUT_JSON_PATH = ROOT_DIR / 'data' / 'spas_catalog_data.json'
OUT_JS_PATH = ROOT_DIR / 'data' / 'spas_catalog_data.js'

def check_compat(spa, cover):
    try:
        l = float(spa.get('length_in') or 0)
        w = float(spa.get('width_in') or 0)
        h = float(spa.get('height_in') or 0)
    except:
        return {'status': 'err', 'reasons': ['Missing or invalid dimensions']}

    if l <= 0 or w <= 0:
        return {'status': 'err', 'reasons': ['Zero or negative dimensions']}

    spa_l = max(l, w)
    spa_w = min(l, w)

    # 1. Swim Spa Radius Sentinel Handling
    raw_r = str(spa.get('corner_radius_in') or '').strip()
    is_swim_spa = (
        'swim' in raw_r.lower() or 
        'swim' in (spa.get('Segment') or '').lower() or 
        'swim' in (spa.get('Marque') or '').lower() or
        spa_l >= 130.0
    )
    if is_swim_spa and (raw_r in ('', 'N/A', 'None') or 'swim' in raw_r.lower()):
        r = 6.0
    else:
        clean_r = re.sub(r'[^0-9.]', '', raw_r)
        try:
            r = float(clean_r) if clean_r else 8.0
        except ValueError:
            r = 8.0

    # 2. Dynamic Specs from models.json
    cols = cover.get('degagement_colonnes', {})
    col_l = float(cols.get('longueur', 0))
    col_w = float(cols.get('largeur', 0))
    
    seal = cover.get('joint_etancheite', {})
    s_l_min = float(seal.get('longueur_min', 0))
    s_l_max = float(seal.get('longueur_max', 999))
    s_w_min = float(seal.get('largeur_min', 0))
    s_w_max = float(seal.get('largeur_max', 999))
    s_r_min = float(seal.get('rayon_min', 2.0))
    s_r_max = float(seal.get('rayon_max', 24.0))

    h_spec = cover.get('hauteur', {})
    h_min = float(h_spec.get('spa_min', 30.0))
    h_max = float(h_spec.get('spa_max', 65.0))

    # 3. Circular Spa Handling (Point-to-Curve Euclidean Distance)
    is_circular = abs(l - w) <= 2.0 and (abs(r - l / 2.0) <= 2.0 or r >= (l / 2.0 - 2.0))
    if is_circular:
        dia = spa_l
        r_circ = dia / 2.0
        margin_x = (col_l - dia) / 2.0
        margin_y = (col_w - dia) / 2.0
        diag_col = math.sqrt((col_l / 2.0)**2 + (col_w / 2.0)**2)
        diag_clearance = diag_col - r_circ

        col_fit = (margin_x >= 0.5) and (margin_y >= 0.5) and (diag_clearance >= 0.5)
        seal_fit = (dia >= s_l_min and dia <= s_l_max) and (dia >= s_w_min and dia <= s_w_max)
        r_fit = True  # Circular adapter kit fits all round spas within diametric bounds
        h_fit = (h >= h_min and h <= h_max) if h > 0 else True

        reasons = []
        if not col_fit: reasons.append(f"Diamètre ({dia}\") excède les colonnes ({col_l}\" x {col_w}\")")
        if not seal_fit: reasons.append(f"Diamètre ({dia}\") hors plage du joint")
        if not h_fit: reasons.append(f"Hauteur ({h}\") hors plage [{h_min}-{h_max}]\")")

        is_perfect = (margin_x >= 1.0) and (margin_y >= 1.0) and seal_fit and h_fit
        is_warn = col_fit and seal_fit and (not is_perfect)
        status = 'ok' if is_perfect else ('warn' if is_warn else 'err')

        return {
            'status': status,
            'orientation': 'circular',
            'margin_x': round(margin_x, 2),
            'margin_y': round(margin_y, 2),
            'diag_clearance': round(diag_clearance, 2),
            'col_fit': col_fit,
            'seal_fit': seal_fit,
            'r_fit': r_fit,
            'h_fit': h_fit,
            'reasons': reasons
        }

    # 4. Strict Entry Orientation Constraint
    gamme = cover.get('gamme', '')
    orient_spec = str(cover.get('orientation_entree', 'any')).lower()
    
    # Swim spas (Legend / Endless Pools) MUST align length with Cover length
    if gamme in ['Legend', 'Endless Pools', 'Legend 89'] or cover.get('type') == 'swim_spa':
        orientations = [{'orient': 'standard', 'l': spa_l, 'w': spa_w}]
    elif 'short side' in orient_spec or 'long side' in orient_spec:
        # Standard orientation alignment only
        orientations = [{'orient': 'standard', 'l': spa_l, 'w': spa_w}]
    else:
        # Any / flexible
        orientations = [
            {'orient': 'standard', 'l': spa_l, 'w': spa_w},
            {'orient': 'rotated', 'l': spa_w, 'w': spa_l}
        ]

    best_fit = None
    for o in orientations:
        ol = o['l']
        ow = o['w']

        margin_x = (col_l - ol) / 2.0
        margin_y = (col_w - ow) / 2.0

        col_fit = (margin_x >= 0.5) and (margin_y >= 0.5)
        seal_fit = (ol >= s_l_min and ol <= s_l_max) and (ow >= s_w_min and ow <= s_w_max)
        r_fit = (r >= s_r_min and r <= s_r_max) if r > 0 else True
        h_fit = (h >= h_min and h <= h_max) if h > 0 else True

        reasons = []
        if margin_x < 0.5: reasons.append(f"Longueur excède colonnes ({ol}\" vs max {col_l}\")")
        if margin_y < 0.5: reasons.append(f"Largeur excède colonnes ({ow}\" vs max {col_w}\")")
        if not (ol >= s_l_min and ol <= s_l_max): reasons.append(f"Longueur hors joint ({ol}\" vs [{s_l_min}-{s_l_max}]\")")
        if not (ow >= s_w_min and ow <= s_w_max): reasons.append(f"Largeur hors joint ({ow}\" vs [{s_w_min}-{s_w_max}]\")")
        if not r_fit: reasons.append(f"Rayon coin {r}\" hors plage [{s_r_min}-{s_r_max}]\")")
        if not h_fit: reasons.append(f"Hauteur {h}\" hors plage [{h_min}-{h_max}]\")")

        is_perfect = (margin_x >= 1.0) and (margin_y >= 1.0) and seal_fit and r_fit and h_fit
        is_warn = col_fit and seal_fit and (not is_perfect)

        status = 'ok' if is_perfect else ('warn' if is_warn else 'err')
        candidate = {
            'status': status,
            'orientation': o['orient'],
            'margin_x': round(margin_x, 2),
            'margin_y': round(margin_y, 2),
            'col_fit': col_fit,
            'seal_fit': seal_fit,
            'r_fit': r_fit,
            'h_fit': h_fit,
            'reasons': reasons
        }

        if best_fit is None or (candidate['status'] == 'ok') or (candidate['status'] == 'warn' and best_fit['status'] == 'err'):
            best_fit = candidate

    return best_fit

def generate_catalog():
    print("=" * 80)
    print("TASK 3.2 & 3.4: REFACTOR COMPATIBILITY ENGINE & COMPILE CATALOG JSON/JS")
    print("=" * 80)

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        spas = list(reader)

    print(f"Loaded {len(spas)} spas from {CSV_PATH}.")

    cover_models = []
    if COVER_MODELS_PATH.exists():
        with open(COVER_MODELS_PATH, 'r', encoding='utf-8') as f:
            cover_models = json.load(f)
    print(f"Loaded {len(cover_models)} Cover models from {COVER_MODELS_PATH}.")

    # Precalculate compatibility for each spa
    gamme_matches = {'Oasis': 0, 'Horizon': 0, 'Evolution': 0, 'Legend': 0, 'Endless Pools': 0, 'Legend 89': 0}
    total_matched_spas = 0

    for idx, spa in enumerate(spas):
        spa['id'] = idx + 1
        compatible_models = []
        optimal_models = []

        # Check for CAD SVG vector contour file
        dxf_p = spa.get('cad_dxf_file', '')
        if dxf_p and dxf_p != 'N/A':
            candidates = [
                dxf_p.replace('.dxf', '_cad.svg'),
                dxf_p.replace('.dxf', '_authentic_cad.svg'),
                dxf_p.replace('_authentic.dxf', '_authentic_cad.svg'),
                dxf_p.replace('.dxf', '.svg')
            ]
            for cand in candidates:
                abs_svg = ROOT_DIR / (cand[2:] if cand.startswith('./') else cand)
                if abs_svg.exists():
                    spa['cad_svg_contour'] = cand
                    break

        matched_gammes = set()
        for c_mod in cover_models:
            fit = check_compat(spa, c_mod)
            if fit['status'] == 'ok':
                optimal_models.append(c_mod['id'])
                compatible_models.append(c_mod['id'])
                matched_gammes.add(c_mod.get('gamme'))
            elif fit['status'] == 'warn':
                compatible_models.append(c_mod['id'])
                matched_gammes.add(c_mod.get('gamme'))
                
        spa['cover_compatible'] = compatible_models
        spa['cover_optimal'] = optimal_models

        if compatible_models:
            total_matched_spas += 1
            for g in matched_gammes:
                if g in gamme_matches:
                    gamme_matches[g] += 1

    print("\nCompatibility Evaluation Results:")
    print(f"  Total spas with at least 1 Cover fit: {total_matched_spas} / {len(spas)} ({total_matched_spas/len(spas)*100:.1f}%)")
    for g, count in gamme_matches.items():
        print(f"  - {g:14}: {count:4d} spas compatibles")

    output_payload = {
        'spas': spas,
        'cover_models': cover_models
    }

    with open(OUT_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(output_payload, f, ensure_ascii=False, indent=2)

    with open(OUT_JS_PATH, 'w', encoding='utf-8') as f:
        f.write('window.SPAFIT_CATALOG_DATA = ')
        json.dump(output_payload, f, ensure_ascii=False)
        f.write(';\n')

    print(f"\n[OK] Catalog JSON successfully generated at {OUT_JSON_PATH}")
    print(f"[OK] Catalog JS successfully generated at {OUT_JS_PATH}")

if __name__ == '__main__':
    generate_catalog()
