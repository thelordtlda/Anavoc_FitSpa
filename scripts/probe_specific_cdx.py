import requests
import json

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
})

test_queries = [
    ("Caldera", "calderaspas.com/*makena*"),
    ("Caldera", "calderaspas.com/*overhead*"),
    ("Caldera", "calderaspas.com/*cantabria*"),
    ("Marquis", "marquisspas.com/*overhead*"),
    ("Marquis", "marquisspas.com/*euphoria*"),
    ("Marquis", "marquisspas.com/*resort*"),
    ("Coast", "coastspas.com/*apex*"),
    ("Coast", "coastspas.com/*cascade*"),
    ("Arctic", "arcticspas.com/*fox*"),
    ("Arctic", "arcticspas.com/*arctic_fox*"),
    ("Arctic", "arcticspas.com/*yukon*"),
    ("Cal Spas", "calspas.com/*escape*"),
    ("Cal Spas", "calspas.com/*platinum*"),
]

for brand, pattern in test_queries:
    url = "http://web.archive.org/cdx/search/cdx"
    params = {
        'url': pattern,
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
            print(f"[{brand}] {pattern} -> {count} results")
            if count > 0:
                for row in data[1:3]:
                    print(f"    {row[1]}: {row[0]}")
        else:
            print(f"[{brand}] {pattern} -> Status {r.status_code}")
    except Exception as e:
        print(f"[{brand}] {pattern} -> Error {e}")
