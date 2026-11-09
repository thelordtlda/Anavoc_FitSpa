import urllib.request
import re
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0'}
url = "https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings"
req = urllib.request.Request(url, headers=HEADERS)
with urllib.request.urlopen(req, timeout=30) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')
links_2010 = []
for a in soup.find_all('a', href=True):
    href = a['href']
    txt = a.get_text(strip=True)
    if '2010' in href or '2010' in txt:
        links_2010.append((txt, href))

print(f"Total 2010 links: {len(links_2010)}")
for t, h in links_2010:
    print(f"  [{t}] {h}")
