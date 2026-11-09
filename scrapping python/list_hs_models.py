from pathlib import Path
import json
from collections import defaultdict

base_dir = Path(__file__).resolve().parent
hs_dir = base_dir / "dataset" / "hot_spring_spas"

models_by_name = defaultdict(list)
for m_dir in hs_dir.glob("*/*"):
    if m_dir.is_dir():
        parts = m_dir.name.split("_")
        # format: hot_spring_<model>_<year>
        meta_p = m_dir / "metadata.json"
        if meta_p.exists():
            with open(meta_p, "r", encoding="utf-8") as f:
                meta = json.load(f)
            model_name = meta.get("model", m_dir.name)
            year = meta.get("year", m_dir.parent.name)
            models_by_name[model_name].append((year, m_dir))

print(f"Total unique models in HotSpring: {len(models_by_name)}")
for m in sorted(models_by_name.keys()):
    years = sorted([y for y, _ in models_by_name[m]])
    print(f"  {m:20}: {len(years)} years ({years[0]} - {years[-1]})")
