from pathlib import Path

base_dir = Path(__file__).resolve().parent
root = base_dir / 'dataset'

for d in root.iterdir():
    if 'hot' in d.name.lower() or 'spring' in d.name.lower() or 'watkins' in d.name.lower():
        print(d.name)
