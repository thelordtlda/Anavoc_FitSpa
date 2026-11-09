import requests
import re
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# 1. Check Bullfrog Design Studio
urls = [
    'https://www.bullfrogspas.com/design-studio/',
    'https://www.bullfrogspas.com/spas/m-series/m9/',
    'https://www.bullfrogspas.com/spas/a-series/a9l/',
]

for url in urls:
    try:
        r = requests.get(url, headers=headers, timeout=15)
        print(f"URL: {url} -> {r.status_code}")
        # search for 3D model extensions
        models = re.findall(r'https?://[^\s"\'<>]+\.(?:glb|gltf|obj|fbx|usdz|dae|stl)', r.text, re.I)
        print("  Direct 3D models:", set(models))
        
        # search for model-viewer or threejs or sketchfab or iframe
        soup = BeautifulSoup(r.text, 'html.parser')
        model_viewers = soup.find_all(['model-viewer', 'canvas'])
        print("  Canvas / model-viewers:", len(model_viewers))
        
        iframes = [i.get('src') for i in soup.find_all('iframe') if i.get('src')]
        print("  iFrames:", iframes[:5])
    except Exception as e:
        print(f"Error {url}: {e}")
