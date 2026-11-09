import json
from pathlib import Path

path = Path("data/spacovers_all_templates.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== ARTESIAN TARGET TEMPLATES ===")
art = data.get("Artesian", {})
for k, val_list in sorted(art.items()):
    if any(m in k for m in ["antigua", "barbados", "captiva", "dove", "bimini", "margarita", "nevis", "santa"]):
        print(f"Key: {k}")
        for item in val_list:
            if "Radius" in item or "″" in item:
                print(f"  {item}")

print("\n=== BULLFROG TARGET TEMPLATES ===")
bf = data.get("Bullfrog", {})
for k, val_list in sorted(bf.items()):
    if any(m in k for m in ["a5", "a6", "a7", "a8", "r6", "r7", "r8"]):
        print(f"Key: {k}")
        for item in val_list:
            if "Radius" in item or "″" in item:
                print(f"  {item}")
