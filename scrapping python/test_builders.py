import json
from pathlib import Path

def test_sundance():
    yearly_data = []
    # 980 Series (2017-2026)
    m980 = {
        "Kingston": {"len": 100.0, "wid": 92.0, "ht": 34.0, "lounge": False},
        "Claremont": {"len": 100.0, "wid": 92.0, "ht": 34.0, "lounge": True},
        "Lisbon": {"len": 89.0, "wid": 89.0, "ht": 34.0, "lounge": True},
        "Odessa": {"len": 89.0, "wid": 89.0, "ht": 34.0, "lounge": False},
    }
    for m, d in m980.items():
        for yr in range(2017, 2027):
            yearly_data.append({
                "brand": "Sundance Spas", "model": m, "series": "980 Series", "year": yr, "gen": "gen1",
                "len_in": d["len"], "wid_in": d["wid"], "ht_in": d["ht"], "rad_in": 11.0,
                "corner_type": "Wide Radius (Rayon large 11 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": f"{yr}_Sundance_Pre-Delivery-Guide.pdf" if yr >= 2024 else f"{yr}_Sundance_980-Series.pdf",
                "notes": f"Modèle haut de gamme Sundance 980 {m}. Rayon de coin large R=11 po avec SunCooler intégré. Nécessite supports SpaFit R=11 po."
            })

    # 880 Series (2010-2026) - Rayon large R=11 po
    m880 = {
        "Aspen": {"len": 110.0, "wid": 89.0, "ht": 41.5, "start": 2012},
        "Maxxus": {"len": 110.0, "wid": 89.0, "ht": 41.5},
        "Cameo": {"len": 89.0, "wid": 89.0, "ht": 37.5},
        "Optima": {"len": 89.0, "wid": 89.0, "ht": 37.5},
        "Altamar": {"len": 86.0, "wid": 86.0, "ht": 37.5},
        "Marin": {"len": 91.0, "wid": 76.0, "ht": 34.0},
        "Capri": {"len": 82.0, "wid": 69.0, "ht": 30.5},
    }
    for m, d in m880.items():
        start_yr = d.get("start", 2010)
        for yr in range(start_yr, 2027):
            yearly_data.append({
                "brand": "Sundance Spas", "model": m, "series": "880 Series", "year": yr, "gen": "gen2" if yr >= 2018 else "gen1",
                "len_in": d["len"], "wid_in": d["wid"], "ht_in": d["ht"], "rad_in": 11.0,
                "corner_type": "Wide Radius (Rayon large 11 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": f"{yr}_Sundance_880-Series.pdf" if yr in [2016, 2018, 2020, 2024, 2026] else "2026_Sundance_Pre-Delivery-Guide.pdf",
                "notes": f"Sundance 880 {m} signature. Rayon de courbure large R=11 po. Équipé de jets Fluidix. Compatible SpaFit kit R=11 po."
            })

    # 780 Series (2010-2026)
    m780 = {
        "Chelsee": {"len": 89.0, "wid": 89.0, "ht": 37.5, "rad": 11.0},
        "Hamilton": {"len": 89.0, "wid": 89.0, "ht": 37.5, "rad": 11.0},
        "Bristol": {"len": 84.0, "wid": 84.0, "ht": 36.0, "rad": 11.0, "start": 2017},
        "Hanover": {"len": 84.0, "wid": 84.0, "ht": 36.0, "rad": 11.0, "start": 2017},
        "Montclair": {"len": 91.0, "wid": 75.0, "ht": 34.5, "rad": 11.0, "start": 2013},
        "Dover": {"len": 82.0, "wid": 69.0, "ht": 30.5, "rad": 11.0},
    }
    for m, d in m780.items():
        start_yr = d.get("start", 2010)
        for yr in range(start_yr, 2027):
            rad = d["rad"] if yr >= 2017 else 8.5
            yearly_data.append({
                "brand": "Sundance Spas", "model": m, "series": "780 Series", "year": yr, "gen": "gen2" if yr >= 2017 else "gen1",
                "len_in": d["len"], "wid_in": d["wid"], "ht_in": d["ht"], "rad_in": rad,
                "corner_type": f"Wide Radius (Rayon {rad} po)",
                "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": f"{yr}_Sundance_780-Series.pdf" if yr in [2016, 2018, 2020, 2024, 2026] else "2026_Sundance_Pre-Delivery-Guide.pdf",
                "notes": f"Modèle Sundance 780 {m}. Rayon {rad} po. Bar top plat sans saillie bloquante pour SpaFit."
            })

    # 680 Series (2010-2026) - Rayon standard R=8.5 po
    m680 = {
        "McKinley": {"len": 89.0, "wid": 89.0, "ht": 36.0, "start": 2015},
        "Ramona": {"len": 89.0, "wid": 89.0, "ht": 36.0, "start": 2015},
        "Edison": {"len": 84.0, "wid": 84.0, "ht": 36.0, "start": 2013},
        "Peyton": {"len": 84.0, "wid": 84.0, "ht": 36.0, "start": 2013},
        "Prado": {"len": 80.0, "wid": 80.0, "ht": 33.0, "start": 2016},
        "Alicia": {"len": 76.0, "wid": 66.0, "ht": 32.0, "start": 2019},
        "Denali": {"len": 79.0, "wid": 79.0, "ht": 36.0, "rad": 39.5, "type": "Round (Spa Rond Diamètre 79 po)"},
        "Tacoma": {"len": 68.0, "wid": 68.0, "ht": 31.0, "rad": 8.5, "type": "Triangle (Spa d'angle triangulaire 68x68 po)"},
    }
    for m, d in m680.items():
        start_yr = d.get("start", 2010)
        for yr in range(start_yr, 2027):
            rad = d.get("rad", 8.5)
            ctype = d.get("type", "Rounded (Rayon standard 8.5 po)")
            yearly_data.append({
                "brand": "Sundance Spas", "model": m, "series": "680 Series", "year": yr, "gen": "gen1",
                "len_in": d["len"], "wid_in": d["wid"], "ht_in": d["ht"], "rad_in": rad,
                "corner_type": ctype,
                "jetpaks": 0, "raised_back": False, "waterfall": False if m in ["Denali", "Tacoma"] else True,
                "keypad": True, "filter": True,
                "manual": f"{yr}_Sundance_680-Series.pdf" if yr in [2016, 2018, 2020, 2024, 2026] else "2026_Sundance_Pre-Delivery-Guide.pdf",
                "notes": f"Modèle Sundance 680 {m}. {ctype}. Compatible SpaFit standard."
            })

    # Select Series (2011-2020)
    mselect = {
        "Constance": {"len": 87.0, "wid": 87.0, "ht": 36.0},
        "Victoria": {"len": 87.0, "wid": 87.0, "ht": 36.0},
    }
    for m, d in mselect.items():
        for yr in range(2011, 2021):
            yearly_data.append({
                "brand": "Sundance Spas", "model": m, "series": "Select Series", "year": yr, "gen": "gen1",
                "len_in": d["len"], "wid_in": d["wid"], "ht_in": d["ht"], "rad_in": 5.5,
                "corner_type": "Tight Radius (Rayon serré 5.5 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": "2018_Sundance_Select-Series.pdf",
                "notes": f"Sundance Select {m} format contemporain à rayon serré 5.5 po."
            })

    # Splash Series (2020-2026)
    msplash = {
        "Berkeley": {"len": 78.0, "wid": 78.0, "ht": 36.0},
        "Brook": {"len": 78.0, "wid": 68.0, "ht": 32.0},
    }
    for m, d in msplash.items():
        for yr in range(2020, 2027):
            yearly_data.append({
                "brand": "Sundance Spas", "model": m, "series": "Splash Series", "year": yr, "gen": "gen1",
                "len_in": d["len"], "wid_in": d["wid"], "ht_in": d["ht"], "rad_in": 8.0,
                "corner_type": "Rounded (Rayon 8 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": False, "keypad": True, "filter": True,
                "manual": "2023_Sundance_Splash-Series.pdf",
                "notes": f"Sundance Splash {m} rotomoulé / value plug and play. Rayon 8 po."
            })

    # Swim Spas (2021-2026)
    mswim = {
        "13 Stream": {"len": 156.0, "wid": 93.0, "ht": 53.0},
        "17 Stream": {"len": 210.0, "wid": 93.0, "ht": 53.0},
        "17 Surf": {"len": 210.0, "wid": 93.0, "ht": 53.0},
    }
    for m, d in mswim.items():
        for yr in range(2021, 2027):
            yearly_data.append({
                "brand": "Sundance Spas", "model": m, "series": "Swim Spa Series", "year": yr, "gen": "gen1",
                "len_in": d["len"], "wid_in": d["wid"], "ht_in": d["ht"], "rad_in": 8.5,
                "corner_type": "Rounded (Rayon 8.5 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": f"{yr}_Sundance_Swim-Spas.pdf",
                "notes": f"Spa de nage Sundance {m}. Dimensions {d['len']}x{d['wid']} po. Conçu pour SpaFit Swim Spa."
            })

    print(f"Sundance Spas total records: {len(yearly_data)}")
    return yearly_data

def test_awp():
    yearly_data = []
    # Hot Tubs (2018-2026)
    awp_models = {
        "982": {"len": 133.0, "wid": 91.0, "ht": 38.0, "series": "800/900 Series", "notes": "Grand spa 982 double/quadruple lounge 133x91 po."},
        "881": {"len": 92.0, "wid": 92.0, "ht": 38.0, "series": "800/900 Series", "notes": "Modèle 881 grand format avec chaise longue ergonomique."},
        "880": {"len": 92.0, "wid": 92.0, "ht": 38.0, "series": "800/900 Series", "notes": "Modèle 880 places ouvertes 92x92 po convivial."},
        "481": {"len": 91.5, "wid": 91.5, "ht": 38.0, "series": "400 Series", "notes": "Modèle 481 6 places avec lounge et appuie-têtes confort."},
        "480": {"len": 91.5, "wid": 91.5, "ht": 38.0, "series": "400 Series", "notes": "Modèle 480 6 places ouvertes 91.5x91.5 po."},
        "472": {"len": 87.0, "wid": 87.0, "ht": 38.0, "series": "400 Series", "notes": "Modèle 472 double chaise longue face à face."},
        "471": {"len": 87.0, "wid": 87.0, "ht": 38.0, "series": "400 Series", "notes": "Modèle 471 5-6 places avec lounge ergonomique."},
        "470": {"len": 87.0, "wid": 87.0, "ht": 38.0, "series": "400 Series", "notes": "Modèle 470 6-7 places assises ouvertes 87x87 po."},
        "461": {"len": 82.0, "wid": 69.5, "ht": 35.0, "series": "400 Series", "notes": "Modèle 461 compact 4 places avec lounge."},
        "460": {"len": 82.0, "wid": 69.5, "ht": 35.0, "series": "400 Series", "notes": "Modèle 460 compact 4-5 places assises."},
        "451": {"len": 81.0, "wid": 64.0, "ht": 31.0, "series": "400 Series", "notes": "Modèle patio 451 3 places (1 lounge + 2 sièges)."},
        "282": {"len": 92.0, "wid": 92.0, "ht": 38.0, "series": "200 Series", "notes": "Série 200 modèle 282 double lounge."},
        "281": {"len": 92.0, "wid": 92.0, "ht": 38.0, "series": "200 Series", "notes": "Série 200 modèle 281 lounge 92x92 po."},
        "280": {"len": 92.0, "wid": 92.0, "ht": 38.0, "series": "200 Series", "notes": "Série 200 modèle 280 assises ouvertes."},
        "271": {"len": 83.0, "wid": 83.0, "ht": 38.0, "series": "200 Series", "notes": "Série 200 modèle 271 format 7 pieds avec lounge."},
        "270": {"len": 83.0, "wid": 83.0, "ht": 38.0, "series": "200 Series", "notes": "Série 200 modèle 270 format 7 pieds ouvert."},
        "261": {"len": 72.0, "wid": 72.0, "ht": 32.0, "series": "200 Series", "notes": "Modèle 261 carré compact 6 pieds."},
        "250": {"len": 83.0, "wid": 63.0, "ht": 31.0, "series": "200 Series", "notes": "Modèle 250 rectangulaire patio."},
        "171": {"len": 83.0, "wid": 83.0, "ht": 38.0, "series": "100 Series", "notes": "Série 100 modèle 171 format 7 pieds d'entrée de gamme."},
        "160": {"len": 71.0, "wid": 71.0, "ht": 32.0, "series": "100 Series", "notes": "Série 100 modèle 160 carré 71x71 po."},
        "151": {"len": 83.0, "wid": 63.0, "ht": 31.0, "series": "100 Series", "notes": "Série 100 modèle 151 3 places avec lounge."},
        "101": {"len": 86.0, "wid": 50.0, "ht": 29.5, "series": "100 Series", "notes": "Modèle 101 compact 2 places tête-à-tête."},
    }
    for m, d in awp_models.items():
        for yr in range(2018, 2027):
            yearly_data.append({
                "brand": "American Whirlpool", "model": m, "series": d["series"], "year": yr, "gen": "gen1",
                "len_in": d["len"], "wid_in": d["wid"], "ht_in": d["ht"], "rad_in": 8.5,
                "corner_type": "Rounded (Rayon 8.5 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": f"2022-American-Whirlpool-{d['series'].split()[0]}-Series-Owners-Manual.pdf",
                "notes": f"American Whirlpool {m}. {d['notes']} Rayon 8.5 po. Compatible SpaFit standard."
            })

    # Swim Spas (2018-2026)
    awp_swims = {
        "DM8": {"len": 218.0, "wid": 90.0, "ht": 53.0, "notes": "Spa de nage 18 pieds bi-zone (nage + spa séparé) DM8."},
        "MX6": {"len": 190.0, "wid": 90.0, "ht": 60.0, "notes": "Spa de nage 16 pieds profond MX6 (60 po de hauteur)."},
        "MX5": {"len": 180.0, "wid": 90.0, "ht": 60.0, "notes": "Spa de nage 15 pieds profond MX5."},
        "RL5": {"len": 180.0, "wid": 90.0, "ht": 60.0, "notes": "Spa de nage 15 pieds d'entraînement RL5."},
        "MB4": {"len": 168.0, "wid": 90.0, "ht": 50.0, "notes": "Spa de nage 14 pieds MB4."},
        "ML4": {"len": 168.0, "wid": 90.0, "ht": 50.0, "notes": "Spa de nage 14 pieds ML4 avec zone de relaxation."},
        "RB4": {"len": 168.0, "wid": 90.0, "ht": 50.0, "notes": "Spa de nage 14 pieds RB4."},
        "RL4": {"len": 168.0, "wid": 90.0, "ht": 50.0, "notes": "Spa de nage 14 pieds RL4."},
        "RF2": {"len": 146.0, "wid": 90.0, "ht": 50.0, "notes": "Spa de nage compact fitness 12 pieds RF2."},
    }
    for m, d in awp_swims.items():
        for yr in range(2018, 2027):
            yearly_data.append({
                "brand": "American Whirlpool", "model": m, "series": "Swim Spa Series", "year": yr, "gen": "gen1",
                "len_in": d["len"], "wid_in": d["wid"], "ht_in": d["ht"], "rad_in": 8.5,
                "corner_type": "Rounded (Rayon 8.5 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": "2022-American-Whirlpool-Swim-Spa-Series-Owners-Manual.pdf",
                "notes": f"Spa de nage American Whirlpool {m}. {d['notes']} Compatible SpaFit Swim Spa."
            })

    print(f"American Whirlpool total records: {len(yearly_data)}")
    return yearly_data

def test_maax():
    yearly_data = []
    # MAAX Spas Models (2010-2026)
    maax_models = {
        "811": {"len": 92.0, "wid": 92.0, "ht": 38.0, "series": "MAAX Elite / 800", "notes": "Spa grand format 811 avec chaise longue."},
        "781": {"len": 91.5, "wid": 91.5, "ht": 38.0, "series": "MAAX 700 Series", "notes": "Modèle 781 6 places avec lounge."},
        "780": {"len": 91.5, "wid": 91.5, "ht": 38.0, "series": "MAAX 700 Series", "notes": "Modèle 780 6 places ouvertes 91.5x91.5 po."},
        "581": {"len": 92.0, "wid": 92.0, "ht": 38.0, "series": "MAAX 500 Series", "notes": "Modèle 581 92x92 po avec lounge.", "start": 2012},
        "571": {"len": 87.0, "wid": 87.0, "ht": 38.0, "series": "MAAX 500 Series", "notes": "Modèle 571 87x87 po avec lounge.", "start": 2012},
        "481": {"len": 91.5, "wid": 91.5, "ht": 38.0, "series": "MAAX 400 Series", "notes": "Modèle 481 6 places avec lounge."},
        "480": {"len": 91.5, "wid": 91.5, "ht": 38.0, "series": "MAAX 400 Series", "notes": "Modèle 480 6 places ouvertes."},
        "471": {"len": 87.0, "wid": 87.0, "ht": 38.0, "series": "MAAX 400 Series", "notes": "Modèle 471 5-6 places avec lounge."},
        "470": {"len": 87.0, "wid": 87.0, "ht": 38.0, "series": "MAAX 400 Series", "notes": "Modèle 470 assises ouvertes."},
        "461": {"len": 82.0, "wid": 69.5, "ht": 35.0, "series": "MAAX 400 Series", "notes": "Modèle compact 461 avec lounge."},
        "460": {"len": 82.0, "wid": 69.5, "ht": 35.0, "series": "MAAX 400 Series", "notes": "Modèle compact 460 assises ouvertes."},
        "451": {"len": 81.0, "wid": 64.0, "ht": 31.0, "series": "MAAX 400 Series", "notes": "Modèle patio 451 3 places."},
        "311": {"len": 83.0, "wid": 83.0, "ht": 38.0, "series": "MAAX 300 Series", "notes": "Modèle 311 7 pieds avec lounge.", "start": 2012},
        "271": {"len": 83.0, "wid": 83.0, "ht": 38.0, "series": "MAAX 200 Series", "notes": "Modèle 271 7 pieds avec lounge."},
        "270": {"len": 83.0, "wid": 83.0, "ht": 38.0, "series": "MAAX 200 Series", "notes": "Modèle 270 7 pieds assises ouvertes."},
        "261": {"len": 72.0, "wid": 72.0, "ht": 32.0, "series": "MAAX 200 Series", "notes": "Modèle 261 carré 6 pieds."},
        "250": {"len": 83.0, "wid": 63.0, "ht": 31.0, "series": "MAAX 200 Series", "notes": "Modèle 250 rectangulaire patio."},
        "171": {"len": 83.0, "wid": 83.0, "ht": 38.0, "series": "MAAX 100 Series", "notes": "Modèle 171 entrée de gamme 7 pieds.", "start": 2012},
        "160": {"len": 71.0, "wid": 71.0, "ht": 32.0, "series": "MAAX 100 Series", "notes": "Modèle 160 compact carré.", "start": 2012},
        "151": {"len": 83.0, "wid": 63.0, "ht": 31.0, "series": "MAAX 100 Series", "notes": "Modèle 151 3 places patio."},
        "101": {"len": 86.0, "wid": 50.0, "ht": 29.5, "series": "MAAX 100 Series", "notes": "Modèle 101 tête-à-tête 2 places."},
    }
    for m, d in maax_models.items():
        start_yr = d.get("start", 2010)
        for yr in range(start_yr, 2027):
            yearly_data.append({
                "brand": "MAAX Spas", "model": m, "series": d["series"], "year": yr, "gen": "gen1",
                "len_in": d["len"], "wid_in": d["wid"], "ht_in": d["ht"], "rad_in": 8.5,
                "corner_type": "Rounded (Rayon 8.5 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": "AW-2018-Owner-Manual-2.pdf" if yr <= 2018 else "2022-American-Whirlpool-400-Series-Owners-Manual.pdf",
                "notes": f"MAAX Spas / Coleman {m}. {d['notes']} Rayon 8.5 po. Compatible SpaFit standard."
            })

    # PowerPool Swim Spas (2014-2026)
    powerpool_swims = {
        "PowerPool DM8": {"len": 218.0, "wid": 90.0, "ht": 53.0, "notes": "Spa de nage bi-zone 18 pieds PowerPool DM8."},
        "PowerPool MX6": {"len": 190.0, "wid": 90.0, "ht": 60.0, "notes": "Spa de nage 16 pieds profond PowerPool MX6."},
        "PowerPool ML4": {"len": 168.0, "wid": 90.0, "ht": 50.0, "notes": "Spa de nage 14 pieds PowerPool ML4."},
        "PowerPool RL4": {"len": 168.0, "wid": 90.0, "ht": 50.0, "notes": "Spa de nage 14 pieds PowerPool RL4."},
        "PowerPool SuperSport": {"len": 168.0, "wid": 90.0, "ht": 50.0, "notes": "Spa de nage PowerPool SuperSport 14 pieds."},
    }
    for m, d in powerpool_swims.items():
        for yr in range(2014, 2027):
            yearly_data.append({
                "brand": "MAAX Spas", "model": m, "series": "PowerPool Series", "year": yr, "gen": "gen1",
                "len_in": d["len"], "wid_in": d["wid"], "ht_in": d["ht"], "rad_in": 8.5,
                "corner_type": "Rounded (Rayon 8.5 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": "2022-American-Whirlpool-Swim-Spa-Series-Owners-Manual.pdf",
                "notes": f"Spa de nage MAAX {m}. {d['notes']} Compatible SpaFit Swim Spa."
            })

    print(f"MAAX Spas total records: {len(yearly_data)}")
    return yearly_data

test_sundance()
test_awp()
test_maax()

