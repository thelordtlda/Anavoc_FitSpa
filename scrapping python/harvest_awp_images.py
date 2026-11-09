import os
import re
import json
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")
IMG_ROOT = BASE_DIR / "images" / "american_whirlpool"
IMG_ROOT.mkdir(parents=True, exist_ok=True)

with open(BASE_DIR / "awp_discovered_products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

spa_prods = [p for p in products if any(k in p["url"] for k in ["-spa", "-model", "-hot-tub", "swim-spa"])]
print(f"Downloading images for {len(spa_prods)} American Whirlpool models...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"
}

for p in spa_prods:
    url = p["url"]
    slug = url.split("/")[-2] if url.endswith("/") else url.split("/")[-1]
    # Normalize model code e.g. "american-whirlpool-481-spa" -> "481", "american-whirlpool-dm8-swim-spa" -> "dm8"
    m_match = re.search(r'(?:american-whirlpool-)?([a-z0-9]+)(?:-(?:spa|model|swim-spa|model-hot-tub|hot-tub))?', slug)
    clean_code = m_match.group(1).lower() if m_match else slug
    
    model_dir = IMG_ROOT / clean_code
    model_dir.mkdir(parents=True, exist_ok=True)
    
    top_file = model_dir / "top_view.jpg"
    side_file = model_dir / "side_view.jpg"
    
    if top_file.exists() and side_file.exists():
        print(f"  [EXISTS] {clean_code} already downloaded.")
        continue
        
    try:
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code != 200:
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Collect product gallery images
        imgs = []
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src") or img.get("data-large_image")
            if src and any(ext in src.lower() for ext in [".jpg", ".png", ".webp"]) and "wp-content/uploads" in src:
                if not any(k in src.lower() for k in ["logo", "icon", "first-filter-demo", "badge", "award"]):
                    imgs.append(src)
                    
        imgs = list(dict.fromkeys(imgs))
        print(f"  Model {clean_code}: {len(imgs)} candidate images found")
        
        top_url = None
        side_url = None
        for img_url in imgs:
            url_lower = img_url.lower()
            if any(k in url_lower for k in ["top", "overhead", "oh", "layout", "render"]):
                if not top_url:
                    top_url = img_url
            elif any(k in url_lower for k in ["side", "iso", "angle", "cabinet", "2025", "2024", "600x600"]):
                if not side_url:
                    side_url = img_url
                    
        if not top_url and imgs:
            top_url = imgs[0]
        if not side_url and len(imgs) > 1:
            side_url = imgs[1]
        elif not side_url and imgs:
            side_url = imgs[0]
            
        if top_url and not top_file.exists():
            ext = ".webp" if ".webp" in top_url.lower() else (".png" if ".png" in top_url.lower() else ".jpg")
            dest = model_dir / f"top_view{ext}"
            res = requests.get(top_url, headers=headers, timeout=25)
            if res.status_code == 200:
                with open(dest, "wb") as f_out:
                    f_out.write(res.content)
                print(f"    [SAVED] {dest.name} ({dest.stat().st_size//1024} KB)")
                
        if side_url and not side_file.exists():
            ext = ".webp" if ".webp" in side_url.lower() else (".png" if ".png" in side_url.lower() else ".jpg")
            dest = model_dir / f"side_view{ext}"
            res = requests.get(side_url, headers=headers, timeout=25)
            if res.status_code == 200:
                with open(dest, "wb") as f_out:
                    f_out.write(res.content)
                print(f"    [SAVED] {dest.name} ({dest.stat().st_size//1024} KB)")
                
    except Exception as e:
        print(f"  [ERROR] {clean_code}: {e}")
    time.sleep(0.3)

print("American Whirlpool image harvesting completed!")
