import requests
from bs4 import BeautifulSoup
import re

url = "https://www.hotspring.com/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
try:
    r = requests.get(url, headers=headers, timeout=15)
    print(f"Status: {r.status_code}")
    soup = BeautifulSoup(r.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    spa_links = [l for l in links if any(k in l.lower() for k in ['highlife', 'limelight', 'hot-spot', 'collection', 'spas', 'model'])]
    spa_links = sorted(list(set(spa_links)))
    print(f"Found {len(spa_links)} spa links:")
    for l in spa_links[:25]:
        print(" ", l)
except Exception as e:
    print(f"Error: {e}")
