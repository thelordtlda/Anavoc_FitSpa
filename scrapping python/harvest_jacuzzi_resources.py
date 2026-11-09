import os
import re
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")
MANUALS_DIR = BASE_DIR / "spa_manuals" / "jacuzzi"
MANUALS_DIR.mkdir(parents=True, exist_ok=True)
CAD_DIR = BASE_DIR / "dataset" / "jacuzzi" / "cad_files"
CAD_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

def harvest_manual_links():
    url = "https://www.jacuzzi.com/en-us/resources/manuals-and-user-guides.html"
    print(f"Fetching {url}...")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        
        pdf_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            title = a.get_text(strip=True)
            if ".pdf" in href.lower() or "imagerelay.com" in href.lower():
                pdf_links.append({"title": title, "url": href})
        
        print(f"Found {len(pdf_links)} PDF/Manual links on page.")
        return pdf_links
    except Exception as e:
        print(f"Error fetching manual links: {e}")
        return []

def harvest_cad_downloads():
    url = "https://www.jacuzzi.com/en-us/cad-downloads.html"
    print(f"Fetching CAD downloads from {url}...")
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        
        cad_links = []
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            title = a.get_text(strip=True)
            if any(ext in href.lower() for ext in [".dwg", ".dxf", ".skp", ".step", ".stp", ".obj", ".glb", ".gltf", ".zip", ".pdf"]):
                cad_links.append({"title": title, "url": href})
        
        print(f"Found {len(cad_links)} CAD/file links on CAD page.")
        return cad_links
    except Exception as e:
        print(f"Error fetching CAD page: {e}")
        return []

if __name__ == "__main__":
    manuals = harvest_manual_links()
    cad = harvest_cad_downloads()
    
    with open(BASE_DIR / "jacuzzi_discovered_manuals.json", "w", encoding="utf-8") as f:
        json.dump(manuals, f, indent=2)
        
    with open(BASE_DIR / "jacuzzi_discovered_cad.json", "w", encoding="utf-8") as f:
        json.dump(cad, f, indent=2)
        
    print("Exported jacuzzi_discovered_manuals.json and jacuzzi_discovered_cad.json")
