import os
import hashlib
import json
from pathlib import Path

DATASET = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset")

def file_hash(path):
    if not path.exists():
        return None
    h = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

print("=== AUDIT COMPLET DU DATASET ===")

# 1. Structure audit: root directories
subdirs = [d for d in DATASET.iterdir() if d.is_dir()]
print(f"Total subdirectories in dataset root: {len(subdirs)}")

# Check for non-standard folder names (aliases, trailing spaces, underscore suffix)
alias_folders = []
for d in subdirs:
    name = d.name
    if name.endswith("_") or name in ["bullfrog", "sundance", "saundance", "trevi", "trévi", "trevi_", "hydropool_", "hotspring", "caldera", "coast_spa", "marquis", "marquise"]:
        alias_folders.append(name)
print(f"Detected alias/duplicate brand folders in root: {len(alias_folders)}")
print("  ->", alias_folders)

# 2. Check for misplaced model folders or non-year folders inside brand directories
misplaced = {}
for d in subdirs:
    non_year = []
    for item in d.iterdir():
        if item.is_dir():
            if not (item.name.isdigit() and len(item.name) == 4):
                non_year.append(item.name)
        elif item.is_file():
            non_year.append(item.name)
    if non_year:
        misplaced[d.name] = non_year

print(f"Brands containing non-year folders or files directly inside: {len(misplaced)}")
for b, items in misplaced.items():
    print(f"  {b}: {items[:10]}")

# 3. Media audit: top_view == side_view
identical_views = []
missing_views = []
total_models = 0

for root, dirs, files in os.walk(DATASET):
    # Only check terminal model folders that contain metadata.json
    if "metadata.json" in files:
        total_models += 1
        r_path = Path(root)
        
        # Check top_view vs side_view
        top_files = list(r_path.glob("top_view.*"))
        side_files = list(r_path.glob("side_view.*"))
        
        if not top_files:
            missing_views.append((str(r_path.relative_to(DATASET)), "missing top_view"))
        if not side_files:
            missing_views.append((str(r_path.relative_to(DATASET)), "missing side_view"))
            
        if top_files and side_files:
            h_top = file_hash(top_files[0])
            h_side = file_hash(side_files[0])
            if h_top == h_side:
                identical_views.append((str(r_path.relative_to(DATASET)), top_files[0].name, side_files[0].name))

print(f"\nTotal model folders audited: {total_models}")
print(f"Models where top_view and side_view are EXACT IDENTICAL FILES: {len(identical_views)}")
if identical_views:
    print("  Exemples d'identiques (premiers 15) :")
    for iv in identical_views[:15]:
        print(f"    {iv[0]}: {iv[1]} == {iv[2]}")

# 4. Footprint audit: Check footprints that are extracted PDF pages vs generated schematics
extracted_pdf_footprints = []
for root, dirs, files in os.walk(DATASET):
    if "footprint.png" in files:
        fp = Path(root) / "footprint.png"
        sz = fp.stat().st_size
        # Generated asset_generator footprints are typically around 180KB - 350KB
        # PDF page rips are often larger or contain specific OCR text
        # Let's inspect which brands have ripped PDF footprints
        rel = str(Path(root).relative_to(DATASET))
        brand = rel.split(os.sep)[0]
        extracted_pdf_footprints.append((brand, sz))

from collections import Counter
print(f"\nFootprints stats by brand:")
brand_fp_counts = Counter(b for b, sz in extracted_pdf_footprints)
for b, count in brand_fp_counts.most_common(20):
    print(f"  {b}: {count} footprints")
