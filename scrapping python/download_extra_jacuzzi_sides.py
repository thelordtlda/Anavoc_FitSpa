import requests
from pathlib import Path

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")
IMG_DIR = BASE_DIR / "images" / "jacuzzi"

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

EXTRA_SIDES = [
    ("j285", "https://www.jacuzzi.com/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dw9eb69742/images/JHT_J-285_Canyon_HorizonGray_Iso.png"),
    ("j245", "https://www.jacuzzi.com/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dwf20b7c60/images/hi-res/JHT_J-245_Canyon_Pecan_Iso.png"),
    ("j235", "https://www.jacuzzi.com/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dwb8cfec81/images/hi-res/JHT_J-235_Platinum_HorizonGray_Iso.png"),
    ("j225", "https://www.jacuzzi.com/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dw5f48a28e/images/hi-res/JHT_J-225_Platinum_Pecan_Iso.png"),
    ("j215", "https://www.jacuzzi.com/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dw135f1d16/images/hi-res/JHT_J-215_Canyon_HorizonGray_Iso.png"),
    ("j408", "https://www.jacuzzi.com/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dw966812f5/images/hi-res/JHT_J408_Platinum_SmokedEbony_Iso.png"),
    ("j408l", "https://www.jacuzzi.com/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dw12a560ea/images/hi-res/JHT_J408L_Porcelain_ModernHardwood_Iso.png"),
    ("j404l", "https://www.jacuzzi.com/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dw9d4a2448/images/hi-res/JHT_J404L_Porcelain_BrushedGray_Iso.png"),
    ("j508", "https://www.jacuzzi.com/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dw78f2d5ce/images/hi-res/JHT_J5_J508_Platinum_Flax_Front.png"),
    ("j508l", "https://www.jacuzzi.com/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dw19882d9c/images/hi-res/JHT_J5_J508L_Platinum_Noir_Front.png"),
    ("j509", "https://www.jacuzzi.com/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dw0d3cc470/images/hi-res/JHT_J5_J509_Platinum_Noir_Front.png"),
    ("j585", "https://www.jacuzzi.com/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dw78f2d5ce/images/hi-res/JHT_J5_J508_Platinum_Flax_Front.png"),
    ("j575", "https://www.jacuzzi.com/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dw19882d9c/images/hi-res/JHT_J5_J508L_Platinum_Noir_Front.png")
]

for m, url in EXTRA_SIDES:
    dest = IMG_DIR / m / "side_view.jpg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 10000:
        continue
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code == 200:
            with open(dest, "wb") as f:
                f.write(r.content)
            print(f"[OK] Downloaded side_view for {m} ({len(r.content)} bytes)")
    except Exception as e:
        print(f"[ERROR] {m}: {e}")
