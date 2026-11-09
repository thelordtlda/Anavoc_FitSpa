"""
builders_master_spas.py
=======================
Générateur de spécifications techniques et millésimes pour Master Spas:
- Michael Phelps Signature Swim Spas
- H2X Fitness Swim Spas
- Legend Series (LSX)
- Twilight Series (TS)
- Clarity Spas
- Healthy Living Spas
"""

from typing import List, Dict, Any

def build_master_spas_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []

    # 1. Michael Phelps Signature Swim Spas
    mp_models = [
        {"model": "MP Momentum Deep", "dims": (231.0, 94.0, 60.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "Michael Phelps Momentum Deep - Double zone autonome spa + nage à propulsion Wave XP"},
        {"model": "MP Signature Deep", "dims": (215.0, 94.0, 60.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "Michael Phelps Signature Deep - Cuve de nage longue 18 pi"},
        {"model": "MP Force Deep", "dims": (201.0, 94.0, 60.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "Michael Phelps Force Deep - Cuve de nage 17 pi"}
    ]

    for yr in range(2011, 2027):
        for m in mp_models:
            gen_id = f"MS-MP-{m['model'].replace(' ', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Master Spas",
                "model": m["model"],
                "model_normalized": f"master_spas_{m['model'].lower().replace(' ', '_')}_{yr}",
                "series": "Michael Phelps Signature Swim Spas",
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
                    "description": "Michael Phelps propulsion Wave XP Pro, écran tactile Touch2O, barres inox de maintien"
                },
                "spafit_notes": f"Compatible SpaFit Legend Swim Spa Bracket. Longueur {l} po, hauteur 60 po."
            })

    # 2. H2X Fitness Swim Spas
    h2x_models = [
        {"model": "Challenger 19D", "dims": (228.0, 94.0, 60.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "H2X Challenger 19D - Propulsion sans air variable à 6 jets XP"},
        {"model": "Challenger 18D", "dims": (215.0, 94.0, 60.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "H2X Challenger 18D - Cuve fitness 18 pi"},
        {"model": "Challenger 15D", "dims": (180.0, 94.0, 60.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "H2X Challenger 15D - Cuve fitness 15 pi"},
        {"model": "Trainer 19", "dims": (228.0, 94.0, 60.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "H2X Trainer 19 - Double zone avec 4 jets VIP de nage"},
        {"model": "Trainer 18", "dims": (215.0, 94.0, 60.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "H2X Trainer 18 - Cuve d'entraînement 18 pi"},
        {"model": "Trainer 15", "dims": (180.0, 94.0, 60.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "H2X Trainer 15 - Cuve d'entraînement 15 pi"},
        {"model": "Trainer 12", "dims": (144.0, 94.0, 51.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "H2X Trainer 12 - Format compact 12 pi"},
        {"model": "Therapool Deep", "dims": (132.0, 94.0, 60.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "H2X Therapool Deep - Spa d'aquagym et rééducation"},
        {"model": "Therapool SE", "dims": (132.0, 94.0, 51.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "notes": "H2X Therapool SE - Spa d'exercice aquatique standard"}
    ]

    for yr in range(2013, 2027):
        for m in h2x_models:
            if "Challenger" in m["model"] and yr < 2018:
                continue
            gen_id = f"MS-H2X-{m['model'].replace(' ', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Master Spas",
                "model": m["model"],
                "model_normalized": f"master_spas_{m['model'].lower().replace(' ', '_')}_{yr}",
                "series": "H2X Fitness Swim Spas",
                "vintage_year": yr,
                "production_years": "2013-2026",
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
                    "description": "Jets de nage VIP/XP, écran de contrôle Balboa Touch, barres d'exercice inox"
                },
                "spafit_notes": f"Compatible SpaFit Legend Swim Spa Bracket. Longueur {l} po."
            })

    # 3. Legend Series
    legend_models = [
        {"model": "LSX 900", "dims": (108.0, 94.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 8},
        {"model": "LSX 800", "dims": (94.0, 94.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 6},
        {"model": "LSX 700", "dims": (84.0, 84.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 7}
    ]

    for yr in range(2010, 2027):
        for m in legend_models:
            gen_id = f"MS-LEG-{m['model'].replace(' ', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Master Spas",
                "model": m["model"],
                "model_normalized": f"master_spas_{m['model'].lower().replace(' ', '_')}_{yr}",
                "series": "Legend Series",
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
                    "description": "Legend Series bar-top haut de gamme avec cascade Bellagio et couvercle EcoPur"
                },
                "spafit_notes": f"Compatible SpaFit Evolution ou Oasis."
            })

    # 4. Twilight Series
    twilight_models = [
        {"model": "TS 8.2", "dims": (94.0, 94.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 6},
        {"model": "TS 8.3", "dims": (94.0, 94.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 6},
        {"model": "TS 8.25", "dims": (94.0, 94.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 7},
        {"model": "TS 7.2", "dims": (84.0, 84.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 6},
        {"model": "TS 7.25", "dims": (84.0, 84.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 7},
        {"model": "TS 6.2", "dims": (78.0, 78.0, 34.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 5},
        {"model": "TS 240", "dims": (78.0, 78.0, 34.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 3},
        {"model": "TS 87.3", "dims": (94.0, 84.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 6}
    ]

    for yr in range(2010, 2027):
        for m in twilight_models:
            gen_id = f"MS-TS-{m['model'].replace(' ', '_').replace('.', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Master Spas",
                "model": m["model"],
                "model_normalized": f"master_spas_{m['model'].lower().replace(' ', '_').replace('.', '_')}_{yr}",
                "series": "Twilight Series",
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
                    "description": "Twilight bar top avec jets d'épaule StressRelief et cascade"
                },
                "spafit_notes": f"Compatible SpaFit Evolution ou Oasis."
            })

    # 5. Clarity Spas
    clarity_models = [
        {"model": "Balance 8", "dims": (94.0, 94.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 8},
        {"model": "Balance 7", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 7},
        {"model": "Precision 8", "dims": (94.0, 94.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 7},
        {"model": "Precision 7", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 6},
        {"model": "Precision 6", "dims": (78.0, 78.0, 34.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "seats": 4}
    ]

    for yr in range(2012, 2027):
        for m in clarity_models:
            gen_id = f"MS-CLA-{m['model'].replace(' ', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Master Spas",
                "model": m["model"],
                "model_normalized": f"master_spas_{m['model'].lower().replace(' ', '_')}_{yr}",
                "series": "Clarity Spas",
                "vintage_year": yr,
                "production_years": "2012-2026",
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
                    "description": "Clarity bar top standard"
                },
                "spafit_notes": f"Compatible SpaFit Evolution ou Oasis."
            })

    return yearly_data
