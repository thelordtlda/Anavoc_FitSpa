import csv
import io
import os
import requests
import time
from PIL import Image
from pathlib import Path
from collections import defaultdict

ROOT_DIR = Path(".").resolve()
CSV_PATH = ROOT_DIR / "data/spas_master_database.csv"

# Load catalog
with open(CSV_PATH, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

from wayback_generational_harvester import (
    compute_dhash, hamming_distance, compute_chromatic_variance,
    get_existing_dhash_index, BRAND_DOMAINS
)

existing_dhashes = get_existing_dhash_index(rows)
print(f"Indexed {len(existing_dhashes)} existing catalog dHashes.")

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

def verify_candidate(content, brand, model, gen, prod, l_in, w_in):
    try:
        img = Image.open(io.BytesIO(content))
    except Exception as e:
        return False, f"Image open failed: {e}", None, None

    w, h = img.size
    if w < 180 or h < 180:
        return False, f"Resolution too low ({w}x{h})", None, None

    # Proportional aspect error against spa dimensions
    if l_in and w_in and l_in != "N/A" and w_in != "N/A":
        try:
            l_f = float(l_in)
            w_f = float(w_in)
            spa_ratio = max(l_f, w_f) / min(l_f, w_f)
            img_ratio = max(w, h) / min(w, h)
            err = abs(img_ratio - spa_ratio) / spa_ratio
            if err > 0.22:
                return False, f"Aspect error {err*100:.1f}% exceeds 22% (img={img_ratio:.2f}, spa={spa_ratio:.2f})", None, None
        except ValueError:
            pass

    # Chromatic variance
    var = compute_chromatic_variance(img)
    colors = len(img.convert('RGB').getcolors(maxcolors=20000) or [])
    if var < 3.0 and colors < 150:
        return False, f"Low chromatic variance/colors ({var:.1f}, {colors} colors)", None, None

    # dHash
    dh = compute_dhash(img)
    min_dist = 64
    closest = None
    for ex_dh, ex_info in existing_dhashes.items():
        dist = hamming_distance(dh, ex_dh)
        if dist < min_dist:
            min_dist = dist
            closest = ex_info

    if min_dist < 9:
        return False, f"dHash collision ({min_dist} bits < 9 bits) with {closest[1]} {closest[2]}", None, None

    return True, f"PASSED (min_dist={min_dist} bits, aspect_err={err*100:.1f}%)", dh, img

# Candidate targets to test
test_targets = [
    # Arctic Spas
    ("Arctic Spas", "Cub", "Gen 1", "2005-2026", "86.0", "86.0", "https://web.archive.org/web/20200123160704im_/https://www.arcticspas.com/wp-content/uploads/01-custom-cub-topimage-300x188.jpg"),
    ("Arctic Spas", "Yukon", "Gen 1", "2005-2026", "86.0", "86.0", "https://web.archive.org/web/20200122195814im_/https://www.arcticspas.com/wp-content/uploads/01-custom-yukon-topimage-300x188.jpg"),
    ("Arctic Spas", "Grizzly", "Gen 1", "2010-2026", "90.0", "90.0", "https://web.archive.org/web/20200514153428im_/https://www.arcticspas.com/wp-content/uploads/03-core-grizzly-topimage-400x284.jpg"),
    ("Arctic Spas", "Orca", "Gen 1", "2010-2026", "90.0", "90.0", "https://web.archive.org/web/20220623090102im_/https://www.arcticspas.com/wp-content/uploads/03-core-orca-topimage-400x284.jpg"),
    ("Arctic Spas", "Summit", "Gen 1", "2005-2015", "93.0", "93.0", "https://web.archive.org/web/20200123160508im_/https://www.arcticspas.com/wp-content/uploads/01-custom-summit-topimage-300x188.jpg"),
    ("Arctic Spas", "Kodiak", "Gen 1", "2005-2015", "90.0", "90.0", "https://web.archive.org/web/20221214005741im_/https://www.arcticspas.com/wp-content/uploads/01-custom-kodiak-topimage-400x284.jpg"),
    ("Arctic Spas", "Mustang", "Gen 1", "2005-2026", "90.0", "90.0", "https://web.archive.org/web/20221214005748im_/https://www.arcticspas.com/wp-content/uploads/02-classic-mustang-topimage-400x284.jpg"),
    ("Arctic Spas", "Eagle", "Gen 1", "2005-2026", "90.0", "90.0", "https://web.archive.org/web/20221214005731im_/https://www.arcticspas.com/wp-content/uploads/02-classic-eagle-topimage-400x284.jpg"),
    # Cal Spas
    ("Cal Spas", "Belair", "Gen 1", "2010-2026", "84.0", "84.0", "https://web.archive.org/web/20260130054559im_/http://www.calspas.com/images/belair.webp"),
    # Caldera Spas
    ("Caldera Spas", "Kauai", "Gen 1", "2005-2015", "84.0", "65.0", "https://web.archive.org/web/20140705000020im_/http://www.calderaspas.com/sites/default/files/Paradise_Kauai.jpg"),
    ("Caldera Spas", "Makena", "Gen 1", "2011-2015", "89.0", "89.0", "https://web.archive.org/web/20140704220257im_/http://www.calderaspas.com/sites/default/files/Paradise_Makena_v1.jpg"),
    ("Caldera Spas", "Salina", "Gen 1", "2011-2015", "89.0", "89.0", "https://web.archive.org/web/20140705004718im_/http://www.calderaspas.com/sites/default/files/Paradise_Salina.jpg"),
]

print("\n=== TESTING DOWNLOAD & VERIFICATION FOR CANDIDATES ===")
for brand, model, gen, prod, l_in, w_in, url in test_targets:
    try:
        r = session.get(url, timeout=15)
        if r.status_code == 200 and len(r.content) > 1000:
            ok, msg, dh, img = verify_candidate(r.content, brand, model, gen, prod, l_in, w_in)
            status_str = "[OK]  " if ok else "[FAIL]"
            print(f"{status_str} {brand} {model} ({l_in}x{w_in}): {msg}")
        else:
            print(f"[FAIL] {brand} {model}: HTTP {r.status_code}")
    except Exception as e:
        print(f"[FAIL] {brand} {model}: Error {e}")
