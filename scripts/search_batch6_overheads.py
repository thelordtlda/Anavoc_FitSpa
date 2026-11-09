import requests
import json
import re

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
})

brands = {
    "Cal Spas": [
        "calspas.com/images/*",
        "calspas.com/wp-content/uploads/*",
    ],
    "Coast Spas": [
        "coastspas.com/images/*",
        "coastspas.com/wp-content/uploads/*",
    ],
    "Marquis Spas": [
        "marquisspas.com/images/*",
        "marquisspas.com/assets/*",
        "marquisspas.com/wp-content/uploads/*",
    ],
    "Arctic Spas": [
        "arcticspas.com/wp-content/uploads/*",
        "arcticspas.com/images/*",
    ],
    "Beachcomber": [
        "beachcomberhottubs.com/hot-tubs/*",
        "beachcomberhottubs.com/images/*",
        "beachcomberhottubs.com/sites/default/files/*",
    ],
    "Hydropool": [
        "hydropoolhottubs.com/images/*",
        "hydropoolhottubs.com/wp-content/uploads/*",
    ],
    "Caldera Spas": [
        "calderaspas.com/sites/default/files/*",
        "calderaspas.com/images/*",
    ]
}

print("=== SEARCHING FOR OVERHEAD / TOP-VIEW PATTERNS ===")
keywords = ["overhead", "top-view", "top_view", "topview", "topimage", "shell", "render", "birds-eye", "overhead-jets", "aerial"]

for brand, patterns in brands.items():
    print(f"\nChecking Brand: {brand}")
    matched_urls = []
    for pat in patterns:
        url = "http://web.archive.org/cdx/search/cdx"
        params = {
            'url': pat,
            'output': 'json',
            'fl': 'original,timestamp',
            'filter': 'mimetype:image/.*',
            'limit': 2000
        }
        try:
            r = session.get(url, params=params, timeout=25)
            if r.status_code == 200:
                data = r.json()
                if len(data) > 1:
                    for row in data[1:]:
                        orig = row[0]
                        orig_l = orig.lower()
                        if any(k in orig_l for k in keywords):
                            if not any(ex in orig_l for ex in ['icon', 'logo', 'button', 'banner']):
                                matched_urls.append((orig, row[1]))
        except Exception as e:
            print(f"  Error on {pat}: {e}")
    print(f"  Found {len(matched_urls)} overhead-keyword images for {brand}")
    for u, ts in matched_urls[:8]:
        print(f"    {ts}: {u}")
