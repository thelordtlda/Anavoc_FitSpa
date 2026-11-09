from pathlib import Path
from collections import Counter

archive = Path("_ARCHIVE")
print("=== _ARCHIVE Top-level inspection ===")
for item in archive.iterdir():
    if item.is_dir():
        count = sum(1 for _ in item.rglob("*") if _.is_file())
        dwg_count = sum(1 for _ in item.rglob("*.dwg") if _.is_file())
        dxf_count = sum(1 for _ in item.rglob("*.dxf") if _.is_file())
        pdf_count = sum(1 for _ in item.rglob("*.pdf") if _.is_file())
        print(f"  {item.name}: {count} files (DWG={dwg_count}, DXF={dxf_count}, PDF={pdf_count})")
    else:
        print(f"  {item.name} (file)")

watkins_p = Path("_ARCHIVE/scrapping_legacy/dataset_raw_watkins_harvest")
if watkins_p.exists():
    exts = Counter(f.suffix.lower() for f in watkins_p.rglob("*") if f.is_file())
    print("\nWatkins harvest folder extensions:", exts)
