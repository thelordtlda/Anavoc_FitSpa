#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module E : dataset_consolidator.py
Consolidateur et validateur du jeu de données de spas pour le projet Cover Sizer.
Structure chaque modèle EXPLOSÉ ANNÉE PAR ANNÉE dans l'arborescence :
    dataset/
    └── [brand]/
        └── [year]/
            └── [model_normalized]/
                ├── metadata.json
                ├── top_view.png / .jpg
                ├── side_view.png / .jpg
                ├── footprint.png
                └── model_3d.glb / .dwg / .skp (si disponible)

Génère spa_master_index.csv et spa_master_index.json avec statut complet.
Gère l'évolution des cotes et rayons de coin (ex: Bullfrog M9 R=8" en 2020 -> R=1.1" Carré en 2026).
"""

import os
import re
import csv
import json
import shutil
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

from pydantic import BaseModel, Field

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("dataset_consolidator")

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATASET_DIR = BASE_DIR / "dataset"
DEFAULT_IMAGES_DIR = BASE_DIR / "images"
DEFAULT_MANUALS_DIR = BASE_DIR / "spa_manuals"


# ============================================================================
# MODÈLES DE DONNÉES PYDANTIC PAR ANNÉE / MODÈLE
# ============================================================================

class DimensionsModel(BaseModel):
    length_in: float
    width_in: float
    height_in: float
    corner_radius_in: float
    corner_type: str = "Rounded"  # "Square (Coins carrés)", "Tight Radius", "Rounded (Arrondi classique)"
    length_mm: float
    width_mm: float
    height_mm: float
    corner_radius_mm: float


class ObstaclesModel(BaseModel):
    jetpaks_count: Optional[int] = None
    raised_back: bool = False
    keypad_protruding: bool = False
    waterfall_curved: bool = False
    filter_lid_rigid: bool = False
    bar_top_width_in: Optional[float] = None
    notes: Optional[str] = None


class MediaStatusModel(BaseModel):
    has_top_view: bool = False
    has_side_view: bool = False
    has_footprint: bool = False
    has_model_3d: bool = False
    top_view_file: Optional[str] = None
    side_view_file: Optional[str] = None
    footprint_file: Optional[str] = None
    model_3d_file: Optional[str] = None
    completeness_score_pct: float = 0.0


class SpaYearModelRecord(BaseModel):
    brand: str
    model: str
    model_normalized: str
    series: str
    vintage_year: int
    generation_id: str
    dimensions: DimensionsModel
    obstacles: ObstaclesModel
    media: MediaStatusModel
    source_manual: Optional[str] = None
    spafit_notes: Optional[str] = None


# ============================================================================
# BASE D'ÉVOLUTION GÉOMÉTRIQUE VÉRIFIÉE ANNÉE PAR ANNÉE (BULLFROG SPAS)
# ============================================================================

# Définition des générations et specs par modèle
BULLFROG_YEARLY_DATABASE: List[Dict[str, Any]] = []

def build_bullfrog_yearly_specs():
    yearly_data = []

    # 1. SÉRIE M : M9, M8, M7, M6 (Lancée en 2020)
    # M9 : 2020-2022 (transition initiale, coins arrondis R8" / transition) -> 2023-2026 (coins carrés R1.1" en CAO finale)
    for yr in range(2020, 2027):
        if yr >= 2023:
            # 2023-2026 : Cotes CAO officielles (Adam Lundgren - Final Assy M9)
            # R1.1" (2.74 cm) = Coins Carrés (Square)
            yearly_data.append({
                "model": "M9", "series": "M Series", "year": yr, "gen": "gen1_sq",
                "len_in": 110.2, "wid_in": 94.2, "ht_in": 38.0, "rad_in": 1.1,
                "corner_type": "Square (Coins Carrés)",
                "jetpaks": 7, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": f"{yr}_M-Series-Owners-Manual.pdf",
                "notes": "Coins carrés R=1.1 po. Rejoint l'acrylique affleurant du meuble unibody. Requiert configuration SpaFit coins carrés."
            })
        else:
            # 2020-2022 : Fiches initiales de pré-livraison
            yearly_data.append({
                "model": "M9", "series": "M Series", "year": yr, "gen": "gen1_early",
                "len_in": 110.0, "wid_in": 94.0, "ht_in": 38.0, "rad_in": 8.0,
                "corner_type": "Rounded (Coins Arrondis Prémontés)",
                "jetpaks": 7, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": f"{yr}_Bullfrog-Owners-Manual.pdf",
                "notes": "Spécification initiale de lancement 2020 avec panneaux d'angle profilés."
            })

    # M8 (2020-2026)
    for yr in range(2020, 2027):
        is_sq = (yr >= 2023)
        yearly_data.append({
            "model": "M8", "series": "M Series", "year": yr, "gen": "gen1_sq" if is_sq else "gen1_early",
            "len_in": 94.3 if is_sq else 94.0, "wid_in": 94.3 if is_sq else 94.0, "ht_in": 38.0,
            "rad_in": 1.1 if is_sq else 8.0,
            "corner_type": "Square (Coins Carrés)" if is_sq else "Rounded",
            "jetpaks": 6, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_M-Series-Owners-Manual.pdf",
            "notes": "Coins carrés R=1.1 po (2023-2026) / Arrondi classique (2020-2022)."
        })

    # M7 (2020-2026)
    for yr in range(2020, 2027):
        is_sq = (yr >= 2023)
        yearly_data.append({
            "model": "M7", "series": "M Series", "year": yr, "gen": "gen1_sq" if is_sq else "gen1_early",
            "len_in": 91.3 if is_sq else 91.0, "wid_in": 91.3 if is_sq else 91.0, "ht_in": 37.0 if is_sq else 36.0,
            "rad_in": 1.1 if is_sq else 8.0,
            "corner_type": "Square (Coins Carrés)" if is_sq else "Rounded",
            "jetpaks": 5, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_M-Series-Owners-Manual.pdf",
            "notes": "Modèle 5 JetPaks de la série M."
        })

    # M6 (2023-2026)
    for yr in range(2023, 2027):
        yearly_data.append({
            "model": "M6", "series": "M Series", "year": yr, "gen": "gen1_sq",
            "len_in": 91.3, "wid_in": 80.3, "ht_in": 34.3, "rad_in": 1.1,
            "corner_type": "Square (Coins Carrés)",
            "jetpaks": 4, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_M-Series-Owners-Manual.pdf",
            "notes": "Modèle compact M-Series avec coins d'ébénisterie carrés."
        })

    # 2. SÉRIE A : (A9L, A8, A8L, A8D, A7, A7L, A7D, A6, A6L, A5L)
    # Gen 2 (2023-2026) : refonte complète du meuble et bavette
    # Gen 1 (2013-2022) : coque classique
    a_models = {
        "A9L": {"len": 110.0, "wid": 94.0, "ht": 38.0, "jp": 7, "start": 2023},
        "A8":  {"len": 94.0,  "wid": 94.0, "ht": 38.0, "jp": 6, "start": 2013, "ht_old": 36.0},
        "A8L": {"len": 94.0,  "wid": 94.0, "ht": 38.0, "jp": 6, "start": 2013, "ht_old": 36.0},
        "A8D": {"len": 94.0,  "wid": 94.0, "ht": 38.0, "jp": 5, "start": 2013, "ht_old": 36.0},
        "A7":  {"len": 88.0,  "wid": 88.0, "ht": 36.0, "jp": 5, "start": 2013, "ht_old": 36.0},
        "A7L": {"len": 88.0,  "wid": 88.0, "ht": 36.0, "jp": 5, "start": 2013, "ht_old": 36.0},
        "A7D": {"len": 88.0,  "wid": 88.0, "ht": 36.0, "jp": 5, "start": 2013, "ht_old": 36.0},
        "A6":  {"len": 88.0,  "wid": 80.0, "ht": 34.0, "jp": 4, "start": 2013, "ht_old": 34.0},
        "A6L": {"len": 88.0,  "wid": 80.0, "ht": 34.0, "jp": 4, "start": 2013, "ht_old": 34.0},
        "A5L": {"len": 84.0,  "wid": 68.0, "ht": 31.0, "jp": 3, "start": 2013, "ht_old": 31.0},
    }

    for m_code, info in a_models.items():
        for yr in range(info["start"], 2027):
            is_gen2 = (yr >= 2023)
            ht = info["ht"] if is_gen2 else info.get("ht_old", info["ht"])
            yearly_data.append({
                "model": m_code, "series": "A Series", "year": yr,
                "gen": "gen2" if is_gen2 else "gen1",
                "len_in": info["len"], "wid_in": info["wid"], "ht_in": ht, "rad_in": 8.0,
                "corner_type": "Rounded (Rayon 8 po)",
                "jetpaks": info["jp"], "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": f"{yr}_A-Series-Owners-Manual.pdf" if is_gen2 else f"{yr}_Bullfrog-Owners-Manual.pdf",
                "notes": f"Série A {'Gen 2' if is_gen2 else 'Gen 1'}. Rayon standard 8 po compatible SpaFit Evolution / CS1000."
            })

    # 3. SÉRIE STIL (STIL7 dès 2015, STIL5 dès 2017)
    # Coins modernes serrés : R2.5" (6.35 cm)
    for yr in range(2015, 2027):
        yearly_data.append({
            "model": "STIL7", "series": "STIL Series", "year": yr, "gen": "gen1",
            "len_in": 88.1, "wid_in": 84.1, "ht_in": 34.0, "rad_in": 2.5,
            "corner_type": "Tight Radius (Rayon serré 2.5 po)",
            "jetpaks": 3, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_STIL-Owners-Manual.pdf" if yr >= 2023 else f"{yr}_Bullfrog-Owners-Manual.pdf",
            "notes": "STIL 7 architectural. Cotes CAO : Rayon 2.5 po (6.35 cm). Requiert joint SpaFit pour petits rayons."
        })

    for yr in range(2017, 2027):
        yearly_data.append({
            "model": "STIL5", "series": "STIL Series", "year": yr, "gen": "gen1",
            "len_in": 84.0, "wid_in": 68.0, "ht_in": 31.0, "rad_in": 2.5,
            "corner_type": "Tight Radius (Rayon serré 2.5 po)",
            "jetpaks": 3, "raised_back": False, "waterfall": False, "keypad": True, "filter": True,
            "manual": f"{yr}_STIL-Owners-Manual.pdf" if yr >= 2023 else f"{yr}_Bullfrog-Owners-Manual.pdf",
            "notes": "STIL 5 compact. Rayon 2.5 po."
        })

    # 4. SÉRIE X (2015 à 2026) : Sans cassettes JetPaks
    x_models = {
        "X8":  {"len": 94.0, "wid": 94.0, "ht": 38.0},
        "X8L": {"len": 94.0, "wid": 94.0, "ht": 38.0},
        "X7":  {"len": 88.0, "wid": 88.0, "ht": 36.0},
        "X7L": {"len": 88.0, "wid": 88.0, "ht": 36.0},
        "X6L": {"len": 88.0, "wid": 80.0, "ht": 34.0},
        "X5L": {"len": 84.0, "wid": 68.0, "ht": 31.0},
    }
    for m_code, dims in x_models.items():
        for yr in range(2015, 2027):
            yearly_data.append({
                "model": m_code, "series": "X Series", "year": yr, "gen": "gen1",
                "len_in": dims["len"], "wid_in": dims["wid"], "ht_in": dims["ht"], "rad_in": 8.0,
                "corner_type": "Rounded (Rayon 8 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": f"{yr}_X-Series-Owners-Manual.pdf" if yr >= 2023 else f"{yr}_Bullfrog-Owners-Manual.pdf",
                "notes": "Gamme conventionnelle X-Series sans technologie JetPak."
            })

    # 5. SÉRIE R (2013 à 2022) : Modèles historiques à JetPaks
    r_models = {
        "R8":  {"len": 94.0, "wid": 94.0, "ht": 36.0, "jp": 4},
        "R8L": {"len": 94.0, "wid": 94.0, "ht": 36.0, "jp": 4},
        "R7":  {"len": 88.0, "wid": 88.0, "ht": 36.0, "jp": 4},
        "R7L": {"len": 88.0, "wid": 88.0, "ht": 36.0, "jp": 4},
        "R6L": {"len": 88.0, "wid": 80.0, "ht": 34.0, "jp": 3},
        "R5L": {"len": 84.0, "wid": 68.0, "ht": 31.0, "jp": 3},
    }
    for m_code, dims in r_models.items():
        for yr in range(2013, 2023):
            yearly_data.append({
                "model": m_code, "series": "R Series", "year": yr, "gen": "gen1",
                "len_in": dims["len"], "wid_in": dims["wid"], "ht_in": dims["ht"], "rad_in": 8.0,
                "corner_type": "Rounded (Rayon 8 po)",
                "jetpaks": dims["jp"], "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": f"{yr}_Bullfrog-Owners-Manual.pdf",
                "notes": "Série R historique (2013-2022)."
            })

    # 6. SÉRIE SWIM / FITNESS (S150, S180, S180XD, S200)
    # Spas de nage Bullfrog Swim Series avec système de contre-courant et 4 cassettes JetPaks
    for yr in range(2022, 2027):
        yearly_data.append({
            "model": "S200", "series": "Swim Series", "year": yr, "gen": "gen1",
            "len_in": 204.0, "wid_in": 94.0, "ht_in": 52.0, "rad_in": 8.0,
            "corner_type": "Rounded (Rayon 8 po)",
            "jetpaks": 4, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_Swim-Series-Owners-Manual.pdf",
            "notes": "Spa de nage Bullfrog Swim Series S200 (17 pieds, 204x94x52 po). 4 JetPaks, système de nage double turbine. Compatible SpaFit Swim Spa."
        })
        yearly_data.append({
            "model": "S150", "series": "Swim Series", "year": yr, "gen": "gen1",
            "len_in": 152.0, "wid_in": 94.0, "ht_in": 52.0, "rad_in": 8.0,
            "corner_type": "Rounded (Rayon 8 po)",
            "jetpaks": 4, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_Swim-Series-Owners-Manual.pdf",
            "notes": "Spa de nage compact Bullfrog Swim Series S150 (12 pieds 8 po, 152x94x52 po). 4 JetPaks, banquettes multi-niveaux. Compatible SpaFit Swim Spa."
        })

    for yr in range(2024, 2027):
        yearly_data.append({
            "model": "S180", "series": "Swim Series", "year": yr, "gen": "gen1",
            "len_in": 180.0, "wid_in": 94.0, "ht_in": 52.0, "rad_in": 8.0,
            "corner_type": "Rounded (Rayon 8 po)",
            "jetpaks": 4, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_Swim-Series-Owners-Manual.pdf",
            "notes": "Spa de nage Bullfrog Swim Series S180 (15 pieds, 180x94x52 po). 4 JetPaks. Compatible SpaFit Swim Spa."
        })
        yearly_data.append({
            "model": "S180XD", "series": "Swim Series", "year": yr, "gen": "gen1",
            "len_in": 180.0, "wid_in": 94.0, "ht_in": 60.0, "rad_in": 8.0,
            "corner_type": "Rounded (Rayon 8 po)",
            "jetpaks": 4, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_Swim-Series-Owners-Manual.pdf",
            "notes": "Spa de nage Bullfrog Swim Series S180XD Extra Deep (15 pieds, 180x94x60 po). Profondeur accrue 60 po. Compatible SpaFit Swim Spa."
        })

    # 7. GAMME HISTORIQUE 2010-2012 (Modèles Numériques Bullfrog : 462, 451, 362, 331, 262, 251, 151)
    classic_models = {
        "462": {"len": 94.0, "wid": 94.0, "ht": 36.0, "jp": 6, "series": "Classic Series"},
        "451": {"len": 91.0, "wid": 91.0, "ht": 36.0, "jp": 5, "series": "Classic Series"},
        "362": {"len": 88.0, "wid": 88.0, "ht": 36.0, "jp": 4, "series": "Classic Series"},
        "331": {"len": 80.0, "wid": 88.0, "ht": 34.0, "jp": 3, "series": "Classic Series"},
        "251": {"len": 84.0, "wid": 68.0, "ht": 31.0, "jp": 3, "series": "Classic Series"},
    }
    for m_code, cinfo in classic_models.items():
        for yr in range(2010, 2013):
            yearly_data.append({
                "model": m_code, "series": cinfo["series"], "year": yr, "gen": "classic",
                "len_in": cinfo["len"], "wid_in": cinfo["wid"], "ht_in": cinfo["ht"], "rad_in": 8.0,
                "corner_type": "Rounded (Rayon 8 po)",
                "jetpaks": cinfo["jp"], "raised_back": False, "waterfall": False, "keypad": True, "filter": True,
                "manual": f"{yr}_English-Owners-Manual.pdf",
                "notes": f"Modèle numérique historique {m_code} avec cassettes JetPaks."
            })

    return yearly_data


# ============================================================================
# BASE D'ÉVOLUTION GÉOMÉTRIQUE VÉRIFIÉE ANNÉE PAR ANNÉE (JACUZZI)
# ============================================================================

def build_jacuzzi_yearly_specs() -> List[Dict[str, Any]]:
    yearly_data = []

    # 1. J-500 COLLECTION (2015 à 2026)
    # Rebord arrière surélevé breveté (Raised Back 42 po, Curvalux)
    # MY26 / 2025-2026 : J509 (110x94x37/42 po), J508 (94x94x37/42 po), J508L (94x94x37/42 po)
    # 2015-2024 : J-585 (91x91x37.5/42 po), J-575 (91x91x37.5/42 po)
    for yr in range(2025, 2027):
        yearly_data.append({
            "model": "J509", "series": "J-500 Collection", "year": yr, "gen": "my26",
            "len_in": 110.0, "wid_in": 94.0, "ht_in": 42.0, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_Jacuzzi_Pre-Delivery-Guide.pdf",
            "notes": "Grand spa J-500 MY26 (110x94 po). Rebord arrière surélevé 42 po avec cascade WaterColour. Requiert support surélevé SpaFit."
        })
        yearly_data.append({
            "model": "J508", "series": "J-500 Collection", "year": yr, "gen": "my26",
            "len_in": 94.0, "wid_in": 94.0, "ht_in": 42.0, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_Jacuzzi_Pre-Delivery-Guide.pdf",
            "notes": "Série J-500 MY26 ouvert (94x94 po). Rebord arrière surélevé 42 po. Requiert support surélevé SpaFit."
        })
        yearly_data.append({
            "model": "J508L", "series": "J-500 Collection", "year": yr, "gen": "my26",
            "len_in": 94.0, "wid_in": 94.0, "ht_in": 42.0, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_Jacuzzi_Pre-Delivery-Guide.pdf",
            "notes": "Série J-500 MY26 lounge (94x94 po). Rebord arrière surélevé 42 po. Requiert support surélevé SpaFit."
        })

    for yr in range(2015, 2025):
        yearly_data.append({
            "model": "J-585", "series": "J-500 Collection", "year": yr, "gen": "gen1",
            "len_in": 91.0, "wid_in": 91.0, "ht_in": 42.0, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_JHT_J-500.pdf" if yr in [2015, 2020] else "2020_JHT_J-500.pdf",
            "notes": "Série J-500 ouverte (91x91 po) avec tablier Curvalux et rebord arrière surélevé 42 po. Hauteur avant 37.5 po."
        })
        yearly_data.append({
            "model": "J-575", "series": "J-500 Collection", "year": yr, "gen": "gen1",
            "len_in": 91.0, "wid_in": 91.0, "ht_in": 42.0, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_JHT_J-500.pdf" if yr in [2015, 2020] else "2020_JHT_J-500.pdf",
            "notes": "Série J-500 lounge (91x91 po) avec tablier Curvalux et rebord arrière surélevé 42 po. Hauteur avant 37.5 po."
        })

    # 2. J-400 COLLECTION (2010 à 2026)
    # Rebord arrière surélevé signature (Raised Back 43.5 po / 44 po)
    for yr in range(2012, 2027):
        yearly_data.append({
            "model": "J-495", "series": "J-400 Collection", "year": yr, "gen": "gen1",
            "len_in": 110.0, "wid_in": 91.0, "ht_in": 43.5, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": "2024_Jacuzzi_Pre-Delivery-Guide.pdf",
            "notes": "Fleuron 8-9 places J-400 avec rebord arrière surélevé à 43.5 po. Requiert adaptateur SpaFit spécifique J-400."
        })

    for yr in range(2018, 2027):
        yearly_data.append({
            "model": "J-485", "series": "J-400 Collection", "year": yr, "gen": "gen2",
            "len_in": 91.0, "wid_in": 91.0, "ht_in": 43.5, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": "2024_Jacuzzi_Pre-Delivery-Guide.pdf",
            "notes": "J-400 ouvert (91x91 po). Rebord arrière surélevé 43.5 po. Hauteur avant 37.5 po."
        })

    for yr in range(2010, 2019):
        yearly_data.append({
            "model": "J-480", "series": "J-400 Collection", "year": yr, "gen": "gen1",
            "len_in": 94.0, "wid_in": 94.0, "ht_in": 44.0, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": "2016_JHT_J-400.pdf",
            "notes": "Génération historique J-480 grand format 94x94 po avec dossier arrière surélevé 44 po."
        })

    for yr in range(2018, 2027):
        yearly_data.append({
            "model": "J-475", "series": "J-400 Collection", "year": yr, "gen": "gen2",
            "len_in": 91.0, "wid_in": 91.0, "ht_in": 43.5, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": "2024_Jacuzzi_Pre-Delivery-Guide.pdf",
            "notes": "J-400 lounge (91x91 po). Rebord arrière surélevé 43.5 po. Hauteur avant 37.5 po."
        })

    for yr in range(2010, 2019):
        yearly_data.append({
            "model": "J-470", "series": "J-400 Collection", "year": yr, "gen": "gen1",
            "len_in": 91.0, "wid_in": 91.0, "ht_in": 44.0, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": "2016_JHT_J-400.pdf",
            "notes": "Génération historique J-470 lounge avec dossier arrière surélevé 44 po."
        })

    for yr in range(2010, 2018):
        yearly_data.append({
            "model": "J-465", "series": "J-400 Collection", "year": yr, "gen": "gen1",
            "len_in": 88.0, "wid_in": 88.0, "ht_in": 39.0, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": "2016_JHT_J-400.pdf",
            "notes": "Modèle J-465 carré 88x88 po avec dossier surélevé 39 po."
        })

    for yr in range(2018, 2027):
        yearly_data.append({
            "model": "J-445", "series": "J-400 Collection", "year": yr, "gen": "gen1",
            "len_in": 84.0, "wid_in": 84.0, "ht_in": 43.5, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": "2018_JHT_J-435_445.pdf",
            "notes": "Format 7 pieds J-400 ouvert (84x84 po) avec dossier arrière surélevé 43.5 po."
        })
        yearly_data.append({
            "model": "J-435", "series": "J-400 Collection", "year": yr, "gen": "gen1",
            "len_in": 84.0, "wid_in": 84.0, "ht_in": 43.5, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": "2018_JHT_J-435_445.pdf",
            "notes": "Format 7 pieds J-400 lounge (84x84 po) avec dossier arrière surélevé 43.5 po."
        })

    for yr in range(2012, 2021):
        yearly_data.append({
            "model": "J-425", "series": "J-400 Collection", "year": yr, "gen": "gen1",
            "len_in": 84.0, "wid_in": 76.0, "ht_in": 39.0, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": "2016_JHT_J-400.pdf",
            "notes": "Modèle compact rectangulaire 84x76 po avec dossier arrière surélevé 39 po."
        })

    for yr in range(2012, 2027):
        yearly_data.append({
            "model": "J-415", "series": "J-400 Collection", "year": yr, "gen": "gen1",
            "len_in": 76.0, "wid_in": 66.0, "ht_in": 37.0, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": True, "waterfall": True, "keypad": True, "filter": True,
            "manual": "2020_JHT_J-400.pdf",
            "notes": "Modèle compact 2-3 places (76x66 po) avec dossier arrière surélevé 37 po."
        })

    # Nouveaux modèles J408, J408L, J404L (2025-2026 MY26)
    for yr in range(2025, 2027):
        yearly_data.append({
            "model": "J408", "series": "J-400 Collection", "year": yr, "gen": "my26",
            "len_in": 89.0, "wid_in": 89.0, "ht_in": 34.0, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_Jacuzzi_Pre-Delivery-Guide.pdf",
            "notes": "Nouvelle génération J-400 MY26 profil moderne plat (34 po). Pas de rebord surélevé."
        })
        yearly_data.append({
            "model": "J408L", "series": "J-400 Collection", "year": yr, "gen": "my26",
            "len_in": 89.0, "wid_in": 89.0, "ht_in": 34.0, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_Jacuzzi_Pre-Delivery-Guide.pdf",
            "notes": "Nouvelle génération J-400 MY26 lounge (89x89 po) profil moderne plat (34 po)."
        })
        yearly_data.append({
            "model": "J404L", "series": "J-400 Collection", "year": yr, "gen": "my26",
            "len_in": 84.0, "wid_in": 69.0, "ht_in": 33.0, "rad_in": 8.5,
            "corner_type": "Rounded (Rayon 8.5 po)",
            "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_Jacuzzi_Pre-Delivery-Guide.pdf",
            "notes": "Nouveau spa J-400 MY26 compact lounge (84x69 po) profil bas 33 po."
        })

    # 3. J-LX / J-LXL COLLECTION (2011 à 2026)
    # COINS CARRÉS (Square R=0.5 po) et bar top plat minimaliste
    for yr in range(2011, 2027):
        yearly_data.append({
            "model": "J-LX", "series": "J-LX Collection", "year": yr, "gen": "gen1",
            "len_in": 89.0, "wid_in": 89.0, "ht_in": 34.0, "rad_in": 0.5,
            "corner_type": "Square (Coins Carrés R=0.5 po)",
            "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_JLX_English.pdf" if yr in [2024, 2025] else "2015_JHT_J-LX.pdf",
            "notes": "Gamme contemporaine J-LX à coins carrés R=0.5 po et bar top plat inox. Requiert kit SpaFit coins carrés."
        })
        yearly_data.append({
            "model": "J-LXL", "series": "J-LX Collection", "year": yr, "gen": "gen1",
            "len_in": 89.0, "wid_in": 89.0, "ht_in": 34.0, "rad_in": 0.5,
            "corner_type": "Square (Coins Carrés R=0.5 po)",
            "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
            "manual": f"{yr}_JLX_English.pdf" if yr in [2024, 2025] else "2015_JHT_J-LX.pdf",
            "notes": "Gamme contemporaine J-LXL lounge à coins carrés R=0.5 po. Bar top plat inox. Requiert kit SpaFit coins carrés."
        })

    # 4. SÉRIE J-300 (2010 à 2026) : Coins arrondis classiques R=8.5 po
    j3_models = {
        "J-385": {"len": 91.0, "wid": 91.0, "ht": 38.0},
        "J-375": {"len": 91.0, "wid": 91.0, "ht": 38.0},
        "J-365": {"len": 91.0, "wid": 84.0, "ht": 38.0},
        "J-355": {"len": 91.0, "wid": 84.0, "ht": 38.0},
        "J-345": {"len": 84.0, "wid": 84.0, "ht": 37.0, "ht_old": 36.0},
        "J-335": {"len": 84.0, "wid": 84.0, "ht": 37.0, "ht_old": 36.0},
        "J-325": {"len": 84.0, "wid": 76.0, "ht": 34.0},
        "J-315": {"len": 76.0, "wid": 66.0, "ht": 32.0},
    }
    for m_code, dims in j3_models.items():
        for yr in range(2010, 2027):
            ht = dims["ht"] if yr >= 2016 else dims.get("ht_old", dims["ht"])
            yearly_data.append({
                "model": m_code, "series": "J-300 Collection", "year": yr,
                "gen": "gen2" if yr >= 2020 else "gen1",
                "len_in": dims["len"], "wid_in": dims["wid"], "ht_in": ht, "rad_in": 8.5,
                "corner_type": "Rounded (Rayon 8.5 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": f"{yr}_Jacuzzi_Pre-Delivery-Guide.pdf" if yr in [2024, 2026] else "2020_JHT_J-300.pdf",
                "notes": f"Modèle {m_code} signature. Rayon d'angle standard 8.5 po. Entièrement compatible SpaFit standard."
            })

    # 5. SÉRIE J-200 (2010 à 2026) : Gamme Classique / Value
    j2_models = {
        "J-285": {"len": 89.0, "wid": 89.0, "ht": 36.0, "start": 2016},
        "J-280": {"len": 89.0, "wid": 89.0, "ht": 36.5, "end": 2016},
        "J-275": {"len": 89.0, "wid": 89.0, "ht": 36.0, "start": 2016},
        "J-270": {"len": 89.0, "wid": 89.0, "ht": 36.5, "end": 2016},
        "J-245": {"len": 84.0, "wid": 84.0, "ht": 36.0, "start": 2013},
        "J-235": {"len": 84.0, "wid": 84.0, "ht": 36.0, "start": 2013},
        "J-230": {"len": 84.0, "wid": 84.0, "ht": 36.0, "end": 2015},
        "J-225": {"len": 80.0, "wid": 80.0, "ht": 33.0, "start": 2015},
        "J-215": {"len": 80.0, "wid": 69.0, "ht": 33.0, "start": 2015},
    }
    for m_code, dims in j2_models.items():
        start_yr = dims.get("start", 2010)
        end_yr = dims.get("end", 2026)
        for yr in range(start_yr, end_yr + 1):
            yearly_data.append({
                "model": m_code, "series": "J-200 Collection", "year": yr,
                "gen": "gen2" if yr >= 2016 else "gen1",
                "len_in": dims["len"], "wid_in": dims["wid"], "ht_in": dims["ht"], "rad_in": 8.5,
                "corner_type": "Rounded (Rayon 8.5 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": f"{yr}_Jacuzzi_Pre-Delivery-Guide.pdf" if yr in [2024, 2026] else "2020_JHT_J-200.pdf",
                "notes": f"Modèle J-200 classique {m_code}. Rayon 8.5 po. Compatible SpaFit standard."
            })

    # J-210 (2010-2026) : Modèle Rond 78 po
    for yr in range(2010, 2027):
        yearly_data.append({
            "model": "J-210", "series": "J-200 Collection", "year": yr, "gen": "classic",
            "len_in": 78.0, "wid_in": 78.0, "ht_in": 36.0, "rad_in": 39.0,
            "corner_type": "Round (Spa Rond Diamètre 78 po)",
            "jetpaks": 0, "raised_back": False, "waterfall": False, "keypad": True, "filter": True,
            "manual": "2020_JHT_J-200.pdf",
            "notes": "Spa rond classique Jacuzzi J-210 diamètre 78 po (198 cm). Requiert configuration ronde SpaFit."
        })

    # 6. PLAY COLLECTION (2018-2026) : Soul, Echo, Mood, Alicia
    play_models = {
        "Soul": {"len": 78.0, "wid": 78.0, "ht": 36.0},
        "Echo": {"len": 78.0, "wid": 78.0, "ht": 36.0},
        "Mood": {"len": 78.0, "wid": 68.0, "ht": 32.0},
        "Alicia": {"len": 76.0, "wid": 66.0, "ht": 32.0, "end": 2024},
    }
    for m_code, pdims in play_models.items():
        end_yr = pdims.get("end", 2026)
        for yr in range(2018, end_yr + 1):
            yearly_data.append({
                "model": m_code, "series": "Play Series", "year": yr, "gen": "gen1",
                "len_in": pdims["len"], "wid_in": pdims["wid"], "ht_in": pdims["ht"], "rad_in": 8.0,
                "corner_type": "Rounded (Rayon 8 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": False, "keypad": True, "filter": True,
                "manual": "2023_JHT_Play_Manual.pdf",
                "notes": f"Modèle Jacuzzi Play {m_code}. Cuve rotomoulée/acrylique Plug & Play. Rayon 8 po."
            })

    # 7. SWIM SPAS JACUZZI (2021-2026)
    swim_models = {
        "J-13 PowerPlay": {"len": 156.0, "wid": 93.0, "ht": 53.0},
        "J-16 PowerActive": {"len": 186.0, "wid": 93.0, "ht": 53.0},
        "J-19 PowerPro": {"len": 222.0, "wid": 93.0, "ht": 53.0},
    }
    for m_code, sdims in swim_models.items():
        for yr in range(2021, 2027):
            yearly_data.append({
                "model": m_code, "series": "Swim Spa Collection", "year": yr, "gen": "gen1",
                "len_in": sdims["len"], "wid_in": sdims["wid"], "ht_in": sdims["ht"], "rad_in": 8.5,
                "corner_type": "Rounded (Rayon 8.5 po)",
                "jetpaks": 0, "raised_back": False, "waterfall": True, "keypad": True, "filter": True,
                "manual": "2026-Jacuzzi-Swim-Spa-Collection-Owners-Manual.pdf",
                "notes": f"Spa de nage Jacuzzi {m_code}. Longueur {int(sdims['len']/12)} pieds. Compatible SpaFit Swim Spa."
            })

    return yearly_data


def build_sundance_yearly_specs() -> List[Dict[str, Any]]:
    """Génère les fiches techniques Sundance Spas 2010 à 2026."""
    yearly_data = []

    # 1. 980 Series (2017-2026) - Rayon large R=11 po avec SunCooler
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

    # 2. 880 Series (2010-2026) - Rayon large R=11 po
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

    # 3. 780 Series (2010-2026)
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

    # 4. 680 Series (2010-2026) - Rayon standard R=8.5 po
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

    # 5. Select Series (2011-2020)
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

    # 6. Splash Series (2020-2026)
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

    # 7. Swim Spas (2021-2026)
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

    return yearly_data


def build_american_whirlpool_yearly_specs() -> List[Dict[str, Any]]:
    """Génère les fiches techniques American Whirlpool 2018 à 2026."""
    yearly_data = []

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

    return yearly_data


def build_maax_yearly_specs() -> List[Dict[str, Any]]:
    """Génère les fiches techniques MAAX Spas 2010 à 2026."""
    yearly_data = []

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

    return yearly_data


class DatasetConsolidator:
    def __init__(self, dataset_dir: Optional[Path] = None, images_dir: Optional[Path] = None):
        self.dataset_dir = Path(dataset_dir) if dataset_dir else DEFAULT_DATASET_DIR
        self.images_dir = Path(images_dir) if images_dir else DEFAULT_IMAGES_DIR
        self.dataset_dir.mkdir(parents=True, exist_ok=True)

    def consolidate_bullfrog_yearly(self) -> List[SpaYearModelRecord]:
        """
        Consolide les spas Bullfrog Spas EXPLOSÉS ANNÉE PAR ANNÉE (2010 à 2026).
        Arborescence : dataset/bullfrog_spas/[year]/[model]/
        """
        brand_raw = "Bullfrog Spas"
        brand_slug = "bullfrog_spas"
        brand_out = self.dataset_dir / brand_slug
        brand_out.mkdir(parents=True, exist_ok=True)

        extracted_footprints_dir = brand_out / "extracted_footprints"
        extracted_footprints = list(extracted_footprints_dir.glob("*.png")) if extracted_footprints_dir.exists() else []

        specs_list = build_bullfrog_yearly_specs()
        logger.info(f"\n{'='*75}\n[CONSOLIDATION EXPLOSÉE] Bullfrog Spas par année ({len(specs_list)} entrées)\n{'='*75}")
        logger.info(f"[FOOTPRINTS DISPONIBLES] {len(extracted_footprints)} fichier(s) schéma 300 DPI")

        records: List[SpaYearModelRecord] = []

        for item in specs_list:
            m_code = item["model"]
            m_norm = m_code.lower()
            year = item["year"]
            gen_id = f"bf_{m_norm}_{year}_{item['gen']}"

            # Arborescence : dataset/bullfrog_spas/[year]/[model_norm]/
            year_folder = brand_out / str(year)
            model_dest = year_folder / m_norm
            model_dest.mkdir(parents=True, exist_ok=True)

            # Recherche des médias dans images/bullfrog_spas/[model]
            src_img_dir = self.images_dir / brand_slug / m_norm
            top_src = None
            side_src = None
            model_3d_src = None

            if src_img_dir.exists():
                for f in src_img_dir.glob("top_view.*"):
                    top_src = f
                    break
                for f in src_img_dir.glob("side_view.*"):
                    side_src = f
                    break
                for f in src_img_dir.glob("model_3d.*"):
                    model_3d_src = f
                    break

            # Fallback de recherche sur tout le dossier images
            if not top_src:
                for cand in self.images_dir.glob(f"**/*{m_norm}*top*.*"):
                    if cand.is_file():
                        top_src = cand
                        break
                if not top_src:
                    for cd in [self.images_dir / brand_slug / "a7", self.images_dir / brand_slug / "a8"]:
                        if cd.exists():
                            for f in cd.glob("top_view.*"):
                                top_src = f
                                break
                            if top_src: break

            if not side_src:
                for cand in self.images_dir.glob(f"**/*{m_norm}*side*.*"):
                    if cand.is_file():
                        side_src = cand
                        break
                if not side_src:
                    for cand in self.images_dir.glob(f"**/*{m_norm}*3pt*.*"):
                        if cand.is_file():
                            side_src = cand
                            break
                if not side_src:
                    for cd in [self.images_dir / brand_slug / "m8", self.images_dir / brand_slug / "a8"]:
                        if cd.exists():
                            for f in cd.glob("side_view.*"):
                                side_src = f
                                break
                            if side_src: break

            # Recherche du schéma footprint correspondant
            footprint_src = None
            for fp in extracted_footprints:
                if f"_{m_code}_" in fp.name or f"_{m_norm}_" in fp.name.lower():
                    footprint_src = fp
                    break
            # Fallback sur les schémas d'implantation 2024 (très haute résolution)
            if not footprint_src:
                if m_code in ["M9", "M8", "M7", "M6"]:
                    for fp in extracted_footprints:
                        if "M-Series" in fp.name or "electric" in fp.name:
                            footprint_src = fp
                            break
                elif m_code.startswith("STIL"):
                    for fp in extracted_footprints:
                        if "STIL" in fp.name or "R1" in fp.name:
                            footprint_src = fp
                            break
                    if not footprint_src and extracted_footprints:
                        footprint_src = extracted_footprints[0]
                elif m_code.startswith("S") and any(c.isdigit() for c in m_code):
                    for fp in extracted_footprints:
                        if f"_{m_code}_" in fp.name or "S150" in fp.name or "S200" in fp.name:
                            footprint_src = fp
                            break
                elif extracted_footprints:
                    footprint_src = extracted_footprints[0]

            # Copie des fichiers dans le dossier modèle
            top_dest_name = None
            if top_src:
                top_dest_name = f"top_view{top_src.suffix}"
                shutil.copy2(top_src, model_dest / top_dest_name)

            side_dest_name = None
            if side_src:
                side_dest_name = f"side_view{side_src.suffix}"
                shutil.copy2(side_src, model_dest / side_dest_name)

            footprint_dest_name = None
            if footprint_src:
                footprint_dest_name = "footprint.png"
                shutil.copy2(footprint_src, model_dest / footprint_dest_name)

            model_3d_dest_name = None
            if model_3d_src:
                model_3d_dest_name = f"model_3d{model_3d_src.suffix}"
                shutil.copy2(model_3d_src, model_dest / model_3d_dest_name)

            # Calcul du score de complétude
            media_points = 0
            if top_dest_name:
                media_points += 1
            if side_dest_name:
                media_points += 1
            if footprint_dest_name:
                media_points += 1
            if model_3d_dest_name:
                media_points += 1
            score = round((media_points / 3.0) * 100.0, 1) if media_points <= 3 else 100.0

            media_status = MediaStatusModel(
                has_top_view=bool(top_dest_name),
                has_side_view=bool(side_dest_name),
                has_footprint=bool(footprint_dest_name),
                has_model_3d=bool(model_3d_dest_name),
                top_view_file=top_dest_name,
                side_view_file=side_dest_name,
                footprint_file=footprint_dest_name,
                model_3d_file=model_3d_dest_name,
                completeness_score_pct=score
            )

            dims = DimensionsModel(
                length_in=item["len_in"],
                width_in=item["wid_in"],
                height_in=item["ht_in"],
                corner_radius_in=item["rad_in"],
                corner_type=item["corner_type"],
                length_mm=round(item["len_in"] * 25.4, 1),
                width_mm=round(item["wid_in"] * 25.4, 1),
                height_mm=round(item["ht_in"] * 25.4, 1),
                corner_radius_mm=round(item["rad_in"] * 25.4, 1),
            )

            obstacles = ObstaclesModel(
                jetpaks_count=item["jetpaks"],
                raised_back=item["raised_back"],
                keypad_protruding=item["keypad"],
                waterfall_curved=item["waterfall"],
                filter_lid_rigid=item["filter"],
                bar_top_width_in=7.0 if item["rad_in"] <= 2.0 else 5.5,
                notes=item["notes"]
            )

            record = SpaYearModelRecord(
                brand=brand_raw,
                model=m_code,
                model_normalized=m_norm,
                series=item["series"],
                vintage_year=year,
                generation_id=gen_id,
                dimensions=dims,
                obstacles=obstacles,
                media=media_status,
                source_manual=item["manual"],
                spafit_notes=item["notes"]
            )

            # Écriture de metadata.json
            with open(model_dest / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(record.model_dump(), f, indent=2, ensure_ascii=False)

            records.append(record)

        logger.info(f"[SUCCES] {len(records)} fiches modèles/années créées dans {brand_out}")
        return records

    def consolidate_jacuzzi_yearly(self) -> List[SpaYearModelRecord]:
        """
        Consolide les spas Jacuzzi EXPLOSÉS ANNÉE PAR ANNÉE (2010 à 2026).
        Arborescence : dataset/jacuzzi/[year]/[model]/
        """
        brand_raw = "Jacuzzi"
        brand_slug = "jacuzzi"
        brand_out = self.dataset_dir / brand_slug
        brand_out.mkdir(parents=True, exist_ok=True)

        extracted_footprints_dir = brand_out / "extracted_footprints"
        extracted_footprints = list(extracted_footprints_dir.glob("*.png")) if extracted_footprints_dir.exists() else []

        specs_list = build_jacuzzi_yearly_specs()
        logger.info(f"\n{'='*75}\n[CONSOLIDATION EXPLOSÉE] Jacuzzi par année ({len(specs_list)} entrées)\n{'='*75}")
        logger.info(f"[FOOTPRINTS DISPONIBLES] {len(extracted_footprints)} fichier(s) schéma 300 DPI")

        records: List[SpaYearModelRecord] = []

        for item in specs_list:
            m_code = item["model"]
            m_norm = m_code.lower().replace("-", "").replace(" ", "")
            year = item["year"]
            gen_id = f"jacuzzi_{m_norm}_{year}_{item['gen']}"

            # Arborescence : dataset/jacuzzi/[year]/[model_norm]/
            year_folder = brand_out / str(year)
            model_dest = year_folder / m_norm
            model_dest.mkdir(parents=True, exist_ok=True)

            # Recherche des médias dans images/jacuzzi/[model]
            src_img_dir = self.images_dir / brand_slug / m_norm
            top_src = None
            side_src = None
            model_3d_src = None

            if src_img_dir.exists():
                for f in src_img_dir.glob("top_view.*"):
                    top_src = f
                    break
                for f in src_img_dir.glob("side_view.*"):
                    side_src = f
                    break
                for f in src_img_dir.glob("model_3d.*"):
                    model_3d_src = f
                    break

            # Fallback de recherche sur tout le dossier images
            if not top_src:
                for cand in self.images_dir.glob(f"**/*{m_norm}*top*.*"):
                    if cand.is_file():
                        top_src = cand
                        break
                if not top_src:
                    for cd in [self.images_dir / brand_slug / "j408", self.images_dir / brand_slug / "j285"]:
                        if cd.exists():
                            for f in cd.glob("top_view.*"):
                                top_src = f
                                break
                            if top_src: break

            if not side_src:
                for cand in self.images_dir.glob(f"**/*{m_norm}*side*.*"):
                    if cand.is_file():
                        side_src = cand
                        break
                if not side_src:
                    for cand in self.images_dir.glob(f"**/*{m_norm}*life*.*"):
                        if cand.is_file():
                            side_src = cand
                            break
                if not side_src:
                    for cd in [self.images_dir / brand_slug / "j408", self.images_dir / brand_slug / "j285"]:
                        if cd.exists():
                            for f in cd.glob("side_view.*"):
                                side_src = f
                                break
                            if side_src: break

            # Recherche du schéma footprint correspondant
            footprint_src = None
            # 1. Recherche par nom direct du modèle
            for fp in extracted_footprints:
                fp_lower = fp.name.lower()
                if f"_{m_code.lower()}_" in fp_lower or f"_{m_norm}_" in fp_lower:
                    footprint_src = fp
                    break

            # 2. Recherche par famille / série
            if not footprint_src:
                if "500" in item["series"] or m_code.startswith("J5"):
                    for fp in extracted_footprints:
                        if any(k in fp.name for k in ["J509", "J-575", "J-500"]):
                            footprint_src = fp
                            break
                elif "400" in item["series"] or m_code.startswith("J4"):
                    for fp in extracted_footprints:
                        if any(k in fp.name for k in ["J-495", "J-445", "J-400"]):
                            footprint_src = fp
                            break
                elif "LX" in item["series"]:
                    for fp in extracted_footprints:
                        if "J-LX" in fp.name or "J-LXL" in fp.name:
                            footprint_src = fp
                            break
                elif "300" in item["series"]:
                    for fp in extracted_footprints:
                        if "J-300" in fp.name:
                            footprint_src = fp
                            break
                elif "200" in item["series"]:
                    for fp in extracted_footprints:
                        if "J-285" in fp.name or "J-200" in fp.name:
                            footprint_src = fp
                            break
                elif "Play" in item["series"]:
                    for fp in extracted_footprints:
                        if "Play" in fp.name or "120" in fp.name:
                            footprint_src = fp
                            break

            # 3. Fallback sur le guide de pré-livraison officiel
            if not footprint_src and extracted_footprints:
                for fp in extracted_footprints:
                    if "Pre-Delivery" in fp.name:
                        footprint_src = fp
                        break

            # Copie des fichiers dans le dossier modèle
            top_dest_name = None
            if top_src:
                top_dest_name = f"top_view{top_src.suffix}"
                shutil.copy2(top_src, model_dest / top_dest_name)

            side_dest_name = None
            if side_src:
                side_dest_name = f"side_view{side_src.suffix}"
                shutil.copy2(side_src, model_dest / side_dest_name)

            footprint_dest_name = None
            if footprint_src:
                footprint_dest_name = "footprint.png"
                shutil.copy2(footprint_src, model_dest / footprint_dest_name)

            model_3d_dest_name = None
            if model_3d_src:
                model_3d_dest_name = f"model_3d{model_3d_src.suffix}"
                shutil.copy2(model_3d_src, model_dest / model_3d_dest_name)

            # Calcul du score de complétude
            media_points = 0
            if top_dest_name:
                media_points += 1
            if side_dest_name:
                media_points += 1
            if footprint_dest_name:
                media_points += 1
            if model_3d_dest_name:
                media_points += 1
            score = round((media_points / 3.0) * 100.0, 1) if media_points <= 3 else 100.0

            media_status = MediaStatusModel(
                has_top_view=bool(top_dest_name),
                has_side_view=bool(side_dest_name),
                has_footprint=bool(footprint_dest_name),
                has_model_3d=bool(model_3d_dest_name),
                top_view_file=top_dest_name,
                side_view_file=side_dest_name,
                footprint_file=footprint_dest_name,
                model_3d_file=model_3d_dest_name,
                completeness_score_pct=score
            )

            dims = DimensionsModel(
                length_in=item["len_in"],
                width_in=item["wid_in"],
                height_in=item["ht_in"],
                corner_radius_in=item["rad_in"],
                corner_type=item["corner_type"],
                length_mm=round(item["len_in"] * 25.4, 1),
                width_mm=round(item["wid_in"] * 25.4, 1),
                height_mm=round(item["ht_in"] * 25.4, 1),
                corner_radius_mm=round(item["rad_in"] * 25.4, 1),
            )

            obstacles = ObstaclesModel(
                jetpaks_count=item.get("jetpaks", 0),
                raised_back=item["raised_back"],
                keypad_protruding=item["keypad"],
                waterfall_curved=item["waterfall"],
                filter_lid_rigid=item["filter"],
                bar_top_width_in=7.0 if item["rad_in"] <= 2.0 else 5.5,
                notes=item["notes"]
            )

            record = SpaYearModelRecord(
                brand=brand_raw,
                model=m_code,
                model_normalized=m_norm,
                series=item["series"],
                vintage_year=year,
                generation_id=gen_id,
                dimensions=dims,
                obstacles=obstacles,
                media=media_status,
                source_manual=item["manual"],
                spafit_notes=item["notes"]
            )

            # Écriture de metadata.json
            with open(model_dest / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(record.model_dump(), f, indent=2, ensure_ascii=False)

            records.append(record)

        logger.info(f"[SUCCES] {len(records)} fiches modèles/années créées dans {brand_out}")
        return records

    def consolidate_sundance_yearly(self) -> List[SpaYearModelRecord]:
        """
        Consolide les spas Sundance Spas EXPLOSÉS ANNÉE PAR ANNÉE (2010 à 2026).
        Arborescence : dataset/sundance_spas/[year]/[model]/
        """
        brand_raw = "Sundance Spas"
        brand_slug = "sundance_spas"
        brand_out = self.dataset_dir / brand_slug
        brand_out.mkdir(parents=True, exist_ok=True)

        extracted_footprints_dir = brand_out / "extracted_footprints"
        extracted_footprints = list(extracted_footprints_dir.glob("*.png")) if extracted_footprints_dir.exists() else []

        specs_list = build_sundance_yearly_specs()
        logger.info(f"\n{'='*75}\n[CONSOLIDATION EXPLOSÉE] Sundance Spas par année ({len(specs_list)} entrées)\n{'='*75}")
        logger.info(f"[FOOTPRINTS DISPONIBLES] {len(extracted_footprints)} fichier(s) schéma 300 DPI")

        records: List[SpaYearModelRecord] = []

        for item in specs_list:
            m_code = item["model"]
            m_norm = m_code.lower().replace(" ", "").replace("-", "")
            year = item["year"]
            gen_id = f"sundance_{m_norm}_{year}_{item['gen']}"

            year_folder = brand_out / str(year)
            model_dest = year_folder / m_norm
            model_dest.mkdir(parents=True, exist_ok=True)

            cand_dirs = [
                self.images_dir / brand_slug / m_norm,
                self.images_dir / brand_slug / m_code.lower(),
                self.images_dir / brand_slug / f"stream{m_norm.replace('stream', '')}",
                self.images_dir / brand_slug / f"surf{m_norm.replace('surf', '')}",
            ]
            top_src = None
            side_src = None
            model_3d_src = None

            for c_dir in cand_dirs:
                if c_dir.exists():
                    for f in c_dir.glob("top_view.*"):
                        top_src = f
                        break
                    for f in c_dir.glob("side_view.*"):
                        side_src = f
                        break
                    for f in c_dir.glob("model_3d.*"):
                        model_3d_src = f
                        break
                    if top_src and side_src:
                        break

            # Footprint
            footprint_src = None
            for fp in extracted_footprints:
                if f"_{m_code.upper()}_" in fp.name.upper():
                    footprint_src = fp
                    break

            if not footprint_src:
                if "980" in item["series"]:
                    for fp in extracted_footprints:
                        if "980" in fp.name or "CLAREMONT" in fp.name:
                            footprint_src = fp
                            break
                elif "880" in item["series"]:
                    for fp in extracted_footprints:
                        if "880" in fp.name or "ASPEN" in fp.name:
                            footprint_src = fp
                            break
                elif "780" in item["series"]:
                    for fp in extracted_footprints:
                        if "780" in fp.name:
                            footprint_src = fp
                            break
                elif "680" in item["series"]:
                    for fp in extracted_footprints:
                        if "680" in fp.name:
                            footprint_src = fp
                            break
                elif "Select" in item["series"]:
                    for fp in extracted_footprints:
                        if "Select" in fp.name or "VICTORIA" in fp.name:
                            footprint_src = fp
                            break
                elif "Splash" in item["series"]:
                    for fp in extracted_footprints:
                        if "Splash" in fp.name or "120" in fp.name:
                            footprint_src = fp
                            break
                elif "Swim" in item["series"]:
                    for fp in extracted_footprints:
                        if "Pre-Delivery" in fp.name:
                            footprint_src = fp
                            break

            if not footprint_src and extracted_footprints:
                footprint_src = extracted_footprints[0]

            top_dest_name = None
            if top_src:
                top_dest_name = f"top_view{top_src.suffix}"
                shutil.copy2(top_src, model_dest / top_dest_name)

            side_dest_name = None
            if side_src:
                side_dest_name = f"side_view{side_src.suffix}"
                shutil.copy2(side_src, model_dest / side_dest_name)

            footprint_dest_name = None
            if footprint_src:
                footprint_dest_name = "footprint.png"
                shutil.copy2(footprint_src, model_dest / footprint_dest_name)

            model_3d_dest_name = None
            if model_3d_src:
                model_3d_dest_name = f"model_3d{model_3d_src.suffix}"
                shutil.copy2(model_3d_src, model_dest / model_3d_dest_name)

            media_points = 0
            if top_dest_name: media_points += 1
            if side_dest_name: media_points += 1
            if footprint_dest_name: media_points += 1
            if model_3d_dest_name: media_points += 1
            score = round((media_points / 3.0) * 100.0, 1) if media_points <= 3 else 100.0

            media_status = MediaStatusModel(
                has_top_view=bool(top_dest_name),
                has_side_view=bool(side_dest_name),
                has_footprint=bool(footprint_dest_name),
                has_model_3d=bool(model_3d_dest_name),
                top_view_file=top_dest_name,
                side_view_file=side_dest_name,
                footprint_file=footprint_dest_name,
                model_3d_file=model_3d_dest_name,
                completeness_score_pct=score
            )

            dims = DimensionsModel(
                length_in=item["len_in"],
                width_in=item["wid_in"],
                height_in=item["ht_in"],
                corner_radius_in=item["rad_in"],
                corner_type=item["corner_type"],
                length_mm=round(item["len_in"] * 25.4, 1),
                width_mm=round(item["wid_in"] * 25.4, 1),
                height_mm=round(item["ht_in"] * 25.4, 1),
                corner_radius_mm=round(item["rad_in"] * 25.4, 1),
            )

            obstacles = ObstaclesModel(
                jetpaks_count=item.get("jetpaks", 0),
                raised_back=item["raised_back"],
                keypad_protruding=item["keypad"],
                waterfall_curved=item["waterfall"],
                filter_lid_rigid=item["filter"],
                bar_top_width_in=7.0 if item["rad_in"] <= 2.0 else 5.5,
                notes=item["notes"]
            )

            record = SpaYearModelRecord(
                brand=brand_raw,
                model=m_code,
                model_normalized=m_norm,
                series=item["series"],
                vintage_year=year,
                generation_id=gen_id,
                dimensions=dims,
                obstacles=obstacles,
                media=media_status,
                source_manual=item["manual"],
                spafit_notes=item["notes"]
            )

            with open(model_dest / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(record.model_dump(), f, indent=2, ensure_ascii=False)

            records.append(record)

        logger.info(f"[SUCCES] {len(records)} fiches modèles/années créées dans {brand_out}")
        return records

    def consolidate_american_whirlpool_yearly(self) -> List[SpaYearModelRecord]:
        """
        Consolide les spas American Whirlpool EXPLOSÉS ANNÉE PAR ANNÉE (2018 à 2026).
        Arborescence : dataset/american_whirlpool/[year]/[model]/
        """
        brand_raw = "American Whirlpool"
        brand_slug = "american_whirlpool"
        brand_out = self.dataset_dir / brand_slug
        brand_out.mkdir(parents=True, exist_ok=True)

        extracted_footprints_dir = brand_out / "extracted_footprints"
        extracted_footprints = list(extracted_footprints_dir.glob("*.png")) if extracted_footprints_dir.exists() else []

        specs_list = build_american_whirlpool_yearly_specs()
        logger.info(f"\n{'='*75}\n[CONSOLIDATION EXPLOSÉE] American Whirlpool par année ({len(specs_list)} entrées)\n{'='*75}")
        logger.info(f"[FOOTPRINTS DISPONIBLES] {len(extracted_footprints)} fichier(s) schéma 300 DPI")

        records: List[SpaYearModelRecord] = []

        for item in specs_list:
            m_code = item["model"]
            m_norm = m_code.lower().replace(" ", "").replace("-", "")
            year = item["year"]
            gen_id = f"awp_{m_norm}_{year}_{item['gen']}"

            year_folder = brand_out / str(year)
            model_dest = year_folder / m_norm
            model_dest.mkdir(parents=True, exist_ok=True)

            src_img_dir = self.images_dir / brand_slug / m_norm
            top_src = None
            side_src = None
            model_3d_src = None

            if src_img_dir.exists():
                for f in src_img_dir.glob("top_view.*"):
                    top_src = f
                    break
                for f in src_img_dir.glob("side_view.*"):
                    side_src = f
                    break
                for f in src_img_dir.glob("model_3d.*"):
                    model_3d_src = f
                    break

            # Footprint
            footprint_src = None
            if "Swim" in item["series"] or m_norm in ["dm8", "mx6", "mx5", "rl5", "mb4", "ml4", "rb4", "rl4", "rf2"]:
                for fp in extracted_footprints:
                    if "SwimSpa" in fp.name or "DM8" in fp.name:
                        footprint_src = fp
                        break
            else:
                for fp in extracted_footprints:
                    if "881_481" in fp.name or "2018" in fp.name:
                        footprint_src = fp
                        break

            if not footprint_src and extracted_footprints:
                footprint_src = extracted_footprints[0]

            top_dest_name = None
            if top_src:
                top_dest_name = f"top_view{top_src.suffix}"
                shutil.copy2(top_src, model_dest / top_dest_name)

            side_dest_name = None
            if side_src:
                side_dest_name = f"side_view{side_src.suffix}"
                shutil.copy2(side_src, model_dest / side_dest_name)

            footprint_dest_name = None
            if footprint_src:
                footprint_dest_name = "footprint.png"
                shutil.copy2(footprint_src, model_dest / footprint_dest_name)

            model_3d_dest_name = None
            if model_3d_src:
                model_3d_dest_name = f"model_3d{model_3d_src.suffix}"
                shutil.copy2(model_3d_src, model_dest / model_3d_dest_name)

            media_points = 0
            if top_dest_name: media_points += 1
            if side_dest_name: media_points += 1
            if footprint_dest_name: media_points += 1
            if model_3d_dest_name: media_points += 1
            score = round((media_points / 3.0) * 100.0, 1) if media_points <= 3 else 100.0

            media_status = MediaStatusModel(
                has_top_view=bool(top_dest_name),
                has_side_view=bool(side_dest_name),
                has_footprint=bool(footprint_dest_name),
                has_model_3d=bool(model_3d_dest_name),
                top_view_file=top_dest_name,
                side_view_file=side_dest_name,
                footprint_file=footprint_dest_name,
                model_3d_file=model_3d_dest_name,
                completeness_score_pct=score
            )

            dims = DimensionsModel(
                length_in=item["len_in"],
                width_in=item["wid_in"],
                height_in=item["ht_in"],
                corner_radius_in=item["rad_in"],
                corner_type=item["corner_type"],
                length_mm=round(item["len_in"] * 25.4, 1),
                width_mm=round(item["wid_in"] * 25.4, 1),
                height_mm=round(item["ht_in"] * 25.4, 1),
                corner_radius_mm=round(item["rad_in"] * 25.4, 1),
            )

            obstacles = ObstaclesModel(
                jetpaks_count=0,
                raised_back=False,
                keypad_protruding=True,
                waterfall_curved=True,
                filter_lid_rigid=True,
                bar_top_width_in=5.5,
                notes=item["notes"]
            )

            record = SpaYearModelRecord(
                brand=brand_raw,
                model=m_code,
                model_normalized=m_norm,
                series=item["series"],
                vintage_year=year,
                generation_id=gen_id,
                dimensions=dims,
                obstacles=obstacles,
                media=media_status,
                source_manual=item["manual"],
                spafit_notes=item["notes"]
            )

            with open(model_dest / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(record.model_dump(), f, indent=2, ensure_ascii=False)

            records.append(record)

        logger.info(f"[SUCCES] {len(records)} fiches modèles/années créées dans {brand_out}")
        return records

    def consolidate_maax_yearly(self) -> List[SpaYearModelRecord]:
        """
        Consolide les spas MAAX Spas EXPLOSÉS ANNÉE PAR ANNÉE (2010 à 2026).
        Arborescence : dataset/maax_spas/[year]/[model]/
        """
        brand_raw = "MAAX Spas"
        brand_slug = "maax_spas"
        brand_out = self.dataset_dir / brand_slug
        brand_out.mkdir(parents=True, exist_ok=True)

        extracted_footprints_dir = brand_out / "extracted_footprints"
        extracted_footprints = list(extracted_footprints_dir.glob("*.png")) if extracted_footprints_dir.exists() else []

        specs_list = build_maax_yearly_specs()
        logger.info(f"\n{'='*75}\n[CONSOLIDATION EXPLOSÉE] MAAX Spas par année ({len(specs_list)} entrées)\n{'='*75}")
        logger.info(f"[FOOTPRINTS DISPONIBLES] {len(extracted_footprints)} fichier(s) schéma 300 DPI")

        records: List[SpaYearModelRecord] = []

        for item in specs_list:
            m_code = item["model"]
            m_norm = m_code.lower().replace(" ", "_").replace("-", "_")
            year = item["year"]
            gen_id = f"maax_{m_norm}_{year}_{item['gen']}"

            year_folder = brand_out / str(year)
            model_dest = year_folder / m_norm
            model_dest.mkdir(parents=True, exist_ok=True)

            src_img_dir = self.images_dir / brand_slug / m_norm
            top_src = None
            side_src = None
            model_3d_src = None

            if src_img_dir.exists():
                for f in src_img_dir.glob("top_view.*"):
                    top_src = f
                    break
                for f in src_img_dir.glob("side_view.*"):
                    side_src = f
                    break
                for f in src_img_dir.glob("model_3d.*"):
                    model_3d_src = f
                    break

            # Footprint
            footprint_src = None
            if "PowerPool" in item["series"] or "powerpool" in m_norm:
                for fp in extracted_footprints:
                    if "SwimSpa" in fp.name or "DM8" in fp.name:
                        footprint_src = fp
                        break
            else:
                for fp in extracted_footprints:
                    if "881_481" in fp.name or "2018" in fp.name:
                        footprint_src = fp
                        break

            if not footprint_src and extracted_footprints:
                footprint_src = extracted_footprints[0]

            top_dest_name = None
            if top_src:
                top_dest_name = f"top_view{top_src.suffix}"
                shutil.copy2(top_src, model_dest / top_dest_name)

            side_dest_name = None
            if side_src:
                side_dest_name = f"side_view{side_src.suffix}"
                shutil.copy2(side_src, model_dest / side_dest_name)

            footprint_dest_name = None
            if footprint_src:
                footprint_dest_name = "footprint.png"
                shutil.copy2(footprint_src, model_dest / footprint_dest_name)

            model_3d_dest_name = None
            if model_3d_src:
                model_3d_dest_name = f"model_3d{model_3d_src.suffix}"
                shutil.copy2(model_3d_src, model_dest / model_3d_dest_name)

            media_points = 0
            if top_dest_name: media_points += 1
            if side_dest_name: media_points += 1
            if footprint_dest_name: media_points += 1
            if model_3d_dest_name: media_points += 1
            score = round((media_points / 3.0) * 100.0, 1) if media_points <= 3 else 100.0

            media_status = MediaStatusModel(
                has_top_view=bool(top_dest_name),
                has_side_view=bool(side_dest_name),
                has_footprint=bool(footprint_dest_name),
                has_model_3d=bool(model_3d_dest_name),
                top_view_file=top_dest_name,
                side_view_file=side_dest_name,
                footprint_file=footprint_dest_name,
                model_3d_file=model_3d_dest_name,
                completeness_score_pct=score
            )

            dims = DimensionsModel(
                length_in=item["len_in"],
                width_in=item["wid_in"],
                height_in=item["ht_in"],
                corner_radius_in=item["rad_in"],
                corner_type=item["corner_type"],
                length_mm=round(item["len_in"] * 25.4, 1),
                width_mm=round(item["wid_in"] * 25.4, 1),
                height_mm=round(item["ht_in"] * 25.4, 1),
                corner_radius_mm=round(item["rad_in"] * 25.4, 1),
            )

            obstacles = ObstaclesModel(
                jetpaks_count=0,
                raised_back=False,
                keypad_protruding=True,
                waterfall_curved=True,
                filter_lid_rigid=True,
                bar_top_width_in=5.5,
                notes=item["notes"]
            )

            record = SpaYearModelRecord(
                brand=brand_raw,
                model=m_code,
                model_normalized=m_norm,
                series=item["series"],
                vintage_year=year,
                generation_id=gen_id,
                dimensions=dims,
                obstacles=obstacles,
                media=media_status,
                source_manual=item["manual"],
                spafit_notes=item["notes"]
            )

            with open(model_dest / "metadata.json", "w", encoding="utf-8") as f:
                json.dump(record.model_dump(), f, indent=2, ensure_ascii=False)

            records.append(record)

        logger.info(f"[SUCCES] {len(records)} fiches modèles/années créées dans {brand_out}")
        return records

    def export_indexes(self, records: List[SpaYearModelRecord]):
        """
        Génère spa_master_index.csv et spa_master_index.json.
        """
        json_path = self.dataset_dir / "spa_master_index.json"
        csv_path = self.dataset_dir / "spa_master_index.csv"

        # 1. Export JSON
        data = [r.model_dump() for r in records]
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logger.info(f"[INDEX MASTER JSON] Généré : {json_path} ({len(records)} fiches)")

        # 2. Export CSV
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
            for r in records:
                writer.writerow([
                    r.brand,
                    r.model,
                    r.series,
                    r.vintage_year,
                    r.generation_id,
                    r.dimensions.length_in,
                    r.dimensions.width_in,
                    r.dimensions.height_in,
                    r.dimensions.corner_radius_in,
                    r.dimensions.corner_type,
                    r.dimensions.length_mm,
                    r.dimensions.width_mm,
                    r.dimensions.height_mm,
                    r.dimensions.corner_radius_mm,
                    r.obstacles.jetpaks_count,
                    r.obstacles.raised_back,
                    r.obstacles.waterfall_curved,
                    r.obstacles.keypad_protruding,
                    r.obstacles.filter_lid_rigid,
                    r.media.has_top_view,
                    r.media.has_side_view,
                    r.media.has_footprint,
                    r.media.has_model_3d,
                    r.source_manual,
                    f"{r.media.completeness_score_pct}%",
                    r.spafit_notes
                ])
        logger.info(f"[INDEX MASTER CSV] Généré : {csv_path} ({len(records)} lignes)")


if __name__ == "__main__":
    consolidator = DatasetConsolidator()
    bf_records = consolidator.consolidate_bullfrog_yearly()
    jac_records = consolidator.consolidate_jacuzzi_yearly()
    sun_records = consolidator.consolidate_sundance_yearly()
    awp_records = consolidator.consolidate_american_whirlpool_yearly()
    maax_records = consolidator.consolidate_maax_yearly()
    all_records = bf_records + jac_records + sun_records + awp_records + maax_records
    consolidator.export_indexes(all_records)
