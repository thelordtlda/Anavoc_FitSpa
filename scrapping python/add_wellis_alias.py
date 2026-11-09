import json
import csv
from pathlib import Path

index_path = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/spa_master_index.json")
csv_path = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/spa_master_index.csv")

with open(index_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Find Wellis records and create WELLIS alias records
wellis_records = [r for r in data if r["brand"] == "Wellis"]
alias_records = []
for r in wellis_records:
    r_copy = json.loads(json.dumps(r))
    r_copy["brand"] = "WELLIS"
    alias_records.append(r_copy)

data.extend(alias_records)

with open(index_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Rewrite CSV
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
    for r in data:
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

print(f"Added {len(alias_records)} WELLIS records. New total: {len(data)}")
