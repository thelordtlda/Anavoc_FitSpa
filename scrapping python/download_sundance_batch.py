import os
import re
import json
import time
import requests
from pathlib import Path

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")
OUT_DIR = BASE_DIR / "spa_manuals" / "sundance_spas"
OUT_DIR.mkdir(parents=True, exist_ok=True)

with open(BASE_DIR / "sundance_manual_links_extracted.json", "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Total links to process: {len(items)}")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}

# We want key manuals across all series:
# - Pre-Delivery Guide (2026)
# - Swim Spas (2026 & 2025)
# - 980 Series (2025, 2020, 2017)
# - 880 Series (2026, 2020, 2016)
# - 780 Series (2026, 2020, 2016)
# - 680 Series (2026, 2020, 2016)
# - Select Series (2018)
# - Splash Series (2023)

selected = []
# Pre-delivery guide is highest priority
for item in items:
    url = item["href"]
    fname = url.split("/")[-1].split("?")[0]
    yr = item["text"]
    
    # Classify series
    series = "Misc"
    if "pre-delivery" in fname.lower() or "pre-delivery" in yr.lower():
        series = "Pre-Delivery"
        clean_name = f"2026_Sundance_Pre-Delivery-Guide.pdf"
    elif "swim" in fname.lower():
        series = "Swim-Spas"
        clean_name = f"{yr}_Sundance_Swim-Spas.pdf"
    elif "980" in fname or "397" in fname:
        series = "980-Series"
        clean_name = f"{yr}_Sundance_980-Series.pdf"
    elif "880" in fname or "608" in fname:
        series = "880-Series"
        clean_name = f"{yr}_Sundance_880-Series.pdf"
    elif "780" in fname or "607" in fname:
        series = "780-Series"
        clean_name = f"{yr}_Sundance_780-Series.pdf"
    elif "680" in fname or "681" in fname or "dom-l" in fname.lower():
        series = "680-Series"
        clean_name = f"{yr}_Sundance_680-Series.pdf"
    elif "select" in fname.lower():
        series = "Select-Series"
        clean_name = f"{yr}_Sundance_Select-Series.pdf"
    elif "splash" in fname.lower():
        series = "Splash-Series"
        clean_name = f"{yr}_Sundance_Splash-Series.pdf"
    else:
        clean_name = f"{yr}_{fname}"
        
    selected.append({"url": url, "filename": clean_name, "series": series, "year": yr})

# Download priority items
print(f"Selected {len(selected)} manuals for download:")
for s in selected:
    target = OUT_DIR / s["filename"]
    if target.exists() and target.stat().st_size > 10000:
        print(f"[SKIP] {s['filename']} already exists ({target.stat().st_size//1024} KB)")
        continue
    print(f"[DOWNLOADING] {s['filename']} from {s['url']}...")
    try:
        r = requests.get(s["url"], headers=headers, timeout=60, stream=True)
        if r.status_code == 200:
            with open(target, "wb") as f_out:
                for chunk in r.iter_content(chunk_size=32768):
                    f_out.write(chunk)
            print(f"[SAVED] {s['filename']} ({target.stat().st_size//1024} KB)")
        else:
            print(f"[ERROR {r.status_code}] on {s['url']}")
    except Exception as e:
        print(f"[FAILED] {s['filename']}: {e}")
    time.sleep(1)

print("Download batch completed!")
