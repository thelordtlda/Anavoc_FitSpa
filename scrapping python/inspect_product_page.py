import requests
from bs4 import BeautifulSoup
import re

url = "https://www.hotspring.com/shop/highlife/grandee"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(url, headers=headers, timeout=15)
soup = BeautifulSoup(r.text, 'html.parser')

print(f"Grandee page length: {len(r.text)}")

# Find any 3D, canvas, glb, gltf, usdz, model-viewer, babylon, threejs
text = r.text.lower()
for ext in ['.glb', '.gltf', '.usdz', '.obj', '.fbx', 'model-viewer', '3d', 'ar-button', 'augmented']:
    count = text.count(ext)
    if count > 0:
        print(f"Found keyword '{ext}': {count} occurrences")

# Find images on this product page
images = soup.find_all('img')
print(f"Total img tags: {len(images)}")
for img in images:
    src = img.get('src', '') or img.get('data-src', '')
    if any(k in src.lower() for k in ['grandee', 'overhead', 'top', 'cabinet', 'hero', 'render', 'tub']):
        print("  IMG:", src)
