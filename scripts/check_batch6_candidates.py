import csv

with open("data/spas_master_database.csv", "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

target_brands = [
    "Coast Spas", "Marquis Spas", "Hydropool", "Beachcomber",
    "Arctic Spas", "Cal Spas", "Caldera Spas"
]

missing_by_brand = {}
for b in target_brands:
    missing = [r for r in rows if r["Marque"] == b and (not r.get("image_top_file") or r["image_top_file"] == "N/A")]
    total = [r for r in rows if r["Marque"] == b]
    missing_by_brand[b] = (len(missing), len(total))

print("=== CANDIDATE SPAS MISSING OVERHEAD PHOTOS ===")
for b, (miss, tot) in missing_by_brand.items():
    print(f"  {b:20s}: {miss:2d} missing / {tot:2d} total spas")
