import urllib.request
from bs4 import BeautifulSoup
import re
import json

urls_to_check = [
    'https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings',
    'https://www.hotspring.com/shop/highlife/grandee',
    'https://www.hotspring.com/shop/limelight/prism',
    'https://www.hotspring.com/shop/hot-spot/tx',
    'https://www.hotspring.com/owners/manuals-and-resources'
]

ext_regex = re.compile(r'https?://[^\s"\'<>]+\.(?:glb|gltf|usdz|skp|rfa|rvt|step|stp|obj|fbx|3ds|dae)', re.IGNORECASE)

found_3d = set()

for url in urls_to_check:
    print(f"Scanning {url}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        matches = ext_regex.findall(html)
        for m in matches:
            found_3d.add(m)
        # Also look for 3d viewer tags like <model-viewer>, sketchfab, or three.js bundles
        soup = BeautifulSoup(html, 'html.parser')
        mv = soup.find_all(['model-viewer', 'canvas'])
        if mv:
            print(f"  Found 3D elements: {[m.name for m in mv]}")
    except Exception as e:
        print(f"  Error: {e}")

print(f"\nTotal 3D models found: {len(found_3d)}")
for f in found_3d:
    print("  ->", f)
