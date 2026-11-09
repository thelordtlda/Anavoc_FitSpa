import requests
from bs4 import BeautifulSoup
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

r = requests.get("https://maaxspas.com/", headers=headers, timeout=15)
print("MAAX Spas home status:", r.status_code)
soup = BeautifulSoup(r.text, "html.parser")
links = list(set([a["href"] for a in soup.find_all("a", href=True)]))
print(f"Found {len(links)} unique links on MAAX Spas home:")
spa_links = [l for l in links if any(k in l.lower() for k in ["spa", "hot-tub", "powerpool", "manual", "spec", "series"])]
for l in spa_links:
    print(" -", l)

with open("D:/SPAFIT/Cover Sizer/scrapping python/maax_home_links.json", "w", encoding="utf-8") as f:
    json.dump(links, f, indent=2)
