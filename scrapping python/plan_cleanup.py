import os
import shutil
import json
from pathlib import Path

DATASET = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset")

print("=== PLAN DE NETTOYAGE COMPLET ===")

# 1. Vérifier les dossiers bullfrog à la racine de bullfrog_spas
bf_dir = DATASET / "bullfrog_spas"
bf_junk = []
if bf_dir.exists():
    for item in bf_dir.iterdir():
        if not (item.name.isdigit() and len(item.name) == 4):
            bf_junk.append(item.name)
print(f"1. Éléments parasites dans bullfrog_spas ({len(bf_junk)}) : {bf_junk[:10]}")

# 2. Vérifier les dossiers de marques en double / alias à la racine de dataset
aliases_to_remove = [
    "bullfrog", "bullfrog_",
    "sundance", "sundance_", "saundance",
    "trevi", "trevi_", "trévi",
    "hotspring",
    "caldera",
    "coast_spa",
    "marquis", "marquise",
    "hydropool_",
    "artesian_elite", "artesian_garden_spas", "artesian_island_spa", "artesian_island_spa_elite", "artesian_south_seas",
    "cantabria",
    "crown", "vector", "celebrity_elite", "celebrity_standard", "premium",
    "beach_collection", "palmbeach_collection", "daytona_beach_collection"
]

existing_aliases = [a for a in aliases_to_remove if (DATASET / a).exists()]
print(f"2. Dossiers de marques en double/alias à supprimer ({len(existing_aliases)}) : {existing_aliases}")

# 3. Vérifier les vues side_view identiques aux top_view
identical_views = []
for root, dirs, files in os.walk(DATASET):
    if "metadata.json" in files:
        top_files = [f for f in files if f.startswith("top_view.")]
        side_files = [f for f in files if f.startswith("side_view.")]
        if top_files and side_files:
            t = Path(root) / top_files[0]
            s = Path(root) / side_files[0]
            if t.stat().st_size == s.stat().st_size:
                identical_views.append(Path(root))

print(f"3. Modèles avec side_view identique à top_view : {len(identical_views)}")

# 4. Vérifier les footprints suspects (comme le fichier de 468 865 octets d'AWP/MAAX)
electrical_fps = []
for root, dirs, files in os.walk(DATASET):
    if "footprint.png" in files:
        fp = Path(root) / "footprint.png"
        if fp.stat().st_size == 468865:
            electrical_fps.append(fp)

print(f"4. Footprints identifiés comme fiches électriques (468 865 octets) : {len(electrical_fps)}")
