import csv
import json
from pathlib import Path

csv_path = Path("data/spas_master_database.csv")
with open(csv_path, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

print("=== 1. ARTESIAN SPAS ROWS WITH PHOTOS ===")
for idx, r in enumerate(rows):
    if r["Marque"] == "Artesian Spas" and r.get("image_top_file") and r["image_top_file"] != "N/A":
        print(f"Row {idx+2:4d}: {r['Modele']:20s} | {r['Generation']:8s} | {r['Annees_Production']:11s} | L={r['length_in']} W={r['width_in']} R={r['corner_radius_in']} | Photo={r['image_top_file']}")

print("\n=== 2. BULLFROG SPAS ROWS WITH PHOTOS ===")
for idx, r in enumerate(rows):
    if r["Marque"] == "Bullfrog Spas" and r.get("image_top_file") and r["image_top_file"] != "N/A":
        print(f"Row {idx+2:4d}: {r['Modele']:20s} | {r['Generation']:8s} | {r['Annees_Production']:11s} | L={r['length_in']} W={r['width_in']} R={r['corner_radius_in']} | Photo={r['image_top_file']}")

print("\n=== 3. ALL REMAINING ROWS WITH SPAN >= 15 YEARS HOLDING PHOTO OR CAD ===")
for idx, r in enumerate(rows):
    has_photo = r.get("image_top_file") and r["image_top_file"] != "N/A"
    has_cad = r.get("cad_dwg_file") and r["cad_dwg_file"] != "N/A"
    if not (has_photo or has_cad):
        continue
    prod = r.get("Annees_Production", "")
    if "-" in prod:
        parts = prod.split("-")
        try:
            start_yr, end_yr = int(parts[0]), int(parts[1])
            span = end_yr - start_yr
            if span >= 15:
                asset_type = "PHOTO+CAD" if (has_photo and has_cad) else ("PHOTO" if has_photo else "CAD")
                print(f"Row {idx+2:4d}: {r['Marque']:18s} | {r['Modele']:18s} | {r['Generation']:8s} | {prod:11s} (span={span:2d}y) | {asset_type:9s} | Photo={Path(r.get('image_top_file','')).name:22s} | DWG={Path(r.get('cad_dwg_file','')).name}")
        except ValueError:
            pass
