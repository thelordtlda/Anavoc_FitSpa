import json
from pathlib import Path

path = Path("data/spacovers_all_templates.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== ARTESIAN TEMPLATES ===")
art = data.get("Artesian", {})
for k, v in sorted(art.items()):
    title = v.get("title", k)
    dims = v.get("dimensions", {})
    years = v.get("years") or v.get("year", "")
    print(f"  {k:45s} | {str(years):12s} | {dims}")

print("\n=== BULLFROG TEMPLATES ===")
bf = data.get("Bullfrog", {})
for k, v in sorted(bf.items()):
    if any(m in k for m in ["a5", "a6", "a7", "a8", "r5", "r6", "r7", "r8"]):
        title = v.get("title", k)
        dims = v.get("dimensions", {})
        years = v.get("years") or v.get("year", "")
        print(f"  {k:45s} | {str(years):12s} | {dims}")
