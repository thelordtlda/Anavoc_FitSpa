import csv
from pathlib import Path

csv_path = Path("data/spas_master_database.csv")
with open(csv_path, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

models = ["aptos", "vigor", "accolade", "landmark", "highlife", "tempo", "cascina", "azure", "mini", "excursion", "monterey", "tristar"]
for idx, r in enumerate(rows):
    m = r.get("Modele", "").lower()
    b = r.get("Marque", "").lower()
    if any(mod in m for mod in models):
        print(f"Row {idx+2:4d}: {r['Marque']:20s} | {r['Modele']:15s} | {r['Generation']:8s} | {r['Annees_Production']:11s} | DWG={r.get('cad_dwg_file')}")
