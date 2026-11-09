import requests
from bs4 import BeautifulSoup
import re

url = "https://www.hotspring.com/hot-tub-models"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
try:
    r = requests.get(url, headers=headers, timeout=15)
    print(f"Status: {r.status_code}, Length: {len(r.text)}")
    soup = BeautifulSoup(r.text, 'html.parser')
    model_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/hot-tub-models/' in href or '/spas/' in href:
            model_links.append(href)
    model_links = sorted(list(set(model_links)))
    print(f"Discovered {len(model_links)} model links on HotSpring site:")
    for l in model_links[:20]:
        print(" ", l)
except Exception as e:
    print(f"Error: {e}")
