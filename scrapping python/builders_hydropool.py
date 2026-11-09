"""
builders_hydropool.py
=====================
Générateur de spécifications techniques et millésimes pour Hydropool Hot Tubs & Swim Spas:
- Self-Cleaning Series (395 à 970)
- Serenity Series (4300 à 6900)
- AquaPlay, AquaSport, AquaTrainer Swim Spas (14AX, 17AX, 19AX)
- Executive Swim Spas (16EX, 19EX Executive Dual Temp)
"""

from typing import List, Dict, Any

def build_hydropool_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []

    # 1. Hydropool Swim Spas
    swim_models = [
        {"model": "AquaPlay 14AX", "dims": (174.0, 93.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "AquaPlay 14AX - Spa de nage d'entrée de gamme récréatif"},
        {"model": "AquaSport 14AX", "dims": (174.0, 93.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "AquaSport 14AX - Nage sportive avec jets de résistance à débit large"},
        {"model": "AquaTrainer 14AX", "dims": (174.0, 93.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "AquaTrainer 14AX - Nage professionnelle à turbine sans remous"},
        {"model": "AquaSport 17AX", "dims": (210.0, 93.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "AquaSport 17AX - Cuve de 17.5 pi pour nageurs expérimentés"},
        {"model": "AquaTrainer 17AX", "dims": (210.0, 93.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "AquaTrainer 17AX - Cuve d'entraînement 17.5 pi avec commande AquaPro"},
        {"model": "AquaSport 19AX", "dims": (226.0, 93.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "AquaSport 19AX - Cuve extra-longue de près de 19 pi"},
        {"model": "AquaTrainer 19AX", "dims": (226.0, 93.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "AquaTrainer 19AX - Cuve d'entraînement ultime 19 pi"},
        {"model": "Executive 16EX", "dims": (186.0, 93.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "Executive 16EX - Forme ergonomique optimisée pour l'écoulement d'eau"},
        {"model": "Executive 19EX", "dims": (226.0, 93.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "Executive 19EX Dual Temp - Double zone indépendante nage et relaxation"}
    ]

    for yr in range(2011, 2027):
        for m in swim_models:
            if "AX" in m["model"] and yr < 2017:
                # Avant 2017, modèles nommés 14fX, 17fX, 19fX
                old_m_name = m["model"].replace("AX", "fX")
                gen_id = f"HP-SWIM-{old_m_name.replace(' ', '_').upper()}-{yr}"
                model_name = old_m_name
            else:
                gen_id = f"HP-SWIM-{m['model'].replace(' ', '_').upper()}-{yr}"
                model_name = m["model"]

            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Hydropool",
                "model": model_name,
                "model_normalized": f"hydropool_{model_name.lower().replace(' ', '_')}_{yr}",
                "series": "Hydropool Swim Spas",
                "vintage_year": yr,
                "production_years": "2011-2026",
                "generation_id": gen_id,
                "is_swim_spa": True,
                "dimensions": {
                    "length_in": l,
                    "width_in": w,
                    "height_in": h,
                    "corner_radius_in": r,
                    "corner_type": m["c_type"],
                    "length_mm": round(l * 25.4, 1),
                    "width_mm": round(w * 25.4, 1),
                    "height_mm": round(h * 25.4, 1),
                    "corner_radius_mm": round(r * 25.4, 1)
                },
                "obstacles": {
                    "has_raised_back": False,
                    "has_curved_waterfall": True,
                    "has_protruding_headrests": True,
                    "has_rigid_filter_lid": True,
                    "description": "Technologie Self-Cleaning brevetée avec skimmer de surface et aspiration sous vide"
                },
                "spafit_notes": f"Compatible SpaFit Legend Swim Spa Bracket. Longueur {l} po."
            })

    # 2. Self-Cleaning Hot Tubs
    sc_models = [
        {"model": "Self-Cleaning 395", "dims": (85.0, 65.0, 30.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 3},
        {"model": "Self-Cleaning 495", "dims": (79.0, 79.0, 37.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 5},
        {"model": "Self-Cleaning 570", "dims": (80.0, 80.0, 37.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 5},
        {"model": "Self-Cleaning 670", "dims": (84.0, 84.0, 39.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 6},
        {"model": "Self-Cleaning 695", "dims": (84.0, 84.0, 39.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 6},
        {"model": "Self-Cleaning 770", "dims": (90.0, 90.0, 39.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 7},
        {"model": "Self-Cleaning 790", "dims": (90.0, 90.0, 39.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 8},
        {"model": "Self-Cleaning 970", "dims": (110.0, 91.0, 39.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 9}
    ]

    for yr in range(2010, 2027):
        for m in sc_models:
            gen_id = f"HP-SC-{m['model'].replace(' ', '_').replace('-', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Hydropool",
                "model": m["model"],
                "model_normalized": f"hydropool_{m['model'].lower().replace(' ', '_').replace('-', '_')}_{yr}",
                "series": "Self-Cleaning Series",
                "vintage_year": yr,
                "production_years": "2010-2026",
                "generation_id": gen_id,
                "is_swim_spa": False,
                "dimensions": {
                    "length_in": l,
                    "width_in": w,
                    "height_in": h,
                    "corner_radius_in": r,
                    "corner_type": m["c_type"],
                    "length_mm": round(l * 25.4, 1),
                    "width_mm": round(w * 25.4, 1),
                    "height_mm": round(h * 25.4, 1),
                    "corner_radius_mm": round(r * 25.4, 1)
                },
                "obstacles": {
                    "has_raised_back": False,
                    "has_curved_waterfall": True,
                    "has_protruding_headrests": True,
                    "has_rigid_filter_lid": True,
                    "description": "Filtre sous pression Self-Cleaning avec couvercle rigide affleurant"
                },
                "spafit_notes": f"Compatible SpaFit Evolution ou Oasis."
            })

    # 3. Serenity Series
    serenity_models = [
        {"model": "Serenity 4300", "dims": (85.0, 62.0, 30.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 3},
        {"model": "Serenity 4500", "dims": (80.0, 80.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 4},
        {"model": "Serenity 5900", "dims": (85.0, 85.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 5},
        {"model": "Serenity 6800", "dims": (85.0, 85.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 6},
        {"model": "Serenity 6900", "dims": (85.0, 85.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 7}
    ]

    for yr in range(2010, 2027):
        for m in serenity_models:
            gen_id = f"HP-SER-{m['model'].replace(' ', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Hydropool",
                "model": m["model"],
                "model_normalized": f"hydropool_{m['model'].lower().replace(' ', '_')}_{yr}",
                "series": "Serenity Series",
                "vintage_year": yr,
                "production_years": "2010-2026",
                "generation_id": gen_id,
                "is_swim_spa": False,
                "dimensions": {
                    "length_in": l,
                    "width_in": w,
                    "height_in": h,
                    "corner_radius_in": r,
                    "corner_type": m["c_type"],
                    "length_mm": round(l * 25.4, 1),
                    "width_mm": round(w * 25.4, 1),
                    "height_mm": round(h * 25.4, 1),
                    "corner_radius_mm": round(r * 25.4, 1)
                },
                "obstacles": {
                    "has_raised_back": False,
                    "has_curved_waterfall": True,
                    "has_protruding_headrests": True,
                    "has_rigid_filter_lid": True,
                    "description": "Serenity bar top régulier avec cascade MoonFalls"
                },
                "spafit_notes": f"Compatible SpaFit Evolution ou Oasis."
            })

    return yearly_data
