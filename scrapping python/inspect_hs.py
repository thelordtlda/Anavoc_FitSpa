from pathlib import Path

base_dir = Path(__file__).resolve().parent
hs_dir = base_dir / 'dataset' / 'hot_spring_spas'

print(f"hot_spring_spas exists: {hs_dir.exists()}")
years = [d.name for d in hs_dir.iterdir() if d.is_dir()]
print(f"Years in hot_spring_spas ({len(years)}): {sorted(years)}")

models_found = list(hs_dir.glob('*/*'))
print(f"Total model dirs in hot_spring_spas: {len(models_found)}")
for m in models_found[:20]:
    print(" -", m.relative_to(hs_dir))

glows = list(hs_dir.glob('*/*glow*'))
print(f"Glow dirs: {glows}")
