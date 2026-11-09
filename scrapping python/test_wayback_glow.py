import urllib.request
from bs4 import BeautifulSoup

url = 'http://web.archive.org/web/20150602160310/http://www.hotspring.com/shop-hot-tub-models/limelight/4-person-hot-tub-glow'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    soup = BeautifulSoup(html, 'html.parser')
    print('Title:', soup.title.string if soup.title else '')
    
    imgs = []
    for img in soup.find_all('img'):
        src = img.get('src') or ''
        alt = img.get('alt', '')
        if any(ext in src.lower() for ext in ['.jpg', '.png', '.gif']):
            imgs.append((src, alt))
            
    print(f'Glow 2015 images found: {len(imgs)}')
    for s, a in imgs:
        if any(k in s.lower() or k in a.lower() for k in ['glow', 'overhead', 'shell', 'cabinet', 'interior', 'hero', 'top']):
            print(f'  ALT: "{a}" -> {s}')
except Exception as e:
    print('Error:', e)
