import os
import re
import json
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")
IMG_ROOT = BASE_DIR / "images" / "sundance_spas"
IMG_ROOT.mkdir(parents=True, exist_ok=True)

with open(BASE_DIR / "sundance_matched_product_urls.json", "r", encoding="utf-8") as f:
    urls = json.load(f)

# Filter only /products/ URLs
prod_urls = [u for u in urls if "/products/" in u]
print(f"Scraping {len(prod_urls)} Sundance product pages for top & side images...")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

for u in prod_urls:
    slug = u.split("/")[-1].replace("-my26", "").lower()
    print(f"\n--- Model: {slug} from {u} ---")
    model_dir = IMG_ROOT / slug
    model_dir.mkdir(parents=True, exist_ok=True)
    
    top_file = model_dir / "top_view.webp"
    side_file = model_dir / "side_view.webp"
    
    if top_file.exists() and side_file.exists():
        print(f"  [EXISTS] {slug} already has top and side views.")
        continue
        
    try:
        r = requests.get(u, headers=headers, timeout=20)
        if r.status_code != 200:
            print(f"  [ERROR] Status {r.status_code}")
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Find images
        found_imgs = []
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src")
            if src and "cdn.prod.website-files.com" in src:
                found_imgs.append(src)
                
        # Also check background-images or JSON-LD in HTML
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string)
                if isinstance(data, dict) and "image" in data:
                    imgs = data["image"] if isinstance(data["image"], list) else [data["image"]]
                    found_imgs.extend(imgs)
            except Exception:
                pass
                
        found_imgs = list(dict.fromkeys(found_imgs))
        print(f"  Found {len(found_imgs)} CDN images for {slug}")
        
        top_url = None
        side_url = None
        
        # Classify top vs side
        for img_url in found_imgs:
            url_lower = img_url.lower()
            if any(k in url_lower for k in ["overhead", "top", "topdown", "oh", "acrylic"]):
                if not top_url:
                    top_url = img_url
            elif any(k in url_lower for k in ["srgb", "side", "iso", "angle", "platinum", "cabinet"]):
                if not side_url:
                    side_url = img_url
                    
        # Fallback if no specific top/side keyword was hit:
        # Usually webflow gallery puts side/hero first, and top view in thumbnails
        if not top_url and len(found_imgs) > 1:
            top_url = found_imgs[1]
        elif not top_url and len(found_imgs) == 1:
            top_url = found_imgs[0]
            
        if not side_url and found_imgs:
            side_url = found_imgs[0]
            
        # Download top view
        if top_url and not top_file.exists():
            print(f"  Downloading top view: {top_url[:80]}...")
            res = requests.get(top_url, headers=headers, timeout=30)
            if res.status_code == 200:
                with open(top_file, "wb") as f_out:
                    f_out.write(res.content)
                print(f"  [SAVED] top_view.webp ({top_file.stat().st_size // 1024} KB)")
                
        # Download side view
        if side_url and not side_file.exists():
            print(f"  Downloading side view: {side_url[:80]}...")
            res = requests.get(side_url, headers=headers, timeout=30)
            if res.status_code == 200:
                with open(side_file, "wb") as f_out:
                    f_out.write(res.content)
                print(f"  [SAVED] side_view.webp ({side_file.stat().st_size // 1024} KB)")
                
    except Exception as e:
        print(f"  [EXCEPTION] {slug}: {e}")
        
    time.sleep(0.5)

print("\n=== Sundance Spas Image Harvesting Completed ===")
