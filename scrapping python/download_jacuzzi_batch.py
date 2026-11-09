import os
import sys
import requests
from pathlib import Path

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")
MANUALS_DIR = BASE_DIR / "spa_manuals" / "jacuzzi"
IMAGES_DIR = BASE_DIR / "images" / "jacuzzi"
MANUALS_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

PDF_TARGETS = [
    ("2015_JHT_J-500.pdf", "https://links.imagerelay.com/cdn/574/ql/3d536bdfa83b4a428ddaa615dcea1fbe/2015_JHT_J-500.pdf"),
    ("2020_JHT_J-500.pdf", "https://links.imagerelay.com/cdn/574/ql/bd0f5160aeb94772a9633bec10d88f05/2020_JHT_J-500.pdf"),
    ("2016_JHT_J-400.pdf", "https://links.imagerelay.com/cdn/574/ql/bfda658d1668431a8de575c8ed1296c3/2016_JHT_J-400.pdf"),
    ("2018_JHT_J-435_445.pdf", "https://links.imagerelay.com/cdn/574/ql/1d9e67b132fe4977b969e767ab28d0fb/2018_JHT_J-435_445.pdf"),
    ("2020_JHT_J-400.pdf", "https://links.imagerelay.com/cdn/574/ql/b71178968cde42ab8c0ff4a610630730/2020_JHT_J-400.pdf"),
    ("2015_JHT_J-300.pdf", "https://links.imagerelay.com/cdn/574/ql/ed596d1250e94d118606ce8f6969c103/2015_JHT_J-300.pdf"),
    ("2020_JHT_J-300.pdf", "https://links.imagerelay.com/cdn/574/ql/049a5e23364d415aa5537635eb68a4da/2020_JHT_J-300.pdf"),
    ("2015_JHT_J-200.pdf", "https://links.imagerelay.com/cdn/574/ql/f545013f8f664b10b2598f589113b8e4/2015_JHT_J-200.pdf"),
    ("2020_JHT_J-200.pdf", "https://links.imagerelay.com/cdn/574/ql/2141e48c19e74ae2b8cde75379d23015/2020_JHT_J-200.pdf"),
    ("2015_JHT_J-LX.pdf", "https://links.imagerelay.com/cdn/574/ql/ee4b6565ced64e08ba0301640ded60c1/2015_JHT_J-LX.pdf"),
    ("2024_JLX_English.pdf", "https://links.imagerelay.com/cdn/574/ql/c1d71cb94e184411a01032f9077f136e/2024-JLX-English-Rev-A.pdf"),
    ("2025_JLX_English.pdf", "https://links.imagerelay.com/cdn/574/ql/4bde3054d78e464486257551e66c6167/25-JLX-ENG-Rev-E-110325-L.pdf"),
    ("2026_J4_English.pdf", "https://links.imagerelay.com/cdn/574/ql/06a768287df94d069b0550be109b6862/26-J4-ENG-60Hz-web-112425-L.pdf"),
    ("2023_JHT_Play_Manual.pdf", "https://links.imagerelay.com/cdn/574/ql/351fba54a19f4feba1b0244d61723206/JHT-Play-Manual-L.pdf"),
]

def download_manuals():
    print(f"=== DOWNLOADING {len(PDF_TARGETS)} JACUZZI MANUALS ===")
    for filename, url in PDF_TARGETS:
        dest = MANUALS_DIR / filename
        if dest.exists() and dest.stat().st_size > 50000:
            print(f"[SKIP] {filename} exists ({dest.stat().st_size} bytes)")
            continue
        print(f"[DOWNLOADING] {filename} from {url}...")
        try:
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200 and len(r.content) > 10000:
                with open(dest, "wb") as f:
                    f.write(r.content)
                print(f"[SAVED] {filename} ({len(r.content)} bytes)")
            else:
                print(f"[FAILED] {filename}: status {r.status_code}, len {len(r.content)}")
        except Exception as e:
            print(f"[ERROR] {filename}: {e}")

if __name__ == "__main__":
    download_manuals()
