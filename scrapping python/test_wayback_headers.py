import urllib.request
from bs4 import BeautifulSoup
import time

time.sleep(2)
url = 'https://web.archive.org/web/20150516151039/http://www.hotspring.com:80/shop-hot-tub-models/limelight/4-person-hot-tub-glow'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://web.archive.org/'
}

req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    print("SUCCESS! Title:", soup.title.string if soup.title else "")
    
    imgs = []
    for img in soup.find_all('img'):
        src = img.get('src') or ''
        alt = img.get('alt', '')
        if any(ext in src.lower() for ext in ['.jpg', '.png', '.gif']):
            imgs.append((src, alt))
            
    print(f"Total images found: {len(imgs)}")
    for s, a in imgs:
        if any(k in s.lower() or k in a.lower() for k in ['glow', 'limelight', 'spa', 'tub', 'overhead', 'shell']):
            print(f"  {a} -> {s}")
except Exception as e:
    print("Error:", e)
