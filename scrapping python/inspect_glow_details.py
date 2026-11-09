import json
from pathlib import Path

base_dir = Path(__file__).resolve().parent
hs_dir = base_dir / 'dataset' / 'hot_spring_spas'

for g in hs_dir.glob('*/hot_spring_glow_*'):
    meta_p = g / 'metadata.json'
    files = [f.name for f in g.iterdir() if f.is_file()]
    if meta_p.exists():
        with open(meta_p, 'r', encoding='utf-8') as f:
            m = json.load(f)
        dims = m.get('dimensions', {})
        print(f"{g.name}: {dims.get('length_in')}x{dims.get('width_in')}x{dims.get('height_in')} (R={dims.get('corner_radius_in')}) | files: {files} | photo={m.get('has_real_photo')} | cad={m.get('has_cad')}")
