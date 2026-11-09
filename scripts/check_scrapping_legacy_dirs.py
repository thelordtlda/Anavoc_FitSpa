from pathlib import Path

p = Path("_ARCHIVE/scrapping_legacy")
print("Subdirectories in _ARCHIVE/scrapping_legacy:")
for sub in p.iterdir():
    if sub.is_dir():
        count = sum(1 for _ in sub.rglob("*") if _.is_file())
        print(f"  {sub.name}: {count} files")
