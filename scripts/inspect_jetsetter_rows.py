import csv

with open('data/spas_master_database.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

for idx in range(485, 494):
    r = rows[idx]
    print(f"Row {idx+2}: {r['Marque']} | {r['Modele']} | {r['Generation']} | {r['Annees_Production']} | DWG={r.get('cad_dwg_file')}")
