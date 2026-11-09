import urllib.request
from bs4 import BeautifulSoup
import json

url = 'https://www.hotspring.com/shop/hot-spot/tx'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

print('Title:', soup.title.string if soup.title else '')

imgs = []
for img in soup.find_all('img'):
    src = img.get('src') or img.get('data-src')
    alt = img.get('alt', '')
    if src:
        imgs.append((src, alt))

print(f'Total images found on Hot Spot TX page: {len(imgs)}')
for src, alt in imgs:
    if any(ext in src.lower() for ext in ['.jpg', '.png', '.webp', '.svg']):
        if any(k in src.lower() or k in alt.lower() for k in ['tx', 'overhead', 'shell', 'cabinet', 'hot-spot', 'tub', 'spa', 'gallery', 'render']):
            print(f'  ALT: "{alt}" | SRC: {src}')
