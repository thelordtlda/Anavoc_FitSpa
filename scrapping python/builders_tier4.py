"""
builders_tier4.py
=================
Générateur de spécifications techniques et millésimes pour le Tier 4 :
- Nordic Hot Tubs (Spas circulaires & rectangulaires)
- Arctic Spas (Spas grand froid & All-Weather Pools / Swim Spas)
- PDC Spas (Spas résidentiels & TruSwim Swim Spas)
- Viking Spas
- Dynasty Spas
- Strong Spas
- Freeflow & Fantasy Spas (Watkins rotomoulés)
- Catalina Spas (Olympic Swim Spas)
- Be Well Canada Spa
- Trévi Spas
"""

from typing import List, Dict, Any

def build_nordic_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []
    models = [
        # Spas ronds circulaires
        {"model": "Crown", "series": "All-Round Series", "dims": (84.0, 84.0, 35.0), "r": 42.0, "c_type": "Circular Round Spa (Diamètre 84 po)", "swim": False},
        {"model": "Impulse", "series": "All-Round Series", "dims": (78.0, 78.0, 31.0), "r": 39.0, "c_type": "Circular Round Spa (Diamètre 78 po)", "swim": False},
        {"model": "Sport", "series": "Sport Series", "dims": (78.0, 78.0, 35.0), "r": 39.0, "c_type": "Circular Round Spa (Diamètre 78 po)", "swim": False},
        {"model": "Stella", "series": "All-Round Series", "dims": (84.0, 62.0, 34.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        # Classic / Luxury
        {"model": "Encore", "series": "Luxury Series", "dims": (84.0, 84.0, 35.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Jubilee", "series": "Luxury Series", "dims": (84.0, 84.0, 35.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Retreat", "series": "Modern Series", "dims": (80.0, 70.0, 34.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Escape", "series": "Classic Series", "dims": (80.0, 80.0, 35.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False}
    ]
    for yr in range(2012, 2027):
        for m in models:
            gen_id = f"NOR-{m['model'].upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Nordic Hot Tubs",
                "model": m["model"],
                "model_normalized": f"nordic_{m['model'].lower()}_{yr}",
                "series": m["series"],
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
                    "has_curved_waterfall": False,
                    "has_protruding_headrests": False,
                    "has_rigid_filter_lid": True,
                    "description": "Cuve rotomoulée Nordic Star ou acrylique ronde avec tourbillon central DTS"
                },
                "spafit_notes": f"Compatible SpaFit Oasis ou Horizon. Forme ronde R={r} po."
            })
    return yearly_data


def build_arctic_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []
    models = [
        # Spas résidentiels Custom
        {"model": "Summit", "series": "Custom Series", "dims": (93.0, 93.0, 39.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Legend", "series": "Custom Series", "dims": (90.0, 90.0, 39.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Kodiak", "series": "Custom Series", "dims": (93.0, 93.0, 39.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Klondiker", "series": "Custom Series", "dims": (86.0, 86.0, 39.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Tundra", "series": "Custom Series", "dims": (93.0, 93.0, 39.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Cub", "series": "Core Series", "dims": (86.0, 69.0, 39.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        # All-Weather Pools / Swim Spas
        {"model": "All-Weather Pool Okanagan", "series": "All-Weather Pools", "dims": (174.0, 93.0, 51.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "All-Weather Pool Ocean", "series": "All-Weather Pools", "dims": (204.0, 93.0, 51.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "All-Weather Pool Hudson", "series": "All-Weather Pools", "dims": (174.0, 93.0, 51.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "All-Weather Pool Kingston", "series": "All-Weather Pools", "dims": (204.0, 93.0, 51.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True}
    ]
    for yr in range(2011, 2027):
        for m in models:
            gen_id = f"ARC-{m['model'].replace(' ', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Arctic Spas",
                "model": m["model"],
                "model_normalized": f"arctic_{m['model'].lower().replace(' ', '_')}_{yr}",
                "series": m["series"],
                "vintage_year": yr,
                "production_years": "2011-2026",
                "generation_id": gen_id,
                "is_swim_spa": m["swim"],
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
                    "description": "Meuble en cèdre rouge massif Western Red Cedar ou No-Maintenance composite FreeHeat"
                },
                "spafit_notes": f"Compatible SpaFit {'Legend' if m['swim'] else 'Oasis/Evolution'}."
            })
    return yearly_data


def build_pdc_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []
    models = [
        # Spas
        {"model": "Biscayne", "series": "Luxury Series", "dims": (92.0, 92.0, 39.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Bali", "series": "Luxury Series", "dims": (92.0, 92.0, 39.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Aruba", "series": "Premium Series", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Fiji", "series": "Premium Series", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        # TruSwim Swim Spas
        {"model": "TruSwim TSX17", "series": "TruSwim Series", "dims": (204.0, 92.0, 56.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "TruSwim TSX19", "series": "TruSwim Series", "dims": (227.0, 92.0, 56.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "TruSwim TSX21 Dual Temp", "series": "TruSwim Series", "dims": (252.0, 92.0, 56.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        # Synergy
        {"model": "Synergy FX15", "series": "Synergy Series", "dims": (180.0, 92.0, 56.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "Synergy FX17", "series": "Synergy Series", "dims": (204.0, 92.0, 56.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True}
    ]
    for yr in range(2013, 2027):
        for m in models:
            gen_id = f"PDC-{m['model'].replace(' ', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "PDC Spas",
                "model": m["model"],
                "model_normalized": f"pdc_{m['model'].lower().replace(' ', '_')}_{yr}",
                "series": m["series"],
                "vintage_year": yr,
                "production_years": "2013-2026",
                "generation_id": gen_id,
                "is_swim_spa": m["swim"],
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
                    "description": "Technologie de nage hydraulique à hélice TruSwim sans turbulences"
                },
                "spafit_notes": f"Compatible SpaFit {'Legend' if m['swim'] else 'Oasis/Evolution'}."
            })
    return yearly_data


def build_viking_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []
    models = [
        {"model": "Heritage", "series": "Heritage Series", "dims": (86.0, 86.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Tradition", "series": "Tradition Series", "dims": (86.0, 86.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Royale", "series": "Royale Series", "dims": (78.0, 78.0, 34.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Aurora", "series": "Aurora Series", "dims": (84.0, 60.0, 34.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Viking 3", "series": "Viking Series", "dims": (72.0, 72.0, 35.0), "r": 36.0, "c_type": "Circular Round Spa (Diamètre 72 po)", "swim": False}
    ]
    for yr in range(2012, 2027):
        for m in models:
            gen_id = f"VIK-{m['model'].upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Viking Spas",
                "model": m["model"],
                "model_normalized": f"viking_{m['model'].lower().replace(' ', '_')}_{yr}",
                "series": m["series"],
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
                    "description": "Coque Soft-Touch antidérapante brevetée"
                },
                "spafit_notes": f"Compatible SpaFit Oasis ou Evolution."
            })
    return yearly_data


def build_trevi_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []
    models = [
        {"model": "Dynastie", "series": "Collection Prestige", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Signature 800", "series": "Collection Signature", "dims": (92.0, 92.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Signature 700", "series": "Collection Signature", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Prestige 500", "series": "Collection Prestige", "dims": (78.0, 78.0, 35.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Exercice 14", "series": "Spas de Nage Trévi", "dims": (168.0, 90.0, 52.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "Exercice 16", "series": "Spas de Nage Trévi", "dims": (192.0, 90.0, 52.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "Exercice 19 Dual Temp", "series": "Spas de Nage Trévi", "dims": (228.0, 90.0, 52.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True}
    ]
    for yr in range(2012, 2027):
        for m in models:
            gen_id = f"TRV-{m['model'].replace(' ', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Trévi Spas",
                "model": m["model"],
                "model_normalized": f"trevi_{m['model'].lower().replace(' ', '_')}_{yr}",
                "series": m["series"],
                "vintage_year": yr,
                "production_years": "2012-2026",
                "generation_id": gen_id,
                "is_swim_spa": m["swim"],
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
                    "description": "Fabrication québécoise Trévi adaptée aux hivers rigoureux"
                },
                "spafit_notes": f"Compatible SpaFit {'Legend' if m['swim'] else 'Oasis/Evolution'}."
            })
    return yearly_data
