"""
brands_catalog.py
=================
Registre unifié et exhaustif des manufacturiers de spas et spas de nage mondiaux
pour le pipeline d'extraction, d'explosion millésime par millésime (2010-2026)
et de dimensionnement SpaFit Cover Sizer.
"""

from typing import List, Dict, Any

SPA_MANUFACTURERS_REGISTRY: List[Dict[str, Any]] = [
    # =========================================================================
    # TIER 1 : DÉJÀ EXÉCUTÉS & CONSOLIDÉS À 100% (1 894 fiches)
    # =========================================================================
    {
        "id": "bullfrog_spas",
        "name": "Bullfrog Spas",
        "parent_group": "Bullfrog International",
        "country": "USA",
        "status": "COMPLETED",
        "record_count": 340,
        "spa_series": ["M Series", "A Series", "R Series", "X Series", "STIL", "Classic Series"],
        "swim_spa_series": ["Swim Series (S150, S180, S180XD, S200)"],
        "spafit_key_factors": "Changement de rayon M9 (8 po -> 1.1 po carré en 2023), cassettes JetPaks amovibles, STIL rayon 2.5 po."
    },
    {
        "id": "jacuzzi",
        "name": "Jacuzzi",
        "parent_group": "Jacuzzi Brands LLC",
        "country": "USA / Global",
        "status": "COMPLETED",
        "record_count": 464,
        "spa_series": ["J-500", "J-400", "J-LX / J-LXL", "J-300", "J-200", "Play Collection"],
        "swim_spa_series": ["Swim Spa Collection (J-13 PowerPlay, J-16 PowerActive, J-19 PowerPro)"],
        "spafit_key_factors": "Rebord arrière surélevé (Raised Back J-400/J-500), coins carrés inox J-LX (R=0.5 po), J-210 rond (R=39 po)."
    },
    {
        "id": "sundance_spas",
        "name": "Sundance Spas",
        "parent_group": "Jacuzzi Brands LLC",
        "country": "USA / Global",
        "status": "COMPLETED",
        "record_count": 399,
        "spa_series": ["980 Series", "880 Series", "780 Series", "680 Series", "Select Series", "Splash Series"],
        "swim_spa_series": ["Swim Spas (13 Stream, 17 Stream, 17 Surf)"],
        "spafit_key_factors": "Larges rayons R=11 po sur 880/980, cascade bombée, Denali rond (R=39.5 po), Tacoma triangulaire."
    },
    {
        "id": "american_whirlpool",
        "name": "American Whirlpool",
        "parent_group": "MAAX Spas Industries",
        "country": "USA",
        "status": "COMPLETED",
        "record_count": 279,
        "spa_series": ["800 Series", "400 Series", "200 Series", "100 Series", "982"],
        "swim_spa_series": ["Swim Spas (DM8, MX6, MX5, RL5, MB4, ML4, RB4, RL4, RF2)"],
        "spafit_key_factors": "Rayon standard R=8.5 po, profil acrylique Zone Therapy, couvercles de filtres affleurants."
    },
    {
        "id": "maax_spas",
        "name": "MAAX Spas",
        "parent_group": "MAAX Spas Industries (incl. Coleman Spas)",
        "country": "USA / Canada",
        "status": "COMPLETED",
        "record_count": 412,
        "spa_series": ["800 Series", "700 Series", "500 Series", "400 Series", "300 Series", "200 Series", "100 Series"],
        "swim_spa_series": ["PowerPool (DM8, MX6, ML4, RL4, SuperSport)"],
        "spafit_key_factors": "Plateformes communes Coleman/MAAX, châssis acier DuraMaax, couvercles à large bordure."
    },

    # =========================================================================
    # TIER 2 : LEADERS MONDIAUX IMMÉDIATS (WATKINS WELLNESS, MASTER SPAS, HYDROPOOL)
    # =========================================================================
    {
        "id": "hot_spring_spas",
        "name": "Hot Spring Spas",
        "parent_group": "Watkins Wellness (Masco Corp)",
        "country": "USA / Global",
        "status": "COMPLETED",
        "spa_series": ["Highlife Collection", "Limelight Collection", "Hot Spot Collection"],
        "swim_spa_series": [],
        "spafit_key_factors": "Design BMW Designworks sur Highlife avec rebord bar-top profilé non plat, Moto-Massage DX, R=8 po."
    },
    {
        "id": "caldera_spas",
        "name": "Caldera Spas",
        "parent_group": "Watkins Wellness (Masco Corp)",
        "country": "USA / Global",
        "status": "COMPLETED",
        "spa_series": ["Utopia Series", "Paradise Series", "Vacanza Series"],
        "swim_spa_series": [],
        "spafit_key_factors": "Rebord Avante all-weather cabinet, cascade Acquarella, assise Euphoria, R=8 po."
    },
    {
        "id": "endless_pools",
        "name": "Endless Pools",
        "parent_group": "Watkins Wellness (Masco Corp)",
        "country": "USA / Global",
        "status": "COMPLETED",
        "spa_series": [],
        "swim_spa_series": [
            "Fitness Systems (E500, E550, E700, E2000)",
            "SwimCross Exercise Systems (X500, X2000)",
            "RecSport Recreation Systems (R200, R500)"
        ],
        "spafit_key_factors": "Leaders mondiaux de spas de nage à turbine hydraulique. Spas doubles zones (E2000, X2000) de 20 pi nécessitant SpaFit Legend."
    },
    {
        "id": "master_spas",
        "name": "Master Spas",
        "parent_group": "Master Spas Inc.",
        "country": "USA / Global",
        "status": "COMPLETED",
        "spa_series": ["Legend Series (LSX)", "Twilight Series (TS)", "Clarity Spas", "Healthy Living Spas"],
        "swim_spa_series": [
            "Michael Phelps Signature Swim Spas (MP Momentum, MP Signature, MP Force)",
            "H2X Fitness Swim Spas (Challenger 15D/18D/19D, Trainer 15/18/19, Therapool Deep/SE)"
        ],
        "spafit_key_factors": "Plus grand manufacturier indépendant. Vagues de propulsion Wave XP, spas doubles bassins MP Momentum (231 po)."
    },
    {
        "id": "hydropool",
        "name": "Hydropool Hot Tubs & Swim Spas",
        "parent_group": "Jacuzzi Brands LLC",
        "country": "Canada / Global",
        "status": "COMPLETED",
        "spa_series": ["Self-Cleaning Series (395 à 970)", "Serenity Series (4300 à 6900)"],
        "swim_spa_series": [
            "AquaPlay (14AX)",
            "AquaSport (14AX, 17AX, 19AX)",
            "AquaTrainer (14AX, 17AX, 19AX)",
            "Executive (16EX, 19EX)"
        ],
        "spafit_key_factors": "Cuve autonettoyante avec aspiration de surface et fond brevetée, coque arrondie R=8.5 po."
    },

    # =========================================================================
    # TIER 3 : AUTRES FABRICANTS NORD-AMÉRICAINS & INTERNATIONAUX MAJEURS
    # =========================================================================
    {
        "id": "cal_spas",
        "name": "Cal Spas",
        "parent_group": "California Acrylic Industries",
        "country": "USA",
        "status": "COMPLETED",
        "spa_series": ["Escape Series", "Platinum Series", "Patio Series", "Special Edition"],
        "swim_spa_series": ["Swim-Pro (F-1222, F-1420, F-1640, F-1770, Champion, Commander, Olympian)"],
        "spafit_key_factors": "Énorme catalogue de plus de 40 modèles, cascades Waterfall Cascade et jets Tornado."
    },
    {
        "id": "artesian_spas",
        "name": "Artesian Spas",
        "parent_group": "May Manufacturing / Artesian Spas",
        "country": "USA",
        "status": "COMPLETED",
        "spa_series": ["Artesian Elite", "Island Spas", "South Seas Spas", "Garden Spas"],
        "swim_spa_series": ["TidalFit Swim Spas (Active Plus, Premium, Pro, Power, Dual Temp)"],
        "spafit_key_factors": "Système de contrôle DirectFlow individuel sur le bar top, spas de nage TidalFit jusqu'à 21 pi."
    },
    {
        "id": "marquis_spas",
        "name": "Marquis Spas",
        "parent_group": "Monomoy Capital Partners / Marquis Corp.",
        "country": "USA",
        "status": "COMPLETED",
        "spa_series": ["The Crown Collection", "Signature Series", "Vector21 Series", "Celebrity Series"],
        "swim_spa_series": ["ATV - Aquatic Training Vessels (V150P, V150W, Kona)"],
        "spafit_key_factors": "Coques incurvées dynamiques, cuves de nage en V (Vector) et cuves ATV profondes (53 po)."
    },
    {
        "id": "wellis",
        "name": "Wellis",
        "parent_group": "Wellis Magyarország Zrt.",
        "country": "Hongrie / Global (Présence USA majeure)",
        "status": "COMPLETED",
        "spa_series": ["PeakLine (Olympus, Everest, Kilimanjaro)", "CityLine (Palermo, Malaga, Elbrus)", "MyLine"],
        "swim_spa_series": ["SwimLine (Danube, Amazonas, Rio Grande Dual Temp)"],
        "spafit_key_factors": "Premier fabricant européen en pleine expansion USA. Châssis composite Poli-Farbe, lignes contemporaines."
    },
    {
        "id": "dimension_one_spas",
        "name": "Dimension One Spas (D1)",
        "parent_group": "Jacuzzi Brands LLC",
        "country": "USA",
        "status": "COMPLETED",
        "spa_series": ["Bay Collection (Amore, Lotus, Sarena, Executive)", "Reflections Collection", "@Home Collection"],
        "swim_spa_series": ["AquaFIT (SPORT, PLAY, PRO, PLUS Dual Temp)"],
        "spafit_key_factors": "Formes bio-ergonomiques uniques, rebord arrière galbé (Curved Top) et jets de cou UltraPure."
    },
    {
        "id": "coast_spas",
        "name": "Coast Spas",
        "parent_group": "Coast Spas Manufacturing",
        "country": "Canada",
        "status": "COMPLETED",
        "spa_series": ["Cascade Series (Infinity Edge)", "Traditional Series (Element, Apex, Radiance)"],
        "swim_spa_series": ["Swim Spas (1300, 1600, 1700, 2100 Dual Temp)"],
        "spafit_key_factors": "Spas à débordement (Infinity Edge) avec bac tampon arrière spécifique : attention à l'alignement SpaFit !"
    },
    {
        "id": "nordic_hot_tubs",
        "name": "Nordic Hot Tubs",
        "parent_group": "Nordic Products Inc.",
        "country": "USA",
        "status": "COMPLETED",
        "spa_series": ["All-Round Spas (Crown, Impulse, Stella)", "Modern Series", "Luxury Series (Encore, Jubilee)", "Classic Series"],
        "swim_spa_series": [],
        "spafit_key_factors": "Pionnier des spas ronds en polyéthylène haute densité et acrylique, rayons circulaires intégraux."
    },
    {
        "id": "arctic_spas",
        "name": "Arctic Spas",
        "parent_group": "Blue Falls Manufacturing",
        "country": "Canada",
        "status": "COMPLETED",
        "spa_series": ["Custom Series (Summit, Legend, Kodiak, Klondiker, Tundra)", "Core Series"],
        "swim_spa_series": ["All-Weather Pools (Okanagan, Ocean, Hudson, Kingston)"],
        "spafit_key_factors": "Conception grand froid canadien, meuble en cèdre rouge massif ou composite FreeHeat, cuves très profondes."
    },
    {
        "id": "pdc_spas",
        "name": "PDC Spas",
        "parent_group": "Plastic Development Company",
        "country": "USA",
        "status": "COMPLETED",
        "spa_series": ["Luxury Series", "Premium Series", "LifeStyle Series"],
        "swim_spa_series": ["TruSwim Series (TSX, TS)", "Synergy Series (FX, SX, DX Dual Temp)"],
        "spafit_key_factors": "Spas de nage haut de gamme à hélice TruSwim sans turbulence."
    },
    {
        "id": "viking_spas",
        "name": "Viking Spas",
        "parent_group": "Viking Spas Inc.",
        "country": "USA",
        "status": "COMPLETED",
        "spa_series": ["Viking Series", "Aurora Series", "Royale Series", "Heritage Series", "Tradition Series"],
        "swim_spa_series": [],
        "spafit_key_factors": "Coques Soft-Touch avec bar-top classique épuré."
    },
    {
        "id": "dynasty_spas",
        "name": "Dynasty Spas",
        "parent_group": "Dynasty Spas Inc.",
        "country": "USA",
        "status": "COMPLETED",
        "spa_series": ["Club Series", "Seaside Series", "Nautical Series", "Alligator Series"],
        "swim_spa_series": ["Dynasty Swim Spas (Aquex Pro, Aquex Party)"],
        "spafit_key_factors": "Bordure acrylique relevée avec fontaines multiples et cascade éclairée."
    },
    {
        "id": "strong_spas",
        "name": "Strong Spas",
        "parent_group": "Strong Spas Manufacturing",
        "country": "USA",
        "status": "COMPLETED",
        "spa_series": ["Summit Series", "Elements Series", "DURA-SHIELD Series"],
        "swim_spa_series": [],
        "spafit_key_factors": "Certains modèles équipés de leur propre couvercle DURA-SHIELD rigide intégré repliable."
    },
    {
        "id": "freeflow_fantasy",
        "name": "Freeflow & Fantasy Spas",
        "parent_group": "Watkins Wellness (Masco Corp)",
        "country": "USA",
        "status": "COMPLETED",
        "spa_series": ["Freeflow (Cascina, Tristar, Azure, Monterey, Excursion)", "Fantasy (Drift, Entice, Splendor)"],
        "swim_spa_series": [],
        "spafit_key_factors": "Spas rotomoulés 110V plug-and-play, poids léger, forme triangulaire ou rectangulaire à rayon prononcé."
    },
    {
        "id": "catalina_spas",
        "name": "Catalina Spas",
        "parent_group": "Catalina Spas Inc.",
        "country": "USA",
        "status": "COMPLETED",
        "spa_series": ["Classic Series", "Carnival Series"],
        "swim_spa_series": ["Olympic Series (12 pi, 14 pi, 16 pi, 18 pi, 21 pi Dual Temp)"],
        "spafit_key_factors": "Pionnier historique des spas de nage avec rails d'exercice et barres de maintien inox."
    },
    {
        "id": "be_well_canada",
        "name": "Be Well Canada Spa",
        "parent_group": "Be Well Spas Inc.",
        "country": "Canada / Europe",
        "status": "COMPLETED",
        "spa_series": ["Original Series (O347, O564, O575, O671, O767)", "Fijian Series"],
        "swim_spa_series": ["Be Well Swim Spas"],
        "spafit_key_factors": "Fabrication québécoise/canadienne, isolation polyuréthane projetée, électronique Gecko."
    },
    {
        "id": "trevi_spas",
        "name": "Trévi Spas",
        "parent_group": "Trévi Fabrication",
        "country": "Canada",
        "status": "COMPLETED",
        "spa_series": ["Collection Dynastie", "Collection Prestige", "Collection Signature"],
        "swim_spa_series": ["Spas de nage Trévi (Exercice 14, 16, 19)"],
        "spafit_key_factors": "Leader du marché québécois/est-canadien, cuves thermoformées et coffrages adaptés aux climats rigoureux."
    }
]

def get_all_manufacturers() -> List[Dict[str, Any]]:
    return SPA_MANUFACTURERS_REGISTRY

def get_completed_brands() -> List[Dict[str, Any]]:
    return [m for m in SPA_MANUFACTURERS_REGISTRY if m["status"] == "COMPLETED"]

def get_in_progress_brands() -> List[Dict[str, Any]]:
    return [m for m in SPA_MANUFACTURERS_REGISTRY if m["status"] == "IN_PROGRESS"]

def get_queued_brands() -> List[Dict[str, Any]]:
    return [m for m in SPA_MANUFACTURERS_REGISTRY if m["status"] == "QUEUED"]
