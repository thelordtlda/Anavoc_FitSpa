import requests
from bs4 import BeautifulSoup
import re
from pathlib import Path
import json

base_dir = Path(__file__).resolve().parent
hs_dataset = base_dir / "dataset" / "hot_spring_spas"

shop_models = [
    ("highlife", "grandee"),
    ("highlife", "envoy"),
    ("highlife", "aria"),
    ("highlife", "vanguard"),
    ("highlife", "sovereign"),
    ("highlife", "prodigy"),
    ("highlife", "jetsetter"),
    ("highlife", "jetsetter-lx"),
    ("limelight", "prism"),
    ("limelight", "pulse"),
    ("limelight", "flash"),
    ("limelight", "flair"),
    ("limelight", "beam"),
    ("hot-spot", "rhythm"),
    ("hot-spot", "relay"),
    ("hot-spot", "pace"),
    ("hot-spot", "stride"),
    ("hot-spot", "sx"),
    ("hot-spot", "tx")
]

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

harvested = {}

for series, model in shop_models:
    url = f"https://www.hotspring.com/shop/{series}/{model}"
    print(f"\nScraping {series}/{model} from {url}...")
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code != 200:
            print(f"  HTTP error {r.status_code}")
            continue
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Find overhead / top-view
        overhead_url = None
        side_url = None
        
        for img in soup.find_all('img'):
            src = img.get('src', '') or img.get('data-src', '')
            if not src: continue
            
            src_l = src.lower()
            # check overhead
            if not overhead_url:
                if any(k in src_l for k in ['overhead', 'top-view', 'top_view', 'seats-overhead']) and model in src_l:
                    overhead_url = src
            # check side / hero / threequarter
            if not side_url:
                if any(k in src_l for k in ['threequarter', 'hero', 'cabinet', 'exterior', 'lifestyle']) and model in src_l:
                    side_url = src
                    
        print(f"  Found overhead: {overhead_url}")
        print(f"  Found side: {side_url}")
        harvested[model] = {
            "series": series,
            "overhead": overhead_url,
            "side": side_url
        }
    except Exception as e:
        print(f"  Error: {e}")

with open("D:/SPAFIT/Cover Sizer/scrapping python/hotspring_current_shop_images.json", "w", encoding="utf-8") as f:
    json.dump(harvested, f, indent=2)

print("\nDone scraping current shop models!")
