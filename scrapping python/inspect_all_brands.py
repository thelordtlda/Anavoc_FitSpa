import csv
import json

input_path = r'C:/Users/nicol/.gemini/antigravity/brain/3fbc6496-e8c6-412d-9f36-bd5b7300d8bf/.user_uploaded/media_1793766220845_80851390.md'

with open(input_path, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

with open('scrapping python/dataset/spa_master_index.json', 'r', encoding='utf-8') as f:
    master_index = json.load(f)

# Group rows by brand
by_brand = {}
for r in rows:
    b = r['Marque']
    by_brand.setdefault(b, []).append(r)

print(f"Total brands: {len(by_brand)}")
for b, r_list in by_brand.items():
    print(f"\n=== BRAND: {b} ({len(r_list)} models) ===")
    for r in r_list:
        print(f"  {r['Modele']} | {r['Sous_Modele_ou_Version']} | {r['Generation']} | {r['Annees_Production']}")
