import csv

with open('data/spas_master_database.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

for idx, r in enumerate(rows):
    if r['Marque'] in ['Freeflow Spas', 'Fantasy Spas', 'Hot Spring Spas', 'Caldera Spas']:
        dwg = r.get('cad_dwg_file', '')
        dwg_str = f"DWG: {dwg}" if dwg and dwg != 'N/A' else "NO DWG"
        print(f"Row {idx+2:4d}: {r['Marque']:16s} | {r['Modele']:15s} | {r['Generation']:8s} | {r['Annees_Production']:11s} | {dwg_str}")
