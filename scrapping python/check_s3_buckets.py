import urllib.request
import re

urls = [
    "https://s3.amazonaws.com/prod-hotspring/?prefix=images",
    "https://s3.amazonaws.com/prod-hotspring/?prefix=spas",
    "https://prod-hotspring.s3.amazonaws.com/?prefix=spas",
    "https://hotspring-wordpress.s3.amazonaws.com/?prefix=dimensions",
    "https://hotspring-wordpress.s3.amazonaws.com/?prefix=uploads"
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read().decode('utf-8', errors='ignore')
        print(f"URL {u}: success! Length: {len(data)}")
        # find keys
        keys = re.findall(r'<Key>(.*?)</Key>', data)
        print(f"  Found {len(keys)} keys: {keys[:5]}")
    except Exception as e:
        print(f"URL {u}: {e}")
