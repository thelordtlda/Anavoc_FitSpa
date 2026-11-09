import csv
import hashlib
from pathlib import Path

csv_path = Path("data/spas_master_database.csv")
with open(csv_path, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

watkins_dir = Path("_ARCHIVE/scrapping_legacy/dataset_raw_watkins_harvest/hot_spring_spas")
all_harvest_dwgs = list(watkins_dir.rglob("*.dwg"))
harvest_hashes = set()
for p in all_harvest_dwgs:
    with open(p, "rb") as f:
        harvest_hashes.add(hashlib.md5(f.read()).hexdigest())

print(f"Total harvest hashes: {len(harvest_hashes)}")

for idx, r in enumerate(rows):
    dwg = r.get("cad_dwg_file")
    if dwg and dwg != "N/A":
        p = Path(dwg)
        if p.exists():
            with open(p, "rb") as f:
                h = hashlib.md5(f.read()).hexdigest()
            if h not in harvest_hashes:
                print(f"Linked DWG not from harvest archive: Row {idx+2}: {r['Marque']} {r['Modele']} {r['Generation']} -> {dwg}")
