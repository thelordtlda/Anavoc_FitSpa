import requests
import fitz
import cv2
import numpy as np
from pathlib import Path

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")
IMG_DIR = BASE_DIR / "images" / "bullfrog_spas"
DATASET_DIR = BASE_DIR / "dataset" / "bullfrog_spas"
FP_DIR = DATASET_DIR / "extracted_footprints"
FP_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# 1. Télécharger les vues zénithales directes de haute qualité
URLS = [
    ("s150", "https://www.bullfrogspas.com/wp-content/uploads/2024/05/S150_TopDown--614x1024.png"),
    ("s200", "https://www.bullfrogspas.com/wp-content/uploads/2024/05/S200_TopDown--768x1280.png")
]

print("=== TÉLÉCHARGEMENT DES VUES ZÉNITHALES SWIM SERIES ===")
for m_code, url in URLS:
    dest_dir = IMG_DIR / m_code
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest_file = dest_dir / "top_view.png"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200 and len(r.content) > 10000:
            with open(dest_file, "wb") as f:
                f.write(r.content)
            print(f"[OK] {m_code}: Sauvegardé top_view.png ({len(r.content)} bytes)")
        else:
            print(f"[WARN] {m_code}: Status {r.status_code}")
    except Exception as e:
        print(f"[ERROR] {m_code}: {e}")

# 2. Extraire les plans cotés vectoriels (300 DPI) depuis les PDF officiels
print("\n=== EXTRACTION DES PLANS COTÉS SWIM SERIES ===")
# S150 depuis 2024_Spa-layouts-electric-installation.pdf (Page 1)
layouts_pdf = BASE_DIR / "spa_manuals" / "bullfrog_spas" / "2024_Spa-layouts-electric-installation.pdf"
if layouts_pdf.exists():
    doc = fitz.open(layouts_pdf)
    page = doc[0]
    zoom = 300.0 / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    img_bgr = cv2.cvtColor(np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3)), cv2.COLOR_RGB2BGR)
    
    # Autocrop
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)
    non_zero = cv2.findNonZero(thresh)
    if non_zero is not None:
        x, y, w, h = cv2.boundingRect(non_zero)
        img_bgr = img_bgr[max(0, y-35):min(img_bgr.shape[0], y+h+35), max(0, x-35):min(img_bgr.shape[1], x+w+35)]
        
    s150_fp = FP_DIR / "2024_Spa-layouts_p1_S150_footprint.png"
    cv2.imwrite(str(s150_fp), img_bgr)
    print(f"[OK] Extrait schéma S150 : {s150_fp.name} ({img_bgr.shape[1]}x{img_bgr.shape[0]} px)")

# S200 et S180 depuis 2024_Pre-Delivery-Guide_8_5x11_v1.pdf (Page 9)
predeliv_pdf = BASE_DIR / "spa_manuals" / "bullfrog_spas" / "2024_Pre-Delivery-Guide_8_5x11_v1.pdf"
if predeliv_pdf.exists():
    doc = fitz.open(predeliv_pdf)
    page = doc[8]  # Page 9 (0-indexed 8)
    zoom = 300.0 / 72.0
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), alpha=False)
    img_bgr = cv2.cvtColor(np.frombuffer(pix.samples, dtype=np.uint8).reshape((pix.height, pix.width, 3)), cv2.COLOR_RGB2BGR)
    
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)
    non_zero = cv2.findNonZero(thresh)
    if non_zero is not None:
        x, y, w, h = cv2.boundingRect(non_zero)
        img_bgr = img_bgr[max(0, y-35):min(img_bgr.shape[0], y+h+35), max(0, x-35):min(img_bgr.shape[1], x+w+35)]
        
    swim_all_fp = FP_DIR / "2024_Pre-Delivery_p9_S200_S180_footprint.png"
    cv2.imwrite(str(swim_all_fp), img_bgr)
    print(f"[OK] Extrait schéma Swim Series (S200/S180) : {swim_all_fp.name} ({img_bgr.shape[1]}x{img_bgr.shape[0]} px)")
