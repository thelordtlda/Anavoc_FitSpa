import csv
import json
import re

input_path = r'C:/Users/nicol/.gemini/antigravity/brain/3fbc6496-e8c6-412d-9f36-bd5b7300d8bf/.user_uploaded/media_1793766220845_80851390.md'

with open(input_path, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

print(f"Total rows to process: {len(rows)}")

# Load master index
with open('scrapping python/dataset/spa_master_index.json', 'r', encoding='utf-8') as f:
    master_index = json.load(f)

# Helper for normalization
def norm(s):
    return re.sub(r'[^a-zA-Z0-9]', '', str(s).lower())

# Check how many rows match master_index with year / generation awareness
entries_by_brand = {}
for e in master_index:
    entries_by_brand.setdefault(e['brand_slug'].lower(), []).append(e)

# Let's inspect all 475 rows and see their resolution
