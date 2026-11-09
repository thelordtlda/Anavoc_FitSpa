import json
from pathlib import Path

base = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/jacuzzi")
years = sorted([d.name for d in base.iterdir() if d.is_dir() and d.name.isdigit()])
print(f"Years present for Jacuzzi: {years}")

sample_paths = [
    base / "2026" / "j509" / "metadata.json",
    base / "2026" / "j408" / "metadata.json",
    base / "2024" / "j495" / "metadata.json",
    base / "2024" / "jlx" / "metadata.json",
    base / "2020" / "j385" / "metadata.json",
    base / "2015" / "j210" / "metadata.json",
    base / "2015" / "j585" / "metadata.json",
    base / "2012" / "j480" / "metadata.json"
]

for p in sample_paths:
    if p.exists():
        with open(p, "r", encoding="utf-8") as f:
            data = json.load(f)
        dims = data["dimensions"]
        obs = data["obstacles"]
        med = data["media"]
        print(f"\n[{data['vintage_year']} {data['brand']} {data['model']}] ({data['series']})")
        print(f"  Dimensions: {dims['length_in']} x {dims['width_in']} x {dims['height_in']} po (Type: {dims['corner_type']}, Rad: {dims['corner_radius_in']} po)")
        print(f"  Obstacles: Raised Back: {obs['raised_back']} | Waterfall: {obs['waterfall_curved']} | Keypad: {obs['keypad_protruding']}")
        print(f"  Media: Top: {med['has_top_view']} | Side: {med['has_side_view']} | Footprint: {med['has_footprint']} (Score: {med['completeness_score_pct']} %)")
        print(f"  Files: {list((p.parent).glob('*.*'))}")
        print(f"  SpaFit Notes: {data['spafit_notes']}")
