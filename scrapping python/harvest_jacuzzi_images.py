import os
import re
import json
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")
IMAGES_DIR = BASE_DIR / "images" / "jacuzzi"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}

# Modèles cibles Jacuzzi
TARGET_MODELS = [
    # J-500
    ("J509", "https://www.jacuzzi.com/en-us/j509/J509-MY26.html"),
    ("J508", "https://www.jacuzzi.com/en-us/j508/J508-MY26.html"),
    ("J508L", "https://www.jacuzzi.com/en-us/j508l/J508L-MY26.html"),
    ("J-585", "https://www.jacuzzi.com/en-us/j508/J508-MY26.html"),
    ("J-575", "https://www.jacuzzi.com/en-us/j508l/J508L-MY26.html"),
    # J-400
    ("J408", "https://www.jacuzzi.com/en-us/j408/J408-MY26.html"),
    ("J408L", "https://www.jacuzzi.com/en-us/j408l/J408L-MY26.html"),
    ("J404L", "https://www.jacuzzi.com/en-us/j404l/J404L-MY26.html"),
    ("J-495", "https://www.jacuzzi.com/en-us/j-495/J-495.html"),
    ("J-485", "https://www.jacuzzi.com/en-us/j-485/J-485.html"),
    ("J-475", "https://www.jacuzzi.com/en-us/j-475/J-475.html"),
    ("J-445", "https://www.jacuzzi.com/en-us/j-445/J-445.html"),
    ("J-435", "https://www.jacuzzi.com/en-us/j-435/J-435.html"),
    # J-300
    ("J-385", "https://www.jacuzzi.com/en-us/j-385/J-385-MY26.html"),
    ("J-375", "https://www.jacuzzi.com/en-us/j-375/J-375-MY26.html"),
    ("J-365", "https://www.jacuzzi.com/en-us/j-365/J-365-MY26.html"),
    ("J-355", "https://www.jacuzzi.com/en-us/j-355/J-355-MY26.html"),
    ("J-345", "https://www.jacuzzi.com/en-us/j-345/J-345-MY26.html"),
    ("J-335", "https://www.jacuzzi.com/en-us/j-335/J-335-MY26.html"),
    ("J-325", "https://www.jacuzzi.com/en-us/j-325/J-325-MY26.html"),
    ("J-315", "https://www.jacuzzi.com/en-us/j-315/J-315-MY26.html"),
    # J-200
    ("J-285", "https://www.jacuzzi.com/en-us/j-285/J-285-MY26.html"),
    ("J-275", "https://www.jacuzzi.com/en-us/j-275/J-275-MY26.html"),
    ("J-245", "https://www.jacuzzi.com/en-us/j-245/J-245-MY26.html"),
    ("J-235", "https://www.jacuzzi.com/en-us/j-235/J-235-MY26.html"),
    ("J-225", "https://www.jacuzzi.com/en-us/j-225/J-225-MY26.html"),
    ("J-215", "https://www.jacuzzi.com/en-us/j-215/J-215-MY26.html"),
    ("J-210", "https://www.jacuzzi.com/en-us/j-210/J-210-MY26.html"),
    # J-LX
    ("J-LX", "https://www.jacuzzi.com/en-us/j-lx/J-LX.html"),
    ("J-LXL", "https://www.jacuzzi.com/en-us/j-lxl/J-LXL.html"),
]

def harvest_model_images():
    print(f"=== HARVESTING IMAGES FOR {len(TARGET_MODELS)} JACUZZI MODELS ===")
    session = requests.Session()
    session.headers.update(HEADERS)

    for m_name, url in TARGET_MODELS:
        m_norm = m_name.lower().replace("-", "")
        dest_dir = IMAGES_DIR / m_norm
        dest_dir.mkdir(parents=True, exist_ok=True)

        top_dest = dest_dir / "top_view.png"
        side_dest = dest_dir / "side_view.jpg"

        if top_dest.exists() and side_dest.exists():
            print(f"[SKIP] {m_name}: images already exist")
            continue

        print(f"[FETCHING] {m_name} from {url}...")
        try:
            r = session.get(url, timeout=10)
            if r.status_code != 200:
                print(f"  [WARN] Status {r.status_code} for {url}")
                continue

            soup = BeautifulSoup(r.text, "html.parser")
            images = [img.get("src") or img.get("data-src") or "" for img in soup.find_all("img")]

            top_url = None
            side_url = None

            for img_url in images:
                if not img_url:
                    continue
                # Overhead (Top view)
                if ("_oh" in img_url.lower() or "overhead" in img_url.lower()) and "1000" in img_url:
                    top_url = img_url
                elif ("_oh" in img_url.lower() or "overhead" in img_url.lower()) and not top_url:
                    top_url = img_url

                # Lifestyle / Side view
                if "lifestyle" in img_url.lower() and "1000" in img_url:
                    side_url = img_url
                elif "lifestyle" in img_url.lower() and not side_url:
                    side_url = img_url

            if top_url:
                if "w=170" in top_url:
                    top_url = top_url.replace("w=170&h=170", "w=1000&h=1000")
                print(f"  -> Downloading top_view from {top_url[:80]}...")
                tr = session.get(top_url, timeout=15)
                if tr.status_code == 200:
                    with open(top_dest, "wb") as f:
                        f.write(tr.content)
                    print(f"  [OK] Saved {top_dest.name} ({len(tr.content)} bytes)")

            if side_url:
                if "w=170" in side_url:
                    side_url = side_url.replace("w=170&h=170", "w=1000&h=1000")
                print(f"  -> Downloading side_view from {side_url[:80]}...")
                sr = session.get(side_url, timeout=15)
                if sr.status_code == 200:
                    with open(side_dest, "wb") as f:
                        f.write(sr.content)
                    print(f"  [OK] Saved {side_dest.name} ({len(sr.content)} bytes)")

            time.sleep(0.5)

        except Exception as e:
            print(f"  [ERROR] {m_name}: {e}")

if __name__ == "__main__":
    harvest_model_images()
