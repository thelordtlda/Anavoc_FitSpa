#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module C : schematic_extractor.py
Analyseur de schémas techniques et plans d'implantation ("footprints") depuis les PDF de spas.
Rendu 300 DPI via PyMuPDF et rognage automatique des marges blanches par vision par ordinateur (OpenCV).
Extraction des cotes réelles (Longueur, Largeur, Hauteur, Rayon de coin, Obstacles).
"""

import os
import re
import sys
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

import fitz  # PyMuPDF
import cv2
import numpy as np
from PIL import Image

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger("schematic_extractor")

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_DATASET_DIR = BASE_DIR / "dataset"

# Mots-clés de détection pour les plans cotés et empreintes au sol
FOOTPRINT_KEYWORDS = [
    "footprint",
    "dimensions",
    "overhead view",
    "specifications",
    "engineering drawing",
    "bar top",
    "corner radius",
    "electrical service",
    "spa dimensions",
    "layout",
    "cutout",
    "elevation",
    "top view",
    "spa features",
    "selector diagram",
    "controls diagram",
    "pre-delivery",
    "chaseway"
]

class SchematicExtractor:
    def __init__(self, output_root: Optional[Path] = None):
        self.output_root = Path(output_root) if output_root else DEFAULT_DATASET_DIR
        self.output_root.mkdir(parents=True, exist_ok=True)

    def autocrop_drawing(self, img_bgr: np.ndarray, margin: int = 35) -> np.ndarray:
        """
        Rogne automatiquement les marges blanches d'une image technique pour isoler
        le dessin coté du spa avec une bordure nette.
        """
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        
        # Pixels non-blancs (les lignes techniques et textes sont plus sombres que 245)
        _, thresh = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)
        
        # Trouver les coordonnées des pixels non-vides
        non_zero = cv2.findNonZero(thresh)
        if non_zero is None:
            return img_bgr  # Page blanche, on retourne l'image telle quelle
            
        x, y, w, h = cv2.boundingRect(non_zero)
        
        # Ajout d'une marge de sécurité
        h_max, w_max = img_bgr.shape[:2]
        x1 = max(0, x - margin)
        y1 = max(0, y - margin)
        x2 = min(w_max, x + w + margin)
        y2 = min(h_max, y + h + margin)
        
        cropped = img_bgr[y1:y2, x1:x2]
        return cropped

    def parse_dimensions_from_text(self, text: str) -> Dict[str, Any]:
        """
        Extrait les dimensions physiques (po et mm), le rayon de coin et les obstacles.
        """
        dims: Dict[str, Any] = {
            "length_in": None,
            "width_in": None,
            "height_in": None,
            "corner_radius_in": None,
            "length_mm": None,
            "width_mm": None,
            "height_mm": None,
            "corner_radius_mm": None,
            "jetpaks_count": None,
            "obstacles": {
                "raised_back": False,
                "waterfall": False,
                "keypad_protruding": False,
                "filter_lid": False
            }
        }

        # 1. Détection de dimensions 3D format: 94" x 94" x 38" ou 7'10" x 7'10" x 38"
        dim_3d_match = re.search(
            r'(\d{2,3}(?:\.\d+)?)\s*(?:\"|po|in)?\s*[xX×]\s*(\d{2,3}(?:\.\d+)?)\s*(?:\"|po|in)?\s*[xX×]\s*(\d{2}(?:\.\d+)?)\s*(?:\"|po|in)?',
            text
        )
        if dim_3d_match:
            try:
                dims["length_in"] = float(dim_3d_match.group(1))
                dims["width_in"] = float(dim_3d_match.group(2))
                dims["height_in"] = float(dim_3d_match.group(3))
                dims["length_mm"] = round(dims["length_in"] * 25.4, 1)
                dims["width_mm"] = round(dims["width_in"] * 25.4, 1)
                dims["height_mm"] = round(dims["height_in"] * 25.4, 1)
            except ValueError:
                pass

        # 2. Détection format métrique: 2.39m x 2.39m x 0.97m ou 239cm x 239cm
        metric_match = re.search(
            r'(\d{1,4}(?:\.\d+)?)\s*(?:m|cm|mm)\s*[xX×]\s*(\d{1,4}(?:\.\d+)?)\s*(?:m|cm|mm)',
            text
        )
        if metric_match and not dims["length_mm"]:
            try:
                v1 = float(metric_match.group(1))
                v2 = float(metric_match.group(2))
                if v1 < 10:  # En mètres
                    dims["length_mm"] = round(v1 * 1000, 1)
                    dims["width_mm"] = round(v2 * 1000, 1)
                elif v1 < 1000: # En cm
                    dims["length_mm"] = round(v1 * 10, 1)
                    dims["width_mm"] = round(v2 * 10, 1)
                else: # En mm
                    dims["length_mm"] = round(v1, 1)
                    dims["width_mm"] = round(v2, 1)
                dims["length_in"] = round(dims["length_mm"] / 25.4, 2)
                dims["width_in"] = round(dims["width_mm"] / 25.4, 2)
            except ValueError:
                pass

        # 3. Rayon de coin (Corner Radius)
        radius_match = re.search(r'(?:corner\s*radius|radius|rayon\s*de\s*coin)\s*[:=]?\s*(\d+(?:\.\d+)?)\s*(?:\"|po|in)?', text, re.I)
        if radius_match:
            try:
                r_val = float(radius_match.group(1))
                dims["corner_radius_in"] = r_val
                dims["corner_radius_mm"] = round(r_val * 25.4, 1)
            except ValueError:
                pass

        # 4. Détection JetPaks (spécifique Bullfrog)
        jetpak_match = re.search(r'(\d+)\s*(?:jetpaks?|jet\s*paks?)', text, re.I)
        if jetpak_match:
            try:
                dims["jetpaks_count"] = int(jetpak_match.group(1))
            except ValueError:
                pass

        # 5. Obstacles géométriques sur le bar top
        text_lower = text.lower()
        if any(w in text_lower for w in ["raised back", "dossier surélevé", "high back", "elevated headrest"]):
            dims["obstacles"]["raised_back"] = True
        if any(w in text_lower for w in ["waterfall", "cascade", "water feature"]):
            dims["obstacles"]["waterfall"] = True
        if any(w in text_lower for w in ["auxiliary control", "touchscreen", "control center", "clavier"]):
            dims["obstacles"]["keypad_protruding"] = True
        if any(w in text_lower for w in ["filter lid", "couvercle de filtre", "rigid filter"]):
            dims["obstacles"]["filter_lid"] = True

        return dims

    def extract_from_pdf(self, pdf_path: Path, brand: str = "Bullfrog Spas") -> List[Dict[str, Any]]:
        """
        Extrait les pages contenant les plans cotés à 300 DPI, les rogne et extrait les cotes.
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            logger.error(f"Fichier PDF introuvable : {pdf_path}")
            return []

        logger.info(f"\n[ANALYSE PDF] {pdf_path.name} ({pdf_path.stat().st_size // 1024} Ko)")
        doc = fitz.open(str(pdf_path))
        num_pages = len(doc)
        logger.info(f"[PAGES] {num_pages} page(s) dans le document.")

        extracted_footprints: List[Dict[str, Any]] = []

        # Identifier le dossier de marque
        brand_slug = re.sub(r"[^a-zA-Z0-9]+", "_", brand.strip().lower()).strip("_")

        for page_idx in range(num_pages):
            page = doc[page_idx]
            text = page.get_text()
            text_lower = text.lower()

            # Score de pertinence
            kw_hits = [kw for kw in FOOTPRINT_KEYWORDS if kw in text_lower]
            drawings = page.get_drawings()
            num_drawings = len(drawings)

            # Est-ce une page technique / footprint ?
            is_technical_page = (
                len(kw_hits) >= 2 or
                ("footprint" in text_lower) or
                ("dimensions" in text_lower and ("electrical" in text_lower or "overhead" in text_lower or num_drawings > 15)) or
                ("bar top" in text_lower)
            )

            if is_technical_page:
                logger.info(f"  -> Page {page_idx + 1} détectée comme plan technique (Mots-clés: {kw_hits}, Tracés: {num_drawings})")

                # Rendu haute définition 300 DPI (72 DPI standard * (300/72))
                zoom = 300.0 / 72.0
                matrix = fitz.Matrix(zoom, zoom)
                pix = page.get_pixmap(matrix=matrix, alpha=False)

                # Conversion NumPy / OpenCV
                img_rgb = np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3))
                img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)

                # Rognage automatique des marges blanches
                cropped = self.autocrop_drawing(img_bgr, margin=35)

                # Extraction des modèles mentionnés sur cette page (Bullfrog, Jacuzzi, Sundance, American Whirlpool, MAAX, etc.)
                sundance_names = r"KINGSTON|CLAREMONT|LISBON|ODESSA|ASPEN|MAXXUS|CAMEO|OPTIMA|ALTAMAR|MARIN|CAPRI|CHELSEE|HAMILTON|BRISTOL|HANOVER|MONTCLAIR|DOVER|PRADO|PEYTON|EDISON|RAMONA|DENALI|TACOMA|CONSTANCE|VICTORIA|BERKELEY|BROOK|STREAM|SURF|SS13ST|SS17ST|SS17SU"
                jacuzzi_names = r"J-?\d{3}[A-Z]?|J\d{3}[A-Z]?|J-?LX[L]?|SOUL|ECHO|MOOD|ALICIA"
                bullfrog_names = r"[MARX]\d[LD]?|STIL\s*\d|CALM\s*\d|S150|S180|S180XD|S200"
                maax_awp_names = r"POWERPOOL|SUPERSPORT|DM8|MBP|ML4|RL4|\b\d{3}\b"
                combined_regex = rf"\b({sundance_names}|{jacuzzi_names}|{bullfrog_names}|{maax_awp_names})\b"
                model_matches = re.findall(combined_regex, text, re.I)
                models_found = list(dict.fromkeys([m.upper().replace(" ", "") for m in model_matches]))
                primary_model = models_found[0] if models_found else f"page_{page_idx + 1}"

                # Dimensions
                parsed_data = self.parse_dimensions_from_text(text)

                # Nom de fichier de sortie
                pdf_stem = pdf_path.stem
                output_filename = f"{pdf_stem}_p{page_idx + 1}_{primary_model}_footprint.png"
                output_dir = self.output_root / brand_slug / "extracted_footprints"
                output_dir.mkdir(parents=True, exist_ok=True)
                output_file = output_dir / output_filename

                cv2.imwrite(str(output_file), cropped)
                logger.info(f"  [EXPORT SCHEMA] Sauvegardé : {output_file.name} ({cropped.shape[1]}x{cropped.shape[0]} px)")

                extracted_footprints.append({
                    "pdf_source": pdf_path.name,
                    "page_number": page_idx + 1,
                    "primary_model": primary_model,
                    "models_detected": models_found,
                    "footprint_path": str(output_file),
                    "dimensions": parsed_data,
                    "resolution": f"{cropped.shape[1]}x{cropped.shape[0]}"
                })

        doc.close()
        logger.info(f"[BILAN] {len(extracted_footprints)} schémas techniques extraits de {pdf_path.name}.")
        return extracted_footprints

if __name__ == "__main__":
    extractor = SchematicExtractor()
    test_dir = BASE_DIR / "spa_manuals" / "bullfrog_spas"
    pdf_files = list(test_dir.glob("*.pdf"))
    if pdf_files:
        for p in pdf_files[:2]:
            extractor.extract_from_pdf(p, brand="Bullfrog Spas")
    else:
        logger.info("Aucun PDF trouvé pour l'instant dans spa_manuals/bullfrog_spas.")
