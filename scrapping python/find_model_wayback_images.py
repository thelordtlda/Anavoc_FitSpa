import requests
import json

base_cdx = "http://web.archive.org/cdx/search/cdx"

models = [
    "grandee", "envoy", "aria", "vanguard", "sovereign", "prodigy", "jetsetter",
    "gleam", "pulse", "flair", "flash", "beam", "bolt", "glow",
    "tempo", "rhythm", "relay", "pace", "stride", "sx", "tx", "vista", "landmark"
]

results = {}

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

for m in models:
    q = f"hotspring.com/*{m}*.png"
    params = {
        'url': f'hotspring.com/sites/default/files/images/spas/*{m}*',
        'output': 'json',
        'fl': 'original,timestamp,mimetype',
        'filter': 'mimetype:image/.*',
        'collapse': 'urlkey',
        'limit': 50
    }
    try:
        r = session.get(base_cdx, params=params, timeout=10)
        if r.status_code == 200:
            data = r.json()
            if len(data) > 1:
                urls = [row[0] for row in data[1:]]
                results[m] = urls
                print(f"[{m.upper()}] found {len(urls)} images on Wayback!")
                for u in urls[:3]:
                    print("  ", u.split('/')[-1])
            else:
                print(f"[{m.upper()}] 0 images")
        else:
            print(f"[{m.upper()}] status {r.status_code}")
    except Exception as e:
        print(f"[{m.upper()}] error: {e}")

with open("D:/SPAFIT/Cover Sizer/scrapping python/discovered_wayback_spas.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print("Finished querying model images!")
