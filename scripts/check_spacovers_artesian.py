import json
from pathlib import Path

path = Path("data/spacovers_all_templates.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total spacovers templates: {len(data)}")

artesian = [d for d in data if "artesian" in d.get("brand","").lower()]
print(f"Total Artesian templates: {len(artesian)}")

for item in artesian:
    model = item.get("model", "")
    years = item.get("years", "") or item.get("year", "")
    dims = f"{item.get('length')}x{item.get('width')}"
    r = item.get("corner_radius", "") or item.get("radius", "")
    print(f"  {model:30s} | {str(years):15s} | {dims:12s} | R={r}")
