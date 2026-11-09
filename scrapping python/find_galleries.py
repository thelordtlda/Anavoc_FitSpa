from pathlib import Path

base_dir = Path(__file__).resolve().parent
for f in base_dir.rglob("*gallery*.html"):
    print(f"Found gallery: {f.relative_to(base_dir)}")
