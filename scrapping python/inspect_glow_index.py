import json
from pathlib import Path

base_dir = Path(__file__).resolve().parent
index_p = base_dir / "dataset" / "spa_master_index.json"
with open(index_p, "r", encoding="utf-8") as f:
    records = json.load(f)

glow_records = [r for r in records if "hot spring" in r.get("brand", "").lower() and "glow" in r.get("model", "").lower()]
print(f"Glow records in index: {len(glow_records)}")
for r in glow_records:
    print(r.get("vintage_year"), r.get("model"), r.get("length_in"), r.get("width_in"), r.get("height_in"), r.get("provenance", {}).get("has_real_photo"), r.get("provenance", {}).get("has_official_cad_dwg"))
