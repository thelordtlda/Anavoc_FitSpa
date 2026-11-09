import os
import sys
import hashlib
from pathlib import Path

DATASET = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset")

print("--- AUDIT RAPIDE DU DATASET ---", flush=True)

# 1. Dossiers à la racine
root_dirs = sorted([d.name for d in DATASET.iterdir() if d.is_dir()])
print(f"Total dossiers à la racine: {len(root_dirs)}", flush=True)

# 2. Identifier les doublons / alias évidents
duplicates = {
    "bullfrog": ["bullfrog", "bullfrog_", "bullfrog_spas"],
    "sundance": ["sundance", "sundance_", "saundance", "sundance_spas"],
    "trevi": ["trevi", "trévi", "trevi_", "trevi_spas"],
    "hotspring": ["hotspring", "hot_spring_spas"],
    "caldera": ["caldera", "caldera_spas"],
    "coast": ["coast_spa", "coast_spas"],
    "marquis": ["marquis", "marquise", "marquis_spas"],
    "hydropool": ["hydropool", "hydropool_"],
    "artesian_sub_brands": ["artesian_elite", "artesian_garden_spas", "artesian_island_spa", "artesian_island_spa_elite", "artesian_south_seas", "artesian_spas"]
}

for group_name, members in duplicates.items():
    present = [m for m in members if m in root_dirs]
    print(f"Groupe {group_name}: {present}", flush=True)

# 3. Dossiers anormaux dans bullfrog_spas
bf_dir = DATASET / "bullfrog_spas"
if bf_dir.exists():
    non_year_bf = [x.name for x in bf_dir.iterdir() if not (x.name.isdigit() and len(x.name) == 4)]
    print(f"\nÉléments non-années dans bullfrog_spas ({len(non_year_bf)}) : {non_year_bf[:15]}", flush=True)

# 4. Vérifier american_whirlpool et autres marques pour side_view == top_view
print("\n--- ANALYSE MEDIA: SIDE_VIEW == TOP_VIEW ---", flush=True)

brands_with_identical_views = {}
sample_identical = []

for brand_dir in DATASET.iterdir():
    if not brand_dir.is_dir():
        continue
    identical_count = 0
    total_brand_models = 0
    for root, dirs, files in os.walk(brand_dir):
        if "metadata.json" in files:
            total_brand_models += 1
            top_files = [f for f in files if f.startswith("top_view.")]
            side_files = [f for f in files if f.startswith("side_view.")]
            if top_files and side_files:
                top_p = Path(root) / top_files[0]
                side_p = Path(root) / side_files[0]
                # Compare sizes first
                if top_p.stat().st_size == side_p.stat().st_size:
                    # Check first 1024 bytes
                    with open(top_p, "rb") as f1, open(side_p, "rb") as f2:
                        if f1.read(1024) == f2.read(1024):
                            identical_count += 1
                            if len(sample_identical) < 10:
                                sample_identical.append(str(Path(root).relative_to(DATASET)))
    if identical_count > 0:
        brands_with_identical_views[brand_dir.name] = (identical_count, total_brand_models)

print(f"Marques ayant des vues top/side identiques : {len(brands_with_identical_views)}", flush=True)
for b, (c, tot) in sorted(brands_with_identical_views.items(), key=lambda x: -x[1][0]):
    print(f"  {b}: {c}/{tot} modèles avec top_view == side_view", flush=True)

print("Exemples de dossiers concernés :", sample_identical, flush=True)

# 5. Vérifier les footprints
print("\n--- ANALYSE FOOTPRINTS : FICHIERS SUSPECTS ---", flush=True)
# Footprint files that came from PDF extracts in early tier 1
pdf_extracted_dirs = ["american_whirlpool", "maax_spas", "jacuzzi", "sundance_spas", "bullfrog_spas"]
for b in pdf_extracted_dirs:
    bp = DATASET / b
    if bp.exists():
        # Check a sample model
        sample_fps = list(bp.glob("2018/*/footprint.png"))[:3]
        for s in sample_fps:
            print(f"  {b} sample 2018 footprint: {s.relative_to(DATASET)}, size: {s.stat().st_size} octets", flush=True)
