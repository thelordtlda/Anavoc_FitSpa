import requests
from bs4 import BeautifulSoup
import json
from pathlib import Path

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")
CAD_DIR = BASE_DIR / "dataset" / "cad_files"
CAD_DIR.mkdir(parents=True, exist_ok=True)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}

urls = [
    "https://www.jacuzzi.com/en-us/cad-downloads.html",
    "https://www.sundancespas.com/en-us/cad-downloads.html",
]

cad_files = []
for u in urls:
    print(f"Checking {u}...")
    try:
        r = requests.get(u, headers=headers, timeout=15)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                text = a.get_text(strip=True)
                if any(ext in href.lower() for ext in [".dwg", ".dxf", ".skp", ".step", ".stp", ".glb", ".obj", ".zip"]):
                    cad_files.append({"source": u, "text": text, "url": href})
    except Exception as e:
        print(f"Error {u}: {e}")

print(f"Found {len(cad_files)} CAD files:")
for c in cad_files:
    print(c)
