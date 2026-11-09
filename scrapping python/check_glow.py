import json
from pathlib import Path

glow_dirs = sorted(list(Path('dataset/hot_spring_spas').glob('*/glow')))
print(f'Found {len(glow_dirs)} glow folders:')
for d in glow_dirs:
    meta_p = d / 'metadata.json'
    if meta_p.exists():
        with open(meta_p, 'r', encoding='utf-8') as f:
            m = json.load(f)
        dims = m.get('dimensions', {})
        print(f"{d.parent.name}/glow: {dims.get('length_in')} x {dims.get('width_in')} x {dims.get('height_in')} (R={dims.get('corner_radius_in')}), photo={m.get('has_real_photo')}, cad={m.get('has_cad')}")
