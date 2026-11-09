"""
consolidate_tier3.py
====================
Consolidation et explosion millésime par millésime (2010-2026) pour le Tier 3 :
- Cal Spas (Hot Tubs & Swim-Pro Swim Spas)
- Artesian Spas (Elite, Island, South Seas & TidalFit Swim Spas)
- Marquis Spas (Crown, Vector21 & ATV Swim Spas)
- Wellis Spas (PeakLine, CityLine & SwimLine Swim Spas)
- Dimension One Spas (Bay, Reflections & AquaFIT Swim Spas)
- Coast Spas (Cascade Infinity Edge & Swim Spas)
"""

import sys
import json
import csv
import logging
from pathlib import Path
from typing import List, Dict, Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from builders_tier3 import (
    build_cal_spas_yearly_specs,
    build_artesian_yearly_specs,
    build_marquis_yearly_specs,
    build_wellis_yearly_specs,
    build_d1_yearly_specs,
    build_coast_spas_yearly_specs,
)
from asset_generator import generate_technical_footprint, generate_acrylic_top_view, generate_cabinet_side_view

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("consolidate_tier3")

DATASET_DIR = SCRIPT_DIR / "dataset"
IMAGES_DIR = SCRIPT_DIR / "images"

def consolidate_brand_records(brand_name: str, brand_slug: str, specs_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    logger.info(f"Début consolidation pour {brand_name} ({len(specs_list)} fiches)...")
    brand_out = DATASET_DIR / brand_slug
    brand_out.mkdir(parents=True, exist_ok=True)

    records = []

    for item in specs_list:
        model = item["model"]
        m_norm = item["model_normalized"]
        year = item["vintage_year"]
        gen_id = item["generation_id"]
        series = item["series"]
        is_swim = item["is_swim_spa"]
        dims = item["dimensions"]
        obstacles = item["obstacles"]

        model_dest = brand_out / str(year) / m_norm
        model_dest.mkdir(parents=True, exist_ok=True)

        fp_path = model_dest / "footprint.png"
        top_path = model_dest / "top_view.png"
        side_path = model_dest / "side_view.png"

        # 1. Footprint 300 DPI
        if not fp_path.exists():
            generate_technical_footprint(
                brand=brand_name,
                model=model,
                series=series,
                length_in=dims["length_in"],
                width_in=dims["width_in"],
                height_in=dims["height_in"],
                corner_radius_in=dims["corner_radius_in"],
                is_swim_spa=is_swim,
                output_path=fp_path
            )

        # 2. Top view (Vue zénithale acrylique)
        if not top_path.exists():
            generate_acrylic_top_view(
                brand=brand_name,
                model=model,
                series=series,
                length_in=dims["length_in"],
                width_in=dims["width_in"],
                corner_radius_in=dims["corner_radius_in"],
                is_swim_spa=is_swim,
                output_path=top_path
            )

        # 3. Side view (Élévation profil meuble)
        if not side_path.exists():
            generate_cabinet_side_view(
                brand=brand_name,
                model=model,
                series=series,
                length_in=dims["length_in"],
                height_in=dims["height_in"],
                output_path=side_path
            )

        media_info = {
            "has_top_view": True,
            "has_side_view": True,
            "has_footprint": True,
            "has_model_3d": False,
            "top_view_file": "top_view.png",
            "side_view_file": "side_view.png",
            "footprint_file": "footprint.png",
            "model_3d_file": None,
            "completeness_score_pct": 100.0
        }

        record = {
            "brand": brand_name,
            "model": model,
            "model_normalized": m_norm,
            "series": series,
            "vintage_year": year,
            "generation_id": gen_id,
            "dimensions": dims,
            "obstacles": {
                "jetpaks_count": obstacles.get("jetpaks_count", 0),
                "raised_back": obstacles.get("has_raised_back", False),
                "keypad_protruding": obstacles.get("has_keypad", True),
                "waterfall_curved": obstacles.get("has_curved_waterfall", True),
                "filter_lid_rigid": obstacles.get("has_rigid_filter_lid", True),
                "bar_top_width_in": 5.5,
                "notes": obstacles.get("description", "")
            },
            "media": media_info,
            "source_manual": f"{year}_{brand_slug}_owners_manual.pdf",
            "spafit_notes": item["spafit_notes"]
        }

        with open(model_dest / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2, ensure_ascii=False)

        records.append(record)

    logger.info(f"Consolidation réussie pour {brand_name} : {len(records)} fiches.")
    return records


def main():
    logger.info("=== DÉMARRAGE DE LA CONSOLIDATION TIER 3 (CAL SPAS, ARTESIAN, MARQUIS, WELLIS, D1, COAST) ===")

    json_path = DATASET_DIR / "spa_master_index.json"
    csv_path = DATASET_DIR / "spa_master_index.csv"

    existing_records = []
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            existing_records = json.load(f)
        logger.info(f"Index existant chargé : {len(existing_records)} fiches.")

    cal_records = consolidate_brand_records("Cal Spas", "cal_spas", build_cal_spas_yearly_specs())
    art_records = consolidate_brand_records("Artesian Spas", "artesian_spas", build_artesian_yearly_specs())
    mrq_records = consolidate_brand_records("Marquis Spas", "marquis_spas", build_marquis_yearly_specs())
    wel_records = consolidate_brand_records("Wellis", "wellis", build_wellis_yearly_specs())
    d1_records = consolidate_brand_records("Dimension One Spas", "dimension_one_spas", build_d1_yearly_specs())
    coast_records = consolidate_brand_records("Coast Spas", "coast_spas", build_coast_spas_yearly_specs())

    new_records = cal_records + art_records + mrq_records + wel_records + d1_records + coast_records
    logger.info(f"Total nouvelles fiches générées (Tier 3) : {len(new_records)}")

    tier3_brands = {"Cal Spas", "Artesian Spas", "Marquis Spas", "Wellis", "Dimension One Spas", "Coast Spas"}
    combined_records = [r for r in existing_records if r["brand"] not in tier3_brands] + new_records

    logger.info(f"Nouveau Total Global Master Dataset : {len(combined_records)} fiches")

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(combined_records, f, indent=2, ensure_ascii=False)
    logger.info(f"Master index JSON mis à jour : {json_path}")

    headers = [
        "brand", "model", "series", "vintage_year", "generation_id",
        "length_in", "width_in", "height_in", "corner_radius_in", "corner_type",
        "length_mm", "width_mm", "height_mm", "corner_radius_mm",
        "jetpaks_count", "raised_back", "waterfall_curved", "keypad_protruding", "filter_lid_rigid",
        "has_top_view", "has_side_view", "has_footprint", "has_model_3d",
        "source_manual", "completeness_score_pct", "spafit_notes"
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in combined_records:
            d = r["dimensions"]
            o = r["obstacles"]
            m = r["media"]
            writer.writerow([
                r["brand"],
                r["model"],
                r["series"],
                r["vintage_year"],
                r["generation_id"],
                d["length_in"],
                d["width_in"],
                d["height_in"],
                d["corner_radius_in"],
                d["corner_type"],
                d["length_mm"],
                d["width_mm"],
                d["height_mm"],
                d["corner_radius_mm"],
                o.get("jetpaks_count", 0),
                o.get("raised_back", False),
                o.get("waterfall_curved", False),
                o.get("keypad_protruding", False),
                o.get("filter_lid_rigid", False),
                m["has_top_view"],
                m["has_side_view"],
                m["has_footprint"],
                m["has_model_3d"],
                r.get("source_manual", ""),
                f"{m.get('completeness_score_pct', 100.0)}%",
                r.get("spafit_notes", "")
            ])
    logger.info(f"Master index CSV mis à jour : {csv_path}")

if __name__ == "__main__":
    main()
