import json
from pathlib import Path

base_dir = Path(__file__).resolve().parent
root = base_dir / 'dataset'
dirs = [d.name for d in root.iterdir() if d.is_dir()]
print(f"Top dirs in dataset ({len(dirs)}): {dirs[:20]}")

# search for glow anywhere in dataset
glow_found = list(root.glob('**/glow*'))
print(f"Any glow found ({len(glow_found)}):")
for g in glow_found:
    print(" -", g.relative_to(root))
