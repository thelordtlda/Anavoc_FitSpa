import json
from pathlib import Path
from collections import Counter

base_dir = Path(__file__).resolve().parent
index_p = base_dir / "dataset" / "spa_master_index.json"

if index_p.exists():
    with open(index_p, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Total spas in spa_master_index.json: {len(data)}")
    brands = Counter(x.get("brand", "Unknown") for x in data)
    print(f"Top 20 brands in master index:")
    for b, count in brands.most_common(20):
        print(f"  {b:30}: {count} records")
else:
    print("dataset/spa_master_index.json not found")
