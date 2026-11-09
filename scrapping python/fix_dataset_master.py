"""
fix_dataset_master.py
=====================
Script de nettoyage structurel et de correction des médias du dataset SpaFit :
1. Nettoie la racine de bullfrog_spas (supprime les 25 dossiers hors-années parasites).
2. Supprime les dossiers de marques en double / alias à la racine de dataset (bullfrog, bullfrog_, suandance, etc.).
3. Corrige tous les side_view qui sont en fait des top_view (489 modèles AWP/MAAX) en générant une vraie élévation latérale de meuble.
4. Remplace tous les faux footprints (fiches électriques 468 865 octets) par des plans 2D cotés haute précision 300 DPI.
5. Re-synchronise spa_master_index.json et spa_master_index.csv avec les métadonnées propres.
"""

import os
import sys
import json
import csv
import shutil
import logging
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from asset_generator import generate_technical_footprint, generate_cabinet_side_view

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("fix_dataset")

DATASET_DIR = SCRIPT_DIR / "dataset"

def step1_clean_parasitic_folders():
    logger.info("=== ÉTAPE 1 : NETTOYAGE DES DOSSIERS PARASITES ET DOUBLONS ===")
    
    # 1.1 Nettoyer la racine de bullfrog_spas
    bf_dir = DATASET_DIR / "bullfrog_spas"
    if bf_dir.exists():
        bf_cleaned = 0
        for item in bf_dir.iterdir():
            if item.is_dir() and not (item.name.isdigit() and len(item.name) == 4):
                shutil.rmtree(item)
                bf_cleaned += 1
            elif item.is_file():
                item.unlink()
                bf_cleaned += 1
        logger.info(f"bullfrog_spas : {bf_cleaned} éléments parasites supprimés de la racine.")

    # 1.2 Nettoyer extracted_footprints et cad_files dans les autres marques
    for b in ["american_whirlpool", "maax_spas", "jacuzzi", "sundance_spas"]:
        bp = DATASET_DIR / b
        if bp.exists():
            for junk in ["extracted_footprints", "cad_files"]:
                jp = bp / junk
                if jp.exists() and jp.is_dir():
                    shutil.rmtree(jp)
                    logger.info(f"Supprimé {b}/{junk}")

    # 1.3 Supprimer les dossiers de marques alias/doublons créés par la saisie utilisateur
    aliases_to_remove = [
        "bullfrog", "bullfrog_",
        "sundance", "sundance_", "saundance",
        "trevi", "trevi_", "trévi",
        "hotspring",
        "caldera",
        "coast_spa",
        "marquis", "marquise",
        "hydropool_",
        "artesian_elite", "artesian_garden_spas", "artesian_island_spa", "artesian_island_spa_elite", "artesian_south_seas", "tidalfit",
        "cantabria",
        "crown", "vector", "celebrity_elite", "celebrity_standard", "premium",
        "beach_collection", "palmbeach_collection", "daytona_beach_collection"
    ]

    removed_aliases = 0
    for a in aliases_to_remove:
        ap = DATASET_DIR / a
        if ap.exists() and ap.is_dir():
            shutil.rmtree(ap)
            removed_aliases += 1
    logger.info(f"Dossiers de marques en double / alias supprimés : {removed_aliases}")

    # Renommer les dossiers avec caractères non conventionnels
    old_dr = DATASET_DIR / "dr._wellness"
    new_dr = DATASET_DIR / "dr_wellness"
    if old_dr.exists() and not new_dr.exists():
        old_dr.rename(new_dr)
        logger.info("Renommé dr._wellness -> dr_wellness")

    old_wd = DATASET_DIR / "water_day___spa"
    new_wd = DATASET_DIR / "water_day_spa"
    if old_wd.exists() and not new_wd.exists():
        old_wd.rename(new_wd)
        logger.info("Renommé water_day___spa -> water_day_spa")


def step2_fix_side_views_and_footprints():
    logger.info("=== ÉTAPE 2 : CORRECTION DES VUES LATÉRALES ET FOOTPRINTS ÉLECTRIQUES ===")
    
    fixed_side_views = 0
    fixed_footprints = 0
    total_models = 0

    for root, dirs, files in os.walk(DATASET_DIR):
        if "metadata.json" not in files:
            continue

        total_models += 1
        model_dir = Path(root)
        meta_file = model_dir / "metadata.json"

        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception as e:
            logger.error(f"Erreur lecture {meta_file}: {e}")
            continue

        brand = meta.get("brand", "")
        model = meta.get("model", "")
        series = meta.get("series", "")
        dims = meta.get("dimensions", {})
        l = dims.get("length_in", 84.0)
        w = dims.get("width_in", 84.0)
        h = dims.get("height_in", 36.0)
        r = dims.get("corner_radius_in", 8.5)
        is_swim = "swim" in series.lower() or "swim" in model.lower() or "swim" in meta.get("spafit_notes", "").lower()

        # --- A. VÉRIFICATION ET CORRECTION DE SIDE_VIEW ---
        top_candidates = [model_dir / f for f in files if f.startswith("top_view.")]
        side_candidates = [model_dir / f for f in files if f.startswith("side_view.")]

        needs_side_regeneration = False
        if not side_candidates:
            needs_side_regeneration = True
        elif top_candidates and side_candidates:
            top_p = top_candidates[0]
            side_p = side_candidates[0]
            # Si même taille exacte ou nom similaire
            if top_p.stat().st_size == side_p.stat().st_size:
                needs_side_regeneration = True
                # Supprimer le faux side_view
                side_p.unlink()

        if needs_side_regeneration:
            new_side = model_dir / "side_view.png"
            generate_cabinet_side_view(brand, model, series, l, h, new_side)
            meta["media"]["has_side_view"] = True
            meta["media"]["side_view_file"] = "side_view.png"
            fixed_side_views += 1

        # --- B. VÉRIFICATION ET CORRECTION DU FOOTPRINT ---
        fp_file = model_dir / "footprint.png"
        needs_fp_regeneration = False

        if not fp_file.exists():
            needs_fp_regeneration = True
        else:
            sz = fp_file.stat().st_size
            # 468 865 octets = fiche électrique American Whirlpool / MAAX
            # Ou fichiers trop petits / corrompus
            if sz == 468865 or sz < 2000:
                needs_fp_regeneration = True

        if needs_fp_regeneration:
            generate_technical_footprint(brand, model, series, l, w, h, r, is_swim, fp_file)
            meta["media"]["has_footprint"] = True
            meta["media"]["footprint_file"] = "footprint.png"
            fixed_footprints += 1

        # Sauvegarder métadonnées mises à jour
        with open(meta_file, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

    logger.info(f"Total modèles audités : {total_models}")
    logger.info(f"Vues latérales (side_view) régénérées avec succès : {fixed_side_views}")
    logger.info(f"Plans techniques (footprint) régénérés avec succès : {fixed_footprints}")


def step3_rebuild_master_indexes():
    logger.info("=== ÉTAPE 3 : RECONSTRUCTION DU MASTER INDEX CONSOLIDÉ ===")
    
    all_records = []
    
    for root, dirs, files in os.walk(DATASET_DIR):
        if "metadata.json" in files:
            meta_path = Path(root) / "metadata.json"
            try:
                with open(meta_path, "r", encoding="utf-8") as f:
                    rec = json.load(f)
                all_records.append(rec)
            except Exception as e:
                logger.error(f"Erreur chargement {meta_path}: {e}")

    logger.info(f"Total fiches propres consolidées : {len(all_records)}")

    # Sauvegarder JSON
    json_path = DATASET_DIR / "spa_master_index.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2, ensure_ascii=False)

    # Sauvegarder CSV
    csv_path = DATASET_DIR / "spa_master_index.csv"
    headers = [
        "brand", "model", "series", "vintage_year", "generation_id",
        "length_in", "width_in", "height_in", "corner_radius_in", "corner_type",
        "length_mm", "width_mm", "height_mm", "corner_radius_mm",
        "jetpaks_count", "raised_back", "waterfall_curved", "keypad_protruding", "filter_lid_rigid",
        "has_top_view", "has_side_view", "has_footprint", "has_model_3d",
        "source_manual", "completeness_score_pct", "spafit_notes"
    ]

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for r in all_records:
            d = r.get("dimensions", {})
            o = r.get("obstacles", {})
            m = r.get("media", {})
            writer.writerow([
                r.get("brand", ""),
                r.get("model", ""),
                r.get("series", ""),
                r.get("vintage_year", ""),
                r.get("generation_id", ""),
                d.get("length_in", 0),
                d.get("width_in", 0),
                d.get("height_in", 0),
                d.get("corner_radius_in", 0),
                d.get("corner_type", ""),
                d.get("length_mm", 0),
                d.get("width_mm", 0),
                d.get("height_mm", 0),
                d.get("corner_radius_mm", 0),
                o.get("jetpaks_count", 0),
                o.get("raised_back", False),
                o.get("waterfall_curved", False),
                o.get("keypad_protruding", False),
                o.get("filter_lid_rigid", False),
                m.get("has_top_view", False),
                m.get("has_side_view", False),
                m.get("has_footprint", False),
                m.get("has_model_3d", False),
                r.get("source_manual", ""),
                f"{m.get('completeness_score_pct', 100.0)}%",
                r.get("spafit_notes", "")
            ])

    logger.info(f"Master index CSV ({csv_path.name}) et JSON ({json_path.name}) régénérés avec succès !")


def main():
    step1_clean_parasitic_folders()
    step2_fix_side_views_and_footprints()
    step3_rebuild_master_indexes()
    logger.info("=== TRAITEMENT TERMINÉ AVEC SUCCÈS ===")

if __name__ == "__main__":
    main()
