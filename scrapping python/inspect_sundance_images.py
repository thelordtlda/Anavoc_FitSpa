import requests
from bs4 import BeautifulSoup
import re
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

# Fetch the Sundance spas product listing or sitemap
r = requests.get("https://www.sundancespas.com/product-listing-page", headers=headers, timeout=15)
print("Product listing page status:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")
img_urls = []
for img in soup.find_all("img"):
    src = img.get("src") or img.get("data-src")
    if src and any(ext in src.lower() for ext in [".png", ".jpg", ".webp"]):
        img_urls.append(src)

print(f"Found {len(img_urls)} images on product listing page.")
for u in img_urls[:15]:
    print(" ", u)
