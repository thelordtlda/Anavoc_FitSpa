import requests
import json

domains = {
    "Coast Spas": ["coastspas.com/wp-content/uploads/*", "coastspas.com/images/*"],
    "Marquis Spas": ["marquisspas.com/wp-content/uploads/*", "marquisspas.com/assets/*", "marquisspas.com/images/*"],
    "Hydropool": ["hydropoolhottubs.com/wp-content/uploads/*", "hydropoolhottubs.com/images/*"],
    "Beachcomber": ["beachcomberhottubs.com/wp-content/uploads/*", "beachcomberhottubs.com/sites/default/files/*"],
    "Arctic Spas": ["arcticspas.com/wp-content/uploads/*", "arcticspas.com/images/*"],
    "Cal Spas": ["calspas.com/wp-content/uploads/*", "calspas.com/images/*"],
    "Caldera Spas": ["calderaspas.com/sites/default/files/images/*", "calderaspas.com/sites/default/files/*"]
}

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
})

print("=== TESTING CDX FOR BATCH #6 BRANDS ===")
for brand, patterns in domains.items():
    print(f"\nBrand: {brand}")
    for pat in patterns:
        url = "http://web.archive.org/cdx/search/cdx"
        params = {
            'url': pat,
            'output': 'json',
            'fl': 'original,timestamp,mimetype',
            'filter': 'mimetype:image/.*',
            'limit': 5
        }
        try:
            r = session.get(url, params=params, timeout=15)
            if r.status_code == 200:
                data = r.json()
                count = len(data) - 1 if len(data) > 0 else 0
                print(f"  {pat}: {count} samples found (Status 200)")
                if count > 0:
                    for row in data[1:3]:
                        print(f"    Sample: {row[0]}")
            else:
                print(f"  {pat}: Status {r.status_code}")
        except Exception as e:
            print(f"  {pat}: Error {e}")
