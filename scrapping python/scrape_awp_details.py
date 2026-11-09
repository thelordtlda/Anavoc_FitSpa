import requests
from bs4 import BeautifulSoup
import json
import re
from pathlib import Path

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")
with open(BASE_DIR / "awp_discovered_products.json", "r", encoding="utf-8") as f:
    products = json.load(f)

# Filter out non-spa products like chemicals or cords
spa_prods = [p for p in products if any(k in p["url"] for k in ["-spa", "-model", "-hot-tub", "swim-spa"])]
print(f"Total Spa Products on American Whirlpool: {len(spa_prods)}")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"
}

scraped_data = []
for p in spa_prods:
    url = p["url"]
    slug = url.split("/")[-2] if url.endswith("/") else url.split("/")[-1]
    print(f"Scraping {slug}...")
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            continue
        soup = BeautifulSoup(r.text, "html.parser")
        
        # Look for dimensions in table or paragraphs
        text = soup.get_text()
        
        # Search for dimensions format: 92" x 92" or 84" x 84"
        dim_match = re.search(r'(\d{2,3}(?:\.\d+)?)\s*(?:\"|”|po|in)?\s*[xX×]\s*(\d{2,3}(?:\.\d+)?)\s*(?:\"|”|po|in)?\s*[xX×]\s*(\d{2}(?:\.\d+)?)\s*(?:\"|”|po|in)?', text)
        dim_2d = re.search(r'(\d{2,3}(?:\.\d+)?)\s*(?:\"|”|po|in)?\s*[xX×]\s*(\d{2,3}(?:\.\d+)?)\s*(?:\"|”|po|in)?', text)
        
        # Images on product page
        imgs = []
        for img in soup.find_all("img"):
            src = img.get("src") or img.get("data-src")
            if src and any(ext in src.lower() for ext in [".jpg", ".png", ".webp"]) and not any(k in src.lower() for k in ["logo", "icon", "banner", "cookie"]):
                imgs.append(src)
                
        scraped_data.append({
            "slug": slug,
            "url": url,
            "dim_3d": dim_match.groups() if dim_match else None,
            "dim_2d": dim_2d.groups() if dim_2d else None,
            "images": list(set(imgs))[:5]
        })
    except Exception as e:
        print(f"  Error on {slug}: {e}")

with open(BASE_DIR / "awp_scraped_specs.json", "w", encoding="utf-8") as f:
    json.dump(scraped_data, f, indent=2)

print(f"\nScraped {len(scraped_data)} American Whirlpool spa specs and images!")
