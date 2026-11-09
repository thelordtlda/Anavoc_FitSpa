import csv
import hashlib
from pathlib import Path
from collections import defaultdict

csv_path = Path("data/spas_master_database.csv")
with open(csv_path, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

# Map linked DWGs
linked_dwg_files = {}
for idx, r in enumerate(rows):
    dwg = r.get("cad_dwg_file")
    if dwg and dwg != "N/A":
        p = Path(dwg)
        linked_dwg_files[p.name.lower()] = (idx + 2, r["Marque"], r["Modele"], r["Generation"], r["Annees_Production"], dwg)

watkins_dir = Path("_ARCHIVE/scrapping_legacy/dataset_raw_watkins_harvest")
all_dwgs = list(watkins_dir.rglob("*.dwg"))
print(f"Total DWG files found in {watkins_dir}: {len(all_dwgs)}")

# Compute MD5 for each file
dwg_records = []
md5_groups = defaultdict(list)
for p in all_dwgs:
    with open(p, "rb") as f:
        data = f.read()
        h = hashlib.md5(data).hexdigest()
    rec = {
        "path": p,
        "name": p.name,
        "rel": str(p.relative_to(watkins_dir)),
        "size": len(data),
        "md5": h,
        "parent": p.parent.name
    }
    dwg_records.append(rec)
    md5_groups[h].append(rec)

print(f"Unique MD5 hashes among {len(all_dwgs)} DWGs: {len(md5_groups)}")

# Check how many are already linked
linked_count = 0
unlinked_records = []
for rec in dwg_records:
    # Check if this file or identical MD5 is linked
    name = rec["name"].lower()
    # Check if linked in catalog
    is_linked = False
    for l_name, l_info in linked_dwg_files.items():
        if l_name == name:
            is_linked = True
            break
    if is_linked:
        linked_count += 1
    else:
        unlinked_records.append(rec)

print(f"Direct filename matches to linked: {linked_count}")
print(f"Unlinked candidate files: {len(unlinked_records)}")

# Group unlinked by model and year
by_model = defaultdict(list)
for rec in unlinked_records:
    parent = rec["parent"]
    # parent is e.g. hot_spring_grandee_2002
    parts = parent.split("_")
    # find year
    year = parts[-1] if parts[-1].isdigit() else "unknown"
    model_parts = parts[:-1]
    model_name = "_".join(model_parts)
    by_model[model_name].append((year, rec))

print(f"\nUnlinked models found ({len(by_model)} unique model series):")
for m, recs in sorted(by_model.items()):
    years = [r[0] for r in recs]
    print(f"  {m:30s}: {len(recs):3d} DWGs (Years: {min(years)}-{max(years)})")
