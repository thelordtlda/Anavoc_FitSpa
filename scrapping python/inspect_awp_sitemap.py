import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

r = requests.get("https://americanwhirlpool.com/sitemap_index.xml", headers=headers, timeout=15)
print("sitemap_index.xml status:", r.status_code)
if r.status_code != 200:
    r = requests.get("https://americanwhirlpool.com/sitemap.xml", headers=headers, timeout=15)
    print("sitemap.xml status:", r.status_code)

if r.status_code == 200:
    root = ET.fromstring(r.content)
    locs = [elem.text for elem in root.iter() if elem.tag.endswith('loc') and elem.text]
    print(f"Found {len(locs)} entries:")
    for l in locs[:20]:
        print(" ", l)
else:
    # Scrape homepage links
    resp = requests.get("https://americanwhirlpool.com/", headers=headers, timeout=15)
    soup = BeautifulSoup(resp.text, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True)]
    print(f"Homepage has {len(links)} links")
    for l in links[:20]:
        print(" ", l)
