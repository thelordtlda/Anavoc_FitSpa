import json
from pathlib import Path
from collections import defaultdict

# 1. Master index
index_path = Path("_ARCHIVE/scrapping_legacy/dataset_raw_watkins_harvest/spa_master_index.json")
with open(index_path, "r", encoding="utf-8") as f:
    master_index = json.load(f)

targets = ["antigua", "barbados", "captiva", "dove canyon", "bimini island", "margarita", "nevis", "santa cruz"]
print("=== ARTESIAN SPAS IN MASTER INDEX ===")
for t in targets:
    entries = [e for e in master_index if "artesian" in e.get("brand","").lower() and t in e.get("model","").lower()]
    by_gen = defaultdict(list)
    for e in entries:
        yr = e.get("year")
        dims = f"{e.get('length_in')}x{e.get('width_in')}x{e.get('height_in')}"
        r = e.get("corner_radius_in")
        by_gen[(dims, r)].append(yr)
    print(f"\nModel: {t.title()} ({len(entries)} entries):")
    for (dims, r), yrs in sorted(by_gen.items()):
        print(f"  {dims} | R={r} | Years: {min(yrs)}-{max(yrs)} ({len(yrs)} yrs)")
