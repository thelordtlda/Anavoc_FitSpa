import urllib.request
from bs4 import BeautifulSoup
import re

url = 'https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, timeout=25) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
soup = BeautifulSoup(html, 'html.parser')

print("Searching for year buttons or headers...")
for tag in soup.find_all(['button', 'h1', 'h2', 'h3', 'h4', 'div', 'span', 'summary', 'li', 'p']):
    t = tag.get_text(strip=True)
    if any(y in t for y in ['2026', '2025', '2024', '2020', '2015', '2010', '2005', '2002']):
        if len(t) < 40 and len(tag.find_all()) < 2:
            print(f"Tag: <{tag.name}> Class: {tag.get('class')} -> '{t}'")
