/**
 * ============================================================================
 * SpaFit — SpaFit Gazebo Configurator (app.js)
 * Scope Initial : Gamme Oasis (avec architecture multi-gammes data/models.json)
 * ============================================================================
 */

const INCH_TO_MM = 25.4;

// Base de données embarquée de secours (identique à data/models.json généré par scripts/extract_specs.py)
const FALLBACK_MODELS = [
  {
    id: "oasis-std-8x8",
    nom: "Oasis — Standard 8' (Short Side / Entrée 93\")",
    code_interne: "8' S/S (3D: D-000122)",
    gamme: "Oasis",
    active_in_ui: true,
    type: "hot_tub",
    orientation_entree: "Short Side (Côté 93 po)",
    unite: "po",
    source_fichiers: [
      "OASIS FOOTPRINT AND ELEVATION.pdf",
      "Overall Dimensions - 2026-04-24.xlsx",
      "Revision mesures legend, Endless Pools, Oasis, Evolution, et Oasis XL V3.xlsx",
      "OASIS-2.STEP"
    ],
    degagement_colonnes: {
      longueur: 98.0,
      largeur: 93.0,
      longueur_cao: 98.32,
      largeur_cao: 92.98,
      diagonale: 130.75,
      largeur_entree: 52.0
    },
    joint_etancheite: {
      longueur_min: 75.0,
      longueur_max: 97.0,
      largeur_min: 70.0,
      largeur_max: 92.0,
      rayon_min: 4.0,
      rayon_recommande: 8.0,
      largeur_bande: 3.5,
      surface_plane_min: 1.25,
      coquille_min_longueur: 74.0,
      coquille_min_largeur: 69.0
    },
    hauteur: {
      spa_min: 34.0,
      spa_max: 48.0,
      poteau_fixe: 76.0,
      poteau_deploye: 92.125,
      epaisseur_toit: 22.875,
      epaisseur_cadre_u: 4.0,
      course_elevation: 48.0,
      hauteur_max_hors_tout: 115.0
    },
    toit_hors_tout: {
      longueur: 105.75,
      largeur: 100.5,
      longueur_avec_operateur: 112.0,
      fondation_longueur: 118.0,
      fondation_largeur: 106.0,
      c_position_moteur: 36.1,
      roller_shade_longueur: 100.57,
      roller_shade_largeur: 95.2
    },
    degagement_installation: {
      maintenance_moteur_entree: 24.0,
      maintenance_cotes: 6.0,
      poteau_patio_min: 0.5
    },
    validation_cao: {
      fichier: "OASIS-2.STEP",
      assemblage_racine: "OASIS-2",
      unite_native: "po",
      poteaux_detectes: 4,
      entraxe_poteaux_x_po: 99.813,
      entraxe_poteaux_z_po: 94.48
    }
  },
  {
    id: "oasis-std-ls",
    nom: "Oasis — Standard 8' (Long Side / Entrée 98\")",
    code_interne: "8' L/S (3D: D-000122)",
    gamme: "Oasis",
    active_in_ui: true,
    type: "hot_tub",
    orientation_entree: "Long Side (Côté 98 po)",
    unite: "po",
    source_fichiers: [
      "OASIS FOOTPRINT AND ELEVATION.pdf",
      "Overall Dimensions - 2026-04-24.xlsx",
      "Revision mesures legend, Endless Pools, Oasis, Evolution, et Oasis XL V3.xlsx",
      "OASIS-2.STEP"
    ],
    degagement_colonnes: {
      longueur: 93.0,
      largeur: 98.0,
      longueur_cao: 92.98,
      largeur_cao: 98.32,
      diagonale: 130.75,
      largeur_entree: 57.0
    },
    joint_etancheite: {
      longueur_min: 70.0,
      longueur_max: 92.0,
      largeur_min: 75.0,
      largeur_max: 97.0,
      rayon_min: 4.0,
      rayon_recommande: 8.0,
      largeur_bande: 3.5,
      surface_plane_min: 1.25,
      coquille_min_longueur: 69.0,
      coquille_min_largeur: 74.0
    },
    hauteur: {
      spa_min: 34.0,
      spa_max: 48.0,
      poteau_fixe: 76.0,
      poteau_deploye: 92.125,
      epaisseur_toit: 22.875,
      epaisseur_cadre_u: 4.0,
      course_elevation: 48.0,
      hauteur_max_hors_tout: 115.0
    },
    toit_hors_tout: {
      longueur: 100.5,
      largeur: 105.8,
      longueur_avec_operateur: 106.79,
      fondation_longueur: 112.0,
      fondation_largeur: 118.0,
      c_position_moteur: 38.7,
      roller_shade_longueur: 95.2,
      roller_shade_largeur: 100.57
    },
    degagement_installation: {
      maintenance_moteur_entree: 24.0,
      maintenance_cotes: 6.0,
      poteau_patio_min: 0.5
    },
    validation_cao: {
      fichier: "OASIS-2.STEP",
      assemblage_racine: "OASIS-2",
      unite_native: "po",
      poteaux_detectes: 4,
      entraxe_poteaux_x_po: 99.813,
      entraxe_poteaux_z_po: 94.48
    }
  },
  {
    id: "oasis-midnight-xl",
    nom: "Oasis Midnight XL — Short Side (XL SM / 101.27\" × 92.75\")",
    code_interne: "XL SM (3D: D-006398)",
    gamme: "Oasis",
    active_in_ui: true,
    type: "hot_tub",
    orientation_entree: "Short Side (Côté 92.75 po)",
    unite: "po",
    source_fichiers: [
      "OASIS FOOTPRINT AND ELEVATION.pdf",
      "Overall Dimensions - 2026-04-24.xlsx",
      "Revision mesures legend, Endless Pools, Oasis, Evolution, et Oasis XL V3.xlsx",
      "OASIS MIDNIGHT XL (SHORT SIDE).STEP"
    ],
    degagement_colonnes: {
      longueur: 101.27,
      largeur: 92.75,
      longueur_cao: 101.0,
      largeur_cao: 92.75,
      diagonale: 133.75,
      largeur_entree: 52.0
    },
    joint_etancheite: {
      longueur_min: 75.0,
      longueur_max: 100.27,
      largeur_min: 70.0,
      largeur_max: 91.75,
      rayon_min: 4.0,
      rayon_recommande: 8.0,
      largeur_bande: 3.5,
      surface_plane_min: 1.25,
      coquille_min_longueur: 74.0,
      coquille_min_largeur: 69.0
    },
    hauteur: {
      spa_min: 34.0,
      spa_max: 48.0,
      poteau_fixe: 76.0,
      poteau_deploye: 92.125,
      epaisseur_toit: 22.875,
      epaisseur_cadre_u: 4.0,
      course_elevation: 48.0,
      hauteur_max_hors_tout: 115.0
    },
    toit_hors_tout: {
      longueur: 109.0,
      largeur: 100.5,
      longueur_avec_operateur: 115.3,
      fondation_longueur: 121.0,
      fondation_largeur: 106.0,
      c_position_moteur: 36.1,
      roller_shade_longueur: 100.5,
      roller_shade_largeur: 95.2
    },
    degagement_installation: {
      maintenance_moteur_entree: 24.0,
      maintenance_cotes: 6.0,
      poteau_patio_min: 0.5
    },
    validation_cao: {
      fichier: "OASIS MIDNIGHT XL (SHORT SIDE).STEP",
      assemblage_racine: "OASIS XL SHORT SIDE",
      unite_native: "mm",
      poteaux_detectes: 4,
      entraxe_poteaux_x_po: 94.48,
      entraxe_poteaux_z_po: 102.963
    }
  },
  {
    id: "oasis-midnight-plus",
    nom: "Oasis Midnight PLUS — Long Side (PLUS LM / 95.75\" × 98\")",
    code_interne: "PLUS LM (3D: D-006398)",
    gamme: "Oasis",
    active_in_ui: true,
    type: "hot_tub",
    orientation_entree: "Long Side (Côté 98 po)",
    unite: "po",
    source_fichiers: [
      "OASIS FOOTPRINT AND ELEVATION.pdf",
      "Overall Dimensions - 2026-04-24.xlsx",
      "Revision mesures legend, Endless Pools, Oasis, Evolution, et Oasis XL V3.xlsx",
      "OASIS MIDNIGHT PLUS (LONG SIDE).STEP"
    ],
    degagement_colonnes: {
      longueur: 95.75,
      largeur: 98.0,
      longueur_cao: 96.0,
      largeur_cao: 98.0,
      diagonale: 133.75,
      largeur_entree: 57.0
    },
    joint_etancheite: {
      longueur_min: 70.0,
      longueur_max: 94.75,
      largeur_min: 75.0,
      largeur_max: 97.0,
      rayon_min: 4.0,
      rayon_recommande: 8.0,
      largeur_bande: 3.5,
      surface_plane_min: 1.25,
      coquille_min_longueur: 69.0,
      coquille_min_largeur: 74.0
    },
    hauteur: {
      spa_min: 34.0,
      spa_max: 48.0,
      poteau_fixe: 76.0,
      poteau_deploye: 92.125,
      epaisseur_toit: 22.875,
      epaisseur_cadre_u: 4.0,
      course_elevation: 48.0,
      hauteur_max_hors_tout: 115.0
    },
    toit_hors_tout: {
      longueur: 103.5,
      largeur: 105.75,
      longueur_avec_operateur: 108.15,
      fondation_longueur: 116.0,
      fondation_largeur: 112.0,
      c_position_moteur: 39.0,
      roller_shade_longueur: 95.2,
      roller_shade_largeur: 100.5
    },
    degagement_installation: {
      maintenance_moteur_entree: 24.0,
      maintenance_cotes: 6.0,
      poteau_patio_min: 0.5
    },
    validation_cao: {
      fichier: "OASIS MIDNIGHT PLUS (LONG SIDE).STEP",
      assemblage_racine: "OASIS MIDNIGHT XL (LONG SIDE)",
      unite_native: "mm",
      poteaux_detectes: 4,
      entraxe_poteaux_x_po: 99.717,
      entraxe_poteaux_z_po: 97.766
    }
  }
];

// ============================================================================
// ÉTAT DE L'APPLICATION
// ============================================================================
const state = {
  allModels: [],
  oasisModels: [],
  selectedModel: null,

  // Unité d'affichage ("po" ou "mm")
  unit: "po",

  // Dimensions du spa stockées en pouces (po)
  spa: {
    lengthIn: 84.0,
    widthIn: 84.0,
    heightIn: 38.0,
    cornerRadiusIn: 8.0,
    radiusAutoDetected: false,
    flatRimWidthIn: 2.5, // Largeur de la surface plane d'appui (min requis : 1.0 po)
    detectedRimWidthIn: null,
    cornersData: null,
    sealLandingAnalysis: null
  },

  // Côté où se situe le moteur / opérateur ("top", "bottom", "left", "right")
  // L'entrée (Entrance I) est automatiquement sur le côté opposé.
  motorSide: "top",

  // Référence d'épaisseur de toit pour le calcul de dépassement poteau ("dome" ou "uframe")
  roofRefMode: "dome",

  // Résultat courant du Fit Engine
  fitResult: null,
  recommendation: null,

  // Vue de dessus 2D (Pan, Zoom, Rotation par pas de 90°, Image détourée, Étalonnage)
  topView: {
    zoom: 1.0,
    panX: 0,
    panY: 0,
    isPanning: false,
    panStartX: 0,
    panStartY: 0,
    rotationDeg: 0, // Strictement 0, 90, 180 ou 270
    showFoundation: true,
    showSealZone: true,
    showSealLanding: true, // Affiche la surface d'appui en rose (bande du rebord plat)
    showRiskFlags: true,   // Affiche les drapeaux d'alerte et d'obstacles sur le pourtour
    riskPinHitBoxes: [],   // Zones cliquables/survolables des drapeaux d'alerte
    hoveredRiskPin: null,  // Épingle survolée pour afficher la tooltip HUD
    activeFocusedRiskId: null, // Épingle mise en surbrillance depuis le panneau latéral
    image: null, // Image rognée et détourée (sans vide autour du spa)
    rawImageSize: null,
    croppedSize: null,
    detectedRadiusNormalized: null, // R_px / W_crop
    detectedRimWidthPx: null,
    rawObstacles: [],
    autoFitToSpa: true, // Calage 100% automatique sur les dimensions L×l du spa
    imageOpacity: 0.85,
    imagePixelsPerInch: null,
    cadSvgImg: null, // Image SVG vectorielle CAO usine (authentique LibreDWG)
    showCadVector: true, // Affichage du tracé CAO usine 1:1
    cadVectorOpacity: 0.9,
    calibration: {
      active: false,
      p1: null,
      p2: null,
      mousePos: null,
      lockedAxis: null // "H" (Horizontal) ou "V" (Vertical) — jamais en angle
    }
  },

  // Vue d'élévation Z (Position Fermée = 0, Position Ouverte = 1)
  elevation: {
    isOpen: false,
    liftProgress: 0.0,
    animFrameId: null
  }
};

// ============================================================================
// UTILITAIRES DE FORMATAGE ET D'UNITÉS
// ============================================================================
function inToDisplay(valIn, decimals = 2) {
  if (state.unit === "mm") {
    return (valIn * INCH_TO_MM).toFixed(decimals === 2 ? 0 : decimals);
  }
  return Number(valIn).toFixed(decimals);
}

function formatUnit(valIn, decimals = 2) {
  if (state.unit === "mm") {
    return `${Math.round(valIn * INCH_TO_MM)} mm`;
  }
  return `${Number(valIn).toFixed(decimals)} po`;
}

function formatDualUnit(valIn, decimals = 2) {
  const poStr = `${Number(valIn).toFixed(decimals)}"`;
  const mmStr = `${Math.round(valIn * INCH_TO_MM)} mm`;
  return state.unit === "po" ? `${poStr} (${mmStr})` : `${mmStr} (${poStr})`;
}

function displayToIn(valDisplay) {
  const num = parseFloat(valDisplay);
  if (isNaN(num)) return 0;
  return state.unit === "mm" ? num / INCH_TO_MM : num;
}

// ============================================================================
// VISION PAR ORDINATEUR : DÉTOURAGE DU VIDE, AUTO-FIT & EXTRAPOLATION DU RAYON
// ============================================================================
/**
 * Analyse une image de spa importée :
 * 1. Détecte la couleur de fond (transparente ou fond blanc/clair/uni) en échantillonnant le pourtour.
 * 2. Retire tout le vide autour du spa et filtre rigoureusement les bordures 1px et cadres de capture.
 * 3. Mesure géométriquement les 4 rayons de courbure individuels (TL, TR, BL, BR) sans faux positifs.
 * 4. Détecte la surface d'appui du rebord (Seal Landing Surface) et identifie les obstacles (clavier, appuis-tête).
 * 5. Rend transparent l'extérieur des coins arrondis du spa pour un détourage net.
 */
function autoCropAndAnalyzeSpaImage(sourceImg) {
  const w = sourceImg.width;
  const h = sourceImg.height;

  const tempCanvas = document.createElement("canvas");
  tempCanvas.width = w;
  tempCanvas.height = h;
  const ctx = tempCanvas.getContext("2d", { willReadFrequently: true });
  ctx.drawImage(sourceImg, 0, 0);

  let imgData, data;
  try {
    imgData = ctx.getImageData(0, 0, w, h);
    data = imgData.data;
  } catch (err) {
    console.warn("Tainted canvas: getImageData failed under local file protocol, using fallback dimensions.", err);
    // Graceful fallback to image dimensions and standard spa proportions without crashing:
    const fallbackCropW = w;
    const fallbackCropH = h;
    const fallbackRadiusPx = Math.min(w, h) * 0.08;
    return {
      dataUrl: sourceImg.src,
      rawW: w,
      rawH: h,
      cropW: fallbackCropW,
      cropH: fallbackCropH,
      medianR_px: fallbackRadiusPx,
      radiusNormalized: 0.08,
      cornersPx: {
        tl: { name: "Nord-Ouest (Haut-Gauche)", stepPx: Math.round(fallbackRadiusPx / 3.414), rPx: fallbackRadiusPx },
        tr: { name: "Nord-Est (Haut-Droite)", stepPx: Math.round(fallbackRadiusPx / 3.414), rPx: fallbackRadiusPx },
        bl: { name: "Sud-Ouest (Bas-Gauche)", stepPx: Math.round(fallbackRadiusPx / 3.414), rPx: fallbackRadiusPx },
        br: { name: "Sud-Est (Bas-Droite)", stepPx: Math.round(fallbackRadiusPx / 3.414), rPx: fallbackRadiusPx }
      },
      detectedRimWidthPx: Math.min(w, h) * 0.05,
      rawObstacles: []
    };
  }

  // 1. Échantillonnage de la couleur d'arrière-plan
  // Échantillonne les 4 marges intérieures en sautant 8 px pour ignorer tout cadre de capture
  const marginOffset = Math.max(8, Math.floor(Math.min(w, h) * 0.025));
  let bgR = 255, bgG = 255, bgB = 255;
  let transparentCount = 0;
  let rSum = 0, gSum = 0, bSum = 0, opaqueCount = 0;

  for (let x = marginOffset; x < w - marginOffset; x += Math.max(2, Math.floor(w / 40))) {
    const idxTop = (marginOffset * w + x) * 4;
    const idxBot = ((h - 1 - marginOffset) * w + x) * 4;
    for (const idx of [idxTop, idxBot]) {
      if (data[idx + 3] < 50) {
        transparentCount++;
      } else {
        rSum += data[idx]; gSum += data[idx + 1]; bSum += data[idx + 2]; opaqueCount++;
      }
    }
  }
  for (let y = marginOffset; y < h - marginOffset; y += Math.max(2, Math.floor(h / 40))) {
    const idxL = (y * w + marginOffset) * 4;
    const idxR = (y * w + (w - 1 - marginOffset)) * 4;
    for (const idx of [idxL, idxR]) {
      if (data[idx + 3] < 50) {
        transparentCount++;
      } else {
        rSum += data[idx]; gSum += data[idx + 1]; bSum += data[idx + 2]; opaqueCount++;
      }
    }
  }

  const isTransparentBg = transparentCount > (opaqueCount + transparentCount) * 0.4;
  if (opaqueCount > 0) {
    bgR = rSum / opaqueCount;
    bgG = gSum / opaqueCount;
    bgB = bSum / opaqueCount;
  }

  // Vérifie si un pixel appartient au spa (acrylique ou composants intérieurs)
  const isSpaPixel = (x, y) => {
    if (x < 0 || x >= w || y < 0 || y >= h) return false;
    const i = (y * w + x) * 4;
    const a = data[i + 3];
    if (a < 55) return false;
    if (isTransparentBg) return true;
    const r = data[i], g = data[i + 1], b = data[i + 2];
    const dist = Math.hypot(r - bgR, g - bgG, b - bgB);
    return dist > 11.5;
  };

  // Détecte si un pixel porte la teinte rose (comme dans le dessin annoté par l'utilisateur)
  const isPinkPixel = (x, y) => {
    if (x < 0 || x >= w || y < 0 || y >= h) return false;
    const i = (y * w + x) * 4;
    const r = data[i], g = data[i + 1], b = data[i + 2];
    return r > 200 && b > 195 && (r - g > 12 || b - g > 12);
  };

  // 2. Détection robuste des 4 limites tangentes du spa (Left, Right, Top, Bottom)
  // Balayage de la zone médiane (35% à 65%) : insensible aux fines bordures 1px de capture d'écran
  const midXStart = Math.floor(w * 0.35);
  const midXEnd = Math.floor(w * 0.65);
  const midYStart = Math.floor(h * 0.35);
  const midYEnd = Math.floor(h * 0.65);

  const topHits = [];
  const botHits = [];
  for (let x = midXStart; x <= midXEnd; x += Math.max(1, Math.floor(w / 50))) {
    for (let y = 8; y < midYStart; y++) {
      if (isSpaPixel(x, y) && isSpaPixel(x, y + 2) && isSpaPixel(x, y + 4)) {
        topHits.push(y);
        break;
      }
    }
    for (let y = h - 9; y > midYEnd; y--) {
      if (isSpaPixel(x, y) && isSpaPixel(x, y - 2) && isSpaPixel(x, y - 4)) {
        botHits.push(y);
        break;
      }
    }
  }

  const leftHits = [];
  const rightHits = [];
  for (let y = midYStart; y <= midYEnd; y += Math.max(1, Math.floor(h / 50))) {
    for (let x = 8; x < midXStart; x++) {
      if (isSpaPixel(x, y) && isSpaPixel(x + 2, y) && isSpaPixel(x + 4, y)) {
        leftHits.push(x);
        break;
      }
    }
    for (let x = w - 9; x > midXEnd; x--) {
      if (isSpaPixel(x, y) && isSpaPixel(x - 2, y) && isSpaPixel(x - 4, y)) {
        rightHits.push(x);
        break;
      }
    }
  }

  const medianOf = (arr, fallback) => {
    if (!arr || !arr.length) return fallback;
    const sorted = [...arr].sort((a, b) => a - b);
    return sorted[Math.floor(sorted.length / 2)];
  };

  const top = medianOf(topHits, 12);
  const bottom = medianOf(botHits, h - 13);
  const left = medianOf(leftHits, 12);
  const right = medianOf(rightHits, w - 13);

  const cropW = Math.max(1, right - left + 1);
  const cropH = Math.max(1, bottom - top + 1);

  // 3. Mesure géométrique individuelle des 4 rayons de coins (TL, TR, BL, BR)
  // Depuis chaque sommet cartésien 90° (apex) vers l'intérieur :
  // d_diag = step * sqrt(2), donc R_px = d_diag / (sqrt(2) - 1) ≈ step * 3.41421356
  const cornerDefs = [
    { key: "tl", name: "Nord-Ouest (Haut-Gauche)", x0: left, y0: top, dx: 1, dy: 1 },
    { key: "tr", name: "Nord-Est (Haut-Droite)", x0: right, y0: top, dx: -1, dy: 1 },
    { key: "bl", name: "Sud-Ouest (Bas-Gauche)", x0: left, y0: bottom, dx: 1, dy: -1 },
    { key: "br", name: "Sud-Est (Bas-Droite)", x0: right, y0: bottom, dx: -1, dy: -1 }
  ];

  const maxSearchStep = Math.floor(Math.min(cropW, cropH) * 0.32);
  const cornersPx = {};
  const radiiPxList = [];

  for (const c of cornerDefs) {
    let bestStep = Math.floor(Math.min(cropW, cropH) * 0.08); // fallback réaliste ~8%
    for (let s = 1; s < maxSearchStep; s++) {
      const px = Math.round(c.x0 + c.dx * s);
      const py = Math.round(c.y0 + c.dy * s);
      const px2 = Math.round(c.x0 + c.dx * (s + 2));
      const py2 = Math.round(c.y0 + c.dy * (s + 2));
      if (isSpaPixel(px, py) && isSpaPixel(px2, py2)) {
        bestStep = s;
        break;
      }
    }
    const dDiag = bestStep * Math.SQRT2;
    const rPx = dDiag / (Math.SQRT2 - 1.0);
    cornersPx[c.key] = {
      name: c.name,
      stepPx: bestStep,
      rPx
    };
    radiiPxList.push(rPx);
  }

  radiiPxList.sort((a, b) => a - b);
  const medianR_px = radiiPxList[Math.floor(radiiPxList.length / 2)];
  const avgCropDim = (cropW + cropH) / 2.0;
  // Plage réaliste de rayon normalisé [3%, 25%]
  const radiusNormalized = Math.max(0.035, Math.min(0.24, medianR_px / avgCropDim));

  // 4. Analyse du rebord supérieur (Seal Landing Lip) & détection d'obstacles
  const sampleRim = (side) => {
    const widths = [];
    const darkIntrusions = [];
    const isHoriz = side === "top" || side === "bottom";
    const steps = 30;

    for (let i = 2; i < steps - 2; i++) {
      const t = i / steps;
      let xOuter, yOuter, stepDx = 0, stepDy = 0;
      if (side === "top") {
        xOuter = left + Math.floor(t * cropW);
        yOuter = top;
        stepDy = 1;
      } else if (side === "bottom") {
        xOuter = left + Math.floor(t * cropW);
        yOuter = bottom;
        stepDy = -1;
      } else if (side === "left") {
        xOuter = left;
        yOuter = top + Math.floor(t * cropH);
        stepDx = 1;
      } else {
        xOuter = right;
        yOuter = top + Math.floor(t * cropH);
        stepDx = -1;
      }

      let rimPx = 0;
      let hasDarkSpot = false;
      const maxRim = Math.floor(Math.min(cropW, cropH) * 0.22);

      // Échantillonner la couleur de référence de l'acrylique sur le rebord externe (s = 2..4)
      let baseR = 0, baseG = 0, baseB = 0, baseCount = 0;
      for (let bs = 2; bs <= 4; bs++) {
        const bx = xOuter + stepDx * bs;
        const by = yOuter + stepDy * bs;
        if (bx >= 0 && bx < w && by >= 0 && by < h) {
          const bidx = (by * w + bx) * 4;
          baseR += data[bidx];
          baseG += data[bidx + 1];
          baseB += data[bidx + 2];
          baseCount++;
        }
      }
      if (baseCount > 0) {
        baseR /= baseCount;
        baseG /= baseCount;
        baseB /= baseCount;
      }
      const baseLum = 0.299 * baseR + 0.587 * baseG + 0.114 * baseB;

      let prevR = baseR, prevG = baseG, prevB = baseB;
      for (let s = 1; s < maxRim; s++) {
        const sx = xOuter + stepDx * s;
        const sy = yOuter + stepDy * s;
        if (sx < 0 || sx >= w || sy < 0 || sy >= h) break;

        if (isPinkPixel(sx, sy)) {
          rimPx++;
          continue;
        }

        const idx = (sy * w + sx) * 4;
        const r = data[idx], g = data[idx + 1], b = data[idx + 2];
        const lum = 0.299 * r + 0.587 * g + 0.114 * b;
        const stepGrad = Math.hypot(r - prevR, g - prevG, b - prevB);
        const diffFromBase = Math.hypot(r - baseR, g - baseG, b - baseB);

        // Détection d'obstacle localisé sur le rebord (clavier sombre, coussin, poignée)
        if (s < 28 && ((baseLum > 140 && lum < 85) || (baseLum <= 140 && Math.abs(lum - baseLum) > 55))) {
          hasDarkSpot = true;
        }

        // Continuité du rebord plat :
        // 1. Sur acrylique clair : lum > 165
        // 2. Sur acrylique sombre (Slate, Black, Tuscan Sun) : continuité de teinte avant la rupture de pente du bassin
        // Une rupture de gradient (> 32 px) ou un écart de teinte important (> 45 px) après 6 px indique la descente du bassin
        const isLightRim = lum > 165;
        const isDarkRimContinuous = baseLum <= 140 && diffFromBase < 45 && stepGrad < 30;

        if (isLightRim || isDarkRimContinuous || (s <= 10 && stepGrad < 25)) {
          rimPx++;
          prevR = r; prevG = g; prevB = b;
        } else {
          break;
        }
      }

      if (rimPx > 4) widths.push(rimPx);
      if (hasDarkSpot) {
        darkIntrusions.push({ side, t, x: xOuter, y: yOuter, residualPx: rimPx });
      }
    }

    return {
      widthPx: widths.length ? medianOf(widths, cropW * 0.055) : cropW * 0.055,
      darkIntrusions
    };
  };

  const rimTop = sampleRim("top");
  const rimBottom = sampleRim("bottom");
  const rimLeft = sampleRim("left");
  const rimRight = sampleRim("right");

  const detectedRimWidthPx = Math.min(
    rimTop.widthPx,
    rimBottom.widthPx,
    rimLeft.widthPx,
    rimRight.widthPx
  );

  const rawObstacles = [
    ...rimTop.darkIntrusions,
    ...rimBottom.darkIntrusions,
    ...rimLeft.darkIntrusions,
    ...rimRight.darkIntrusions
  ];

  // 5. Création de l'image rognée et détourée (fond extérieur transparent)
  const cropCanvas = document.createElement("canvas");
  cropCanvas.width = cropW;
  cropCanvas.height = cropH;
  const cropCtx = cropCanvas.getContext("2d");
  const cropImgData = cropCtx.createImageData(cropW, cropH);
  const outData = cropImgData.data;

  for (let y = 0; y < cropH; y++) {
    for (let x = 0; x < cropW; x++) {
      const srcIdx = ((top + y) * w + (left + x)) * 4;
      const dstIdx = (y * cropW + x) * 4;

      const inCornerZone =
        (x < medianR_px * 1.15 && y < medianR_px * 1.15) ||
        (x > cropW - medianR_px * 1.15 && y < medianR_px * 1.15) ||
        (x < medianR_px * 1.15 && y > cropH - medianR_px * 1.15) ||
        (x > cropW - medianR_px * 1.15 && y > cropH - medianR_px * 1.15);

      if (inCornerZone && !isSpaPixel(left + x, top + y)) {
        outData[dstIdx + 3] = 0;
      } else {
        outData[dstIdx] = data[srcIdx];
        outData[dstIdx + 1] = data[srcIdx + 1];
        outData[dstIdx + 2] = data[srcIdx + 2];
        outData[dstIdx + 3] = data[srcIdx + 3];
      }
    }
  }
  cropCtx.putImageData(cropImgData, 0, 0);

  let outDataUrl = "";
  try {
    outDataUrl = cropCanvas.toDataURL("image/png");
  } catch (e) {
    outDataUrl = sourceImg.src;
  }

  return {
    dataUrl: outDataUrl,
    rawW: w,
    rawH: h,
    cropW,
    cropH,
    medianR_px,
    radiusNormalized,
    cornersPx,
    detectedRimWidthPx,
    rawObstacles
  };
}

/**
 * Calcule et applique le rayon de coin en pouces et la largeur de rebord plat
 * à partir des mesures géométriques détectées sur l'image et des dimensions courantes du spa.
 */
function applyExtrapolatedRadiusFromImage() {
  if (!state.topView.detectedRadiusNormalized) return;
  const avgSpaDimIn = (state.spa.lengthIn + state.spa.widthIn) / 2.0;
  let rIn = state.topView.detectedRadiusNormalized * avgSpaDimIn;
  // Arrondi au 0.25 po le plus proche dans une plage physique réaliste [2.0", 20.0"]
  rIn = Math.max(2.0, Math.min(20.0, Math.round(rIn * 4) / 4));
  state.spa.cornerRadiusIn = rIn;
  state.spa.radiusAutoDetected = true;

  // Calcul des 4 coins individuels en pouces
  if (state.topView.cornersPx && state.topView.croppedSize) {
    const pxPerIn = (state.topView.croppedSize.w + state.topView.croppedSize.h) / (state.spa.lengthIn + state.spa.widthIn);
    const cData = {};
    for (const [k, c] of Object.entries(state.topView.cornersPx)) {
      const cornerRIn = Math.round((c.rPx / pxPerIn) * 4) / 4;
      cData[k] = {
        name: c.name,
        rIn: Math.max(1.5, Math.min(20.0, cornerRIn))
      };
    }
    state.spa.cornersData = cData;
  }

  const inputR = document.getElementById("inputCornerRadius");
  if (inputR) {
    inputR.value = inToDisplay(state.spa.cornerRadiusIn, 2);
  }
  const pillR = document.getElementById("autoRadiusPill");
  if (pillR) pillR.classList.remove("hidden");

  // Détection automatique de la largeur de rebord plat (si disponible)
  if (state.topView.detectedRimWidthPx && state.topView.croppedSize) {
    const pxPerIn = state.topView.croppedSize.w / state.spa.lengthIn;
    let rimIn = state.topView.detectedRimWidthPx / pxPerIn;
    rimIn = Math.max(0.75, Math.min(8.0, Math.round(rimIn * 4) / 4));
    state.spa.flatRimWidthIn = rimIn;
    state.spa.detectedRimWidthIn = rimIn;

    const inputRim = document.getElementById("inputFlatRimWidth");
    if (inputRim) {
      inputRim.value = inToDisplay(rimIn, 2);
    }
    const pillRim = document.getElementById("autoRimPill");
    if (pillRim) pillRim.classList.remove("hidden");
  }
}

// ============================================================================
// ANALYSE STRUCTURÉE DE LA SURFACE D'APPUI DU JOINT (SEAL LANDING & OBSTACLES)
// ============================================================================
/**
 * Règle physique SpaFit Oasis :
 * - Le dessus du spa doit offrir au moins 1.0 po (25.4 mm) de largeur plane continue (1.25" recommandé).
 * - Le rayon de coin minimal doit être d'au moins 4.0 po (102 mm).
 * - Tout obstacle (clavier Balboa surélevé, appui-tête saillant, cascade) ou rétrécissement < 1"
 *   est identifié et précisément "flaggé" comme zone à risque sur le plan 2D.
 */
function analyzeSealLandingSurface(model, spa) {
  const seal = model.joint_etancheite;
  const rMin = seal.rayon_min || 4.0;
  const rimMin = 1.0; // 1.0 pouce minimum requis par SpaFit
  const rimRec = 1.25; // 1.25 pouce recommandé

  const riskFlags = [];
  const currentRimW = spa.flatRimWidthIn || 2.5;

  // 1. Validation de la largeur de rebord plat
  const isRimCompliant = currentRimW >= rimMin;
  const isRimOptimal = currentRimW >= rimRec;

  if (!isRimCompliant) {
    riskFlags.push({
      id: "risk-narrow-rim-global",
      type: "NARROW_LIP",
      severity: "err",
      side: "top",
      xIn: 0,
      yIn: -spa.widthIn / 2 + currentRimW / 2,
      badgeText: "Rebord < 1.0\"",
      title: "Rebord plat insuffisant (< 1.0 po)",
      message: `La largeur d'appui mesurée est de ${formatUnit(currentRimW, 2)}, inférieure au minimum de ${formatUnit(rimMin, 2)}. Le joint néoprène risque de reposer dans le vide ou de ne pas comprimer hermétiquement.`,
      recommendation: "Un rebord plat minimal de 1.0 po (25.4 mm) est strictement nécessaire sur tout le pourtour pour garantir l'étanchéité."
    });
  } else if (!isRimOptimal) {
    riskFlags.push({
      id: "risk-rim-marginal",
      type: "NARROW_LIP",
      severity: "warn",
      side: "top",
      xIn: 0,
      yIn: -spa.widthIn / 2 + currentRimW / 2,
      badgeText: "Rebord limite",
      title: "Rebord plat limite (1.0 po – 1.25 po)",
      message: `Largeur d'appui de ${formatUnit(currentRimW, 2)} : conforme au seuil de 1.0 po mais sous les 1.25 po recommandés pour un contact optimal.`,
      recommendation: "Assurer un centrage rigoureux de la structure Oasis lors du montage pour que le joint ne déborde pas."
    });
  }

  // 2. Validation des rayons de coins (avec prise en compte des spas ronds)
  const isRoundSpa = spa.isRound || (spa.shape && spa.shape.toLowerCase().includes("rond")) ||
    (Math.abs(spa.lengthIn - spa.widthIn) <= 2.0 && (spa.cornerRadiusIn >= (Math.min(spa.lengthIn, spa.widthIn) / 2.0 - 4.0)));

  const corners = spa.cornersData || {
    tl: { name: "Nord-Ouest (Haut-Gauche)", rIn: spa.cornerRadiusIn, xIn: -spa.lengthIn / 2, yIn: -spa.widthIn / 2 },
    tr: { name: "Nord-Est (Haut-Droite)", rIn: spa.cornerRadiusIn, xIn: spa.lengthIn / 2, yIn: -spa.widthIn / 2 },
    bl: { name: "Sud-Ouest (Bas-Gauche)", rIn: spa.cornerRadiusIn, xIn: -spa.lengthIn / 2, yIn: spa.widthIn / 2 },
    br: { name: "Sud-Est (Bas-Droite)", rIn: spa.cornerRadiusIn, xIn: spa.lengthIn / 2, yIn: spa.widthIn / 2 }
  };

  let minObservedR = spa.cornerRadiusIn;
  if (!isRoundSpa) {
    for (const [key, c] of Object.entries(corners)) {
      const rVal = c.rIn || spa.cornerRadiusIn;
      if (rVal < minObservedR) minObservedR = rVal;
      if (rVal < rMin) {
        riskFlags.push({
          id: `risk-corner-${key}`,
          type: "RADIUS_TOO_SMALL",
          severity: "err",
          side: `corner_${key}`,
          xIn: c.xIn || (key.includes("l") ? -spa.lengthIn / 2 : spa.lengthIn / 2),
          yIn: c.yIn || (key.includes("t") ? -spa.widthIn / 2 : spa.widthIn / 2),
          badgeText: `Coin R=${rVal.toFixed(1)}" < 4"`,
          title: `Coin ${c.name} : Rayon R = ${formatUnit(rVal, 2)} (< 4.0 po)`,
          message: `Le rayon de courbure (${formatUnit(rVal, 2)}) est inférieur au seuil minimal de 4.0 po (102 mm). Le joint ne pourra pas épouser cet angle vif, générant une fuite d'air et d'eau.`,
          recommendation: "Un rayon d'au moins 4.0 po est requis. Des kits d'adaptation d'angle ou cales de coin peuvent être nécessaires."
        });
      }
    }
  }

  // 3. Détection et signalement d'obstacles réels sur le pourtour (balayage des 4 côtés : top, bottom, left, right)
  if (state.topView.rawObstacles && state.topView.rawObstacles.length > 0) {
    const sideHits = { top: [], bottom: [], left: [], right: [] };
    for (const obs of state.topView.rawObstacles) {
      if (sideHits[obs.side]) sideHits[obs.side].push(obs);
    }

    for (const [side, hits] of Object.entries(sideHits)) {
      if (hits.length === 0) continue;
      const avgT = hits.reduce((acc, h) => acc + h.t, 0) / hits.length;
      let xIn = 0, yIn = 0;
      let sideName = "";

      if (side === "top") {
        xIn = (avgT - 0.5) * spa.lengthIn;
        yIn = -spa.widthIn / 2 + currentRimW / 2;
        sideName = "Nord (Haut)";
      } else if (side === "bottom") {
        xIn = (avgT - 0.5) * spa.lengthIn;
        yIn = spa.widthIn / 2 - currentRimW / 2;
        sideName = "Sud (Bas)";
      } else if (side === "left") {
        xIn = -spa.lengthIn / 2 + currentRimW / 2;
        yIn = (avgT - 0.5) * spa.widthIn;
        sideName = "Ouest (Gauche)";
      } else if (side === "right") {
        xIn = spa.lengthIn / 2 - currentRimW / 2;
        yIn = (avgT - 0.5) * spa.widthIn;
        sideName = "Est (Droite)";
      }

      const isCenter = Math.abs(avgT - 0.5) < 0.22;
      const obsType = isCenter ? "Clavier / Écran de commande" : "Appui-tête / Cascade / Buse";

      riskFlags.push({
        id: `risk-obstacle-${side}`,
        type: "OBSTACLE_INTERFERENCE",
        severity: "warn",
        side,
        xIn,
        yIn,
        badgeText: isCenter ? "Clavier" : "Obstacle",
        title: `${obsType} — Rebord ${sideName}`,
        message: `Intrusion détectée sur la zone d'appui (${sideName}, pos=${Math.round(avgT * 100)}%). Tout composant faisant saillie au-dessus du rebord empêchera la compression hermétique du joint d'étanchéité.`,
        recommendation: "Vérifier que le composant est affleurant sous le plan de contact du joint, ou retirer l'appui-tête amovible avant fermeture."
      });
    }
  }

  // 4. Trace du joint d'étanchéité (ligne médiane du joint sur le toit)
  const sNomL = (seal.longueur_min + seal.longueur_max) / 2.0;
  const sNomW = (seal.largeur_min + seal.largeur_max) / 2.0;

  return {
    isRimCompliant,
    isRimOptimal,
    currentRimW,
    minObservedR,
    minRadiusCompliant: minObservedR >= rMin,
    riskFlags,
    sNomL,
    sNomW
  };
}


// ============================================================================
// VOLET 2 : MOTEUR DE CALCUL ET DE VALIDATION (FIT ENGINE)
// ============================================================================
function evaluateFit(model, spa, roofRefMode = "dome") {
  const colX = model.degagement_colonnes.longueur;
  const colY = model.degagement_colonnes.largeur;

  // 1. Dégagements horizontaux (X et Y)
  const marginX = (colX - spa.lengthIn) / 2.0;
  const marginY = (colY - spa.widthIn) / 2.0;

  const getMarginStatus = (m) => {
    if (m >= 1.25) return "ok";
    if (m >= 0.5) return "warn";
    return "err";
  };

  const statusX = getMarginStatus(marginX);
  const statusY = getMarginStatus(marginY);

  // 2. Empreinte du joint d'étanchéité & analyse de la surface d'appui (Seal Landing)
  const seal = model.joint_etancheite;
  const landingAnalysis = analyzeSealLandingSurface(model, spa);
  state.spa.sealLandingAnalysis = landingAnalysis;

  const lengthInSeal = spa.lengthIn >= seal.longueur_min && spa.lengthIn <= seal.longueur_max;
  const widthInSeal = spa.widthIn >= seal.largeur_min && spa.widthIn <= seal.largeur_max;

  const lengthNearSealEdge =
    lengthInSeal &&
    (spa.lengthIn - seal.longueur_min < 1.0 || seal.longueur_max - spa.lengthIn < 0.75);
  const widthNearSealEdge =
    widthInSeal &&
    (spa.widthIn - seal.largeur_min < 1.0 || seal.largeur_max - spa.widthIn < 0.75);

  let statusSealDim = "ok";
  if (!lengthInSeal || !widthInSeal || !landingAnalysis.isRimCompliant) {
    statusSealDim = "err";
  } else if (lengthNearSealEdge || widthNearSealEdge || !landingAnalysis.isRimOptimal || landingAnalysis.riskFlags.some(f => f.severity === "warn")) {
    statusSealDim = "warn";
  }

  // Vérification du rayon de coin effectif minimal (min 4.0 po selon spécification, recommandé 8.0 po)
  const isRound = spa.isRound || (spa.shape && spa.shape.toLowerCase().includes("rond")) ||
    (Math.abs(spa.lengthIn - spa.widthIn) <= 2.0 && landingAnalysis.minObservedR >= (Math.min(spa.lengthIn, spa.widthIn) / 2.0 - 4.0));

  const rMin = seal.rayon_min || 4.0;
  const rMax = isRound ? (Math.max(spa.lengthIn, spa.widthIn) / 2.0 + 4.0) : 16.0;
  let statusRadius = "ok";

  if (isRound) {
    const expectedR = (spa.lengthIn + spa.widthIn) / 4.0;
    if (Math.abs(landingAnalysis.minObservedR - expectedR) > 6.0) {
      statusRadius = "warn";
    }
  } else {
    if (landingAnalysis.minObservedR < rMin || landingAnalysis.minObservedR > rMax) {
      statusRadius = "err";
    } else if (landingAnalysis.minObservedR < 5.5 || landingAnalysis.minObservedR > 12.0) {
      statusRadius = "warn";
    }
  }

  // 3. Mécanique d'ajustement en hauteur (Axe Z)
  const hSpec = model.hauteur;
  const heightInRange = spa.heightIn >= hSpec.spa_min && spa.heightIn <= hSpec.spa_max;
  const heightNearEdge =
    heightInRange &&
    (spa.heightIn - hSpec.spa_min < 1.0 || hSpec.spa_max - spa.heightIn < 1.0);

  let statusHeight = "ok";
  if (!heightInRange) {
    statusHeight = "err";
  } else if (heightNearEdge) {
    statusHeight = "warn";
  }

  const roofThickness =
    roofRefMode === "uframe"
      ? (hSpec.epaisseur_cadre_u || 4.0)
      : hSpec.epaisseur_toit;
  const postHeightRef =
    roofRefMode === "uframe"
      ? hSpec.poteau_fixe
      : (hSpec.poteau_deploye || 92.125);

  // Formule 1 : Dépassement du poteau au-dessus du toit fermé
  const postProtrusionClosed = postHeightRef - (spa.heightIn + roofThickness);

  // Formule 2 : Hauteur libre sous toit ouvert
  const clearHeightOpen = spa.heightIn + hSpec.course_elevation;

  // Formule 3 : Hauteur totale maximale déployée
  const totalHeightDeployed = spa.heightIn + hSpec.course_elevation + roofThickness;
  const totalHeightDome = spa.heightIn + hSpec.course_elevation + hSpec.epaisseur_toit;

  const maxAllowedOverall = hSpec.hauteur_max_hors_tout || 115.0;
  let statusTotalHeight = "ok";
  if (totalHeightDome > maxAllowedOverall + 3.875) {
    statusTotalHeight = "err";
  } else if (totalHeightDome > maxAllowedOverall) {
    statusTotalHeight = "warn";
  }

  const allStatuses = [statusX, statusY, statusSealDim, statusRadius, statusHeight];
  let globalStatus = "ok";
  if (allStatuses.includes("err")) {
    globalStatus = "err";
  } else if (allStatuses.includes("warn")) {
    globalStatus = "warn";
  }

  const spaDiagonal = Math.hypot(spa.lengthIn, spa.widthIn);

  return {
    colX,
    colY,
    marginX,
    marginY,
    statusX,
    statusY,
    lengthInSeal,
    widthInSeal,
    statusSealDim,
    statusRadius,
    heightInRange,
    statusHeight,
    roofThickness,
    postHeightRef,
    postProtrusionClosed,
    clearHeightOpen,
    totalHeightDeployed,
    totalHeightDome,
    maxAllowedOverall,
    statusTotalHeight,
    globalStatus,
    spaDiagonal
  };
}

function findSmartRecommendation() {
  if (!state.selectedModel || !state.fitResult) return null;
  if (state.fitResult.globalStatus === "ok") return null;

  const rank = { ok: 3, warn: 2, err: 1 };
  const currentScore =
    rank[state.fitResult.globalStatus] * 100 +
    Math.min(state.fitResult.marginX, state.fitResult.marginY);

  let bestCandidate = null;
  let bestScore = currentScore;

  for (const m of state.oasisModels) {
    for (const swap of [false, true]) {
      const testSpa = {
        lengthIn: swap ? state.spa.widthIn : state.spa.lengthIn,
        widthIn: swap ? state.spa.lengthIn : state.spa.widthIn,
        heightIn: state.spa.heightIn,
        cornerRadiusIn: state.spa.cornerRadiusIn
      };
      const res = evaluateFit(m, testSpa, state.roofRefMode);
      const score = rank[res.globalStatus] * 100 + Math.min(res.marginX, res.marginY);
      if (score > bestScore + 0.25 && rank[res.globalStatus] >= 2) {
        bestScore = score;
        bestCandidate = {
          modelId: m.id,
          modelName: m.nom,
          swapLW: swap,
          status: res.globalStatus,
          minMargin: Math.min(res.marginX, res.marginY)
        };
      }
    }
  }
  return bestCandidate;
}

// ============================================================================
// MISE À JOUR DE L'INTERFACE UTILISATEUR (DOM)
// ============================================================================
function updateUI() {
  if (!state.selectedModel) return;

  // Si une image est chargée en mode auto-fit, met à jour l'échelle px/po automatiquement
  if (state.topView.image && state.topView.autoFitToSpa && state.topView.croppedSize) {
    const isRot90 = state.topView.rotationDeg === 90 || state.topView.rotationDeg === 270;
    const targetSpanIn = isRot90 ? state.spa.widthIn : state.spa.lengthIn;
    state.topView.imagePixelsPerInch = state.topView.croppedSize.w / targetSpanIn;
    document.getElementById("calibrationScaleBadge").textContent =
      `Auto-Fit : ${state.topView.imagePixelsPerInch.toFixed(2)} px/po (Détouré)`;
  }

  state.fitResult = evaluateFit(state.selectedModel, state.spa, state.roofRefMode);
  state.recommendation = findSmartRecommendation();

  const r = state.fitResult;
  const m = state.selectedModel;

  // 1. Badge de statut global
  const globalBadge = document.getElementById("globalStatusBadge");
  const globalText = document.getElementById("globalStatusText");
  globalBadge.className = "badge-status";
  if (r.globalStatus === "ok") {
    globalBadge.classList.add("badge-ok");
    globalText.textContent = "COMPATIBLE OASIS";
  } else if (r.globalStatus === "warn") {
    globalBadge.classList.add("badge-warn");
    globalText.textContent = "AJUSTEMENT CRITIQUE";
  } else {
    globalBadge.classList.add("badge-err");
    globalText.textContent = "INCOMPATIBLE";
  }

  // 2. Sous-labels d'unités secondaires
  const updateSecondaryLabel = (id, valIn) => {
    const el = document.getElementById(id);
    if (!el) return;
    if (state.unit === "po") {
      el.textContent = `${Math.round(valIn * INCH_TO_MM)} mm (${(valIn * 2.54).toFixed(1)} cm)`;
    } else {
      el.textContent = `${valIn.toFixed(2)} po`;
    }
  };
  updateSecondaryLabel("subSpaLength", state.spa.lengthIn);
  updateSecondaryLabel("subSpaWidth", state.spa.widthIn);
  updateSecondaryLabel("subSpaHeight", state.spa.heightIn);
  updateSecondaryLabel("subCornerRadius", state.spa.cornerRadiusIn);
  updateSecondaryLabel("subFlatRimWidth", state.spa.flatRimWidthIn || 2.5);

  document.querySelectorAll(".unit-label").forEach((el) => {
    el.textContent = state.unit;
  });

  document.getElementById("spaDiagonalInfo").textContent =
    `Diag. spa : ${formatUnit(r.spaDiagonal, 1)} / Libre : ${formatUnit(m.degagement_colonnes.diagonale || 130.75, 1)}`;

  // 3. Recommandation intelligente
  const recBox = document.getElementById("smartRecommendationBox");
  const recText = document.getElementById("smartRecommendationText");
  if (state.recommendation) {
    recBox.classList.remove("hidden");
    const actionDesc = [];
    if (state.recommendation.modelId !== m.id) {
      actionDesc.push(`passer sur « ${state.recommendation.modelName} »`);
    }
    if (state.recommendation.swapLW) {
      actionDesc.push("pivoter le spa de 90° (L ↔ l)");
    }
    recText.innerHTML = `💡 <strong>Optimisation détectée :</strong> En choisissant de ${actionDesc.join(" et ")}, la marge minimale passe à <strong>+${formatUnit(state.recommendation.minMargin, 2)}</strong>.`;
  } else {
    recBox.classList.add("hidden");
  }

  // 4. Cartes du Fit Engine — A. Dégagements Horizontaux
  document.getElementById("activeModelCodeBadge").textContent =
    m.code_interne || m.id;

  const applyCardState = (cardId, statusTextId, status, labels) => {
    const card = document.getElementById(cardId);
    const txt = document.getElementById(statusTextId);
    if (card) card.className = `metric-card metric-${status}`;
    if (txt) {
      txt.textContent = labels[status];
      txt.className =
        status === "ok"
          ? "font-bold text-emerald-400"
          : status === "warn"
          ? "font-bold text-amber-400"
          : "font-bold text-rose-400";
    }
  };

  applyCardState("cardMarginX", "statusMarginXText", r.statusX, {
    ok: "CONFORME",
    warn: "TOLÉRANCE CRITIQUE",
    err: r.marginX < 0 ? "COLLISION POTEAUX" : "DÉGAGEMENT < 0.5\""
  });
  const signX = r.marginX >= 0 ? "+" : "";
  document.getElementById("valMarginX").innerHTML =
    `${signX}${formatUnit(r.marginX, 2)} <span class="text-xs font-normal text-slate-400">/ côté</span>`;
  document.getElementById("subMarginX").textContent =
    `Entre poteaux X : ${formatUnit(r.colX, 2)} (CAO ${m.degagement_colonnes.longueur_cao || r.colX}")`;

  applyCardState("cardMarginY", "statusMarginYText", r.statusY, {
    ok: "CONFORME",
    warn: "TOLÉRANCE CRITIQUE",
    err: r.marginY < 0 ? "COLLISION POTEAUX" : "DÉGAGEMENT < 0.5\""
  });
  const signY = r.marginY >= 0 ? "+" : "";
  document.getElementById("valMarginY").innerHTML =
    `${signY}${formatUnit(r.marginY, 2)} <span class="text-xs font-normal text-slate-400">/ côté</span>`;
  document.getElementById("subMarginY").textContent =
    `Entre poteaux Y : ${formatUnit(r.colY, 2)} (CAO ${m.degagement_colonnes.largeur_cao || r.colY}")`;

  // 5. Cartes du Fit Engine — B. Empreinte et surface d'appui du joint (Seal Landing)
  const landing = state.spa.sealLandingAnalysis || analyzeSealLandingSurface(m, state.spa);
  const sealOverallStatus =
    r.statusSealDim === "err" || r.statusRadius === "err"
      ? "err"
      : r.statusSealDim === "warn" || r.statusRadius === "warn"
      ? "warn"
      : "ok";

  const sealBadge = document.getElementById("sealGlobalBadge");
  if (sealOverallStatus === "ok") {
    sealBadge.textContent = "ÉTANCHÉITÉ CONFORME";
    sealBadge.className = "text-[11px] font-bold text-emerald-400";
  } else if (sealOverallStatus === "warn") {
    sealBadge.textContent = "ATTENTION D'ÉTANCHÉITÉ";
    sealBadge.className = "text-[11px] font-bold text-amber-400";
  } else {
    sealBadge.textContent = "RISQUE DE FUITE JOINT";
    sealBadge.className = "text-[11px] font-bold text-rose-400";
  }

  document.getElementById("cardSealFootprint").className = `metric-card metric-${r.statusSealDim}`;
  const s = m.joint_etancheite;
  document.getElementById("valSealFootprint").textContent =
    `L: [${formatUnit(s.longueur_min, 0)}–${formatUnit(s.longueur_max, 0)}] • l: [${formatUnit(s.largeur_min, 0)}–${formatUnit(s.largeur_max, 0)}]`;
  document.getElementById("subSealFootprint").textContent =
    r.lengthInSeal && r.widthInSeal
      ? `Empreinte couvercle Oasis`
      : `⚠ Spa hors de l'empreinte du joint !`;

  // Carte Surface d'appui (Rebord plat)
  const landingCard = document.getElementById("cardSealLanding");
  const landingStatusText = document.getElementById("statusSealLandingText");
  const landingVal = document.getElementById("valSealLanding");
  const landingSub = document.getElementById("subSealLanding");

  const rimStatus = landing.isRimCompliant ? (landing.isRimOptimal ? "ok" : "warn") : "err";
  if (landingCard) landingCard.className = `metric-card metric-${rimStatus}`;
  if (landingStatusText) {
    landingStatusText.textContent = landing.isRimCompliant ? (landing.isRimOptimal ? "≥ 1.25\" OPTIMAL" : "≥ 1.0\" LIMITE") : "< 1.0\" RISQUE";
    landingStatusText.className = landing.isRimCompliant ? (landing.isRimOptimal ? "font-bold text-emerald-400" : "font-bold text-amber-400") : "font-bold text-rose-400";
  }
  if (landingVal) landingVal.textContent = formatDualUnit(landing.currentRimW, 2);
  if (landingSub) landingSub.textContent = landing.isRimCompliant ? "Contact hermétique continu" : "Largeur trop étroite (< 1\")";

  // Carte Rayon de coin (R)
  applyCardState("cardCornerRadius", "statusRadiusText", r.statusRadius, {
    ok: state.spa.radiusAutoDetected ? "AUTO-EXTRAPOLÉ" : "OPTIMAL",
    warn: "TOLÉRANCE LIMITE",
    err: landing.minObservedR < 4 ? "RAYON < 4\" (FUITE)" : "RAYON TROP GRAND"
  });
  document.getElementById("valCornerRadius").textContent =
    `R = ${formatDualUnit(landing.minObservedR, 2)}`;
  document.getElementById("subCornerRadiusSpec").textContent =
    `Min requis : ${formatUnit(s.rayon_min || 4, 1)} | Rec. : ${formatUnit(s.rayon_recommande || 8, 1)}`;

  // Liste interactive des points à risque sur le pourtour
  const risksBadge = document.getElementById("sealRisksCountBadge");
  const risksList = document.getElementById("sealRisksList");
  if (risksBadge && risksList) {
    const flags = landing.riskFlags;
    const errCount = flags.filter(f => f.severity === "err").length;
    const warnCount = flags.filter(f => f.severity === "warn").length;

    if (flags.length === 0) {
      risksBadge.textContent = "0 risque détecté (Conforme)";
      risksBadge.className = "text-[10px] font-mono px-1.5 py-0.2 rounded bg-emerald-950 text-emerald-300 border border-emerald-800";
      risksList.innerHTML = `
        <div class="text-[11px] text-emerald-300/90 bg-emerald-950/40 border border-emerald-800/60 rounded px-2.5 py-1.5 flex items-center gap-1.5">
          <span>✓</span>
          <span>Surface d'appui plane ≥ 1.0 po et coins R ≥ 4.0 po continus sur tout le pourtour.</span>
        </div>
      `;
    } else {
      risksBadge.textContent = `${flags.length} risque${flags.length > 1 ? "s" : ""} (${errCount} critique${errCount > 1 ? "s" : ""}, ${warnCount} attention)`;
      risksBadge.className = errCount > 0
        ? "text-[10px] font-mono px-1.5 py-0.2 rounded bg-rose-950 text-rose-300 border border-rose-800"
        : "text-[10px] font-mono px-1.5 py-0.2 rounded bg-amber-950 text-amber-300 border border-amber-800";

      risksList.innerHTML = flags.map(f => `
        <div class="risk-item-card risk-${f.severity} cursor-pointer" onclick="focusRiskPinOnCanvas('${f.id}')" title="Cliquer pour afficher l'emplacement exact sur le plan">
          <div class="flex items-start gap-1.5 flex-1 min-w-0">
            <span class="text-sm select-none">${f.severity === "err" ? "🚫" : "⚠️"}</span>
            <div class="min-w-0 flex-1">
              <div class="font-bold text-[11px] ${f.severity === "err" ? "text-rose-300" : "text-amber-300"} truncate">
                ${f.title}
              </div>
              <div class="text-[10px] text-slate-400 line-clamp-2">
                ${f.message}
              </div>
            </div>
          </div>
          <button type="button" class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 hover:bg-slate-700 text-sky-300 border border-slate-700 whitespace-nowrap">
            Localiser
          </button>
        </div>
      `).join("");
    }
  }

  // 6. Cartes du Fit Engine — C. Mécanique d'ajustement en hauteur (Axe Z)
  applyCardState("cardSpaHeight", "statusHeightText", r.statusHeight, {
    ok: "CONFORME",
    warn: "LIMITE PLAGE",
    err: "HORS PLAGE Z"
  });
  document.getElementById("valSpaHeightCheck").textContent =
    `${formatUnit(state.spa.heightIn, 1)} ∈ [${formatUnit(m.hauteur.spa_min, 0)}, ${formatUnit(m.hauteur.spa_max, 0)}]`;

  const protSign = r.postProtrusionClosed >= 0 ? "+" : "";
  document.getElementById("cardPostProtrusion").className =
    `metric-card metric-${r.postProtrusionClosed >= 0 ? "ok" : "warn"}`;
  document.getElementById("valPostProtrusion").textContent =
    `${protSign}${formatDualUnit(r.postProtrusionClosed, 2)}`;
  document.getElementById("subPostProtrusion").textContent =
    `${r.postHeightRef}" - (${state.spa.heightIn.toFixed(1)}" + ${r.roofThickness}")`;

  document.getElementById("valClearHeightOpen").textContent =
    formatDualUnit(r.clearHeightOpen, 2);
  document.getElementById("subClearHeightOpen").textContent =
    `H_spa (${state.spa.heightIn.toFixed(1)}") + Course (${m.hauteur.course_elevation}")`;

  applyCardState("cardTotalDeployed", "statusTotalHeightText", r.statusTotalHeight, {
    ok: "OK",
    warn: "> 115\" MANUEL",
    err: "OBSTACLE HAUT"
  });
  document.getElementById("valTotalDeployed").textContent =
    formatDualUnit(r.totalHeightDeployed, 2);
  document.getElementById("subTotalDeployed").textContent =
    `Faîtage dôme : ${formatUnit(r.totalHeightDome, 2)} (Réf max: ${formatUnit(r.maxAllowedOverall, 0)})`;

  // 7. Résumé technique du modèle Oasis sélectionné
  const grid = document.getElementById("modelSpecsSummaryGrid");
  const cad = m.validation_cao || {};
  const sideLabels = { top: "Haut (Nord)", bottom: "Bas (Sud)", left: "Gauche (Ouest)", right: "Droite (Est)" };
  grid.innerHTML = `
    <div><span class="text-slate-500">Toit hors-tout (E×B):</span> <span class="text-slate-200">${formatUnit(m.toit_hors_tout.longueur, 2)} × ${formatUnit(m.toit_hors_tout.largeur, 2)}</span></div>
    <div><span class="text-slate-500">Avec opérateur (A):</span> <span class="text-slate-200">${formatUnit(m.toit_hors_tout.longueur_avec_operateur || m.toit_hors_tout.longueur, 2)}</span></div>
    <div><span class="text-slate-500">Fondation min (D×A):</span> <span class="text-slate-200">${formatUnit(m.toit_hors_tout.fondation_longueur || 118, 0)} × ${formatUnit(m.toit_hors_tout.fondation_largeur || 106, 0)}</span></div>
    <div><span class="text-slate-500">Moteur (${sideLabels[state.motorSide]}):</span> <span class="text-sky-300">C = ${formatUnit(m.toit_hors_tout.c_position_moteur || 36.1, 1)}</span></div>
    <div><span class="text-slate-500">Fichier STEP CAO:</span> <span class="text-sky-300">${cad.fichier || "OASIS-2.STEP"}</span></div>
    <div><span class="text-slate-500">Entraxe CAO 3D:</span> <span class="text-emerald-300">${cad.entraxe_poteaux_x_po || 99.81}" × ${cad.entraxe_poteaux_z_po || 94.48}"</span></div>
  `;

  drawTopView();
  drawElevationView();
}

// ============================================================================
// PRIMITIVES GRAPHIQUES 2D PARTAGÉES (CANVAS INTERACTIF + EXPORT PLAN HD)
// ============================================================================
function drawRoundedRectPath(ctx, x, y, w, h, r) {
  const radius = Math.max(0, Math.min(r, w / 2, h / 2));
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + w - radius, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + radius);
  ctx.lineTo(x + w, y + h - radius);
  ctx.quadraticCurveTo(x + w, y + h, x + w - radius, y + h);
  ctx.lineTo(x + radius, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();
}

function drawDimensionLine(ctx, x1, y1, x2, y2, label, color = "#38bdf8", offset = 0, fontSize = 11) {
  ctx.save();
  ctx.strokeStyle = color;
  ctx.fillStyle = color;
  ctx.lineWidth = 1.4;

  const dx = x2 - x1;
  const dy = y2 - y1;
  const len = Math.hypot(dx, dy);
  if (len < 6) {
    ctx.restore();
    return;
  }
  const ux = dx / len;
  const uy = dy / len;
  const nx = -uy;
  const ny = ux;

  const sx1 = x1 + nx * offset;
  const sy1 = y1 + ny * offset;
  const sx2 = x2 + nx * offset;
  const sy2 = y2 + ny * offset;

  // Lignes de rappel si offset != 0
  if (Math.abs(offset) > 3) {
    ctx.save();
    ctx.strokeStyle = color;
    ctx.globalAlpha = 0.4;
    ctx.lineWidth = 1;
    ctx.setLineDash([2, 2]);
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(sx1, sy1);
    ctx.moveTo(x2, y2);
    ctx.lineTo(sx2, sy2);
    ctx.stroke();
    ctx.restore();
  }

  ctx.beginPath();
  ctx.moveTo(sx1, sy1);
  ctx.lineTo(sx2, sy2);
  ctx.stroke();

  const arrowSize = 5.5;
  ctx.beginPath();
  ctx.moveTo(sx1, sy1);
  ctx.lineTo(sx1 + ux * arrowSize + nx * (arrowSize * 0.5), sy1 + uy * arrowSize + ny * (arrowSize * 0.5));
  ctx.lineTo(sx1 + ux * arrowSize - nx * (arrowSize * 0.5), sy1 + uy * arrowSize - ny * (arrowSize * 0.5));
  ctx.closePath();
  ctx.fill();

  ctx.beginPath();
  ctx.moveTo(sx2, sy2);
  ctx.lineTo(sx2 - ux * arrowSize + nx * (arrowSize * 0.5), sy2 - uy * arrowSize + ny * (arrowSize * 0.5));
  ctx.lineTo(sx2 - ux * arrowSize - nx * (arrowSize * 0.5), sy2 - uy * arrowSize - ny * (arrowSize * 0.5));
  ctx.closePath();
  ctx.fill();

  if (label) {
    const mx = (sx1 + sx2) / 2;
    const my = (sy1 + sy2) / 2;
    ctx.font = `600 ${fontSize}px 'JetBrains Mono', monospace`;
    const metrics = ctx.measureText(label);
    const padX = 6;
    const boxW = metrics.width + padX * 2;
    const boxH = fontSize + 6;

    ctx.fillStyle = "rgba(15, 23, 42, 0.94)";
    ctx.fillRect(mx - boxW / 2, my - boxH / 2, boxW, boxH);
    ctx.strokeStyle = color;
    ctx.lineWidth = 1;
    ctx.strokeRect(mx - boxW / 2, my - boxH / 2, boxW, boxH);

    ctx.fillStyle = color;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";
    ctx.fillText(label, mx, my + 0.5);
  }
  ctx.restore();
}

/**
 * Dessine la scène complète de la Vue de dessus 2D (Footprint Oasis + Moteur + Spa + Cotes)
 * centrée en (0, 0) avec l'échelle `scale` (pixels par pouce).
 */
function renderTopDownScene(ctx, scale, options = {}) {
  const m = state.selectedModel;
  const r = state.fitResult;
  const showFoundation = options.showFoundation ?? state.topView.showFoundation;
  const showSealZone = options.showSealZone ?? state.topView.showSealZone;
  const isExport = Boolean(options.isExport);

  const fndL = m.toit_hors_tout.fondation_longueur || 118.0;
  const fndW = m.toit_hors_tout.fondation_largeur || 106.0;
  const roofL = m.toit_hors_tout.longueur;
  const roofW = m.toit_hors_tout.largeur;
  const colInX = m.degagement_colonnes.longueur;
  const colInY = m.degagement_colonnes.largeur;

  // -------------------------------------------------------------------------
  // 1. DALLE DE FONDATION MINIMALE & DÉGAGEMENT DE MAINTENANCE (24" et 6")
  // -------------------------------------------------------------------------
  if (showFoundation) {
    // Le dégagement de maintenance est de 24" côté moteur & entrée, et 6" sur les 2 autres côtés
    const isMotorTopBottom = state.motorSide === "top" || state.motorSide === "bottom";
    const clearX = isMotorTopBottom ? 6.0 : 24.0;
    const clearY = isMotorTopBottom ? 24.0 : 6.0;
    const maintL = roofL + clearX * 2;
    const maintW = roofW + clearY * 2;

    ctx.save();
    ctx.strokeStyle = "rgba(148, 163, 184, 0.38)";
    ctx.fillStyle = "rgba(15, 23, 42, 0.25)";
    ctx.lineWidth = 1.2;
    ctx.setLineDash([6, 6]);
    ctx.fillRect((-maintL / 2) * scale, (-maintW / 2) * scale, maintL * scale, maintW * scale);
    ctx.strokeRect((-maintL / 2) * scale, (-maintW / 2) * scale, maintL * scale, maintW * scale);
    ctx.setLineDash([]);

    ctx.fillStyle = "rgba(148, 163, 184, 0.72)";
    ctx.font = "500 10px 'Inter', sans-serif";
    ctx.textAlign = "right";
    ctx.fillText(
      `Zone maintenance recommandée (24" moteur/entrée, 6" côtés)`,
      (maintL / 2) * scale - 6,
      (maintW / 2) * scale - 6
    );

    // Dalle de fondation minimale (D x A)
    ctx.strokeStyle = "rgba(148, 163, 184, 0.65)";
    ctx.lineWidth = 1.5;
    ctx.strokeRect((-fndL / 2) * scale, (-fndW / 2) * scale, fndL * scale, fndW * scale);
    ctx.fillStyle = "#cbd5e1";
    ctx.font = "600 10px 'JetBrains Mono', monospace";
    ctx.textAlign = "left";
    ctx.fillText(
      `Fondation min : ${formatUnit(fndL, 0)} × ${formatUnit(fndW, 0)}`,
      (-fndL / 2) * scale + 6,
      (-fndW / 2) * scale + 13
    );
    ctx.restore();
  }

  // -------------------------------------------------------------------------
  // 2. IMAGE DU SPA DÉTOURÉE & AUTO-ÉTALLONNÉE (AVEC ROTATION 0°/90°/180°/270°)
  // -------------------------------------------------------------------------
  if (state.topView.image) {
    ctx.save();
    ctx.globalAlpha = state.topView.imageOpacity;

    const img = state.topView.image;
    const rotRad = (state.topView.rotationDeg * Math.PI) / 180;
    const isRot90 = state.topView.rotationDeg === 90 || state.topView.rotationDeg === 270;

    let drawW_px, drawH_px;
    if (state.topView.autoFitToSpa) {
      // Le vide ayant été retiré autour du spa, l'image rognée correspond exactement à L_spa × l_spa
      drawW_px = (isRot90 ? state.spa.widthIn : state.spa.lengthIn) * scale;
      drawH_px = (isRot90 ? state.spa.lengthIn : state.spa.widthIn) * scale;
    } else if (state.topView.imagePixelsPerInch && state.topView.imagePixelsPerInch > 0) {
      drawW_px = (img.width / state.topView.imagePixelsPerInch) * scale;
      drawH_px = (img.height / state.topView.imagePixelsPerInch) * scale;
    } else {
      drawW_px = state.spa.lengthIn * scale;
      drawH_px = state.spa.widthIn * scale;
    }

    // Masque d'écrêtage aux coins arrondis du spa pour un rendu ultra-propre
    ctx.save();
    drawRoundedRectPath(
      ctx,
      (-state.spa.lengthIn / 2) * scale,
      (-state.spa.widthIn / 2) * scale,
      state.spa.lengthIn * scale,
      state.spa.widthIn * scale,
      state.spa.cornerRadiusIn * scale
    );
    ctx.clip();

    ctx.rotate(rotRad);
    ctx.drawImage(img, -drawW_px / 2, -drawH_px / 2, drawW_px, drawH_px);
    ctx.restore();
    ctx.restore();
  }

  // -------------------------------------------------------------------------
  // 2.B TRACÉ VECTORIEL CAO FACTORY AUTHENTIQUE (LibreDWG DXF/SVG 1:1)
  // -------------------------------------------------------------------------
  if (state.topView.cadSvgImg && state.topView.showCadVector) {
    ctx.save();
    ctx.globalAlpha = state.topView.cadVectorOpacity || 0.9;

    const cadImg = state.topView.cadSvgImg;
    const rotRad = (state.topView.rotationDeg * Math.PI) / 180;
    const isRot90 = state.topView.rotationDeg === 90 || state.topView.rotationDeg === 270;
    const drawW_px = (isRot90 ? state.spa.widthIn : state.spa.lengthIn) * scale;
    const drawH_px = (isRot90 ? state.spa.lengthIn : state.spa.widthIn) * scale;

    ctx.save();
    drawRoundedRectPath(
      ctx,
      (-state.spa.lengthIn / 2) * scale,
      (-state.spa.widthIn / 2) * scale,
      state.spa.lengthIn * scale,
      state.spa.widthIn * scale,
      state.spa.cornerRadiusIn * scale
    );
    ctx.clip();

    ctx.rotate(rotRad);
    ctx.drawImage(cadImg, -drawW_px / 2, -drawH_px / 2, drawW_px, drawH_px);
    ctx.restore();
    ctx.restore();
  }

  // -------------------------------------------------------------------------
  // 3. CONTOUR EXTÉRIEUR DU TOIT OASIS + POSITION EXACTE DU MOTEUR (C) & ENTRÉE (I)
  // -------------------------------------------------------------------------
  ctx.save();
  ctx.strokeStyle = "#38bdf8";
  ctx.lineWidth = 2;
  ctx.setLineDash([8, 5]);
  ctx.strokeRect((-roofL / 2) * scale, (-roofW / 2) * scale, roofL * scale, roofW * scale);
  ctx.setLineDash([]);

  // Positionnement fidèle du MOTEUR (cote C depuis la face interne du poteau),
  // du CONDUIT ÉLECTRIQUE et de l'ENTRÉE opposée (cote I) selon state.motorSide
  const motorOffsetC = m.toit_hors_tout.c_position_moteur || 36.1;
  const entranceSpanI = m.degagement_colonnes.largeur_entree || 52.0;
  const motorBoxLen = 11.5 * scale;
  const motorBoxThick = 6.2 * scale;
  const conduitBoxLen = 15.0 * scale;
  const conduitBoxThick = 4.6 * scale;

  const drawMotorAndEntrance = () => {
    ctx.save();
    if (state.motorSide === "top" || state.motorSide === "bottom") {
      const signY = state.motorSide === "top" ? -1 : 1;
      const frameEdgeY = signY * (roofW / 2) * scale;
      const postInnerLeftX = (-colInX / 2) * scale;

      // Cote C depuis la face interne du poteau gauche jusqu'au bord/axe du moteur
      const motorCenterX = postInnerLeftX + motorOffsetC * scale;
      const motorTopY = state.motorSide === "top" ? frameEdgeY - motorBoxThick : frameEdgeY;

      // Boîtier MOTEUR (doit être supporté par la fondation)
      ctx.fillStyle = "rgba(56, 189, 248, 0.25)";
      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 1.8;
      ctx.fillRect(motorCenterX - motorBoxLen / 2, motorTopY, motorBoxLen, motorBoxThick);
      ctx.strokeRect(motorCenterX - motorBoxLen / 2, motorTopY, motorBoxLen, motorBoxThick);

      ctx.fillStyle = "#e0f2fe";
      ctx.font = "700 9.5px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText("MOTOR", motorCenterX, motorTopY + motorBoxThick / 2 + 3);

      // Boîtier Conduit Électrique (entre le poteau gauche et le moteur)
      const conduitCenterX = postInnerLeftX + (motorOffsetC * 0.45) * scale;
      const conduitTopY = state.motorSide === "top" ? frameEdgeY - conduitBoxThick : frameEdgeY;
      ctx.fillStyle = "rgba(148, 163, 184, 0.2)";
      ctx.strokeStyle = "#94a3b8";
      ctx.lineWidth = 1.2;
      ctx.fillRect(conduitCenterX - conduitBoxLen / 2, conduitTopY, conduitBoxLen, conduitBoxThick);
      ctx.strokeRect(conduitCenterX - conduitBoxLen / 2, conduitTopY, conduitBoxLen, conduitBoxThick);
      ctx.fillStyle = "#cbd5e1";
      ctx.font = "600 8px 'Inter', sans-serif";
      ctx.fillText("CONDUIT ÉLEC.", conduitCenterX, conduitTopY + conduitBoxThick / 2 + 2.5);

      // Ligne de cote (C) du poteau gauche au moteur
      const dimOffset = state.motorSide === "top" ? -motorBoxThick - 12 : motorBoxThick + 12;
      drawDimensionLine(
        ctx,
        postInnerLeftX,
        frameEdgeY,
        motorCenterX,
        frameEdgeY,
        `C = ${formatUnit(motorOffsetC, 1)}`,
        "#38bdf8",
        dimOffset,
        10
      );

      // ENTRÉE (I) sur le côté opposé
      const entEdgeY = -signY * (roofW / 2) * scale;
      const entPx = entranceSpanI * scale;
      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      ctx.moveTo(-entPx / 2, entEdgeY);
      ctx.lineTo(entPx / 2, entEdgeY);
      ctx.stroke();

      ctx.fillStyle = "#38bdf8";
      ctx.font = "700 10px 'Inter', sans-serif";
      ctx.textAlign = "center";
      const labelOffsetY = state.motorSide === "top" ? 15 : -8;
      ctx.fillText(
        `ENTRÉE (I = ${formatUnit(entranceSpanI, 0)})`,
        0,
        entEdgeY + labelOffsetY
      );
    } else {
      // Moteur à Gauche ("left") ou à Droite ("right")
      const signX = state.motorSide === "left" ? -1 : 1;
      const frameEdgeX = signX * (roofL / 2) * scale;
      const postInnerTopY = (-colInY / 2) * scale;

      const motorCenterY = postInnerTopY + motorOffsetC * scale;
      const motorLeftX = state.motorSide === "left" ? frameEdgeX - motorBoxThick : frameEdgeX;

      ctx.fillStyle = "rgba(56, 189, 248, 0.25)";
      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 1.8;
      ctx.fillRect(motorLeftX, motorCenterY - motorBoxLen / 2, motorBoxThick, motorBoxLen);
      ctx.strokeRect(motorLeftX, motorCenterY - motorBoxLen / 2, motorBoxThick, motorBoxLen);

      ctx.save();
      ctx.translate(motorLeftX + motorBoxThick / 2, motorCenterY);
      ctx.rotate(-Math.PI / 2);
      ctx.fillStyle = "#e0f2fe";
      ctx.font = "700 9.5px 'JetBrains Mono', monospace";
      ctx.textAlign = "center";
      ctx.fillText("MOTOR", 0, 3);
      ctx.restore();

      // Conduit électrique
      const conduitCenterY = postInnerTopY + (motorOffsetC * 0.45) * scale;
      const conduitLeftX = state.motorSide === "left" ? frameEdgeX - conduitBoxThick : frameEdgeX;
      ctx.fillStyle = "rgba(148, 163, 184, 0.2)";
      ctx.strokeStyle = "#94a3b8";
      ctx.lineWidth = 1.2;
      ctx.fillRect(conduitLeftX, conduitCenterY - conduitBoxLen / 2, conduitBoxThick, conduitBoxLen);
      ctx.strokeRect(conduitLeftX, conduitCenterY - conduitBoxLen / 2, conduitBoxThick, conduitBoxLen);

      // Ligne de cote (C)
      const dimOffset = state.motorSide === "left" ? -motorBoxThick - 14 : motorBoxThick + 14;
      drawDimensionLine(
        ctx,
        frameEdgeX,
        postInnerTopY,
        frameEdgeX,
        motorCenterY,
        `C = ${formatUnit(motorOffsetC, 1)}`,
        "#38bdf8",
        dimOffset,
        10
      );

      // ENTRÉE (I) sur le côté opposé
      const entEdgeX = -signX * (roofL / 2) * scale;
      const entPx = entranceSpanI * scale;
      ctx.strokeStyle = "#38bdf8";
      ctx.lineWidth = 3.5;
      ctx.beginPath();
      ctx.moveTo(entEdgeX, -entPx / 2);
      ctx.lineTo(entEdgeX, entPx / 2);
      ctx.stroke();

      ctx.save();
      ctx.translate(entEdgeX + (state.motorSide === "left" ? 14 : -14), 0);
      ctx.rotate(-Math.PI / 2);
      ctx.fillStyle = "#38bdf8";
      ctx.font = "700 10px 'Inter', sans-serif";
      ctx.textAlign = "center";
      ctx.fillText(`ENTRÉE (I = ${formatUnit(entranceSpanI, 0)})`, 0, 0);
      ctx.restore();
    }
    ctx.restore();
  };

  drawMotorAndEntrance();
  ctx.restore();

  // -------------------------------------------------------------------------
  // 4. BANDE D'APPUI DU JOINT (SURFACE D'APPUI DU REBORD PLAT EN ROSE ≥ 1.0 PO)
  // -------------------------------------------------------------------------
  const seal = m.joint_etancheite;
  const landing = state.spa.sealLandingAnalysis || analyzeSealLandingSurface(m, state.spa);
  const showSealLanding = options.showSealLanding ?? state.topView.showSealLanding;
  const showRiskFlags = options.showRiskFlags ?? state.topView.showRiskFlags;

  if (showSealLanding) {
    ctx.save();
    const rimPx = (landing.currentRimW || 2.5) * scale;
    const outerW = state.spa.lengthIn * scale;
    const outerH = state.spa.widthIn * scale;
    const outerR = state.spa.cornerRadiusIn * scale;
    const innerW = Math.max(6, outerW - 2 * rimPx);
    const innerH = Math.max(6, outerH - 2 * rimPx);
    const innerR = Math.max(0, outerR - rimPx);

    // Dessin de la surface plane en bande rose (identique à l'annotation fournie par l'utilisateur)
    ctx.beginPath();
    drawRoundedRectPath(ctx, -outerW / 2, -outerH / 2, outerW, outerH, outerR);
    drawRoundedRectPath(ctx, -innerW / 2, -innerH / 2, innerW, innerH, innerR);
    ctx.fillStyle = "rgba(244, 114, 182, 0.28)"; // Rose translucide
    ctx.fill("evenodd");

    // Ligne limite extérieure rose
    ctx.strokeStyle = "rgba(244, 114, 182, 0.85)";
    ctx.lineWidth = 1.8;
    drawRoundedRectPath(ctx, -outerW / 2, -outerH / 2, outerW, outerH, outerR);
    ctx.stroke();

    // Ligne limite intérieure (début de la descente vers le bassin intérieur)
    ctx.strokeStyle = "rgba(244, 114, 182, 0.65)";
    ctx.lineWidth = 1.2;
    ctx.setLineDash([4, 3]);
    drawRoundedRectPath(ctx, -innerW / 2, -innerH / 2, innerW, innerH, innerR);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.restore();
  }

  // -------------------------------------------------------------------------
  // 5. TRACE ET EMPREINTE DU JOINT D'ÉTANCHÉITÉ SPAFIT
  // -------------------------------------------------------------------------
  if (showSealZone) {
    ctx.save();
    // Ligne médiane du joint d'étanchéité (sous le toit)
    const sL = (seal.longueur_min + seal.longueur_max) / 2.0 * scale;
    const sW = (seal.largeur_min + seal.largeur_max) / 2.0 * scale;
    const sR = Math.max(4.0, state.spa.cornerRadiusIn) * scale;

    ctx.strokeStyle = "#10b981"; // Vert émeraude haute visibilité
    ctx.lineWidth = 2.4;
    ctx.setLineDash([6, 4]);
    drawRoundedRectPath(ctx, -sL / 2, -sW / 2, sL, sW, sR);
    ctx.stroke();
    ctx.setLineDash([]);

    // Bande de tolérance min/max du joint
    const sMaxL = seal.longueur_max * scale;
    const sMaxW = seal.largeur_max * scale;
    const sMinL = seal.longueur_min * scale;
    const sMinW = seal.largeur_min * scale;

    ctx.beginPath();
    ctx.rect(-sMaxL / 2, -sMaxW / 2, sMaxL, sMaxW);
    ctx.rect(-sMinL / 2, -sMinW / 2, sMinL, sMinW);
    ctx.fillStyle = "rgba(16, 185, 129, 0.08)";
    ctx.fill("evenodd");
    ctx.restore();
  }

  // -------------------------------------------------------------------------
  // 5. CONTOUR THÉORIQUE DU SPA (AVEC RAYON R ET BANDE DE JOINT 3.5")
  // -------------------------------------------------------------------------
  ctx.save();
  const spaW_px = state.spa.lengthIn * scale;
  const spaH_px = state.spa.widthIn * scale;
  const spaR_px = state.spa.cornerRadiusIn * scale;

  const spaStrokeColor =
    r.globalStatus === "ok"
      ? "#34d399"
      : r.globalStatus === "warn"
      ? "#fbbf24"
      : "#f87171";
  const spaFillColor = state.topView.image
    ? "rgba(15, 23, 42, 0.05)"
    : r.globalStatus === "ok"
    ? "rgba(16, 185, 129, 0.14)"
    : r.globalStatus === "warn"
    ? "rgba(245, 158, 11, 0.14)"
    : "rgba(239, 68, 68, 0.16)";

  drawRoundedRectPath(ctx, -spaW_px / 2, -spaH_px / 2, spaW_px, spaH_px, spaR_px);
  ctx.fillStyle = spaFillColor;
  ctx.fill();
  ctx.lineWidth = 2.2;
  ctx.strokeStyle = spaStrokeColor;
  ctx.stroke();

  // Cartouche central du spa (lisible même par-dessus une photo)
  const labelBoxW = 210;
  const labelBoxH = 38;
  ctx.fillStyle = "rgba(15, 23, 42, 0.88)";
  ctx.strokeStyle = spaStrokeColor;
  ctx.lineWidth = 1.2;
  drawRoundedRectPath(ctx, -labelBoxW / 2, -labelBoxH / 2, labelBoxW, labelBoxH, 6);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = "#f8fafc";
  ctx.font = "700 11.5px 'Inter', sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(
    `SPA : ${formatUnit(state.spa.lengthIn, 1)} × ${formatUnit(state.spa.widthIn, 1)}`,
    0,
    -5
  );
  ctx.fillStyle = "#bae6fd";
  ctx.font = "600 10.5px 'JetBrains Mono', monospace";
  ctx.fillText(
    `H: ${formatUnit(state.spa.heightIn, 1)} • R: ${formatUnit(state.spa.cornerRadiusIn, 2)}`,
    0,
    10
  );
  ctx.restore();

  // -------------------------------------------------------------------------
  // 5.B DRAPEAUX D'ALERTE ET D'OBSTACLES SUR LE POURTOUR (RISK CALLOUTS)
  // -------------------------------------------------------------------------
  if (!isExport) {
    state.topView.riskPinHitBoxes = [];
  }

  if (showRiskFlags && landing.riskFlags && landing.riskFlags.length > 0) {
    ctx.save();
    for (const flag of landing.riskFlags) {
      const pinX = flag.xIn * scale;
      const pinY = flag.yIn * scale;

      let badgeOffsetX = 0;
      let badgeOffsetY = 0;
      if (flag.side === "bottom") {
        badgeOffsetY = 32;
      } else if (flag.side === "top") {
        badgeOffsetY = -32;
      } else if (flag.side === "left") {
        badgeOffsetX = -40;
      } else if (flag.side === "right") {
        badgeOffsetX = 40;
      } else if (flag.side.includes("corner")) {
        const signX = flag.xIn >= 0 ? 1 : -1;
        const signY = flag.yIn >= 0 ? 1 : -1;
        badgeOffsetX = signX * 28;
        badgeOffsetY = signY * 28;
      }

      const bx = pinX + badgeOffsetX;
      const by = pinY + badgeOffsetY;
      const isErr = flag.severity === "err";
      const pinColor = isErr ? "#ef4444" : "#f59e0b";
      const isFocused = state.topView.activeFocusedRiskId === flag.id;

      // Ligne de rappel
      ctx.beginPath();
      ctx.strokeStyle = pinColor;
      ctx.lineWidth = 1.5;
      ctx.setLineDash([3, 2]);
      ctx.moveTo(pinX, pinY);
      ctx.lineTo(bx, by);
      ctx.stroke();
      ctx.setLineDash([]);

      // Point d'ancrage sur le rebord
      ctx.fillStyle = pinColor;
      ctx.beginPath();
      ctx.arc(pinX, pinY, 4.5, 0, Math.PI * 2);
      ctx.fill();

      // Badge d'alerte callout
      const badgeW = 92;
      const badgeH = 22;

      if (isFocused) {
        ctx.strokeStyle = "#38bdf8";
        ctx.lineWidth = 3;
        drawRoundedRectPath(ctx, bx - badgeW / 2 - 3, by - badgeH / 2 - 3, badgeW + 6, badgeH + 6, 7);
        ctx.stroke();
      }

      ctx.fillStyle = isErr ? "rgba(220, 38, 38, 0.94)" : "rgba(217, 119, 6, 0.94)";
      ctx.strokeStyle = isErr ? "#fca5a5" : "#fde68a";
      ctx.lineWidth = 1.2;
      drawRoundedRectPath(ctx, bx - badgeW / 2, by - badgeH / 2, badgeW, badgeH, 5);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = "#ffffff";
      ctx.font = "700 9.5px 'Inter', sans-serif";
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      const icon = isErr ? "🚫" : "⚠️";
      ctx.fillText(`${icon} ${flag.badgeText || "Risque"}`, bx, by + 0.5);

      if (!isExport) {
        state.topView.riskPinHitBoxes.push({
          id: flag.id,
          x: bx,
          y: by,
          w: badgeW,
          h: badgeH,
          flag
        });
      }
    }
    ctx.restore();
  }

  // -------------------------------------------------------------------------
  // 6. EMPLACEMENT ET EMPREINTE DES 4 POTEAUX OASIS AUX COINS (D-000139)
  // -------------------------------------------------------------------------
  const postThickX = (roofL - colInX) / 2.0;
  const postThickY = (roofW - colInY) / 2.0;

  ctx.save();
  ctx.strokeStyle = "rgba(251, 191, 36, 0.45)";
  ctx.lineWidth = 1.1;
  ctx.strokeRect((-colInX / 2) * scale, (-colInY / 2) * scale, colInX * scale, colInY * scale);

  // Diagonale H entre poteaux
  ctx.beginPath();
  ctx.setLineDash([3, 5]);
  ctx.strokeStyle = "rgba(251, 191, 36, 0.3)";
  ctx.moveTo((-colInX / 2) * scale, (colInY / 2) * scale);
  ctx.lineTo((colInX / 2) * scale, (-colInY / 2) * scale);
  ctx.stroke();
  ctx.setLineDash([]);

  for (const [sx, sy] of [
    [-1, -1],
    [1, -1],
    [1, 1],
    [-1, 1]
  ]) {
    const px = sx < 0 ? (-colInX / 2 - postThickX) * scale : (colInX / 2) * scale;
    const py = sy < 0 ? (-colInY / 2 - postThickY) * scale : (colInY / 2) * scale;
    const pw = postThickX * scale;
    const ph = postThickY * scale;

    ctx.fillStyle = "rgba(245, 158, 11, 0.88)";
    ctx.strokeStyle = "#fef08a";
    ctx.lineWidth = 1.6;
    drawRoundedRectPath(ctx, px, py, pw, ph, 2.5);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = "#0f172a";
    ctx.beginPath();
    ctx.arc(px + pw / 2, py + ph / 2, 2.2, 0, Math.PI * 2);
    ctx.fill();
  }
  ctx.restore();

  // -------------------------------------------------------------------------
  // 7. LIGNES DE COTES DE DÉGAGEMENT (MARGE X GAUCHE/DROITE, MARGE Y HAUT/BAS)
  // -------------------------------------------------------------------------
  const colorX = r.statusX === "ok" ? "#34d399" : r.statusX === "warn" ? "#fbbf24" : "#f87171";
  const colorY = r.statusY === "ok" ? "#34d399" : r.statusY === "warn" ? "#fbbf24" : "#f87171";

  if (Math.abs(r.marginX) >= 0.15) {
    // Marge X Gauche
    drawDimensionLine(
      ctx,
      (-colInX / 2) * scale,
      0,
      (-state.spa.lengthIn / 2) * scale,
      0,
      `Marge X: ${formatUnit(r.marginX, 2)}`,
      colorX,
      -32
    );
    if (isExport) {
      // Marge X Droite également sur le plan d'export
      drawDimensionLine(
        ctx,
        (state.spa.lengthIn / 2) * scale,
        0,
        (colInX / 2) * scale,
        0,
        `Marge X: ${formatUnit(r.marginX, 2)}`,
        colorX,
        32
      );
    }
  }

  if (Math.abs(r.marginY) >= 0.15) {
    // Marge Y Haut
    drawDimensionLine(
      ctx,
      0,
      (-colInY / 2) * scale,
      0,
      (-state.spa.widthIn / 2) * scale,
      `Marge Y: ${formatUnit(r.marginY, 2)}`,
      colorY,
      44
    );
    if (isExport) {
      // Marge Y Bas sur le plan d'export
      drawDimensionLine(
        ctx,
        0,
        (state.spa.widthIn / 2) * scale,
        0,
        (colInY / 2) * scale,
        `Marge Y: ${formatUnit(r.marginY, 2)}`,
        colorY,
        -44
      );
    }
  }

  // Cote intérieure totale entre colonnes X (G) et Y (F)
  drawDimensionLine(
    ctx,
    (-colInX / 2) * scale,
    (-colInY / 2) * scale,
    (colInX / 2) * scale,
    (-colInY / 2) * scale,
    `Entre poteaux X (G) = ${formatUnit(colInX, 2)}`,
    "#fbbf24",
    16
  );

  drawDimensionLine(
    ctx,
    (-colInX / 2) * scale,
    (colInY / 2) * scale,
    (-colInX / 2) * scale,
    (-colInY / 2) * scale,
    `Entre poteaux Y (F) = ${formatUnit(colInY, 2)}`,
    "#fbbf24",
    18
  );
}

function drawTopView() {
  const canvas = document.getElementById("topViewCanvas");
  if (!canvas || !state.selectedModel || !state.fitResult) return;

  const rect = canvas.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  if (canvas.width !== Math.floor(rect.width * dpr) || canvas.height !== Math.floor(rect.height * dpr)) {
    canvas.width = Math.floor(rect.width * dpr);
    canvas.height = Math.floor(rect.height * dpr);
  }

  const ctx = canvas.getContext("2d");
  ctx.save();
  ctx.scale(dpr, dpr);

  const W = rect.width;
  const H = rect.height;
  ctx.clearRect(0, 0, W, H);

  const maxWorldSpanIn = 160;
  const basePxPerIn = Math.min(W, H) / maxWorldSpanIn;
  const scale = basePxPerIn * state.topView.zoom;

  const cx = W / 2 + state.topView.panX;
  const cy = H / 2 + state.topView.panY;

  ctx.save();
  ctx.translate(cx, cy);

  renderTopDownScene(ctx, scale, { isExport: false });

  // -------------------------------------------------------------------------
  // OUTIL D'ÉTALONNAGE MANUEL ORTHOGONAL À 2 POINTS (VERROUILLÉ 90° H OU V)
  // -------------------------------------------------------------------------
  if (state.topView.calibration.active || state.topView.calibration.p1) {
    const cal = state.topView.calibration;
    const drawMarker = (pt, label) => {
      ctx.save();
      ctx.strokeStyle = "#f59e0b";
      ctx.fillStyle = "#f59e0b";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(pt.x, pt.y, 6, 0, Math.PI * 2);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(pt.x - 10, pt.y);
      ctx.lineTo(pt.x + 10, pt.y);
      ctx.moveTo(pt.x, pt.y - 10);
      ctx.lineTo(pt.x, pt.y + 10);
      ctx.stroke();
      ctx.font = "700 11px 'JetBrains Mono', monospace";
      ctx.fillText(label, pt.x + 10, pt.y - 8);
      ctx.restore();
    };

    if (cal.p1) {
      drawMarker(cal.p1, "P1");
      const targetPt = cal.p2 || cal.mousePos;
      if (targetPt) {
        ctx.save();
        ctx.strokeStyle = "#f59e0b";
        ctx.lineWidth = 2.2;
        ctx.setLineDash([5, 4]);
        ctx.beginPath();
        ctx.moveTo(cal.p1.x, cal.p1.y);
        ctx.lineTo(targetPt.x, targetPt.y);
        ctx.stroke();
        ctx.setLineDash([]);

        // Badge indiquant l'axe orthogonal verrouillé (HORIZONTAL 0° ou VERTICAL 90°)
        const mx = (cal.p1.x + targetPt.x) / 2;
        const my = (cal.p1.y + targetPt.y) / 2;
        const axisLabel = Math.abs(targetPt.x - cal.p1.x) >= Math.abs(targetPt.y - cal.p1.y)
          ? "AXE HORIZONTAL (0°)"
          : "AXE VERTICAL (90°)";
        ctx.fillStyle = "rgba(15, 23, 42, 0.9)";
        ctx.fillRect(mx - 68, my - 22, 136, 16);
        ctx.fillStyle = "#fbbf24";
        ctx.font = "700 9.5px 'JetBrains Mono', monospace";
        ctx.textAlign = "center";
        ctx.fillText(axisLabel, mx, my - 11);
        ctx.restore();
      }
    }
    if (cal.p2) {
      drawMarker(cal.p2, "P2 (90°)");
    }
  }

  // -------------------------------------------------------------------------
  // TOOLTIP HUD INTERACTIF AU SURVOL D'UN DRAPEAU D'ALERTE / OBSTACLE
  // -------------------------------------------------------------------------
  if (state.topView.hoveredRiskPin) {
    const hp = state.topView.hoveredRiskPin;
    const f = hp.flag;
    const isErr = f.severity === "err";

    ctx.save();
    const tooltipW = 290;
    const tooltipH = 92;
    let tx = hp.x - tooltipW / 2;
    let ty = hp.y - tooltipH - 18;

    // Confinement dans la zone visible
    if (tx + cx < 15) tx = -cx + 15;
    if (tx + cx + tooltipW > W - 15) tx = W - cx - 15 - tooltipW;
    if (ty + cy < 15) ty = hp.y + 24;

    ctx.fillStyle = "rgba(15, 23, 42, 0.96)";
    ctx.strokeStyle = isErr ? "#ef4444" : "#f59e0b";
    ctx.lineWidth = 1.6;
    drawRoundedRectPath(ctx, tx, ty, tooltipW, tooltipH, 8);
    ctx.fill();
    ctx.stroke();

    ctx.fillStyle = isErr ? "#f87171" : "#fbbf24";
    ctx.font = "700 11px 'Inter', sans-serif";
    ctx.textAlign = "left";
    ctx.textBaseline = "top";
    const icon = isErr ? "🚫" : "⚠️";
    ctx.fillText(`${icon} ${f.title}`, tx + 10, ty + 10);

    ctx.fillStyle = "#e2e8f0";
    ctx.font = "400 9.5px 'Inter', sans-serif";
    const words = (f.message || "").split(" ");
    let line = "";
    let lineY = ty + 28;
    for (const w of words) {
      const test = line + w + " ";
      if (ctx.measureText(test).width > tooltipW - 20) {
        ctx.fillText(line, tx + 10, lineY);
        line = w + " ";
        lineY += 13;
        if (lineY > ty + 56) break;
      } else {
        line = test;
      }
    }
    ctx.fillText(line, tx + 10, lineY);

    ctx.fillStyle = "#38bdf8";
    ctx.font = "600 9px 'Inter', sans-serif";
    ctx.fillText("💡 " + (f.recommendation || "Vérifier le dégagement."), tx + 10, ty + tooltipH - 15);
    ctx.restore();
  }

  ctx.restore();
  ctx.restore();
}

/**
 * Centre et met en surbrillance une épingle de risque depuis le clic dans la barre latérale
 */
window.focusRiskPinOnCanvas = function(riskId) {
  state.topView.activeFocusedRiskId = riskId;
  const landing = state.spa.sealLandingAnalysis;
  if (!landing) return;
  const flag = landing.riskFlags.find((f) => f.id === riskId);
  if (flag) {
    const pin = state.topView.riskPinHitBoxes.find((p) => p.id === riskId);
    if (pin) {
      state.topView.hoveredRiskPin = pin;
    } else {
      state.topView.hoveredRiskPin = {
        id: flag.id,
        x: flag.xIn * 6.5 * state.topView.zoom,
        y: flag.yIn * 6.5 * state.topView.zoom,
        flag
      };
    }
  }
  drawTopView();
};

// ============================================================================
// VOLET 3.3 : RENDU DU CANEVAS 2D — VUE DE PROFIL D'ÉLÉVATION (AXE Z)
// ============================================================================
function renderElevationScene(ctx, W, H, liftProgress) {
  const m = state.selectedModel;
  const r = state.fitResult;

  const groundY = H - 36;
  const topMargin = 24;
  const maxZ_in = 126.0;
  const scale = (groundY - topMargin) / maxZ_in;
  const cx = W / 2;

  const zToY = (zIn) => groundY - zIn * scale;

  // 1. Ligne de plafond maximal (115 po)
  const maxRefY = zToY(r.maxAllowedOverall);
  ctx.save();
  ctx.strokeStyle = "rgba(245, 158, 11, 0.38)";
  ctx.lineWidth = 1;
  ctx.setLineDash([6, 4]);
  ctx.beginPath();
  ctx.moveTo(35, maxRefY);
  ctx.lineTo(W - 35, maxRefY);
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.fillStyle = "rgba(251, 191, 36, 0.85)";
  ctx.font = "600 10px 'JetBrains Mono', monospace";
  ctx.textAlign = "right";
  ctx.fillText(`Plafond spéc. max Oasis : ${formatDualUnit(r.maxAllowedOverall, 0)}`, W - 40, maxRefY - 5);
  ctx.restore();

  // 2. Sol (Z = 0) et dalle de béton
  ctx.save();
  const slabW = (m.toit_hors_tout.fondation_longueur || 118) * scale * 1.15;
  ctx.fillStyle = "rgba(51, 65, 85, 0.65)";
  ctx.strokeStyle = "#64748b";
  ctx.lineWidth = 1.5;
  ctx.fillRect(cx - slabW / 2, groundY, slabW, 14);
  ctx.strokeRect(cx - slabW / 2, groundY, slabW, 14);

  ctx.strokeStyle = "#94a3b8";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(25, groundY);
  ctx.lineTo(W - 25, groundY);
  ctx.stroke();

  ctx.fillStyle = "#94a3b8";
  ctx.font = "700 10px 'JetBrains Mono', monospace";
  ctx.textAlign = "left";
  ctx.fillText("SOL (Z = 0)", 30, groundY - 5);
  ctx.restore();

  // 3. Spa posé au sol
  const spaW_px = state.spa.lengthIn * scale * 1.15;
  const spaH_px = state.spa.heightIn * scale;
  const spaTopY = zToY(state.spa.heightIn);

  ctx.save();
  const spaColor =
    r.statusHeight === "ok"
      ? "rgba(16, 185, 129, 0.22)"
      : r.statusHeight === "warn"
      ? "rgba(245, 158, 11, 0.22)"
      : "rgba(239, 68, 68, 0.25)";
  const spaBorder =
    r.statusHeight === "ok" ? "#10b981" : r.statusHeight === "warn" ? "#f59e0b" : "#ef4444";

  ctx.fillStyle = spaColor;
  ctx.strokeStyle = spaBorder;
  ctx.lineWidth = 2;
  ctx.fillRect(cx - spaW_px / 2, spaTopY, spaW_px, spaH_px);
  ctx.strokeRect(cx - spaW_px / 2, spaTopY, spaW_px, spaH_px);

  const lipH = Math.min(8, spaH_px * 0.12);
  ctx.fillStyle = "rgba(248, 250, 252, 0.25)";
  ctx.fillRect(cx - spaW_px / 2 - 2, spaTopY, spaW_px + 4, lipH);

  ctx.fillStyle = "#f8fafc";
  ctx.font = "700 11px 'Inter', sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(
    `SPA (H = ${formatDualUnit(state.spa.heightIn, 1)})`,
    cx,
    spaTopY + spaH_px / 2 + 4
  );
  ctx.restore();

  // 4. Poteaux fixes Oasis
  const colSpanPx = m.degagement_colonnes.longueur * scale * 1.15;
  const postW_px = Math.max(8, 3.8 * scale * 1.15);
  const leftPostX = cx - colSpanPx / 2 - postW_px;
  const rightPostX = cx + colSpanPx / 2;

  const currentLiftIn = liftProgress * m.hauteur.course_elevation;
  const roofBaseZ = state.spa.heightIn + currentLiftIn;
  const roofBaseY = zToY(roofBaseZ);

  const fixedPostTopY = zToY(m.hauteur.poteau_fixe);
  const deployedPostTopZ = Math.max(m.hauteur.poteau_deploye || 92.125, roofBaseZ + 4.0);
  const deployedPostTopY = zToY(deployedPostTopZ);

  ctx.save();
  for (const px of [leftPostX, rightPostX]) {
    ctx.fillStyle = "rgba(148, 163, 184, 0.32)";
    ctx.strokeStyle = "#64748b";
    ctx.lineWidth = 1.2;
    ctx.fillRect(px + 1.5, deployedPostTopY, postW_px - 3, groundY - deployedPostTopY);
    ctx.strokeRect(px + 1.5, deployedPostTopY, postW_px - 3, groundY - deployedPostTopY);

    ctx.fillStyle = "rgba(245, 158, 11, 0.78)";
    ctx.strokeStyle = "#fde68a";
    ctx.lineWidth = 1.5;
    ctx.fillRect(px, fixedPostTopY, postW_px, groundY - fixedPostTopY);
    ctx.strokeRect(px, fixedPostTopY, postW_px, groundY - fixedPostTopY);
  }
  ctx.restore();

  // 5. Toiles rétractables (Roller Shades)
  if (currentLiftIn > 1.0) {
    ctx.save();
    const shadeDropIn = Math.min(currentLiftIn, 42.0);
    const shadeH_px = shadeDropIn * scale;
    ctx.fillStyle = "rgba(56, 189, 248, 0.08)";
    ctx.strokeStyle = "rgba(56, 189, 248, 0.25)";
    ctx.setLineDash([3, 3]);
    ctx.fillRect(cx - colSpanPx / 2, roofBaseY, colSpanPx, shadeH_px);
    ctx.strokeRect(cx - colSpanPx / 2, roofBaseY, colSpanPx, shadeH_px);
    ctx.restore();
  }

  // 6. Toit pyramidal Oasis & Équerres de coins
  const roofOutW_px = m.toit_hors_tout.longueur * scale * 1.15;
  const uFrameIn = m.hauteur.epaisseur_cadre_u || 4.0;
  const domeTotalIn = m.hauteur.epaisseur_toit || 22.875;

  const uFrameTopY = zToY(roofBaseZ + uFrameIn);
  const domePeakY = zToY(roofBaseZ + domeTotalIn);

  ctx.save();
  ctx.fillStyle = "#10b981";
  ctx.fillRect(cx - spaW_px / 2, roofBaseY - 2, spaW_px, 3);

  const bracketH = Math.max(8, 5.5 * scale);
  ctx.fillStyle = "#38bdf8";
  ctx.strokeStyle = "#e0f2fe";
  ctx.lineWidth = 1.5;
  ctx.fillRect(leftPostX - 2, roofBaseY - bracketH, postW_px + 8, bracketH);
  ctx.strokeRect(leftPostX - 2, roofBaseY - bracketH, postW_px + 8, bracketH);
  ctx.fillRect(rightPostX - 6, roofBaseY - bracketH, postW_px + 8, bracketH);
  ctx.strokeRect(rightPostX - 6, roofBaseY - bracketH, postW_px + 8, bracketH);

  ctx.fillStyle = "rgba(30, 41, 59, 0.95)";
  ctx.strokeStyle = "#38bdf8";
  ctx.lineWidth = 2;
  ctx.fillRect(cx - roofOutW_px / 2, uFrameTopY, roofOutW_px, roofBaseY - uFrameTopY);
  ctx.strokeRect(cx - roofOutW_px / 2, uFrameTopY, roofOutW_px, roofBaseY - uFrameTopY);

  ctx.beginPath();
  ctx.moveTo(cx - roofOutW_px / 2, uFrameTopY);
  ctx.quadraticCurveTo(cx - roofOutW_px * 0.25, domePeakY + 4, cx, domePeakY);
  ctx.quadraticCurveTo(cx + roofOutW_px * 0.25, domePeakY + 4, cx + roofOutW_px / 2, uFrameTopY);
  ctx.closePath();

  const roofGrad = ctx.createLinearGradient(0, domePeakY, 0, uFrameTopY);
  roofGrad.addColorStop(0, "rgba(56, 189, 248, 0.42)");
  roofGrad.addColorStop(1, "rgba(30, 58, 138, 0.55)");
  ctx.fillStyle = roofGrad;
  ctx.fill();
  ctx.strokeStyle = "#38bdf8";
  ctx.lineWidth = 2;
  ctx.stroke();

  ctx.strokeStyle = "rgba(186, 230, 253, 0.28)";
  ctx.lineWidth = 1;
  const numRibs = 14;
  for (let i = 1; i < numRibs; i++) {
    const t = i / numRibs;
    const rx = cx - roofOutW_px / 2 + t * roofOutW_px;
    const distFromCenter = Math.abs(t - 0.5) * 2;
    const ryTop = domePeakY + Math.pow(distFromCenter, 1.55) * (uFrameTopY - domePeakY);
    ctx.beginPath();
    ctx.moveTo(rx, uFrameTopY);
    ctx.lineTo(rx, ryTop);
    ctx.stroke();
  }
  ctx.restore();

  // 7. Lignes de cotes verticales
  drawDimensionLine(
    ctx,
    leftPostX - 26,
    groundY,
    leftPostX - 26,
    roofBaseY,
    liftProgress > 0.1
      ? `Sous toit : ${formatUnit(roofBaseZ, 1)}`
      : `H_spa : ${formatUnit(state.spa.heightIn, 1)}`,
    "#38bdf8",
    0
  );

  if (liftProgress < 0.5) {
    const refTopY = state.roofRefMode === "uframe" ? fixedPostTopY : zToY(m.hauteur.poteau_deploye || 92.125);
    const roofRefTopY = state.roofRefMode === "uframe" ? uFrameTopY : domePeakY;
    drawDimensionLine(
      ctx,
      leftPostX - 110,
      roofRefTopY,
      leftPostX - 110,
      refTopY,
      `Dépassement : ${formatUnit(r.postProtrusionClosed, 1)}`,
      "#fbbf24",
      0
    );
  } else {
    drawDimensionLine(
      ctx,
      leftPostX - 110,
      spaTopY,
      leftPostX - 110,
      roofBaseY,
      `Course : +${formatUnit(currentLiftIn, 1)}`,
      "#34d399",
      0
    );
  }

  drawDimensionLine(
    ctx,
    rightPostX + postW_px + 34,
    groundY,
    rightPostX + postW_px + 34,
    domePeakY,
    `H Totale : ${formatUnit(roofBaseZ + domeTotalIn, 1)}`,
    "#f59e0b",
    0
  );

  drawDimensionLine(
    ctx,
    rightPostX + postW_px + 118,
    roofBaseY,
    rightPostX + postW_px + 118,
    domePeakY,
    `Dôme : ${formatUnit(domeTotalIn, 2)}`,
    "#94a3b8",
    0
  );
}

function drawElevationView() {
  const canvas = document.getElementById("elevationCanvas");
  if (!canvas || !state.selectedModel || !state.fitResult) return;

  const rect = canvas.parentElement.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  if (canvas.width !== Math.floor(rect.width * dpr) || canvas.height !== Math.floor(rect.height * dpr)) {
    canvas.width = Math.floor(rect.width * dpr);
    canvas.height = Math.floor(rect.height * dpr);
  }

  const ctx = canvas.getContext("2d");
  ctx.save();
  ctx.scale(dpr, dpr);

  const W = rect.width;
  const H = rect.height;
  ctx.clearRect(0, 0, W, H);

  renderElevationScene(ctx, W, H, state.elevation.liftProgress);
  ctx.restore();
}

// ============================================================================
// EXPORTATION DU PLAN FINAL "FOOTPRINT & FIT" HAUTE DÉFINITION (PNG HD)
// ============================================================================
function exportFootprintPlan() {
  if (!state.selectedModel || !state.fitResult) return;

  const m = state.selectedModel;
  const r = state.fitResult;

  const expW = 2200;
  const expH = 1480;
  const outCanvas = document.createElement("canvas");
  outCanvas.width = expW;
  outCanvas.height = expH;
  const ctx = outCanvas.getContext("2d");

  // 1. Fond général sombre style plan d'ingénierie CAO
  ctx.fillStyle = "#0b1120";
  ctx.fillRect(0, 0, expW, expH);

  // Grille technique subtile
  ctx.strokeStyle = "rgba(51, 65, 85, 0.22)";
  ctx.lineWidth = 1;
  for (let x = 0; x < expW; x += 40) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, expH);
    ctx.stroke();
  }
  for (let y = 0; y < expH; y += 40) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(expW, y);
    ctx.stroke();
  }

  // Cadre extérieur du plan
  ctx.strokeStyle = "#334155";
  ctx.lineWidth = 3;
  ctx.strokeRect(20, 20, expW - 40, expH - 40);

  // 2. Cartouche d'en-tête supérieur
  ctx.fillStyle = "#111827";
  ctx.fillRect(22, 22, expW - 44, 96);
  ctx.strokeStyle = "#334155";
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.moveTo(20, 118);
  ctx.lineTo(expW - 20, 118);
  ctx.stroke();

  ctx.fillStyle = "#38bdf8";
  ctx.font = "800 26px 'Inter', sans-serif";
  ctx.textAlign = "left";
  ctx.fillText("SPAFIT — PLAN DE COMPATIBILITÉ & FOOTPRINT OASIS", 48, 62);

  ctx.fillStyle = "#94a3b8";
  ctx.font = "500 15px 'JetBrains Mono', monospace";
  const nowStr = new Date().toISOString().slice(0, 10);
  ctx.fillText(
    `Modèle : ${m.nom}  |  Réf CAO : ${m.code_interne}  |  Date : ${nowStr}`,
    48,
    94
  );

  // Badge de statut global dans l'en-tête du plan
  const statusLabel =
    r.globalStatus === "ok"
      ? "COMPATIBLE OASIS"
      : r.globalStatus === "warn"
      ? "AJUSTEMENT CRITIQUE"
      : "INCOMPATIBLE";
  const statusColor =
    r.globalStatus === "ok" ? "#10b981" : r.globalStatus === "warn" ? "#f59e0b" : "#ef4444";

  ctx.fillStyle = statusColor;
  drawRoundedRectPath(ctx, expW - 360, 42, 310, 54, 27);
  ctx.fill();
  ctx.fillStyle = "#0b1120";
  ctx.font = "800 20px 'Inter', sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(statusLabel, expW - 205, 75);

  // 3. Zone Gauche (1260 x 1300) : Vue de dessus 2D (Footprint & Dégagements)
  const leftBox = { x: 40, y: 140, w: 1240, h: 1300 };
  ctx.fillStyle = "rgba(15, 23, 42, 0.78)";
  ctx.strokeStyle = "#334155";
  ctx.lineWidth = 2;
  ctx.fillRect(leftBox.x, leftBox.y, leftBox.w, leftBox.h);
  ctx.strokeRect(leftBox.x, leftBox.y, leftBox.w, leftBox.h);

  ctx.fillStyle = "#e2e8f0";
  ctx.font = "700 18px 'Inter', sans-serif";
  ctx.textAlign = "left";
  ctx.fillText("1. VUE DE DESSUS 2D — FOOTPRINT OASIS, MOTEUR & DÉGAGEMENTS", leftBox.x + 24, leftBox.y + 36);

  ctx.save();
  ctx.beginPath();
  ctx.rect(leftBox.x, leftBox.y + 50, leftBox.w, leftBox.h - 50);
  ctx.clip();
  ctx.translate(leftBox.x + leftBox.w / 2, leftBox.y + 50 + (leftBox.h - 50) / 2);
  const topExportScale = 7.4; // Échelle généreuse pour voir tous les détails
  renderTopDownScene(ctx, topExportScale, {
    showFoundation: true,
    showSealZone: true,
    showSealLanding: true,
    showRiskFlags: true,
    isExport: true
  });
  ctx.restore();

  // 4. Zone Haut-Droite (840 x 560) : Coupe Latérale d'Élévation Z (Position Ouverte)
  const rightTopBox = { x: 1310, y: 140, w: 850, h: 560 };
  ctx.fillStyle = "rgba(15, 23, 42, 0.78)";
  ctx.strokeStyle = "#334155";
  ctx.lineWidth = 2;
  ctx.fillRect(rightTopBox.x, rightTopBox.y, rightTopBox.w, rightTopBox.h);
  ctx.strokeRect(rightTopBox.x, rightTopBox.y, rightTopBox.w, rightTopBox.h);

  ctx.fillStyle = "#e2e8f0";
  ctx.font = "700 18px 'Inter', sans-serif";
  ctx.textAlign = "left";
  ctx.fillText("2. COUPE D'ÉLÉVATION LATÉRALE (AXE Z — POSITION DÉPLOYÉE)", rightTopBox.x + 24, rightTopBox.y + 36);

  ctx.save();
  ctx.translate(rightTopBox.x, rightTopBox.y + 50);
  renderElevationScene(ctx, rightTopBox.w, rightTopBox.h - 55, 1.0);
  ctx.restore();

  // 5. Zone Bas-Droite (840 x 715) : Tableau Officiel des Cotes & Dégagements
  const rightBotBox = { x: 1310, y: 725, w: 850, h: 715 };
  ctx.fillStyle = "rgba(15, 23, 42, 0.9)";
  ctx.strokeStyle = "#334155";
  ctx.lineWidth = 2;
  ctx.fillRect(rightBotBox.x, rightBotBox.y, rightBotBox.w, rightBotBox.h);
  ctx.strokeRect(rightBotBox.x, rightBotBox.y, rightBotBox.w, rightBotBox.h);

  ctx.fillStyle = "#38bdf8";
  ctx.font = "700 18px 'Inter', sans-serif";
  ctx.textAlign = "left";
  ctx.fillText("3. TABLEAU DE VALIDATION DIMENSIONNELLE & DÉGAGEMENTS", rightBotBox.x + 24, rightBotBox.y + 38);

  const sideLabels = { top: "Haut (Nord)", bottom: "Bas (Sud)", left: "Gauche (Ouest)", right: "Droite (Est)" };
  const s = m.joint_etancheite;
  const landing = state.spa.sealLandingAnalysis || analyzeSealLandingSurface(m, state.spa);
  const rows = [
    ["Modèle Couverture Oasis", `${m.nom}`],
    ["Dimensions du Spa (L × l × H)", `${formatDualUnit(state.spa.lengthIn, 1)} × ${formatDualUnit(state.spa.widthIn, 1)} × ${formatDualUnit(state.spa.heightIn, 1)}`],
    ["Surface d'appui du rebord (Plat)", `${formatDualUnit(landing.currentRimW, 2)}  [${landing.isRimCompliant ? "CONFORME ≥ 1.0\"" : "INSUFFISANT < 1.0\""}] (Min requis : 1.0 po / Rec : 1.25 po)`],
    ["Rayon de coin effectif (R)", `${formatDualUnit(landing.minObservedR, 2)}  [${landing.minRadiusCompliant ? "CONFORME ≥ 4.0\"" : "NON CONFORME < 4.0\""}] (Min requis : 4.0 po)`],
    ["Points d'inspection sur pourtour", `${landing.riskFlags.length === 0 ? "0 risque (Appui continu hermétique sur tout le pourtour)" : landing.riskFlags.map(f => f.badgeText).join(", ")}`],
    ["Dégagement intérieur Poteaux (G × F)", `${formatDualUnit(r.colX, 2)} × ${formatDualUnit(r.colY, 2)} (Diag H = ${formatUnit(m.degagement_colonnes.diagonale || 130.75, 2)})`],
    ["Marge Horizontale X (Longueur)", `${r.marginX >= 0 ? "+" : ""}${formatDualUnit(r.marginX, 2)} / côté  [${r.statusX === "ok" ? "CONFORME ≥ 1.25\"" : r.statusX === "warn" ? "CRITIQUE 0.5\"–1.25\"" : "COLLISION < 0.5\""}]`],
    ["Marge Horizontale Y (Largeur)", `${r.marginY >= 0 ? "+" : ""}${formatDualUnit(r.marginY, 2)} / côté  [${r.statusY === "ok" ? "CONFORME ≥ 1.25\"" : r.statusY === "warn" ? "CRITIQUE 0.5\"–1.25\"" : "COLLISION < 0.5\""}]`],
    ["Plage Joint d'étanchéité (Seal)", `L: [${formatUnit(s.longueur_min, 0)}–${formatUnit(s.longueur_max, 0)}] • l: [${formatUnit(s.largeur_min, 0)}–${formatUnit(s.largeur_max, 0)}] (Bande ${formatUnit(s.largeur_bande, 1)})`],
    ["Position Moteur (C) & Entrée (I)", `Moteur ${sideLabels[state.motorSide]} (C = ${formatDualUnit(m.toit_hors_tout.c_position_moteur || 36.1, 1)}) | Entrée opposée (I = ${formatDualUnit(m.degagement_colonnes.largeur_entree || 52, 0)})`],
    ["Hauteur libre sous toit ouvert", `${formatDualUnit(r.clearHeightOpen, 2)} (H_spa + Course ${formatUnit(m.hauteur.course_elevation, 0)})`],
    ["Hauteur totale déployée (Faîtage)", `${formatDualUnit(r.totalHeightDome, 2)} (Max recommandé : ${formatDualUnit(r.maxAllowedOverall, 0)})`],
    ["Dépassement poteau (Position fermée)", `${r.postProtrusionClosed >= 0 ? "+" : ""}${formatDualUnit(r.postProtrusionClosed, 2)}`],
    ["Dalle de fondation minimale (D × A)", `${formatDualUnit(m.toit_hors_tout.fondation_longueur || 118, 0)} × ${formatDualUnit(m.toit_hors_tout.fondation_largeur || 106, 0)}`],
    ["Dégagements de maintenance", `24 po (61 cm) côté moteur & entrée | 6 po (15.2 cm) côtés latéraux | 0.5 po min sous patio`]
  ];

  let ry = rightBotBox.y + 74;
  for (let i = 0; i < rows.length; i++) {
    const [k, v] = rows[i];
    if (i % 2 === 0) {
      ctx.fillStyle = "rgba(30, 41, 59, 0.55)";
      ctx.fillRect(rightBotBox.x + 16, ry - 20, rightBotBox.w - 32, 44);
    }
    ctx.fillStyle = "#94a3b8";
    ctx.font = "600 13.5px 'Inter', sans-serif";
    ctx.textAlign = "left";
    ctx.fillText(k, rightBotBox.x + 28, ry + 5);

    ctx.fillStyle = "#f8fafc";
    ctx.font = "600 13.5px 'JetBrains Mono', monospace";
    ctx.textAlign = "right";
    ctx.fillText(v, rightBotBox.x + rightBotBox.w - 28, ry + 5);
    ry += 48;
  }

  // Téléchargement automatique du PNG
  const link = document.createElement("a");
  const safeId = m.id.replace(/[^a-z0-9_-]/gi, "_");
  link.download = `SpaFit_Footprint_${safeId}_${Math.round(state.spa.lengthIn)}x${Math.round(state.spa.widthIn)}.png`;
  link.href = outCanvas.toDataURL("image/png");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

// ============================================================================
// ANIMATION CINÉMATIQUE DE LA COUPE D'ÉLÉVATION (FERMÉE <-> OUVERTE)
// ============================================================================
function setElevationOpenState(open) {
  state.elevation.isOpen = open;
  document.getElementById("btnElevClosed").classList.toggle("active", !open);
  document.getElementById("btnElevOpen").classList.toggle("active", open);

  const target = open ? 1.0 : 0.0;
  if (state.elevation.animFrameId) {
    cancelAnimationFrame(state.elevation.animFrameId);
  }

  const animate = () => {
    const diff = target - state.elevation.liftProgress;
    if (Math.abs(diff) < 0.01) {
      state.elevation.liftProgress = target;
      drawElevationView();
      state.elevation.animFrameId = null;
      return;
    }
    state.elevation.liftProgress += diff * 0.16;
    drawElevationView();
    state.elevation.animFrameId = requestAnimationFrame(animate);
  };
  state.elevation.animFrameId = requestAnimationFrame(animate);
}

// ============================================================================
// CHARGEMENT ET TRAITEMENT AUTOMATIQUE D'UNE PHOTO DE SPA
// ============================================================================
function processLoadedSpaImageElement(rawImg, sourceLabel = "Photo importée") {
  const analysis = autoCropAndAnalyzeSpaImage(rawImg);

  const croppedImg = new Image();
  croppedImg.onload = () => {
    state.topView.image = croppedImg;
    state.topView.rawImageSize = { w: analysis.rawW, h: analysis.rawH };
    state.topView.croppedSize = { w: analysis.cropW, h: analysis.cropH };
    state.topView.detectedRadiusNormalized = analysis.radiusNormalized;
    state.topView.cornersPx = analysis.cornersPx;
    state.topView.detectedRimWidthPx = analysis.detectedRimWidthPx;
    state.topView.rawObstacles = analysis.rawObstacles || [];
    state.topView.autoFitToSpa = true;

    // Extrapolation automatique du rayon de coin (R) à partir des 4 coins de l'image
    applyExtrapolatedRadiusFromImage();

    document.getElementById("btnClearImage").classList.remove("hidden");
    const banner = document.getElementById("autoVisionBanner");
    const reportTxt = document.getElementById("autoVisionReportText");
    banner.classList.remove("hidden");
    const rimNote = state.spa.flatRimWidthIn
      ? ` • Rebord plat détecté : <strong>${formatUnit(state.spa.flatRimWidthIn, 2)}</strong>`
      : "";
    reportTxt.innerHTML =
      `<strong>${sourceLabel} :</strong> Vide retiré (${analysis.rawW}×${analysis.rawH} px → <strong>${analysis.cropW}×${analysis.cropH} px</strong>) • ` +
      `Étalonné auto sur <strong>${formatUnit(state.spa.lengthIn, 1)} × ${formatUnit(state.spa.widthIn, 1)}</strong> • ` +
      `Rayon extrapolé : <strong>R = ${formatDualUnit(state.spa.cornerRadiusIn, 2)}</strong>${rimNote}`;

    updateUI();
  };
  croppedImg.src = analysis.dataUrl;
}

function loadUserImageFile(file) {
  if (!file || !file.type.startsWith("image/")) return;
  const reader = new FileReader();
  reader.onload = (ev) => {
    const rawImg = new Image();
    rawImg.onload = () => {
      processLoadedSpaImageElement(rawImg, file.name);
    };
    rawImg.src = ev.target.result;
  };
  reader.readAsDataURL(file);
}

/**
 * Génère une photo synthétique de spa sur fond blanc (avec marges vides autour et coins arrondis)
 * puis la passe dans le pipeline `processLoadedSpaImageElement` pour démontrer le rognage du vide,
 * l'étalonnage automatique et l'extrapolation du rayon.
 */
function generateDemoSpaBlueprint() {
  const offCanvas = document.createElement("canvas");
  offCanvas.width = 960;
  offCanvas.height = 860;
  const ctx = offCanvas.getContext("2d");

  // Fond blanc avec large marge vide autour du spa (comme une photo catalogue)
  ctx.fillStyle = "#ffffff";
  ctx.fillRect(0, 0, 960, 860);

  // Coquille du spa (680 x 680 px) centrée avec un rayon de 68 px (= 10% -> ~8.4" sur un spa de 84")
  const spaW = 680;
  const spaH = 680;
  const rPx = 68;
  const x0 = (960 - spaW) / 2;
  const y0 = (860 - spaH) / 2;

  drawRoundedRectPath(ctx, x0, y0, spaW, spaH, rPx);
  ctx.fillStyle = "#e2e8f0";
  ctx.fill();
  ctx.lineWidth = 6;
  ctx.strokeStyle = "#94a3b8";
  ctx.stroke();

  // Cuve intérieure acrylique
  drawRoundedRectPath(ctx, x0 + 34, y0 + 34, spaW - 68, spaH - 68, rPx - 18);
  ctx.fillStyle = "#cbd5e1";
  ctx.fill();
  ctx.strokeStyle = "#64748b";
  ctx.lineWidth = 3;
  ctx.stroke();

  // Sièges ergonomiques, coussins d'angle et jets
  ctx.fillStyle = "#334155";
  for (const [hx, hy, rot] of [
    [x0 + 75, y0 + 75, -Math.PI / 4],
    [x0 + spaW - 75, y0 + 75, Math.PI / 4],
    [x0 + 75, y0 + spaH - 75, -3 * Math.PI / 4]
  ]) {
    ctx.save();
    ctx.translate(hx, hy);
    ctx.rotate(rot);
    drawRoundedRectPath(ctx, -45, -14, 90, 28, 12);
    ctx.fill();
    ctx.restore();
  }

  for (const [jx, jy, jr] of [
    [x0 + 170, y0 + 170, 75],
    [x0 + spaW - 170, y0 + 170, 75],
    [x0 + 170, y0 + spaH - 170, 75],
    [x0 + spaW - 170, y0 + spaH - 170, 75],
    [480, 430, 62]
  ]) {
    ctx.beginPath();
    ctx.arc(jx, jy, jr, 0, Math.PI * 2);
    ctx.fillStyle = "#f1f5f9";
    ctx.fill();
    ctx.strokeStyle = "#94a3b8";
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(jx, jy, 10, 0, Math.PI * 2);
    ctx.fillStyle = "#1e293b";
    ctx.fill();
  }

  const rawImg = new Image();
  rawImg.onload = () => {
    processLoadedSpaImageElement(rawImg, "Photo Spa Catalogue Démo");
  };
  rawImg.src = offCanvas.toDataURL("image/png");
}

// ============================================================================
// MODALE DE LA BASE DE DONNÉES COMPLÈTE (`data/models.json`)
// ============================================================================
function populateDbModal() {
  const tbody = document.getElementById("dbModalTableBody");
  const countBadge = document.getElementById("dbCountBadge");
  if (countBadge) countBadge.textContent = String(state.allModels.length);
  if (!tbody) return;

  tbody.innerHTML = state.allModels
    .map((m) => {
      const isOasis = Boolean(m.active_in_ui);
      const col = m.degagement_colonnes || {};
      const seal = m.joint_etancheite || {};
      const h = m.hauteur || {};
      const roof = m.toit_hors_tout || {};
      return `
        <tr class="${isOasis ? "bg-sky-950/30 text-slate-100" : "text-slate-400"} hover:bg-slate-800/50">
          <td class="py-2 px-3">
            ${
              isOasis
                ? `<span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-[10px] font-bold">ACTIF UI</span>`
                : `<span class="px-2 py-0.5 rounded bg-slate-800 text-slate-500 text-[10px]">Verrouillé</span>`
            }
          </td>
          <td class="py-2 px-3 font-semibold ${isOasis ? "text-sky-300" : ""}">${m.gamme}</td>
          <td class="py-2 px-3">${m.nom}</td>
          <td class="py-2 px-3">${col.longueur}" × ${col.largeur}"</td>
          <td class="py-2 px-3">[${seal.longueur_min}"–${seal.longueur_max}"] × [${seal.largeur_min}"–${seal.largeur_max}"]</td>
          <td class="py-2 px-3">${h.spa_min}" – ${h.spa_max}"</td>
          <td class="py-2 px-3">Course ${h.course_elevation}" / Toit ${h.epaisseur_toit}"</td>
          <td class="py-2 px-3">${roof.longueur}" × ${roof.largeur}"</td>
          <td class="py-2 px-3 text-[10px] text-slate-500">${(m.source_fichiers || []).length} fichiers</td>
        </tr>
      `;
    })
    .join("");
}

// ============================================================================
// INITIALISATION ET ÉCOUTEURS D'ÉVÉNEMENTS
// ============================================================================
async function initApp() {
  // 1. Chargement dynamique de models.json ou depuis window.SPAFIT_CATALOG_DATA (Zero-CORS)
  if (window.SPAFIT_CATALOG_DATA && window.SPAFIT_CATALOG_DATA.cover_models && window.SPAFIT_CATALOG_DATA.cover_models.length > 0) {
    state.allModels = window.SPAFIT_CATALOG_DATA.cover_models;
  } else {
    try {
      const resp = await fetch("data/models.json");
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      state.allModels = await resp.json();
    } catch (err) {
      console.info("Utilisation de la base models.json embarquée (mode local autonome).", err);
      state.allModels = FALLBACK_MODELS;
    }
  }

  // Déverrouillage des 30 modèles SpaFit (Oasis, Horizon, Evolution, Legend, Endless Pools, Legend 89)
  state.oasisModels = state.allModels;
  state.selectedModel = state.allModels[0];

  // Peupler le sélecteur de modèles SpaFit avec regroupement par gamme
  const selectEl = document.getElementById("modelSelect");
  if (selectEl) {
    const gammes = {};
    for (const m of state.allModels) {
      const g = m.gamme || "SpaFit";
      if (!gammes[g]) gammes[g] = [];
      gammes[g].push(m);
    }

    selectEl.innerHTML = Object.entries(gammes)
      .map(([gammeName, models]) => `
        <optgroup label="Gamme ${gammeName}" class="bg-slate-900 text-sky-400 font-bold">
          ${models.map(m => `
            <option value="${m.id}" class="bg-slate-950 text-slate-100 font-normal" style="background-color:#0f172a;color:#f8fafc;">
              ${m.nom} ${m.dimensions_toit ? `(${m.dimensions_toit.longueur_ext}"×${m.dimensions_toit.largeur_ext}")` : ''}
            </option>
          `).join("")}
        </optgroup>
      `).join("");
    selectEl.value = state.selectedModel.id;

    selectEl.addEventListener("change", () => {
      const found = state.allModels.find((m) => m.id === selectEl.value);
      if (found) {
        state.selectedModel = found;
        updateUI();
      }
    });
  }

  // 1.B Fonction de chargement d'un Spa depuis le Master Catalog (1,339 spas)
  window.loadSpaFromMasterCatalog = function(spaId) {
    if (!window.SPAFIT_CATALOG_DATA || !window.SPAFIT_CATALOG_DATA.spas) return;
    const numId = parseInt(spaId, 10);
    const spa = window.SPAFIT_CATALOG_DATA.spas.find(s => s.id === numId);
    if (!spa) return;

    // Dimensions
    state.spa.lengthIn = parseFloat(spa.length_in) || 84.0;
    state.spa.widthIn = parseFloat(spa.width_in) || 84.0;
    state.spa.heightIn = parseFloat(spa.height_in) || 38.0;
    const rClean = (spa.corner_radius_in || '').toString().replace(/[^0-9.]/g, '');
    state.spa.cornerRadiusIn = parseFloat(rClean) || 8.0;
    state.spa.flatRimWidthIn = 2.5;
    state.spa.radiusAutoDetected = false;
    state.spa.brand = spa.Marque || '';
    state.spa.model = spa.Modele || '';
    state.spa.generation = spa.Generation || '';
    state.spa.isRound = (spa.Forme && spa.Forme.toLowerCase().includes('ron')) ||
                        (spa.Segment && spa.Segment.toLowerCase().includes('ron')) ||
                        (Math.abs(state.spa.lengthIn - state.spa.widthIn) <= 2.0 && state.spa.cornerRadiusIn >= (state.spa.lengthIn / 2.0 - 4.0));

    // Bannière d'information du spa sélectionné
    const infoEl = document.getElementById("activeSpaBanner");
    if (infoEl) {
      infoEl.classList.remove("hidden");
      infoEl.innerHTML = `
        <div class="flex items-center gap-2 text-xs">
          <span class="font-bold text-sky-400 uppercase tracking-wider">${spa.Marque}</span>
          <span class="text-white font-semibold">${spa.Modele}</span>
          <span class="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-mono">${spa.Generation || ''} (${spa.Annees_Production || ''})</span>
          <span class="text-slate-400 font-mono text-[11px]">${spa.length_in}" × ${spa.width_in}" × ${spa.height_in}" • R=${spa.corner_radius_in}"</span>
          ${spa.cad_svg_contour ? '<span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40 text-[10px] font-bold">📐 CAD USINE</span>' : ''}
          ${spa.image_top_file && spa.image_top_file !== 'N/A' ? '<span class="px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 text-[10px] font-bold">📷 PHOTO</span>' : ''}
        </div>
      `;
    }

    // Chargement de l'image vue de dessus si disponible
    if (spa.image_top_file && spa.image_top_file !== 'N/A') {
      const img = new Image();
      img.onload = () => {
        try {
          const cropRes = autoCropAndAnalyzeSpaImage(img);
          state.topView.image = img;
          state.topView.rawImageSize = { w: cropRes.rawW, h: cropRes.rawH };
          state.topView.croppedSize = { w: cropRes.cropW, h: cropRes.cropH };
          state.topView.detectedRadiusNormalized = cropRes.radiusNormalized;
          state.topView.cornersPx = cropRes.cornersPx;
          state.topView.detectedRimWidthPx = cropRes.detectedRimWidthPx;
          state.topView.rawObstacles = cropRes.rawObstacles || [];
          applyExtrapolatedRadiusFromImage();
        } catch (err) {
          console.warn("Traitement de l'image non rognée:", err);
          state.topView.image = img;
        }
        updateUI();
        drawTopView();
      };
      img.src = spa.image_top_file;
    } else {
      state.topView.image = null;
      state.topView.rawObstacles = [];
    }

    // Chargement du vecteur CAO usine authentique (LibreDWG DXF/SVG)
    const cadBadge = document.getElementById("cadVectorBadge");
    if (spa.cad_svg_contour) {
      const cadImg = new Image();
      cadImg.onload = () => {
        state.topView.cadSvgImg = cadImg;
        state.topView.showCadVector = true;
        if (cadBadge) cadBadge.classList.remove("hidden");
        updateUI();
        drawTopView();
      };
      cadImg.src = spa.cad_svg_contour;
    } else {
      state.topView.cadSvgImg = null;
      if (cadBadge) cadBadge.classList.add("hidden");
    }

    // Sélection automatique du modèle SpaFit optimal
    let bestSpaFitId = null;
    if (spa.cover_optimal && spa.cover_optimal.length > 0) {
      bestSpaFitId = spa.cover_optimal[0];
    } else if (spa.cover_compatible && spa.cover_compatible.length > 0) {
      bestSpaFitId = spa.cover_compatible[0];
    }
    if (bestSpaFitId) {
      const foundModel = state.allModels.find(m => m.id === bestSpaFitId);
      if (foundModel) {
        state.selectedModel = foundModel;
        if (selectEl) selectEl.value = foundModel.id;
      }
    }

    syncInputsFromState();
    updateUI();
    drawTopView();
    drawElevationView();
  };

  // 1.C Autocomplete pour la recherche rapide dans le catalogue 1,339 spas
  const searchInput = document.getElementById("catalogSpaSearchInput");
  const suggestionsBox = document.getElementById("catalogSpaSuggestions");

  if (searchInput && suggestionsBox && window.SPAFIT_CATALOG_DATA && window.SPAFIT_CATALOG_DATA.spas) {
    const spasList = window.SPAFIT_CATALOG_DATA.spas;

    const renderSuggestions = (query) => {
      const q = query.trim().toLowerCase();
      if (!q || q.length < 2) {
        suggestionsBox.classList.add("hidden");
        suggestionsBox.innerHTML = "";
        return;
      }
      const matches = spasList.filter(s => 
        (s.Marque && s.Marque.toLowerCase().includes(q)) ||
        (s.Modele && s.Modele.toLowerCase().includes(q)) ||
        (s.Serie_Collection && s.Serie_Collection.toLowerCase().includes(q))
      ).slice(0, 15);

      if (matches.length === 0) {
        suggestionsBox.innerHTML = `<div class="p-3 text-xs text-slate-500 text-center">Aucun spa trouvé pour "${query}"</div>`;
        suggestionsBox.classList.remove("hidden");
        return;
      }

      suggestionsBox.innerHTML = matches.map(s => `
        <div class="p-2.5 hover:bg-sky-950/50 cursor-pointer transition-colors flex items-center justify-between gap-2 border-b border-slate-800 last:border-b-0" data-spa-id="${s.id}">
          <div>
            <div class="flex items-center gap-2">
              <span class="text-xs font-bold text-sky-400">${s.Marque}</span>
              <span class="text-xs text-white font-semibold">${s.Modele}</span>
              <span class="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-800 text-slate-300">${s.Generation || ''} (${s.Annees_Production || ''})</span>
            </div>
            <div class="text-[11px] text-slate-400 font-mono mt-0.5">
              ${s.length_in}" × ${s.width_in}" × ${s.height_in}" • R=${s.corner_radius_in}"
            </div>
          </div>
          <div class="flex items-center gap-1.5">
            ${s.cad_svg_contour ? '<span class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold">CAD</span>' : ''}
            ${s.image_top_file && s.image_top_file !== 'N/A' ? '<span class="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300 font-bold">PHOTO</span>' : ''}
          </div>
        </div>
      `).join("");

      suggestionsBox.classList.remove("hidden");

      suggestionsBox.querySelectorAll("[data-spa-id]").forEach(el => {
        el.addEventListener("click", () => {
          const sId = parseInt(el.getAttribute("data-spa-id"), 10);
          window.loadSpaFromMasterCatalog(sId);
          suggestionsBox.classList.add("hidden");
          const selectedSpa = spasList.find(s => s.id === sId);
          if (selectedSpa) {
            searchInput.value = `${selectedSpa.Marque} ${selectedSpa.Modele} (${selectedSpa.Generation || 'Gen'})`;
          }
        });
      });
    };

    searchInput.addEventListener("input", (e) => renderSuggestions(e.target.value));
    searchInput.addEventListener("focus", (e) => renderSuggestions(e.target.value));
    document.addEventListener("click", (e) => {
      if (!searchInput.contains(e.target) && !suggestionsBox.contains(e.target)) {
        suggestionsBox.classList.add("hidden");
      }
    });
  }

  // 1.D Support de l'argument URL ?spa_id=X
  const urlParams = new URLSearchParams(window.location.search);
  const spaIdParam = urlParams.get("spa_id");
  if (spaIdParam) {
    window.loadSpaFromMasterCatalog(spaIdParam);
  }

  populateDbModal();

  const syncInputsFromState = () => {
    document.getElementById("inputSpaLength").value = inToDisplay(state.spa.lengthIn, 2);
    document.getElementById("inputSpaWidth").value = inToDisplay(state.spa.widthIn, 2);
    document.getElementById("inputSpaHeight").value = inToDisplay(state.spa.heightIn, 2);
    document.getElementById("inputCornerRadius").value = inToDisplay(state.spa.cornerRadiusIn, 2);
    const inputRim = document.getElementById("inputFlatRimWidth");
    if (inputRim) inputRim.value = inToDisplay(state.spa.flatRimWidthIn || 2.5, 2);
    document.getElementById("inputCalibRealDist").value = inToDisplay(state.spa.lengthIn, 1);
  };

  // 2. Écouteurs des champs de dimensions du spa
  const bindNumericInput = (id, key) => {
    const input = document.getElementById(id);
    if (!input) return;
    input.addEventListener("input", () => {
      const valIn = displayToIn(input.value);
      if (valIn > 0 || key === "cornerRadiusIn" || key === "flatRimWidthIn") {
        state.spa[key] = Math.max(0, valIn);
        if (key === "cornerRadiusIn") {
          state.spa.radiusAutoDetected = false;
          document.getElementById("autoRadiusPill")?.classList.add("hidden");
        } else if (key === "flatRimWidthIn") {
          document.getElementById("autoRimPill")?.classList.add("hidden");
        } else if (
          (key === "lengthIn" || key === "widthIn") &&
          state.topView.detectedRadiusNormalized &&
          state.spa.radiusAutoDetected
        ) {
          applyExtrapolatedRadiusFromImage();
        }
        updateUI();
      }
    });
  };
  bindNumericInput("inputSpaLength", "lengthIn");
  bindNumericInput("inputSpaWidth", "widthIn");
  bindNumericInput("inputSpaHeight", "heightIn");
  bindNumericInput("inputCornerRadius", "cornerRadiusIn");
  bindNumericInput("inputFlatRimWidth", "flatRimWidthIn");

  // 3. Bascule d'unités po / mm
  const setUnit = (newUnit) => {
    if (state.unit === newUnit) return;
    state.unit = newUnit;
    document.getElementById("unitBtnIn").classList.toggle("active", newUnit === "po");
    document.getElementById("unitBtnMm").classList.toggle("active", newUnit === "mm");
    syncInputsFromState();
    updateUI();
  };
  document.getElementById("unitBtnIn").addEventListener("click", () => setUnit("po"));
  document.getElementById("unitBtnMm").addEventListener("click", () => setUnit("mm"));

  // 4. Préréglages rapides de spas
  document.querySelectorAll(".preset-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.spa.lengthIn = parseFloat(btn.dataset.l);
      state.spa.widthIn = parseFloat(btn.dataset.w);
      state.spa.heightIn = parseFloat(btn.dataset.h);
      if (state.topView.detectedRadiusNormalized) {
        applyExtrapolatedRadiusFromImage();
      } else {
        state.spa.cornerRadiusIn = parseFloat(btn.dataset.r);
      }
      syncInputsFromState();
      updateUI();
    });
  });

  // 5. Permuter Longueur <-> Largeur (90°)
  document.getElementById("btnSwapLW").addEventListener("click", () => {
    const tmp = state.spa.lengthIn;
    state.spa.lengthIn = state.spa.widthIn;
    state.spa.widthIn = tmp;
    syncInputsFromState();
    updateUI();
  });

  // 6. Sélecteur de côté du moteur (Haut / Bas / Gauche / Droite)
  document.querySelectorAll(".motor-pos-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      state.motorSide = btn.dataset.side;
      document.querySelectorAll(".motor-pos-btn").forEach((b) => {
        b.classList.toggle("active", b.dataset.side === state.motorSide);
      });
      updateUI();
    });
  });

  // 7. Appliquer la recommandation intelligente en 1 clic
  document.getElementById("btnApplyRecommendation").addEventListener("click", () => {
    if (!state.recommendation) return;
    if (state.recommendation.swapLW) {
      const tmp = state.spa.lengthIn;
      state.spa.lengthIn = state.spa.widthIn;
      state.spa.widthIn = tmp;
      syncInputsFromState();
    }
    const targetModel = state.oasisModels.find((m) => m.id === state.recommendation.modelId);
    if (targetModel) {
      state.selectedModel = targetModel;
      document.getElementById("modelSelect").value = targetModel.id;
    }
    updateUI();
  });

  // 8. Référence de toit pour le calcul de dépassement poteau
  document.getElementById("roofRefMode").addEventListener("change", (e) => {
    state.roofRefMode = e.target.value;
    updateUI();
  });

  // 9. Contrôles de la Vue de dessus 2D (Opacité & Rotation strictement 90° / 180°)
  const opacitySlider = document.getElementById("sliderImageOpacity");
  opacitySlider.addEventListener("input", () => {
    state.topView.imageOpacity = parseInt(opacitySlider.value, 10) / 100;
    document.getElementById("valImageOpacity").textContent = `${opacitySlider.value}%`;
    drawTopView();
  });

  // Rotation verrouillée aux multiples de 90° (0, 90, 180, 270)
  const setRotation90 = (deg) => {
    const snapped = ((Math.round(deg / 90) * 90) % 360 + 360) % 360;
    state.topView.rotationDeg = snapped;

    document.querySelectorAll(".rot-step-btn").forEach((b) => {
      b.classList.toggle("active", parseInt(b.dataset.deg, 10) === snapped);
    });
    updateUI();
    drawTopView();
  };

  document.querySelectorAll(".rot-step-btn").forEach((btn) => {
    btn.addEventListener("click", () => setRotation90(parseInt(btn.dataset.deg, 10)));
  });
  document.getElementById("btnRotMinus90").addEventListener("click", () => setRotation90(state.topView.rotationDeg - 90));
  document.getElementById("btnRotPlus90").addEventListener("click", () => setRotation90(state.topView.rotationDeg + 90));
  document.getElementById("btnRot180").addEventListener("click", () => setRotation90(state.topView.rotationDeg + 180));

  document.getElementById("chkShowFoundation").addEventListener("change", (e) => {
    state.topView.showFoundation = e.target.checked;
    drawTopView();
  });
  document.getElementById("chkShowSealZone").addEventListener("change", (e) => {
    state.topView.showSealZone = e.target.checked;
    drawTopView();
  });
  document.getElementById("chkShowSealLanding")?.addEventListener("change", (e) => {
    state.topView.showSealLanding = e.target.checked;
    drawTopView();
  });
  document.getElementById("chkShowRiskFlags")?.addEventListener("change", (e) => {
    state.topView.showRiskFlags = e.target.checked;
    drawTopView();
  });

  const setZoom = (newZoom) => {
    state.topView.zoom = Math.max(0.4, Math.min(4.0, newZoom));
    document.getElementById("valZoomPct").textContent = `${Math.round(state.topView.zoom * 100)}%`;
    drawTopView();
  };
  document.getElementById("btnZoomIn").addEventListener("click", () => setZoom(state.topView.zoom * 1.2));
  document.getElementById("btnZoomOut").addEventListener("click", () => setZoom(state.topView.zoom / 1.2));
  document.getElementById("btnRecenterTop").addEventListener("click", () => {
    state.topView.panX = 0;
    state.topView.panY = 0;
    setZoom(1.0);
  });

  // 10. Importation d'image (Auto-Crop + Auto-Fit + Extrapolation du Rayon)
  document.getElementById("fileImageInput").addEventListener("change", (e) => {
    if (e.target.files && e.target.files[0]) {
      loadUserImageFile(e.target.files[0]);
    }
  });
  document.getElementById("btnLoadDemoBlueprint").addEventListener("click", generateDemoSpaBlueprint);
  document.getElementById("btnReFitAutoImage").addEventListener("click", () => {
    state.topView.autoFitToSpa = true;
    applyExtrapolatedRadiusFromImage();
    updateUI();
  });

  document.getElementById("btnClearImage").addEventListener("click", () => {
    state.topView.image = null;
    state.topView.rawImageSize = null;
    state.topView.croppedSize = null;
    state.topView.detectedRadiusNormalized = null;
    state.topView.imagePixelsPerInch = null;
    state.topView.calibration.active = false;
    state.topView.calibration.p1 = null;
    state.topView.calibration.p2 = null;
    state.spa.radiusAutoDetected = false;
    document.getElementById("autoRadiusPill")?.classList.add("hidden");
    document.getElementById("btnClearImage").classList.add("hidden");
    document.getElementById("autoVisionBanner").classList.add("hidden");
    document.getElementById("calibrationBanner").classList.add("hidden");
    document.getElementById("calibrationScaleBadge").textContent = "Échelle : Vectorielle native";
    drawTopView();
  });

  const topWrapper = document.getElementById("topCanvasWrapper");
  topWrapper.addEventListener("dragover", (e) => {
    e.preventDefault();
    topWrapper.classList.add("drag-over");
  });
  topWrapper.addEventListener("dragleave", () => {
    topWrapper.classList.remove("drag-over");
  });
  topWrapper.addEventListener("drop", (e) => {
    e.preventDefault();
    topWrapper.classList.remove("drag-over");
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      loadUserImageFile(e.dataTransfer.files[0]);
    }
  });

  // 11. Outil d'étalonnage manuel orthogonal à 2 points (Verrouillé à 90° H ou V)
  const topCanvas = document.getElementById("topViewCanvas");
  const getLocalCanvasCoords = (evt) => {
    const rect = topCanvas.getBoundingClientRect();
    const cx = rect.width / 2 + state.topView.panX;
    const cy = rect.height / 2 + state.topView.panY;
    return {
      x: evt.clientX - rect.left - cx,
      y: evt.clientY - rect.top - cy
    };
  };

  /**
   * Projette le 2e point P2 strictement à l'horizontale (y2 = y1) ou à la verticale (x2 = x1) par rapport à P1
   */
  const snapOrthogonalPoint = (p1, rawPt) => {
    const dx = Math.abs(rawPt.x - p1.x);
    const dy = Math.abs(rawPt.y - p1.y);
    if (dx >= dy) {
      return { x: rawPt.x, y: p1.y, axis: "H" };
    }
    return { x: p1.x, y: rawPt.y, axis: "V" };
  };

  document.getElementById("btnCalibrate2Pts").addEventListener("click", () => {
    if (!state.topView.image) {
      generateDemoSpaBlueprint();
    }
    state.topView.calibration.active = true;
    state.topView.calibration.p1 = null;
    state.topView.calibration.p2 = null;
    topWrapper.classList.add("calibrating");
    document.getElementById("calibrationBanner").classList.remove("hidden");
    document.getElementById("calibrationInputGroup").classList.add("hidden");
    document.getElementById("calibrationInputGroup").classList.remove("flex");
    document.getElementById("calibrationStepText").textContent =
      "Étape 1/2 : Cliquez P1. Le segment P1–P2 sera verrouillé à 90° (Horizontal ou Vertical).";
    drawTopView();
  });

  document.getElementById("btnCancelCalibration").addEventListener("click", () => {
    state.topView.calibration.active = false;
    state.topView.calibration.p1 = null;
    state.topView.calibration.p2 = null;
    topWrapper.classList.remove("calibrating");
    document.getElementById("calibrationBanner").classList.add("hidden");
    drawTopView();
  });

  document.getElementById("btnApplyCalibration").addEventListener("click", () => {
    const cal = state.topView.calibration;
    if (!cal.p1 || !cal.p2 || !state.topView.image) return;

    const realDistIn = displayToIn(document.getElementById("inputCalibRealDist").value);
    if (realDistIn <= 0) return;

    const rect = topCanvas.getBoundingClientRect();
    const basePxPerIn = Math.min(rect.width, rect.height) / 160;
    const scale = basePxPerIn * state.topView.zoom;

    const distCanvasPx = Math.hypot(cal.p2.x - cal.p1.x, cal.p2.y - cal.p1.y);
    const currentMeasuredIn = distCanvasPx / scale;

    const oldPpi =
      state.topView.imagePixelsPerInch ||
      state.topView.image.width / state.spa.lengthIn;
    const newPpi = oldPpi * (currentMeasuredIn / realDistIn);

    state.topView.autoFitToSpa = false;
    state.topView.imagePixelsPerInch = newPpi;
    state.topView.calibration.active = false;
    topWrapper.classList.remove("calibrating");
    document.getElementById("calibrationBanner").classList.add("hidden");
    document.getElementById("calibrationScaleBadge").textContent =
      `Étalonné 90° : ${newPpi.toFixed(2)} px/po`;
    drawTopView();
  });

  topCanvas.addEventListener("mousemove", (e) => {
    if (state.topView.calibration.active || state.topView.isPanning) return;
    const local = getLocalCanvasCoords(e);
    let hovered = null;
    for (const pin of state.topView.riskPinHitBoxes) {
      if (Math.abs(local.x - pin.x) <= pin.w / 2 + 6 && Math.abs(local.y - pin.y) <= pin.h / 2 + 6) {
        hovered = pin;
        break;
      }
    }
    if (hovered !== state.topView.hoveredRiskPin) {
      state.topView.hoveredRiskPin = hovered;
      topCanvas.style.cursor = hovered ? "pointer" : "default";
      drawTopView();
    }
  });

  topCanvas.addEventListener("click", (e) => {
    if (state.topView.calibration.active) return;
    const local = getLocalCanvasCoords(e);
    for (const pin of state.topView.riskPinHitBoxes) {
      if (Math.abs(local.x - pin.x) <= pin.w / 2 + 6 && Math.abs(local.y - pin.y) <= pin.h / 2 + 6) {
        state.topView.activeFocusedRiskId = pin.id;
        state.topView.hoveredRiskPin = pin;
        drawTopView();
        break;
      }
    }
  });

  topCanvas.addEventListener("mousedown", (e) => {
    if (state.topView.calibration.active) {
      const rawPt = getLocalCanvasCoords(e);
      if (!state.topView.calibration.p1) {
        state.topView.calibration.p1 = rawPt;
        document.getElementById("calibrationStepText").textContent =
          "Étape 2/2 : Cliquez P2 (verrouillé automatiquement à l'horizontale ou à la verticale)...";
      } else if (!state.topView.calibration.p2) {
        const snapped = snapOrthogonalPoint(state.topView.calibration.p1, rawPt);
        state.topView.calibration.p2 = snapped;
        document.getElementById("calibrationStepText").textContent =
          `Segment ${snapped.axis === "H" ? "Horizontal" : "Vertical"} défini. Saisissez la cote réelle :`;
        const grp = document.getElementById("calibrationInputGroup");
        grp.classList.remove("hidden");
        grp.classList.add("flex");
      } else {
        state.topView.calibration.p1 = rawPt;
        state.topView.calibration.p2 = null;
        document.getElementById("calibrationInputGroup").classList.add("hidden");
        document.getElementById("calibrationInputGroup").classList.remove("flex");
      }
      drawTopView();
      return;
    }

    state.topView.isPanning = true;
    state.topView.panStartX = e.clientX - state.topView.panX;
    state.topView.panStartY = e.clientY - state.topView.panY;
  });

  window.addEventListener("mousemove", (e) => {
    if (state.topView.calibration.active && state.topView.calibration.p1 && !state.topView.calibration.p2) {
      const rawPt = getLocalCanvasCoords(e);
      state.topView.calibration.mousePos = snapOrthogonalPoint(state.topView.calibration.p1, rawPt);
      drawTopView();
    }
    if (!state.topView.isPanning) return;
    state.topView.panX = e.clientX - state.topView.panStartX;
    state.topView.panY = e.clientY - state.topView.panStartY;
    drawTopView();
  });

  window.addEventListener("mouseup", () => {
    state.topView.isPanning = false;
  });

  topCanvas.addEventListener(
    "wheel",
    (e) => {
      e.preventDefault();
      const factor = e.deltaY < 0 ? 1.1 : 1 / 1.1;
      setZoom(state.topView.zoom * factor);
    },
    { passive: false }
  );

  // 12. Exportation du Plan Footprint HD
  document.getElementById("btnExportFootprintHeader").addEventListener("click", exportFootprintPlan);
  document.getElementById("btnExportFootprintCanvas").addEventListener("click", exportFootprintPlan);

  // 13. Bascule Position Fermée / Position Ouverte sur la coupe d'élévation Z
  document.getElementById("btnElevClosed").addEventListener("click", () => setElevationOpenState(false));
  document.getElementById("btnElevOpen").addEventListener("click", () => setElevationOpenState(true));

  // 14. Modale Base de données multi-gammes
  const dbModal = document.getElementById("dbModal");
  document.getElementById("btnOpenDbModal").addEventListener("click", () => dbModal.classList.remove("hidden"));
  document.getElementById("btnCloseDbModal").addEventListener("click", () => dbModal.classList.add("hidden"));
  dbModal.addEventListener("click", (e) => {
    if (e.target === dbModal) dbModal.classList.add("hidden");
  });

  // 15. Redimensionnement de la fenêtre
  window.addEventListener("resize", () => {
    drawTopView();
    drawElevationView();
  });

  // Premier rendu
  syncInputsFromState();
  updateUI();
}

document.addEventListener("DOMContentLoaded", initApp);
