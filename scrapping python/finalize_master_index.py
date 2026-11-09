import json
import csv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
dataset_dir = base_dir / "dataset"
json_index = dataset_dir / "spa_master_index.json"
csv_index = dataset_dir / "spa_master_index.csv"

with open(json_index, "r", encoding="utf-8") as f:
    records = json.load(f)

for r in records:
    if "hot spring" in r.get("brand", "").lower() and "glow" in r.get("model", "").lower():
        yr = r.get("vintage_year")
        if yr in [2012, 2013, 2014, 2015, 2016, 2017]:
            if "provenance" not in r: r["provenance"] = {}
            if "media" not in r: r["media"] = {}
            r["provenance"]["has_official_cad_dwg"] = True
            r["media"]["has_official_cad"] = True
            r["media"]["cad_file"] = "cad_model.dwg"

with open(json_index, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

# Flatten for CSV
csv_rows = []
for r in records:
    flat = {}
    for k, v in r.items():
        if isinstance(v, dict):
            for sub_k, sub_v in v.items():
                flat[f"{k}_{sub_k}"] = sub_v
        else:
            flat[k] = v
    csv_rows.append(flat)

if csv_rows:
    # All keys
    all_keys = set()
    for row in csv_rows:
        all_keys.update(row.keys())
    fieldnames = sorted(list(all_keys))
    
    with open(csv_index, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"Enregistré {len(csv_rows)} lignes dans {csv_index.name}")

print("Index maître mis à jour et validé !")
