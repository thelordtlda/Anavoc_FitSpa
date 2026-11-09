import requests
import xml.etree.ElementTree as ET
import re
import json
from pathlib import Path

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

# Fetch sitemap.xml to find all product pages
r = requests.get("https://www.sundancespas.com/sitemap.xml", headers=headers, timeout=15)
root = ET.fromstring(r.content)
all_urls = [elem.text for elem in root.iter() if elem.tag.endswith('loc') and elem.text]

spa_urls = [u for u in all_urls if not any(x in u for x in ["/dealers/", "/de/", "/pl/", "/nl/", "/fr/", "/es-419/", "/en-gb/"])]
print(f"Total US/EN URLs: {len(spa_urls)}")

# Filter models
model_slugs = ["kingston", "claremont", "lisbon", "odessa", "aspen", "maxxus", "cameo", "optima", "altamar", "marin", "capri", "chelsee", "hamilton", "bristol", "hanover", "montclair", "dover", "prado", "peyton", "edison", "ramona", "denali", "tacoma", "alicia", "stream", "surf"]

matched_urls = []
for u in spa_urls:
    if any(m in u.lower() for m in model_slugs):
        matched_urls.append(u)

print(f"Matched {len(matched_urls)} spa product URLs:")
for u in matched_urls:
    print(" -", u)

with open("D:/SPAFIT/Cover Sizer/scrapping python/sundance_matched_product_urls.json", "w", encoding="utf-8") as f:
    json.dump(matched_urls, f, indent=2)
