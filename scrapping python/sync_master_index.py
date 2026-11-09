import json
import csv
from pathlib import Path

base_dir = Path(__file__).resolve().parent
dataset_dir = base_dir / "dataset"
json_index = dataset_dir / "spa_master_index.json"
csv_index = dataset_dir / "spa_master_index.csv"

print("--- Synchronisation de spa_master_index.json et spa_master_index.csv ---")

with open(json_index, "r", encoding="utf-8") as f:
    records = json.load(f)

print(f"Total enregistrements : {len(records)}")

updated_count = 0
for r in records:
    # Si le modèle est Glow de Hot Spring Spas
    if "hot spring" in r.get("brand", "").lower() and "glow" in r.get("model", "").lower():
        r["length_in"] = 84.0
        r["width_in"] = 76.0
        r["height_in"] = 33.0
        r["length_mm"] = 2134
        r["width_mm"] = 1930
        r["height_mm"] = 838
        r["corner_radius_in"] = 8.0
        r["corner_radius_mm"] = 203
        r["dimensions_str"] = "84.0\" x 76.0\" x 33.0\""
        r["dimensions_formatted"] = "84.0\" x 76.0\" x 33.0\" (R: 8.0\")"
        updated_count += 1
        
    # Vérifier si cad_model.dwg existe sur le disque pour ce modèle
    # Structure de chemin
    yr = str(r.get("year", ""))
    slug = r.get("model_slug") or r.get("model", "").lower().replace(" ", "_")
    brand_slug = r.get("brand", "").lower().replace(" ", "_")
    
    # Check folder
    candidates = list(dataset_dir.glob(f"{brand_slug}/{yr}/*{slug}*"))
    if not candidates:
        candidates = list(dataset_dir.glob(f"*/{yr}/*{slug}*"))
    if candidates:
        m_dir = candidates[0]
        if (m_dir / "cad_model.dwg").exists():
            r["has_cad"] = True
            r["cad_file"] = "cad_model.dwg"
            r["cad_format"] = "DWG"
        if (m_dir / "top_view.jpg").exists():
            # Check metadata.json inside
            mp = m_dir / "metadata.json"
            if mp.exists():
                try:
                    with open(mp, "r", encoding="utf-8") as mf:
                        mdata = json.load(mf)
                    r["has_real_photo"] = mdata.get("provenance", {}).get("has_real_photo", False)
                except Exception:
                    pass

print(f"Modèles Glow mis à jour avec les cotes officielles 84x76x33 : {updated_count}")

# Sauvegarder spa_master_index.json
with open(json_index, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)
print("spa_master_index.json sauvegardé !")

# Sauvegarder spa_master_index.csv
if records:
    fieldnames = list(records[0].keys())
    with open(csv_index, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print("spa_master_index.csv sauvegardé !")
