import csv
import requests
from pathlib import Path
from collections import defaultdict

csv_path = Path("data/spas_master_database.csv")
with open(csv_path, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f, delimiter=";"))

# Missing models by brand
target_brands = ["Coast Spas", "Marquis Spas", "Hydropool", "Arctic Spas", "Cal Spas", "Caldera Spas", "Beachcomber"]
candidates_by_brand = defaultdict(list)
for idx, r in enumerate(rows):
    b = r["Marque"]
    if b in target_brands and (not r.get("image_top_file") or r["image_top_file"] == "N/A"):
        m = r["Modele"]
        gen = r["Generation"]
        prod = r["Annees_Production"]
        candidates_by_brand[b].append((idx, m, gen, prod, r.get("length_in"), r.get("width_in")))

brand_cdx_patterns = {
    "Coast Spas": ["coastspas.com/images/*", "coastspas.com/wp-content/uploads/*"],
    "Marquis Spas": ["marquisspas.com/assets/*", "marquisspas.com/images/*"],
    "Hydropool": ["hydropoolhottubs.com/images/*", "hydropoolhottubs.com/wp-content/uploads/*"],
    "Arctic Spas": ["arcticspas.com/wp-content/uploads/*", "arcticspas.com/images/*"],
    "Cal Spas": ["calspas.com/images/*", "calspas.com/wp-content/uploads/*"],
    "Caldera Spas": ["calderaspas.com/sites/default/files/*", "calderaspas.com/images/*"],
    "Beachcomber": ["beachcomberhottubs.com/*"]
}

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

print("=== CDX MATCH SCAN ACROSS BATCH #6 CANDIDATES ===")
for b in target_brands:
    cands = candidates_by_brand[b]
    patterns = brand_cdx_patterns.get(b, [])
    print(f"\n--- {b} ({len(cands)} candidates) ---")
    all_urls = []
    for pat in patterns:
        url = "http://web.archive.org/cdx/search/cdx"
        params = {
            'url': pat,
            'output': 'json',
            'fl': 'original,timestamp',
            'filter': 'mimetype:image/.*',
            'limit': 1000
        }
        try:
            r = session.get(url, params=params, timeout=25)
            if r.status_code == 200:
                data = r.json()
                if len(data) > 1:
                    all_urls.extend(data[1:])
        except Exception as e:
            print(f"  Error on {pat}: {e}")
    
    print(f"  Total CDX images fetched: {len(all_urls)}")
    # Try matching candidates
    matches_found = 0
    for idx, m, gen, prod, l_in, w_in in cands:
        tok = m.lower().replace(" classic", "").replace(" curve", "").replace(" elite", "").strip()
        subtoks = [t for t in tok.split() if len(t) >= 3]
        if not subtoks:
            subtoks = [tok]
        
        found_sample = []
        for orig, ts in all_urls:
            orig_lower = orig.lower()
            if any(st in orig_lower for st in subtoks):
                # check exclusions
                if not any(ex in orig_lower for ex in ['logo', 'icon', 'button', 'banner', 'dealer', 'warranty']):
                    found_sample.append((orig, ts))
        if found_sample:
            matches_found += 1
            print(f"  MATCH: {m} ({prod}) -> {len(found_sample)} candidate URLs (e.g. {found_sample[0][0]} [{found_sample[0][1]}])")
    print(f"  Total models with candidate matches in CDX: {matches_found} / {len(cands)}")
