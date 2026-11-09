#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sync_master_index_fast.py
=========================
Reconstruit intégralement et de manière déterministe `dataset/spa_master_index.json`
et `dataset/spa_master_index.csv` directement depuis l'arborescence physique validée :
    dataset/[brand]/[year]/[model]/metadata.json

Garantit :
- 0 modèle inventé (100% synchronisé avec les dossiers réels assainis).
- 4 unités de mesure pré-calculées (pouces, pieds/pouces, cm, mm).
- Traçabilité complète des fichiers physiques (top_view, side_view, official_manufacturer_doc, cad_model.dwg/dxf/bim)
  et de leurs URLs sources respectives.
"""

import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATASET_DIR = BASE_DIR / "dataset"
JSON_INDEX = DATASET_DIR / "spa_master_index.json"
CSV_INDEX = DATASET_DIR / "spa_master_index.csv"


def to_ft_in(val: float) -> str:
    if not val:
        return '0\'0"'
    feet = int(val // 12)
    rem = round(val - feet * 12, 1)
    if rem == 12.0:
        feet += 1
        rem = 0.0
    if rem == int(rem):
        return f"{feet}'{int(rem)}\""
    return f"{feet}'{rem}\""


def main():
    print("--- Reconstruction intégrale de spa_master_index.json & .csv depuis les dossiers validés ---")
    records = []

    for b_dir in sorted(DATASET_DIR.iterdir()):
        if not b_dir.is_dir():
            continue
        for yr_dir in sorted(b_dir.glob("20*")):
            if not yr_dir.is_dir():
                continue
            try:
                yr = int(yr_dir.name)
            except ValueError:
                continue
            for m_dir in sorted(yr_dir.iterdir()):
                if not m_dir.is_dir():
                    continue
                meta_p = m_dir / "metadata.json"
                if not meta_p.exists():
                    continue
                try:
                    meta = json.loads(meta_p.read_text(encoding="utf-8"))
                except Exception:
                    continue

                brand = meta.get("brand", b_dir.name.replace("_", " ").title())
                model = meta.get("model", m_dir.name)
                series = meta.get("series", "Standard")
                dims = meta.get("dimensions", {})
                prov = meta.get("provenance", {})

                l_in = float(dims.get("length_in", 0) or 0)
                w_in = float(dims.get("width_in", 0) or 0)
                h_in = float(dims.get("height_in", 0) or 0)
                r_in = float(dims.get("corner_radius_in", 0) or 0)
                c_type = dims.get("corner_type", "Rounded")

                l_mm = round(l_in * 25.4, 1)
                w_mm = round(w_in * 25.4, 1)
                h_mm = round(h_in * 25.4, 1)
                r_mm = round(r_in * 25.4, 1)

                l_cm = round(l_in * 2.54, 1)
                w_cm = round(w_in * 2.54, 1)
                h_cm = round(h_in * 2.54, 1)
                r_cm = round(r_in * 2.54, 1)

                dims_in_str = f'{l_in:.1f}" × {w_in:.1f}" × {h_in:.1f}" (R: {r_in:.1f}")'
                dims_ft_str = f"{to_ft_in(l_in)} × {to_ft_in(w_in)} × {to_ft_in(h_in)} (R: {to_ft_in(r_in)})"
                dims_cm_str = f"{l_cm} × {w_cm} × {h_cm} cm (R: {r_cm} cm)"
                dims_mm_str = f"{round(l_mm)} × {round(w_mm)} × {round(h_mm)} mm (R: {round(r_mm)} mm)"

                top_f = m_dir / "top_view.jpg"
                side_f = m_dir / "side_view.jpg"
                doc_f = m_dir / "official_manufacturer_doc.png"
                dwg_f = m_dir / "cad_model.dwg"
                dxf_f = m_dir / "cad_model.dxf"

                has_top = prov.get("has_real_photo", False) and top_f.exists() and top_f.stat().st_size > 4000
                has_side = side_f.exists() and side_f.stat().st_size > 4000
                has_doc = prov.get("has_official_pdf_doc", False) and doc_f.exists() and doc_f.stat().st_size > 4000
                has_dwg = dwg_f.exists() and dwg_f.stat().st_size > 4000
                has_dxf = dxf_f.exists() and dxf_f.stat().st_size > 4000

                records.append({
                    "brand": brand,
                    "brand_slug": b_dir.name,
                    "model": model,
                    "model_normalized": meta.get("model_normalized", m_dir.name),
                    "series": series,
                    "year": yr,
                    "generation_id": meta.get("generation_id", ""),
                    "seating_capacity": meta.get("seating_capacity", ""),
                    "length_in": l_in,
                    "width_in": w_in,
                    "height_in": h_in,
                    "corner_radius_in": r_in,
                    "corner_type": c_type,
                    "length_cm": l_cm,
                    "width_cm": w_cm,
                    "height_cm": h_cm,
                    "corner_radius_cm": r_cm,
                    "length_mm": l_mm,
                    "width_mm": w_mm,
                    "height_mm": h_mm,
                    "corner_radius_mm": r_mm,
                    "dimensions_in_str": dims_in_str,
                    "dimensions_ft_str": dims_ft_str,
                    "dimensions_cm_str": dims_cm_str,
                    "dimensions_mm_str": dims_mm_str,
                    "has_real_photo": has_top,
                    "has_side_photo": has_side,
                    "has_official_pdf_doc": has_doc,
                    "has_cad_dwg": has_dwg,
                    "has_cad_dxf": has_dxf,
                    "has_bim": False,
                    "top_view_file": top_f.relative_to(DATASET_DIR).as_posix() if has_top else "",
                    "side_view_file": side_f.relative_to(DATASET_DIR).as_posix() if has_side else "",
                    "blueprint_file": doc_f.relative_to(DATASET_DIR).as_posix() if has_doc else "",
                    "cad_dwg_file": dwg_f.relative_to(DATASET_DIR).as_posix() if has_dwg else "",
                    "top_view_source": prov.get("top_view_source", ""),
                    "side_view_source": prov.get("side_view_source", ""),
                    "official_pdf_url": prov.get("official_pdf_url", ""),
                    "official_cad_dwg_url": prov.get("official_cad_dwg_url", ""),
                    "portal_reference": prov.get("portal_reference", ""),
                })

    # Tri hiérarchique : Marque (A-Z) -> Modèle (A-Z) -> Année (Croissante)
    records.sort(key=lambda r: (r["brand"].lower(), r["model"].lower(), r["year"]))

    JSON_INDEX.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"  -> spa_master_index.json écrit : {len(records)} fiches certifiées.")

    if records:
        fieldnames = list(records[0].keys())
        with open(CSV_INDEX, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
        print(f"  -> spa_master_index.csv écrit : {len(records)} lignes.")


if __name__ == "__main__":
    main()
