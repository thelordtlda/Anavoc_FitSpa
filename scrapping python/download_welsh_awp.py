import requests
from pathlib import Path

OUT_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python/spa_manuals/american_whirlpool")
OUT_DIR.mkdir(parents=True, exist_ok=True)

urls = [
    "https://welshhottubs.co.uk/wp-content/uploads/2024/09/2022-American-Whirlpool-Swim-Spa-Series-Owners-Manual.pdf",
    "https://welshhottubs.co.uk/wp-content/uploads/2024/04/AW-2018-Owner-Manual-2.pdf"
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}

for u in urls:
    fname = u.split("/")[-1]
    target = OUT_DIR / fname
    print(f"Downloading {fname}...")
    try:
        r = requests.get(u, headers=headers, timeout=30)
        if r.status_code == 200:
            with open(target, "wb") as f:
                f.write(r.content)
            print(f"Saved {fname} ({len(r.content)//1024} KB)")
        else:
            print("Failed:", r.status_code)
    except Exception as e:
        print("Error:", e)
