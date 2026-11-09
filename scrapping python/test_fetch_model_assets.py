import urllib.request
from bs4 import BeautifulSoup
import re
import json

test_models = {
    'grandee': 'https://www.hotspring.com/shop/highlife/grandee',
    'prism': 'https://www.hotspring.com/shop/limelight/prism',
    'flair': 'https://www.hotspring.com/shop/limelight/flair',
    'aria': 'https://www.hotspring.com/shop/highlife/aria'
}

for name, url in test_models.items():
    print(f"\n=== Model: {name} ({url}) ===")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        soup = BeautifulSoup(html, 'html.parser')
        
        # Look for overhead and dimension images
        overhead = None
        side = None
        dims_img = None
        
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or ''
            alt = img.get('alt', '')
            if 'overhead' in src.lower() or 'overhead' in alt.lower():
                if not overhead: overhead = src
            if ('dimensions' in src.lower() or 'dimension' in src.lower()) and any(ext in src.lower() for ext in ['.png', '.jpg']):
                if not dims_img: dims_img = src
            if ('high-angle' in src.lower() or 'three-quarter' in src.lower() or 'hero' in src.lower()):
                if not side: side = src
                
        print(f"  Overhead photo : {overhead}")
        print(f"  Side/Hero photo: {side}")
        print(f"  Dimensions plan: {dims_img}")
        
    except Exception as e:
        print(f"  Error: {e}")
