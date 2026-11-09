from pathlib import Path
import json

base_dir = Path(__file__).resolve().parent
dataset_dir = base_dir / "dataset"

# 1. Update all Glow models in dataset/hot_spring_spas
glow_dirs = list(dataset_dir.glob("hot_spring_spas/*/hot_spring_glow_*"))
print(f"Updating {len(glow_dirs)} Glow folders...")
for g in glow_dirs:
    meta_p = g / "metadata.json"
    if meta_p.exists():
        with open(meta_p, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["dimensions"]["length_in"] = 84.0
        data["dimensions"]["width_in"] = 76.0
        data["dimensions"]["height_in"] = 33.0
        data["dimensions"]["length_mm"] = 2134
        data["dimensions"]["width_mm"] = 1930
        data["dimensions"]["height_mm"] = 838
        data["dimensions"]["corner_radius_in"] = 8.0
        data["dimensions"]["corner_radius_mm"] = 203
        
        with open(meta_p, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Updated {g.name} metadata: 84.0 x 76.0 x 33.0 in (2134 x 1930 x 838 mm)")

# 2. Update builders_watkins.py if present
bw_path = base_dir / "builders_watkins.py"
if bw_path.exists():
    text = bw_path.read_text(encoding="utf-8")
    if '{"model": "Glow", "dims": (76.0, 76.0, 33.0)' in text:
        text = text.replace('{"model": "Glow", "dims": (76.0, 76.0, 33.0)', '{"model": "Glow", "dims": (84.0, 76.0, 33.0)')
        bw_path.write_text(text, encoding="utf-8")
        print("Updated builders_watkins.py Glow definition to (84.0, 76.0, 33.0)")

print("Done updating Glow dimensions!")
