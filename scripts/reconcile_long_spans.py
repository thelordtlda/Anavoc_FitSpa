import csv
import copy
import shutil
import time
from pathlib import Path

ROOT_DIR = Path(".").resolve()
CSV_PATH = ROOT_DIR / "data/spas_master_database.csv"
ARCHIVE_LOG = ROOT_DIR / "_ARCHIVE/ARCHIVE_LOG.md"

def log_archive(item_name, source_path, dest_path, reason):
    ARCHIVE_LOG.parent.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"| {timestamp} | `{item_name}` | `{source_path}` | `{dest_path}` | {reason} |\n"
    with open(ARCHIVE_LOG, "a", encoding="utf-8") as f:
        f.write(log_entry)
    print(f"  [ARCHIVE LOG] {item_name} -> {dest_path}")

def safe_copy(src: Path, dst: Path):
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src), str(dst))

def main():
    print("======================================================================")
    print("  TASK 9.2: FINISH LONG-SPAN GENERATIONAL ALIGNMENT (ARTESIAN & BULLFROG) ")
    print("======================================================================")

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Loaded {len(rows)} catalog rows.")

    artesian_targets = {
        "Antigua": ("2005-2015", "2016-2026", "8.0", "8.0"),
        "Barbados": ("2005-2015", "2016-2026", "7.0", "7.0"),
        "Captiva": ("2005-2015", "2016-2026", "8.0", "8.0"),
        "Dove Canyon": ("2008-2015", "2016-2026", "8.5", "6.0"),
        "Eagle Crest": ("2008-2015", "2016-2026", "8.0", "8.0"),
        "Quail Ridge": ("2008-2015", "2016-2026", "8.0", "8.0"),
        "Bimini Island": ("2007-2015", "2016-2026", "8.0", "8.0"),
        "Margarita": ("2007-2015", "2016-2026", "8.0", "8.0"),
        "Nevis": ("2007-2015", "2016-2026", "8.0", "8.0"),
        "Santa Cruz": ("2005-2015", "2016-2026", "8.0", "8.0"),
    }

    bullfrog_targets = [
        "A5L", "R5L", "X5L", "A6", "A6L", "R6", "R6L", "X6L",
        "A7", "A7L", "R7", "R7L", "X7", "X7L"
    ]

    new_rows = []
    for idx, r in enumerate(rows):
        brand = r.get("Marque")
        model = r.get("Modele")
        gen = r.get("Generation")
        years = r.get("Annees_Production")

        # 1. Artesian Spas Splitting
        if brand == "Artesian Spas" and model in artesian_targets and ("2005-2026" in years or "2007-2026" in years or "2008-2026" in years):
            y_g1, y_g2, r_g1, r_g2 = artesian_targets[model]
            safe_model = model.replace(" ", "_")
            
            # Move photo to Gen 2 folder if present
            current_photo = r.get("image_top_file")
            g2_photo_rel = "N/A"
            if current_photo and current_photo != "N/A":
                src_photo = ROOT_DIR / current_photo
                photo_name = src_photo.name
                dst_photo = ROOT_DIR / f"assets/Artesian Spas/{safe_model}_Gen_2_{y_g2}/images/overhead/{photo_name}"
                safe_copy(src_photo, dst_photo)
                g2_photo_rel = f"./assets/Artesian Spas/{safe_model}_Gen_2_{y_g2}/images/overhead/{photo_name}"

            # Gen 1 (Historical: 2005/2007/2008 - 2015)
            g1 = copy.deepcopy(r)
            g1["Generation"] = "Gen 1"
            g1["Annees_Production"] = y_g1
            g1["corner_radius_in"] = r_g1
            try:
                g1["corner_radius_cm"] = str(round(float(r_g1) * 2.54, 1))
            except ValueError:
                pass
            g1["image_top_file"] = "N/A"
            g1["image_top_source_url"] = "N/A"
            g1["footprint_file"] = f"./assets/Artesian Spas/{safe_model}_Gen_1_{y_g1}/footprint/{safe_model}_blueprint.pdf"
            g1["audit_notes"] = f"Split Artesian Island/Platinum Gen 1 ({y_g1}); historical vintage"
            new_rows.append(g1)

            # Gen 2 (Modern: 2016-2026) - holds verified modern photo
            g2 = copy.deepcopy(r)
            g2["Generation"] = "Gen 2"
            g2["Annees_Production"] = y_g2
            g2["corner_radius_in"] = r_g2
            try:
                g2["corner_radius_cm"] = str(round(float(r_g2) * 2.54, 1))
            except ValueError:
                pass
            g2["image_top_file"] = g2_photo_rel
            g2["footprint_file"] = f"./assets/Artesian Spas/{safe_model}_Gen_2_{y_g2}/footprint/{safe_model}_blueprint.pdf"
            g2["audit_notes"] = f"Split Artesian Island/Platinum Gen 2 ({y_g2}); holds verified modern photo"
            new_rows.append(g2)
            print(f"  Split Artesian Spas {model} into Gen 1 ({y_g1}) and Gen 2 ({y_g2})")
            continue

        # 2. Bullfrog Spas Splitting (2013-2026 -> 2013-2022 Gen 1 and 2023-2026 Gen 2)
        if brand == "Bullfrog Spas" and model in bullfrog_targets and years == "2013-2026":
            safe_model = model.replace(" ", "_")
            current_photo = r.get("image_top_file")

            # Gen 1 (2013-2022) - holds 2015 photo
            g1 = copy.deepcopy(r)
            g1["Generation"] = "Gen 1"
            g1["Annees_Production"] = "2013-2022"
            g1["corner_radius_in"] = "8.0"
            g1["corner_radius_cm"] = "20.3"
            g1["footprint_file"] = f"./assets/Bullfrog Spas/{safe_model}_Gen_1_2013-2022/footprint/{safe_model}_blueprint.pdf"
            if current_photo and current_photo != "N/A":
                src_photo = ROOT_DIR / current_photo
                photo_name = src_photo.name
                dst_photo = ROOT_DIR / f"assets/Bullfrog Spas/{safe_model}_Gen_1_2013-2022/images/overhead/{photo_name}"
                safe_copy(src_photo, dst_photo)
                g1["image_top_file"] = f"./assets/Bullfrog Spas/{safe_model}_Gen_1_2013-2022/images/overhead/{photo_name}"
            g1["audit_notes"] = "Bounded Bullfrog Gen 1 to authentic 2013-2022 production span; holds 2015 photo"
            new_rows.append(g1)

            # Gen 2 (2023-2026) - modern redesign, sharper corners R=4.0in
            g2 = copy.deepcopy(r)
            g2["Generation"] = "Gen 2"
            g2["Annees_Production"] = "2023-2026"
            g2["corner_radius_in"] = "4.0"
            g2["corner_radius_cm"] = "10.2"
            g2["image_top_file"] = "N/A"
            g2["image_top_source_url"] = "N/A"
            g2["footprint_file"] = f"./assets/Bullfrog Spas/{safe_model}_Gen_2_2023-2026/footprint/{safe_model}_blueprint.pdf"
            g2["audit_notes"] = "Added Bullfrog Gen 2 (2023-2026 redesign with R=4.0in corners)"
            new_rows.append(g2)
            print(f"  Split Bullfrog Spas {model} into Gen 1 (2013-2022) and Gen 2 (2023-2026)")
            continue

        # Keep row as-is
        new_rows.append(r)

    print(f"\nFinal catalog rows: {len(new_rows)} (Net change: {len(new_rows) - len(rows):+d} rows)")

    # Assertions
    photos = [r["image_top_file"] for r in new_rows if r.get("image_top_file") and r.get("image_top_file") != "N/A"]
    dwgs = [r["cad_dwg_file"] for r in new_rows if r.get("cad_dwg_file") and r.get("cad_dwg_file") != "N/A"]
    dxfs = [r["cad_dxf_file"] for r in new_rows if r.get("cad_dxf_file") and r.get("cad_dxf_file") != "N/A"]

    print(f"Total linked photos: {len(photos)} (Unique: {len(set(photos))})")
    assert len(photos) == len(set(photos)), "Duplicate photos detected!"

    print(f"Total linked DWGs: {len(dwgs)} (Unique: {len(set(dwgs))})")
    assert len(dwgs) == len(set(dwgs)), "Duplicate DWGs detected!"

    # Write back to CSV
    with open(CSV_PATH, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        writer.writerows(new_rows)

    print(f"[OK] Successfully updated {len(new_rows)} rows in {CSV_PATH}")

if __name__ == "__main__":
    main()
