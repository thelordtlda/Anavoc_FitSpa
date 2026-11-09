from pathlib import Path

base_dir = Path(__file__).resolve().parent
for p in base_dir.rglob("*master_index*"):
    print(p.relative_to(base_dir))
