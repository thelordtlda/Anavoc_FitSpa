import json
from pathlib import Path

path = Path("data/spacovers_all_templates.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Top-level keys in spacovers_all_templates.json: {list(data.keys())[:15]}")
for k, v in list(data.items())[:5]:
    print(f"Key: {k} -> Type: {type(v)}")
    if isinstance(v, list) and len(v) > 0:
        print(f"  First elem: {v[0]}")
    elif isinstance(v, dict):
        print(f"  Keys: {list(v.keys())[:5]}")
