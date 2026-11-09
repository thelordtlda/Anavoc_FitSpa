import requests

url = "http://web.archive.org/cdx/search/cdx"
# Query specifically with higher limit or deeper path
patterns = [
    'calderaspas.com/sites/default/files/images/spas/*',
    'calderaspas.com/sites/default/files/images/hot-tubs/*',
    'calderaspas.com/sites/default/files/images/*',
    'calderaspas.com/sites/default/files/*',
    'coastspas.com/images/*',
    'marquisspas.com/assets/*',
    'arcticspas.com/wp-content/uploads/*',
    'calspas.com/images/*',
]

for pat in patterns:
    params = {
        'url': pat,
        'output': 'json',
        'fl': 'original,timestamp',
        'filter': 'mimetype:image/.*',
        'limit': 500
    }
    r = requests.get(url, params=params, timeout=20)
    if r.status_code == 200:
        data = r.json()
        count = len(data) - 1 if len(data) > 0 else 0
        print(f"{pat}: {count} files")
        # Check if any model names appear
        for row in data[1:10]:
            print(f"  {row[0]}")
