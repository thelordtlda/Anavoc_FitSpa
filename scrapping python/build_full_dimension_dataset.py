import csv
import json
import re

input_path = r'C:/Users/nicol/.gemini/antigravity/brain/3fbc6496-e8c6-412d-9f36-bd5b7300d8bf/.user_uploaded/media_1793766220845_80851390.md'

with open(input_path, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

with open('scrapping python/dataset/spa_master_index.json', 'r', encoding='utf-8') as f:
    master_index = json.load(f)

print(f"Total rows in user file: {len(rows)}")

# Let's see how each model matches and prepare a master dictionary of exact dimensions
