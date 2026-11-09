import urllib.request
import re

url = "https://s3.amazonaws.com/prod-hotspring/?prefix=dimensions"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = resp.read().decode('utf-8', errors='ignore')

keys = re.findall(r'<Key>(.*?)</Key>', data)
by_ext = {}
for k in keys:
    ext = k.split('.')[-1].lower() if '.' in k else 'folder'
    by_ext[ext] = by_ext.get(ext, 0) + 1

print(f"Total keys: {len(keys)}")
print(f"By extension: {by_ext}")
