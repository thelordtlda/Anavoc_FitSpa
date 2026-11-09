"""
builders_tier3.py
=================
Générateur de spécifications techniques et millésimes pour le Tier 3:
- Cal Spas (Escape, Platinum, Patio & Swim-Pro Swim Spas)
- Artesian Spas & TidalFit Swim Spas
- Marquis Spas & ATV Swim Spas
- Wellis Spas & SwimLine Swim Spas
- Dimension One Spas (D1) & AquaFIT Swim Spas
- Coast Spas (Cascade Infinity Edge & Swim Spas)
"""

from typing import List, Dict, Any

def build_cal_spas_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []

    # Hot Tubs Cal Spas
    models = [
        {"model": "EC-751L", "series": "Escape Series", "dims": (84.0, 84.0, 40.5), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "seats": 6},
        {"model": "EC-751B", "series": "Escape Series", "dims": (84.0, 84.0, 40.5), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "seats": 7},
        {"model": "EC-864L", "series": "Escape Series", "dims": (93.0, 93.0, 40.5), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "seats": 6},
        {"model": "EC-864B", "series": "Escape Series", "dims": (93.0, 93.0, 40.5), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "seats": 7},
        {"model": "PL-881L", "series": "Platinum Series", "dims": (93.0, 93.0, 40.5), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "seats": 6},
        {"model": "PL-881B", "series": "Platinum Series", "dims": (93.0, 93.0, 40.5), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "seats": 7},
        {"model": "PL-760L", "series": "Platinum Series", "dims": (84.0, 84.0, 40.5), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "seats": 6},
        {"model": "PZ-517L", "series": "Patio Series", "dims": (78.0, 78.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "seats": 5},
        {"model": "PZ-525L", "series": "Patio Series", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "seats": 6},
        {"model": "PZ-617T", "series": "Patio Series", "dims": (72.0, 72.0, 34.0), "r": 8.5, "c_type": "Rounded Triangle Corner", "swim": False, "seats": 3},
        # Swim-Pro Swim Spas
        {"model": "Swim-Pro F-1222 Freestyle", "series": "Swim-Pro Series", "dims": (141.0, 93.0, 51.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "seats": 3},
        {"model": "Swim-Pro F-1420 Champion", "series": "Swim-Pro Series", "dims": (168.0, 93.0, 51.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "seats": 3},
        {"model": "Swim-Pro F-1640 Commander", "series": "Swim-Pro Series", "dims": (190.0, 93.0, 51.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "seats": 3},
        {"model": "Swim-Pro F-1770 Olympian", "series": "Swim-Pro Series", "dims": (200.0, 93.0, 51.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "seats": 3}
    ]

    for yr in range(2012, 2027):
        for m in models:
            gen_id = f"CALSPAS-{m['model'].replace(' ', '_').replace('-', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Cal Spas",
                "model": m["model"],
                "model_normalized": f"cal_spas_{m['model'].lower().replace(' ', '_').replace('-', '_')}_{yr}",
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
                    "description": "Cal Spas bar top avec cascade Cascade Waterfall et filtre Bio-Clean"
                },
                "spafit_notes": f"Compatible SpaFit {'Legend Swim Spa' if m['swim'] else 'Oasis/Evolution'}. Longueur {l} po."
            })

    return yearly_data


def build_artesian_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []

    models = [
        # Artesian Elite
        {"model": "Piper Glen", "series": "Artesian Elite", "dims": (91.0, 91.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Pelican Reef", "series": "Artesian Elite", "dims": (108.0, 91.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Dove Canyon", "series": "Artesian Elite", "dims": (91.0, 91.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Eagle Crest", "series": "Artesian Elite", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        # Island Spas
        {"model": "Grand Bahama", "series": "Island Spas", "dims": (91.0, 91.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Grand Cayman", "series": "Island Spas", "dims": (91.0, 91.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Captiva", "series": "Island Spas", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Antigua", "series": "Island Spas", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Santa Cruz", "series": "Island Spas", "dims": (84.0, 61.0, 32.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        # South Seas
        {"model": "South Seas 860L", "series": "South Seas Spas", "dims": (91.0, 91.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "South Seas 748L", "series": "South Seas Spas", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "South Seas 519P", "series": "South Seas Spas", "dims": (78.0, 78.0, 32.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        # TidalFit Swim Spas
        {"model": "TidalFit Active EP-12", "series": "TidalFit Swim Spas", "dims": (144.0, 91.0, 45.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "TidalFit Premium EP-14", "series": "TidalFit Swim Spas", "dims": (168.0, 91.0, 54.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "TidalFit Pro EP-15", "series": "TidalFit Swim Spas", "dims": (180.0, 91.0, 54.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "TidalFit Power EP-16", "series": "TidalFit Swim Spas", "dims": (192.0, 91.0, 54.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "TidalFit Dual Temp DT-19", "series": "TidalFit Swim Spas", "dims": (228.0, 91.0, 54.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "TidalFit Dual Temp DT-21", "series": "TidalFit Swim Spas", "dims": (252.0, 91.0, 54.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True}
    ]

    for yr in range(2012, 2027):
        for m in models:
            gen_id = f"ART-{m['model'].replace(' ', '_').replace('-', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Artesian Spas",
                "model": m["model"],
                "model_normalized": f"artesian_{m['model'].lower().replace(' ', '_').replace('-', '_')}_{yr}",
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
                    "description": "Contrôles individuels DirectFlow sur bar-top et système de filtration ProPure"
                },
                "spafit_notes": f"Compatible SpaFit {'Legend' if m['swim'] else 'Oasis/Evolution'}."
            })

    return yearly_data


def build_marquis_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []

    models = [
        # Crown Collection
        {"model": "The Summit", "series": "Crown Collection", "dims": (94.0, 94.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "The Epic", "series": "Crown Collection", "dims": (90.0, 90.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "The Euphoria", "series": "Crown Collection", "dims": (90.0, 90.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "The Resort", "series": "Crown Collection", "dims": (84.0, 84.0, 34.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "The Promise", "series": "Crown Collection", "dims": (84.0, 84.0, 34.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "The Spirit", "series": "Crown Collection", "dims": (84.0, 66.0, 34.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        # Vector21
        {"model": "V94", "series": "Vector21 Series", "dims": (94.0, 94.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "V94L", "series": "Vector21 Series", "dims": (94.0, 94.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "V84", "series": "Vector21 Series", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "V84L", "series": "Vector21 Series", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "V77L", "series": "Vector21 Series", "dims": (77.0, 77.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "V65L", "series": "Vector21 Series", "dims": (84.0, 65.0, 29.5), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        # ATV Swim Spas
        {"model": "ATV-14 Sport", "series": "ATV Swim Spas", "dims": (168.0, 90.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "ATV-14 Splash", "series": "ATV Swim Spas", "dims": (168.0, 90.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "ATV-17 Sport", "series": "ATV Swim Spas", "dims": (204.0, 90.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "ATV-17 Kona", "series": "ATV Swim Spas", "dims": (204.0, 90.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True}
    ]

    for yr in range(2013, 2027):
        for m in models:
            gen_id = f"MRQ-{m['model'].replace(' ', '_').replace('-', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Marquis Spas",
                "model": m["model"],
                "model_normalized": f"marquis_{m['model'].lower().replace(' ', '_').replace('-', '_')}_{yr}",
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
                    "description": "Marquis Dynamic Flow Control et cascade Jewel"
                },
                "spafit_notes": f"Compatible SpaFit {'Legend' if m['swim'] else 'Oasis/Evolution'}."
            })

    return yearly_data


def build_wellis_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []

    models = [
        # PeakLine
        {"model": "Olympus", "series": "PeakLine", "dims": (140.0, 91.0, 40.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Everest", "series": "PeakLine", "dims": (93.0, 93.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Kilimanjaro", "series": "PeakLine", "dims": (91.0, 91.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Elbrus", "series": "PeakLine", "dims": (86.0, 86.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        # CityLine
        {"model": "Malaga", "series": "CityLine", "dims": (86.0, 86.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Palermo", "series": "CityLine", "dims": (86.0, 86.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        # MyLine
        {"model": "Jupiter", "series": "MyLine", "dims": (79.0, 79.0, 34.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        {"model": "Mars", "series": "MyLine", "dims": (84.0, 63.0, 30.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False},
        # SwimLine
        {"model": "Danube", "series": "SwimLine", "dims": (177.0, 93.0, 58.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "Amazonas", "series": "SwimLine", "dims": (215.0, 91.0, 58.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True},
        {"model": "Rio Grande Dual Temp", "series": "SwimLine", "dims": (236.0, 91.0, 58.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True}
    ]

    for yr in range(2014, 2027):
        for m in models:
            gen_id = f"WEL-{m['model'].replace(' ', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Wellis",
                "model": m["model"],
                "model_normalized": f"wellis_{m['model'].lower().replace(' ', '_')}_{yr}",
                "series": m["series"],
                "vintage_year": yr,
                "production_years": "2014-2026",
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
                    "description": "Châssis composite Poli-Farbe et isolation scandinave"
                },
                "spafit_notes": f"Compatible SpaFit {'Legend' if m['swim'] else 'Oasis/Evolution'}."
            })

    return yearly_data


def build_d1_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []

    models = [
        # Bay Collection (rebord arrière incurvé caractéristique)
        {"model": "Amore Bay", "series": "Bay Collection", "dims": (108.0, 92.0, 40.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "raised": True},
        {"model": "Sarena Bay", "series": "Bay Collection", "dims": (112.0, 92.0, 40.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "raised": True},
        {"model": "Lotus Bay", "series": "Bay Collection", "dims": (91.0, 91.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "raised": True},
        {"model": "Executive", "series": "Bay Collection", "dims": (91.0, 91.0, 38.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "raised": True},
        # Reflections Collection
        {"model": "Chairman", "series": "Reflections Collection", "dims": (92.0, 92.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "raised": False},
        {"model": "Diplomat", "series": "Reflections Collection", "dims": (92.0, 92.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "raised": False},
        {"model": "Nautilus", "series": "Reflections Collection", "dims": (91.0, 91.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "raised": False},
        {"model": "California", "series": "Reflections Collection", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "raised": False},
        {"model": "Aurora", "series": "Reflections Collection", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "raised": False},
        {"model": "Triad", "series": "Reflections Collection", "dims": (84.0, 66.0, 30.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "raised": False},
        # AquaFIT Swim Spas
        {"model": "AquaFIT SPORT", "series": "AquaFIT Series", "dims": (156.0, 90.0, 52.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "raised": False},
        {"model": "AquaFIT PLAY", "series": "AquaFIT Series", "dims": (192.0, 90.0, 52.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "raised": False},
        {"model": "AquaFIT PRO", "series": "AquaFIT Series", "dims": (228.0, 90.0, 52.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "raised": False},
        {"model": "AquaFIT PLUS Dual Temp", "series": "AquaFIT Series", "dims": (228.0, 90.0, 52.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "raised": False}
    ]

    for yr in range(2010, 2027):
        for m in models:
            gen_id = f"D1-{m['model'].replace(' ', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Dimension One Spas",
                "model": m["model"],
                "model_normalized": f"d1_{m['model'].lower().replace(' ', '_')}_{yr}",
                "series": m["series"],
                "vintage_year": yr,
                "production_years": "2010-2026",
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
                    "has_raised_back": m.get("raised", False),
                    "has_curved_waterfall": True,
                    "has_protruding_headrests": True,
                    "has_rigid_filter_lid": True,
                    "description": "Formes bio-ergonomiques D1 et rebord arrière curviligne Bay Series"
                },
                "spafit_notes": f"Compatible SpaFit {'Legend' if m['swim'] else 'Oasis/Evolution'}."
            })

    return yearly_data


def build_coast_spas_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []

    models = [
        # Cascade Series (Infinity Edge / Bord miroir à débordement)
        {"model": "Mirage Curve", "series": "Cascade Series (Infinity Edge)", "dims": (92.0, 92.0, 40.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "infinity": True},
        {"model": "Cascade II", "series": "Cascade Series (Infinity Edge)", "dims": (92.0, 92.0, 40.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "infinity": True},
        {"model": "Horizon", "series": "Cascade Series (Infinity Edge)", "dims": (84.0, 84.0, 40.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "infinity": True},
        # Traditional Series
        {"model": "Apex", "series": "Traditional Series", "dims": (92.0, 92.0, 40.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "infinity": False},
        {"model": "Element", "series": "Traditional Series", "dims": (84.0, 84.0, 40.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "infinity": False},
        {"model": "Radiance", "series": "Traditional Series", "dims": (84.0, 84.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "infinity": False},
        {"model": "Zenith", "series": "Traditional Series", "dims": (80.0, 80.0, 36.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "infinity": False},
        {"model": "Omni", "series": "Traditional Series", "dims": (84.0, 64.0, 30.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": False, "infinity": False},
        # Swim Spas
        {"model": "Swim Collection 1300", "series": "Coast Swim Spas", "dims": (158.0, 90.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "infinity": False},
        {"model": "Swim Collection 1600", "series": "Coast Swim Spas", "dims": (188.0, 90.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "infinity": False},
        {"model": "Swim Collection 1700", "series": "Coast Swim Spas", "dims": (204.0, 90.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "infinity": False},
        {"model": "Swim Collection 2100 Dual Temp", "series": "Coast Swim Spas", "dims": (250.0, 90.0, 53.0), "r": 8.5, "c_type": "Rounded (Rayon 8.5 po)", "swim": True, "infinity": False}
    ]

    for yr in range(2011, 2027):
        for m in models:
            gen_id = f"COAST-{m['model'].replace(' ', '_').upper()}-{yr}"
            l, w, h = m["dims"]
            r = m["r"]
            yearly_data.append({
                "brand": "Coast Spas",
                "model": m["model"],
                "model_normalized": f"coast_{m['model'].lower().replace(' ', '_')}_{yr}",
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
                    "has_raised_back": m.get("infinity", False),
                    "has_curved_waterfall": True,
                    "has_protruding_headrests": True,
                    "has_rigid_filter_lid": True,
                    "description": "Bord miroir Infinity Edge avec bac de débordement arrière ou coque traditionnelle Hydro Cyclonic Filtration"
                },
                "spafit_notes": f"Compatible SpaFit {'Legend' if m['swim'] else 'Oasis/Evolution'}. ATTENTION : bord Infinity Edge nécessite calage SpaFit spécifique."
            })

    return yearly_data
