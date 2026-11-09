import csv
import shutil
import os
import time
from pathlib import Path
import copy

ROOT_DIR = Path(".").resolve()
CSV_PATH = ROOT_DIR / "data" / "spas_master_database.csv"
CHECKPOINTS_DIR = ROOT_DIR / "data" / "checkpoints"
ARCHIVE_DIR = ROOT_DIR / "_ARCHIVE"
ARCHIVE_LOG = ARCHIVE_DIR / "ARCHIVE_LOG.md"

def log_archive(item_name, source_path, dest_path, reason):
    ARCHIVE_LOG.parent.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"| {timestamp} | `{item_name}` | `{source_path}` | `{dest_path}` | {reason} |\n"
    with open(ARCHIVE_LOG, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(f"  [ARCHIVE LOG] {item_name} -> {dest_path}")

def safe_move(src: Path, dst: Path, log_reason=""):
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists():
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()
    shutil.move(str(src), str(dst))
    log_archive(src.name, str(src.relative_to(ROOT_DIR)), str(dst.relative_to(ROOT_DIR)), log_reason)

def safe_copy(src: Path, dst: Path):
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src), str(dst))
    print(f"  [COPY] {src.name} -> {dst}")

def main():
    print("======================================================================")
    print("       PHASE 8: GENERATIONAL RECONCILIATION & SSOT REMEDIATION        ")
    print("======================================================================")

    # 1. Create Backup Checkpoint
    CHECKPOINTS_DIR.mkdir(parents=True, exist_ok=True)
    ts_str = time.strftime('%Y%m%d_%H%M%S')
    backup_file = CHECKPOINTS_DIR / f"spas_master_database_backup_{ts_str}.csv"
    shutil.copy2(CSV_PATH, backup_file)
    print(f"Created pre-Phase 8 checkpoint backup: {backup_file.name}")

    # 2. File and Directory Migrations
    print("\n--- Migrating & Archiving Asset Files & Folders ---")
    
    # 2.1 Dimension One Amore Bay Gen 1: Purge misattributed 2015 photo
    d1_g1_photo = ROOT_DIR / "assets/Dimension One Spas/Amore Bay_AMO-G1_2005-2014/images/overhead/Amore_Bay_overhead.png"
    if d1_g1_photo.exists():
        arch_target = ARCHIVE_DIR / "misattributed_assets/Amore_Bay_overhead_2015_on_gen1.png"
        safe_move(d1_g1_photo, arch_target, "Purged AmoreBay2015 thumbnail misattributed to Gen 1 (2005-2014)")

    # 2.2 Hot Spring Flare -> Flair folder renaming & CAD migration
    flare_g1_dir = ROOT_DIR / "assets/Hot Spring Spas/Flare_FL_2008-2017"
    flair_g1_dir = ROOT_DIR / "assets/Hot Spring Spas/Flair_FL_2008-2017"
    if flare_g1_dir.exists() and not flair_g1_dir.exists():
        flare_g1_dir.rename(flair_g1_dir)
        print(f"  Renamed {flare_g1_dir.name} -> {flair_g1_dir.name}")

    flare_g2_dir = ROOT_DIR / "assets/Hot Spring Spas/Flare_FLR_2018-2026"
    flair_g2_dir = ROOT_DIR / "assets/Hot Spring Spas/Flair_FLR_2018-2026"
    if flare_g2_dir.exists() and not flair_g2_dir.exists():
        flare_g2_dir.rename(flair_g2_dir)
        print(f"  Renamed {flare_g2_dir.name} -> {flair_g2_dir.name}")

    # Copy Flair_2026.dwg and Flair_2026.dxf into Flair_FLR_2018-2026/cad/
    flair_ghost_cad = ROOT_DIR / "assets/Hot Spring Spas/Flair_Gen_1_2008-2026/cad"
    flair_g2_cad = flair_g2_dir / "cad"
    if (flair_ghost_cad / "Flair_2026.dwg").exists():
        safe_copy(flair_ghost_cad / "Flair_2026.dwg", flair_g2_cad / "Flair_2026.dwg")
    if (flair_ghost_cad / "Flair_2026.dxf").exists():
        safe_copy(flair_ghost_cad / "Flair_2026.dxf", flair_g2_cad / "Flair_2026.dxf")

    # Archive Hot Spring ghost folders
    flair_ghost_dir = ROOT_DIR / "assets/Hot Spring Spas/Flair_Gen_1_2008-2026"
    if flair_ghost_dir.exists():
        safe_move(flair_ghost_dir, ARCHIVE_DIR / "redundant_assets/Flair_Gen_1_2008-2026", "Archived ghost umbrella-split folder Flair 2008-2026")

    flash_ghost_dir = ROOT_DIR / "assets/Hot Spring Spas/Flash_Gen_1_2008-2026"
    if flash_ghost_dir.exists():
        safe_move(flash_ghost_dir, ARCHIVE_DIR / "redundant_assets/Flash_Gen_1_2008-2026", "Archived ghost umbrella-split folder Flash 2008-2026")

    # 2.3 Jacuzzi J-325: Move photo to J-325-G2 and archive legacy folder
    j325_old_photo = ROOT_DIR / "assets/Jacuzzi/J-325_Gen_1_2005-2026/images/overhead/J-325_overhead.png"
    j325_g2_photo = ROOT_DIR / "assets/Jacuzzi/J-325_J-325-G2_2008-2013/images/overhead/J-325_overhead.png"
    if j325_old_photo.exists():
        safe_copy(j325_old_photo, j325_g2_photo)
    
    j325_legacy_dir = ROOT_DIR / "assets/Jacuzzi/J-325_Gen_1_2005-2026"
    if j325_legacy_dir.exists():
        safe_move(j325_legacy_dir, ARCHIVE_DIR / "redundant_assets/J-325_Gen_1_2005-2026", "Archived unsplit J-325 legacy folder")

    # Archive legacy J-215 / J-225 folders
    j215_legacy_dir = ROOT_DIR / "assets/Jacuzzi/J-215_Gen_1_2005-2026"
    if j215_legacy_dir.exists():
        safe_move(j215_legacy_dir, ARCHIVE_DIR / "redundant_assets/J-215_Gen_1_2005-2026", "Archived legacy J-215 2005-2026 folder")

    j225_legacy_dir = ROOT_DIR / "assets/Jacuzzi/J-225_Gen_1_2005-2026"
    if j225_legacy_dir.exists():
        safe_move(j225_legacy_dir, ARCHIVE_DIR / "redundant_assets/J-225_Gen_1_2005-2026", "Archived legacy J-225 2005-2026 folder")

    # 2.4 Sundance Spas: Move photos and archive legacy unsplit folders
    # Dover
    dover_old_photo = ROOT_DIR / "assets/Sundance Spas/Dover_Gen_1_2005-2026/images/overhead/Dover_overhead.jpg"
    dover_g1_photo = ROOT_DIR / "assets/Sundance Spas/Dover_DOV-G1_2005-2016/images/overhead/Dover_overhead.jpg"
    if dover_old_photo.exists():
        safe_copy(dover_old_photo, dover_g1_photo)
    dover_legacy_dir = ROOT_DIR / "assets/Sundance Spas/Dover_Gen_1_2005-2026"
    if dover_legacy_dir.exists():
        safe_move(dover_legacy_dir, ARCHIVE_DIR / "redundant_assets/Dover_Gen_1_2005-2026", "Archived unsplit Dover legacy folder")

    # Marin
    marin_old_photo = ROOT_DIR / "assets/Sundance Spas/Marin_Gen_1_2005-2026/images/overhead/Marin_overhead.jpg"
    marin_g1_photo = ROOT_DIR / "assets/Sundance Spas/Marin_MAR-G1_2005-2015/images/overhead/Marin_overhead.jpg"
    if marin_old_photo.exists():
        safe_copy(marin_old_photo, marin_g1_photo)
    marin_legacy_dir = ROOT_DIR / "assets/Sundance Spas/Marin_Gen_1_2005-2026"
    if marin_legacy_dir.exists():
        safe_move(marin_legacy_dir, ARCHIVE_DIR / "redundant_assets/Marin_Gen_1_2005-2026", "Archived unsplit Marin legacy folder")

    # Peyton
    peyton_old_photo = ROOT_DIR / "assets/Sundance Spas/Peyton_Gen_1_2012-2026/images/overhead/Peyton_overhead.jpg"
    peyton_g1_photo = ROOT_DIR / "assets/Sundance Spas/Peyton_PEY-G1_2012-2017/images/overhead/Peyton_overhead.jpg"
    if peyton_old_photo.exists():
        safe_copy(peyton_old_photo, peyton_g1_photo)
    peyton_legacy_dir = ROOT_DIR / "assets/Sundance Spas/Peyton_Gen_1_2012-2026"
    if peyton_legacy_dir.exists():
        safe_move(peyton_legacy_dir, ARCHIVE_DIR / "redundant_assets/Peyton_Gen_1_2012-2026", "Archived unsplit Peyton legacy folder")

    # Edison 680
    edison_legacy_dir = ROOT_DIR / "assets/Sundance Spas/Edison_680_Gen_1_2012-2026"
    if edison_legacy_dir.exists():
        safe_move(edison_legacy_dir, ARCHIVE_DIR / "redundant_assets/Edison_680_Gen_1_2012-2026", "Archived unsplit Edison 680 legacy folder")

    # Bristol
    bristol_legacy_dir = ROOT_DIR / "assets/Sundance Spas/Bristol_Gen_1_2012-2026"
    if bristol_legacy_dir.exists():
        safe_move(bristol_legacy_dir, ARCHIVE_DIR / "redundant_assets/Bristol_Gen_1_2012-2026", "Archived unsplit Bristol legacy folder")

    # 3. Read and Remediate CSV Rows
    print("\n--- Rebuilding Master Database Rows ---")
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Loaded {len(rows)} initial rows.")

    new_rows = []
    for idx, r in enumerate(rows):
        brand = r.get("Marque")
        model = r.get("Modele")
        gen = r.get("Generation")
        years = r.get("Annees_Production")

        # 3.1 Hot Spring Strobe: purge borrowed photo
        if brand == "Hot Spring Spas" and model == "Strobe":
            r_new = copy.deepcopy(r)
            r_new["image_top_file"] = "N/A"
            r_new["image_top_source_url"] = "N/A"
            r_new["audit_notes"] = "Borrowed Pace photo unlinked to enforce 1:1 asset unicity"
            new_rows.append(r_new)
            continue

        # 3.2 Hot Spring Flair ghost row 2008-2026
        if brand == "Hot Spring Spas" and model == "Flair" and years == "2008-2026":
            print(f"  Removing ghost row: Hot Spring Flair {years}")
            continue

        # 3.3 Hot Spring Flash ghost row 2008-2026
        if brand == "Hot Spring Spas" and model == "Flash" and years == "2008-2026":
            print(f"  Removing ghost row: Hot Spring Flash {years}")
            continue

        # 3.4 Hot Spring Flare Gen 1 2008-2017 -> Flair Gen 1 2008-2017
        if brand == "Hot Spring Spas" and model == "Flare" and gen == "Gen 1":
            r_new = copy.deepcopy(r)
            r_new["Modele"] = "Flair"
            r_new["cad_dwg_file"] = "./assets/Hot Spring Spas/Flair_FL_2008-2017/cad/Flare_2012.dwg"
            r_new["cad_dxf_file"] = "./assets/Hot Spring Spas/Flair_FL_2008-2017/cad/Flare_2012_authentic.dxf"
            r_new["image_top_file"] = "./assets/Hot Spring Spas/Flair_FL_2008-2017/images/overhead/Flare_overhead.png"
            r_new["footprint_file"] = "./assets/Hot Spring Spas/Flair_FL_2008-2017/footprint/Flair_blueprint.pdf"
            r_new["audit_notes"] = "Reconciled spelling Flare->Flair; holds 2012 factory DWG/DXF"
            new_rows.append(r_new)
            continue

        # 3.5 Hot Spring Flare Gen 2 2018-2026 -> Flair Gen 2 2018-2026
        if brand == "Hot Spring Spas" and model == "Flare" and gen == "Gen 2":
            r_new = copy.deepcopy(r)
            r_new["Modele"] = "Flair"
            r_new["cad_dwg_file"] = "./assets/Hot Spring Spas/Flair_FLR_2018-2026/cad/Flair_2026.dwg"
            r_new["cad_dxf_file"] = "./assets/Hot Spring Spas/Flair_FLR_2018-2026/cad/Flair_2026.dxf"
            r_new["image_top_file"] = "./assets/Hot Spring Spas/Flair_FLR_2018-2026/images/overhead/Flare_overhead.png"
            r_new["footprint_file"] = "./assets/Hot Spring Spas/Flair_FLR_2018-2026/footprint/Flair_blueprint.pdf"
            r_new["audit_notes"] = "Reconciled spelling Flare->Flair; holds 2026 factory DWG/DXF"
            new_rows.append(r_new)
            continue

        # 3.6 Hot Spring Flash Gen 2 2018-2026 -> Flash Gen 1 2018-2026
        if brand == "Hot Spring Spas" and model == "Flash" and years == "2018-2026":
            r_new = copy.deepcopy(r)
            r_new["Generation"] = "Gen 1"
            r_new["cad_dwg_file"] = "./assets/Hot Spring Spas/Flash_FLS_2018-2026/cad/Flash_2026.dwg"
            r_new["cad_dxf_file"] = "./assets/Hot Spring Spas/Flash_FLS_2018-2026/cad/Flash_2026_authentic.dxf"
            r_new["image_top_file"] = "./assets/Hot Spring Spas/Flash_FLS_2018-2026/images/overhead/Flash_overhead.png"
            r_new["footprint_file"] = "./assets/Hot Spring Spas/Flash_FLS_2018-2026/footprint/Flash_blueprint.pdf"
            r_new["audit_notes"] = "Corrected Generation to Gen 1 (introduced 2018); holds 2026 factory DWG/DXF"
            new_rows.append(r_new)
            continue

        # 3.7 Jacuzzi J-215 (2005-2026 -> 2015-2026)
        if brand == "Jacuzzi" and model == "J-215":
            r_new = copy.deepcopy(r)
            r_new["Annees_Production"] = "2015-2026"
            r_new["length_in"] = "80.0"
            r_new["length_cm"] = "203.2"
            r_new["width_in"] = "69.0"
            r_new["width_cm"] = "175.3"
            r_new["height_in"] = "33.0"
            r_new["height_cm"] = "83.8"
            r_new["corner_radius_in"] = "8.5"
            r_new["corner_radius_cm"] = "21.6"
            r_new["footprint_file"] = "./assets/Jacuzzi/J-215_J-215_2015-2026/footprint/J-215_blueprint.pdf"
            r_new["audit_notes"] = "Corrected production launch window to authentic 2015-2026"
            new_rows.append(r_new)
            continue

        # 3.8 Jacuzzi J-225 (2005-2026 -> 2015-2026)
        if brand == "Jacuzzi" and model == "J-225":
            r_new = copy.deepcopy(r)
            r_new["Annees_Production"] = "2015-2026"
            r_new["length_in"] = "80.0"
            r_new["length_cm"] = "203.2"
            r_new["width_in"] = "80.0"
            r_new["width_cm"] = "203.2"
            r_new["height_in"] = "33.0"
            r_new["height_cm"] = "83.8"
            r_new["corner_radius_in"] = "8.5"
            r_new["corner_radius_cm"] = "21.6"
            r_new["footprint_file"] = "./assets/Jacuzzi/J-225_J-225_2015-2026/footprint/J-225_blueprint.pdf"
            r_new["audit_notes"] = "Corrected production launch window to authentic 2015-2026"
            new_rows.append(r_new)
            continue

        # 3.9 Jacuzzi J-325 (Split into 4 generations)
        if brand == "Jacuzzi" and model == "J-325":
            print(f"  Splitting Jacuzzi J-325 into 4 generations...")
            # Gen 1 (2005-2007)
            g1 = copy.deepcopy(r)
            g1["Generation"] = "Gen 1"
            g1["Code_Usine_Chassis"] = "J-325-G1"
            g1["Serie_Collection"] = "J-300"
            g1["Annees_Production"] = "2005-2007"
            g1["length_in"] = "84.0"
            g1["length_cm"] = "213.4"
            g1["width_in"] = "76.0"
            g1["width_cm"] = "193.0"
            g1["height_in"] = "34.0"
            g1["height_cm"] = "86.4"
            g1["corner_radius_in"] = "8.5"
            g1["corner_radius_cm"] = "21.6"
            g1["image_top_file"] = "N/A"
            g1["image_top_source_url"] = "N/A"
            g1["footprint_file"] = "./assets/Jacuzzi/J-325_J-325-G1_2005-2007/footprint/J-325_blueprint.pdf"
            g1["audit_notes"] = "Split J-325 into standard J-300 generation sequence (Gen 1 2005-2007)"
            new_rows.append(g1)

            # Gen 2 (2008-2013) - holds photo
            g2 = copy.deepcopy(r)
            g2["Generation"] = "Gen 2"
            g2["Code_Usine_Chassis"] = "J-325-G2"
            g2["Serie_Collection"] = "J-300"
            g2["Annees_Production"] = "2008-2013"
            g2["length_in"] = "84.0"
            g2["length_cm"] = "213.4"
            g2["width_in"] = "76.0"
            g2["width_cm"] = "193.0"
            g2["height_in"] = "34.0"
            g2["height_cm"] = "86.4"
            g2["corner_radius_in"] = "8.5"
            g2["corner_radius_cm"] = "21.6"
            g2["image_top_file"] = "./assets/Jacuzzi/J-325_J-325-G2_2008-2013/images/overhead/J-325_overhead.png"
            g2["image_top_source_url"] = "https://web.archive.org/web/20140223194723im_/http://www.jacuzzihottubs.com/wp-content/uploads/2013/09/j-325-overhead-257x257.png"
            g2["footprint_file"] = "./assets/Jacuzzi/J-325_J-325-G2_2008-2013/footprint/J-325_blueprint.pdf"
            g2["audit_notes"] = "Split J-325 into standard J-300 generation sequence; Gen 2 holds authentic Sept 2013 photo"
            new_rows.append(g2)

            # Gen 3 (2014-2019)
            g3 = copy.deepcopy(r)
            g3["Generation"] = "Gen 3"
            g3["Code_Usine_Chassis"] = "J-325-G3"
            g3["Serie_Collection"] = "J-300"
            g3["Annees_Production"] = "2014-2019"
            g3["length_in"] = "84.0"
            g3["length_cm"] = "213.4"
            g3["width_in"] = "76.0"
            g3["width_cm"] = "193.0"
            g3["height_in"] = "34.0"
            g3["height_cm"] = "86.4"
            g3["corner_radius_in"] = "8.5"
            g3["corner_radius_cm"] = "21.6"
            g3["image_top_file"] = "N/A"
            g3["image_top_source_url"] = "N/A"
            g3["footprint_file"] = "./assets/Jacuzzi/J-325_J-325-G3_2014-2019/footprint/J-325_blueprint.pdf"
            g3["audit_notes"] = "Split J-325 into standard J-300 generation sequence (Gen 3 2014-2019)"
            new_rows.append(g3)

            # Gen 4 (2020-2026)
            g4 = copy.deepcopy(r)
            g4["Generation"] = "Gen 4"
            g4["Code_Usine_Chassis"] = "J-325-G4"
            g4["Serie_Collection"] = "J-300"
            g4["Annees_Production"] = "2020-2026"
            g4["length_in"] = "84.0"
            g4["length_cm"] = "213.4"
            g4["width_in"] = "76.0"
            g4["width_cm"] = "193.0"
            g4["height_in"] = "34.0"
            g4["height_cm"] = "86.4"
            g4["corner_radius_in"] = "8.5"
            g4["corner_radius_cm"] = "21.6"
            g4["image_top_file"] = "N/A"
            g4["image_top_source_url"] = "N/A"
            g4["footprint_file"] = "./assets/Jacuzzi/J-325_J-325-G4_2020-2026/footprint/J-325_blueprint.pdf"
            g4["audit_notes"] = "Split J-325 into standard J-300 generation sequence (Gen 4 2020-2026)"
            new_rows.append(g4)
            continue

        # 3.10 Sundance Bristol (2012-2026 -> 2017-2026, R=11.0)
        if brand == "Sundance Spas" and model == "Bristol":
            r_new = copy.deepcopy(r)
            r_new["Annees_Production"] = "2017-2026"
            r_new["Code_Usine_Chassis"] = "BRI-G1"
            r_new["length_in"] = "84.0"
            r_new["length_cm"] = "213.4"
            r_new["width_in"] = "84.0"
            r_new["width_cm"] = "213.4"
            r_new["height_in"] = "36.0"
            r_new["height_cm"] = "91.4"
            r_new["corner_radius_in"] = "11.0"
            r_new["corner_radius_cm"] = "27.9"
            r_new["footprint_file"] = "./assets/Sundance Spas/Bristol_BRI_2017-2026/footprint/Bristol_blueprint.pdf"
            r_new["audit_notes"] = "Corrected launch window to 2017-2026 (780 Series redesign); corner radius verified at R=11.0in."
            new_rows.append(r_new)
            continue

        # 3.11 Sundance Dover (Split Gen 1 R=8.5 and Gen 2 R=11.0)
        if brand == "Sundance Spas" and model == "Dover":
            print(f"  Splitting Sundance Dover into 2 generations...")
            # Gen 1 (2005-2016, R=8.5)
            g1 = copy.deepcopy(r)
            g1["Generation"] = "Gen 1"
            g1["Code_Usine_Chassis"] = "DOV-G1"
            g1["Annees_Production"] = "2005-2016"
            g1["length_in"] = "82.0"
            g1["length_cm"] = "208.3"
            g1["width_in"] = "69.0"
            g1["width_cm"] = "175.3"
            g1["height_in"] = "30.5"
            g1["height_cm"] = "77.5"
            g1["corner_radius_in"] = "8.5"
            g1["corner_radius_cm"] = "21.6"
            g1["image_top_file"] = "./assets/Sundance Spas/Dover_DOV-G1_2005-2016/images/overhead/Dover_overhead.jpg"
            g1["footprint_file"] = "./assets/Sundance Spas/Dover_DOV-G1_2005-2016/footprint/Dover_blueprint.pdf"
            g1["audit_notes"] = "Split Dover Gen 1 (2005-2016, R=8.5in); holds authentic overhead photo"
            new_rows.append(g1)

            # Gen 2 (2017-2026, R=11.0)
            g2 = copy.deepcopy(r)
            g2["Generation"] = "Gen 2"
            g2["Code_Usine_Chassis"] = "DOV-G2"
            g2["Annees_Production"] = "2017-2026"
            g2["length_in"] = "82.0"
            g2["length_cm"] = "208.3"
            g2["width_in"] = "69.0"
            g2["width_cm"] = "175.3"
            g2["height_in"] = "30.5"
            g2["height_cm"] = "77.5"
            g2["corner_radius_in"] = "11.0"
            g2["corner_radius_cm"] = "27.9"
            g2["image_top_file"] = "N/A"
            g2["image_top_source_url"] = "N/A"
            g2["footprint_file"] = "./assets/Sundance Spas/Dover_DOV-G2_2017-2026/footprint/Dover_blueprint.pdf"
            g2["audit_notes"] = "Split Dover Gen 2 (2017-2026, R=11.0in redesign); 0 shared photo"
            new_rows.append(g2)
            continue

        # 3.12 Sundance Marin (Split Gen 1 2005-2015 and Gen 2 2016-2026)
        if brand == "Sundance Spas" and model == "Marin":
            print(f"  Splitting Sundance Marin into 2 generations...")
            # Gen 1 (2005-2015)
            g1 = copy.deepcopy(r)
            g1["Generation"] = "Gen 1"
            g1["Code_Usine_Chassis"] = "MAR-G1"
            g1["Annees_Production"] = "2005-2015"
            g1["length_in"] = "91.0"
            g1["length_cm"] = "231.1"
            g1["width_in"] = "76.0"
            g1["width_cm"] = "193.0"
            g1["height_in"] = "34.0"
            g1["height_cm"] = "86.4"
            g1["corner_radius_in"] = "11.0"
            g1["corner_radius_cm"] = "27.9"
            g1["image_top_file"] = "./assets/Sundance Spas/Marin_MAR-G1_2005-2015/images/overhead/Marin_overhead.jpg"
            g1["footprint_file"] = "./assets/Sundance Spas/Marin_MAR-G1_2005-2015/footprint/Marin_blueprint.pdf"
            g1["audit_notes"] = "Split Marin Gen 1 (2005-2015, R=11.0in); holds authentic overhead photo"
            new_rows.append(g1)

            # Gen 2 (2016-2026)
            g2 = copy.deepcopy(r)
            g2["Generation"] = "Gen 2"
            g2["Code_Usine_Chassis"] = "MAR-G2"
            g2["Annees_Production"] = "2016-2026"
            g2["length_in"] = "91.0"
            g2["length_cm"] = "231.1"
            g2["width_in"] = "76.0"
            g2["width_cm"] = "193.0"
            g2["height_in"] = "34.0"
            g2["height_cm"] = "86.4"
            g2["corner_radius_in"] = "11.0"
            g2["corner_radius_cm"] = "27.9"
            g2["image_top_file"] = "N/A"
            g2["image_top_source_url"] = "N/A"
            g2["footprint_file"] = "./assets/Sundance Spas/Marin_MAR-G2_2016-2026/footprint/Marin_blueprint.pdf"
            g2["audit_notes"] = "Split Marin Gen 2 (2016-2026, 880 Series redesign); 0 shared photo"
            new_rows.append(g2)
            continue

        # 3.13 Sundance Edison 680 (Split Gen 1 2013-2017 and Gen 2 2018-2026)
        if brand == "Sundance Spas" and model == "Edison 680":
            print(f"  Splitting Sundance Edison 680 into 2 generations...")
            # Gen 1 (2013-2017)
            g1 = copy.deepcopy(r)
            g1["Generation"] = "Gen 1"
            g1["Code_Usine_Chassis"] = "EDI-G1"
            g1["Annees_Production"] = "2013-2017"
            g1["length_in"] = "84.0"
            g1["length_cm"] = "213.4"
            g1["width_in"] = "84.0"
            g1["width_cm"] = "213.4"
            g1["height_in"] = "36.0"
            g1["height_cm"] = "91.4"
            g1["corner_radius_in"] = "8.5"
            g1["corner_radius_cm"] = "21.6"
            g1["image_top_file"] = "N/A"
            g1["image_top_source_url"] = "N/A"
            g1["footprint_file"] = "./assets/Sundance Spas/Edison_680_EDI-G1_2013-2017/footprint/Edison_680_blueprint.pdf"
            g1["audit_notes"] = "Split Edison 680 Gen 1 (2013-2017, R=8.5in)"
            new_rows.append(g1)

            # Gen 2 (2018-2026)
            g2 = copy.deepcopy(r)
            g2["Generation"] = "Gen 2"
            g2["Code_Usine_Chassis"] = "EDI-G2"
            g2["Annees_Production"] = "2018-2026"
            g2["length_in"] = "84.0"
            g2["length_cm"] = "213.4"
            g2["width_in"] = "84.0"
            g2["width_cm"] = "213.4"
            g2["height_in"] = "36.0"
            g2["height_cm"] = "91.4"
            g2["corner_radius_in"] = "8.5"
            g2["corner_radius_cm"] = "21.6"
            g2["image_top_file"] = "N/A"
            g2["image_top_source_url"] = "N/A"
            g2["footprint_file"] = "./assets/Sundance Spas/Edison_680_EDI-G2_2018-2026/footprint/Edison_680_blueprint.pdf"
            g2["audit_notes"] = "Split Edison 680 Gen 2 (2018-2026 680 Series redesign, R=8.5in)"
            new_rows.append(g2)
            continue

        # 3.14 Sundance Peyton (Split Gen 1 2012-2017 and Gen 2 2018-2026)
        if brand == "Sundance Spas" and model == "Peyton":
            print(f"  Splitting Sundance Peyton into 2 generations...")
            # Gen 1 (2012-2017)
            g1 = copy.deepcopy(r)
            g1["Generation"] = "Gen 1"
            g1["Code_Usine_Chassis"] = "PEY-G1"
            g1["Annees_Production"] = "2012-2017"
            g1["length_in"] = "84.0"
            g1["length_cm"] = "213.4"
            g1["width_in"] = "84.0"
            g1["width_cm"] = "213.4"
            g1["height_in"] = "36.0"
            g1["height_cm"] = "91.4"
            g1["corner_radius_in"] = "8.5"
            g1["corner_radius_cm"] = "21.6"
            g1["image_top_file"] = "./assets/Sundance Spas/Peyton_PEY-G1_2012-2017/images/overhead/Peyton_overhead.jpg"
            g1["footprint_file"] = "./assets/Sundance Spas/Peyton_PEY-G1_2012-2017/footprint/Peyton_blueprint.pdf"
            g1["audit_notes"] = "Split Peyton Gen 1 (2012-2017, R=8.5in); holds authentic overhead photo"
            new_rows.append(g1)

            # Gen 2 (2018-2026)
            g2 = copy.deepcopy(r)
            g2["Generation"] = "Gen 2"
            g2["Code_Usine_Chassis"] = "PEY-G2"
            g2["Annees_Production"] = "2018-2026"
            g2["length_in"] = "84.0"
            g2["length_cm"] = "213.4"
            g2["width_in"] = "84.0"
            g2["width_cm"] = "213.4"
            g2["height_in"] = "36.0"
            g2["height_cm"] = "91.4"
            g2["corner_radius_in"] = "8.5"
            g2["corner_radius_cm"] = "21.6"
            g2["image_top_file"] = "N/A"
            g2["image_top_source_url"] = "N/A"
            g2["footprint_file"] = "./assets/Sundance Spas/Peyton_PEY-G2_2018-2026/footprint/Peyton_blueprint.pdf"
            g2["audit_notes"] = "Split Peyton Gen 2 (2018-2026 680 Series redesign, R=8.5in); 0 shared photo"
            new_rows.append(g2)
            continue

        # 3.15 Dimension One Amore Bay Gen 1 (2005-2014)
        if brand == "Dimension One Spas" and model == "Amore Bay" and gen == "Gen 1":
            r_new = copy.deepcopy(r)
            r_new["image_top_file"] = "N/A"
            r_new["image_top_source_url"] = "N/A"
            r_new["audit_notes"] = "Purged misattributed 2015 overhead thumbnail to prevent generational leak"
            new_rows.append(r_new)
            continue

        # All other rows preserved
        new_rows.append(r)

    print(f"\nFinal row count: {len(new_rows)} (Net change: {len(new_rows) - len(rows):+d} rows)")

    # 4. Rigorous Unicity Assertions
    photos = [r["image_top_file"] for r in new_rows if r.get("image_top_file") and r.get("image_top_file") != "N/A"]
    dwgs = [r["cad_dwg_file"] for r in new_rows if r.get("cad_dwg_file") and r.get("cad_dwg_file") != "N/A"]
    dxfs = [r["cad_dxf_file"] for r in new_rows if r.get("cad_dxf_file") and r.get("cad_dxf_file") != "N/A"]

    print(f"Total linked photos: {len(photos)} (Unique: {len(set(photos))})")
    assert len(photos) == len(set(photos)), f"ERROR: Duplicate photos found: {len(photos)} vs {len(set(photos))}"

    print(f"Total linked DWGs: {len(dwgs)} (Unique: {len(set(dwgs))})")
    assert len(dwgs) == len(set(dwgs)), f"ERROR: Duplicate DWGs found: {len(dwgs)} vs {len(set(dwgs))}"

    print(f"Total linked DXFs: {len(dxfs)} (Unique: {len(set(dxfs))})")
    assert len(dxfs) == len(set(dxfs)), f"ERROR: Duplicate DXFs found: {len(dxfs)} vs {len(set(dxfs))}"

    # 5. Write to CSV
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(new_rows)

    print(f"\nSuccessfully wrote {len(new_rows)} rows to {CSV_PATH}")

if __name__ == "__main__":
    main()
