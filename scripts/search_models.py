import csv

with open('data/spas_master_database.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

for idx, r in enumerate(rows):
    m = r['Modele'].lower()
    if any(k in m for k in ['aptos', 'vigor', 'accolade', 'landmark']):
        print(f"Row {idx+2}: {r['Marque']} | {r['Modele']} | {r['Generation']} | {r['Annees_Production']}")
