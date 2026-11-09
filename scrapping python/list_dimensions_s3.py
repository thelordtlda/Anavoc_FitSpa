import urllib.request
import re

url = "https://s3.amazonaws.com/prod-hotspring/?prefix=dimensions"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = resp.read().decode('utf-8', errors='ignore')
    keys = re.findall(r'<Key>(.*?)</Key>', data)
    print(f"Total keys in prod-hotspring/dimensions: {len(keys)}")
    for k in keys[:30]:
        print(" ", k)
except Exception as e:
    print(e)
