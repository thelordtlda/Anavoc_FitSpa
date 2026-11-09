import requests
import xml.etree.ElementTree as ET
import re

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

r = requests.get("https://www.sundancespas.com/sitemap.xml", headers=headers, timeout=15)
print("Sitemap root status:", r.status_code)
# Parse XML
try:
    root = ET.fromstring(r.content)
    sitemaps = [elem.text for elem in root.iter() if elem.tag.endswith('loc')]
    print(f"Found {len(sitemaps)} sub-sitemaps:")
    for sm in sitemaps:
        print(" -", sm)
except Exception as e:
    print("Error parsing root sitemap:", e)
    print(r.text[:500])
