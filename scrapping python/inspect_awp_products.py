import requests
import xml.etree.ElementTree as ET
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

r = requests.get("https://americanwhirlpool.com/product-sitemap.xml", headers=headers, timeout=15)
root = ET.fromstring(r.content)
products = []
for url_elem in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
    loc = url_elem.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
    # Check for image elements if present
    imgs = [img.find('{http://www.google.com/schemas/sitemap-image/1.1}loc').text 
            for img in url_elem.findall('{http://www.google.com/schemas/sitemap-image/1.1}image')
            if img.find('{http://www.google.com/schemas/sitemap-image/1.1}loc') is not None]
    products.append({"url": loc, "images": imgs})

print(f"Found {len(products)} products in American Whirlpool sitemap:")
for p in products:
    slug = p["url"].split("/")[-2] if p["url"].endswith("/") else p["url"].split("/")[-1]
    print(f" - {slug}: {len(p['images'])} images (url: {p['url']})")

with open("D:/SPAFIT/Cover Sizer/scrapping python/awp_discovered_products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, indent=2)
