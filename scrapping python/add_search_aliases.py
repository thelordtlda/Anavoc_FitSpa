import json
import csv
from pathlib import Path

index_path = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/spa_master_index.json")
csv_path = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/spa_master_index.csv")

with open(index_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Mapping of alias terms to brand/series criteria
alias_rules = [
    ("HotSpring", lambda r: r.get("brand") == "Hot Spring Spas"),
    ("Saundance", lambda r: r.get("brand") == "Sundance Spas"),
    ("Sundance ", lambda r: r.get("brand") == "Sundance Spas"),
    ("Bullfrog ", lambda r: r.get("brand") == "Bullfrog Spas"),
    ("Marquise", lambda r: r.get("brand") == "Marquis Spas"),
    ("Trevi", lambda r: "trévi" in r.get("brand", "").lower()),
    ("Trevi ", lambda r: "trévi" in r.get("brand", "").lower()),
    ("Artesian Garden Spas", lambda r: r.get("brand") == "Artesian Spas" and ("garden" in r.get("series", "").lower() or "cruz" in r.get("model", "").lower())),
    ("Artesian Island Spa", lambda r: r.get("brand") == "Artesian Spas" and ("island" in r.get("series", "").lower() or "bahama" in r.get("model", "").lower() or "cayman" in r.get("model", "").lower() or "antigua" in r.get("model", "").lower() or "captiva" in r.get("model", "").lower())),
    ("Artesian Island Spa Elite", lambda r: r.get("brand") == "Artesian Spas" and ("island" in r.get("series", "").lower() or "bahama" in r.get("model", "").lower())),
    ("Artesian South Seas", lambda r: r.get("brand") == "Artesian Spas" and "south seas" in r.get("model", "").lower()),
    ("TidalFit", lambda r: r.get("brand") == "Artesian Spas" and "tidalfit" in r.get("model", "").lower()),
    ("Cantabria", lambda r: r.get("brand") == "Caldera Spas" and "cantabria" in r.get("model", "").lower()),
    ("Celebrity Elite", lambda r: r.get("brand") == "Marquis Spas" and ("celebrity" in r.get("series", "").lower() or "vector" in r.get("series", "").lower() or "v" in r.get("model", "").lower())),
    ("Celebrity Standard", lambda r: r.get("brand") == "Marquis Spas" and ("celebrity" in r.get("series", "").lower() or "vector" in r.get("series", "").lower() or "v" in r.get("model", "").lower())),
    ("Crown", lambda r: "crown" in r.get("model", "").lower() or "crown" in r.get("series", "").lower()),
    ("Vector", lambda r: r.get("brand") == "Marquis Spas" and "v" in r.get("model", "").lower()),
    ("Beach Collection", lambda r: "beach" in r.get("model", "").lower() or "beach" in r.get("brand", "").lower()),
    ("Palmbeach Collection", lambda r: "palmbeach" in r.get("model", "").lower() or "beach" in r.get("brand", "").lower()),
    ("Daytona Beach Collection", lambda r: "daytona" in r.get("model", "").lower() or "beach" in r.get("brand", "").lower()),
    ("WELLIS", lambda r: r.get("brand", "").lower() == "wellis"),
]

for r in data:
    if "aliases" not in r:
        r["aliases"] = []
    for alias_name, predicate in alias_rules:
        if predicate(r):
            if alias_name not in r["aliases"]:
                r["aliases"].append(alias_name)

# Resave JSON
with open(index_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

# Resave CSV with aliases column
headers = [
    "brand", "model", "series", "vintage_year", "generation_id",
    "length_in", "width_in", "height_in", "corner_radius_in", "corner_type",
    "length_mm", "width_mm", "height_mm", "corner_radius_mm",
    "jetpaks_count", "raised_back", "waterfall_curved", "keypad_protruding", "filter_lid_rigid",
    "has_top_view", "has_side_view", "has_footprint", "has_model_3d",
    "source_manual", "completeness_score_pct", "spafit_notes", "aliases"
]

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for r in data:
        d = r.get("dimensions", {})
        o = r.get("obstacles", {})
        m = r.get("media", {})
        writer.writerow([
            r.get("brand", ""),
            r.get("model", ""),
            r.get("series", ""),
            r.get("vintage_year", ""),
            r.get("generation_id", ""),
            d.get("length_in", 0),
            d.get("width_in", 0),
            d.get("height_in", 0),
            d.get("corner_radius_in", 0),
            d.get("corner_type", ""),
            d.get("length_mm", 0),
            d.get("width_mm", 0),
            d.get("height_mm", 0),
            d.get("corner_radius_mm", 0),
            o.get("jetpaks_count", 0),
            o.get("raised_back", False),
            o.get("waterfall_curved", False),
            o.get("keypad_protruding", False),
            o.get("filter_lid_rigid", False),
            m.get("has_top_view", False),
            m.get("has_side_view", False),
            m.get("has_footprint", False),
            m.get("has_model_3d", False),
            r.get("source_manual", ""),
            f"{m.get('completeness_score_pct', 100.0)}%",
            r.get("spafit_notes", ""),
            "|".join(r.get("aliases", []))
        ])

print("Aliases added and Master Index updated!")
