import json
from pathlib import Path

path = Path("data/spacovers_all_templates.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

art = data.get("Artesian", {})
for k in list(art.keys())[:5]:
    print(f"Key: {k}")
    print(f"Val: {art[k]}")
