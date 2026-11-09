import requests
from bs4 import BeautifulSoup
import re

url = "https://www.hotspring.com/shop/highlife/grandee"
headers = {'User-Agent': 'Mozilla/5.0'}
r = requests.get(url, headers=headers, timeout=15)

# Search for ar-button in HTML
soup = BeautifulSoup(r.text, 'html.parser')
ar_tags = soup.find_all(lambda tag: 'ar' in tag.get('class', []) or 'ar-button' in tag.get('class', []) or 'ar' in tag.get('id', '') or tag.has_attr('ar'))
print(f"AR tags found: {len(ar_tags)}")
for t in ar_tags:
    print(t)

# Also regex for any 3d model files: .glb, .gltf, .usdz, .fbx, .obj, .zip, etc.
models_3d = re.findall(r'https?://[^\s"\'<>]+\.(?:glb|gltf|usdz|obj|fbx|step|stp|skp|rfa)', r.text, re.IGNORECASE)
print(f"3D model URLs directly matching: {set(models_3d)}")

# Search for data-ar or model-viewer or sketchfab or 3d script
for script in soup.find_all('script'):
    stext = script.string or ""
    if any(k in stext.lower() for k in ['glb', 'gltf', 'usdz', 'model-viewer', 'augmented']):
        print("Script snippet:", stext[:200])
