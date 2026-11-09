import urllib.request
import re
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
url = "https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings"
req = urllib.request.Request(url, headers=HEADERS)
with urllib.request.urlopen(req, timeout=30) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')

links = soup.find_all('a', href=True)
glow_links = []
for a in links:
    href = a['href']
    text = a.get_text(strip=True)
    if 'glow' in href.lower() or 'glow' in text.lower():
        glow_links.append((text, href))

print(f"Total Glow links on HotSpring page: {len(glow_links)}")
for t, h in glow_links:
    print(f"  {t} -> {h}")
