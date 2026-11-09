import os
import re
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")
MANUALS_DIR = BASE_DIR / "spa_manuals" / "sundance_spas"
MANUALS_DIR.mkdir(parents=True, exist_ok=True)
CAD_DIR = BASE_DIR / "dataset" / "sundance_spas" / "cad_files"
CAD_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

def harvest_sundance_manuals():
    urls = [
        "https://www.sundancespas.com/en-us/owner-resources/manuals-and-user-guides.html",
        "https://www.sundancespas.com/en-us/owner-resources/pre-delivery-guides.html",
        "https://www.sundancespas.com/en-us/cad-downloads.html",
        "https://www.sundancespas.com/en-us/owner-resources/specifications.html",
    ]
    
    discovered_links = []
    seen = set()
    
    for url in urls:
        print(f"Fetching {url}...")
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            print(f"Status {r.status_code} for {url}")
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, "html.parser")
                for a in soup.find_all("a", href=True):
                    href = a["href"].strip()
                    title = a.get_text(strip=True)
                    if any(x in href.lower() for x in [".pdf", "imagerelay.com", ".dwg", ".dxf", ".skp", ".step", ".stp"]):
                        full_url = href if href.startswith("http") else f"https://www.sundancespas.com{href}"
                        if full_url not in seen:
                            seen.add(full_url)
                            discovered_links.append({"title": title, "url": full_url, "source": url})
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            
    return discovered_links

if __name__ == "__main__":
    links = harvest_sundance_manuals()
    print(f"Found {len(links)} links for Sundance Spas.")
    out_file = BASE_DIR / "sundance_discovered_links.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(links, f, indent=2, ensure_ascii=False)
    print(f"Exported to {out_file}")
