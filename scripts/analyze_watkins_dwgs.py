import csv
import hashlib
from pathlib import Path
from collections import defaultdict

# 1. Load catalog rows
csv_path = Path("data/spas_master_database.csv")
with open(csv_path, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

# 2. Index linked DWGs
linked_dwgs = {}
for idx, r in enumerate(rows):
    dwg = r.get("cad_dwg_file")
    if dwg and dwg != "N/A":
        p = Path(dwg)
        linked_dwgs[p.name.lower()] = (idx + 2, r["Marque"], r["Modele"], r["Generation"], r["Annees_Production"], dwg)

print(f"Total catalog rows: {len(rows)}")
print(f"Total currently linked DWGs in catalog: {len(linked_dwgs)}")

# 3. Scan all 277 DWGs in Watkins harvest
watkins_dir = Path("_ARCHIVE/scrapping_legacy/dataset_raw_watkins_harvest/hot_spring_spas")
all_dwgs = sorted(list(watkins_dir.rglob("*.dwg")))
print(f"Total DWGs in Watkins harvest: {len(all_dwgs)}")

dwg_info = []
for p in all_dwgs:
    folder_name = p.parent.name # e.g. hot_spring_grandee_2002
    parts = folder_name.split("_")
    year = int(parts[-1]) if parts[-1].isdigit() else 0
    # model token
    model_tokens = parts[2:-1] if len(parts) >= 4 else parts[2:]
    model_str = " ".join(model_tokens).title()
    
    with open(p, "rb") as f:
        data = f.read()
        md5 = hashlib.md5(data).hexdigest()

    dwg_info.append({
        "path": p,
        "folder": folder_name,
        "year": year,
        "model": model_str,
        "size": len(data),
        "md5": md5
    })

# Check unique MD5s
by_md5 = defaultdict(list)
for item in dwg_info:
    by_md5[item["md5"]].append(item)

print(f"Unique binary MD5 hashes: {len(by_md5)}")

# Print breakdown by model
by_model = defaultdict(list)
for item in dwg_info:
    by_model[item["model"]].append(item)

print("\n=== MODEL BREAKDOWN ===")
for model, items in sorted(by_model.items()):
    years = [it["year"] for it in items]
    unique_hashes = len(set(it["md5"] for it in items))
    print(f"Model '{model:20s}': {len(items):2d} DWGs | Years {min(years)}-{max(years)} | Unique binaries: {unique_hashes}")
