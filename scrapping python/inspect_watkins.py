import csv
import json
import re

input_path = r'C:/Users/nicol/.gemini/antigravity/brain/3fbc6496-e8c6-412d-9f36-bd5b7300d8bf/.user_uploaded/media_1793766220845_80851390.md'

with open(input_path, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

print(f"Total rows in user list: {len(rows)}")

with open('scrapping python/dataset/spa_master_index.json', 'r', encoding='utf-8') as f:
    master_index = json.load(f)

print(f"Total entries in master index: {len(master_index)}")

# Print all Watkins models
watkins_brands = ['Hot Spring Spas', 'Caldera Spas', 'Endless Pools', 'Freeflow Spas', 'Lifesmart Spas', 'Tiger River Spas', 'Solana Spas']
watkins_rows = [r for r in rows if r['Marque'] in watkins_brands]
print(f"\n--- Watkins rows: {len(watkins_rows)} ---")
for r in watkins_rows:
    print(f"{r['Marque']} | {r['Modele']} | {r['Sous_Modele_ou_Version']} | {r['Generation']} | {r['Annees_Production']}")
