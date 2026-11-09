import json
from pathlib import Path

base_dir = Path(__file__).resolve().parent
index_p = base_dir / "dataset" / "spa_master_index.json"
with open(index_p, "r", encoding="utf-8") as f:
    records = json.load(f)

hs_records = [r for r in records if "hot spring" in r.get("brand", "").lower()]
print("Keys in hs_record:", list(hs_records[0].keys()))
print("Sample record:", hs_records[0])
