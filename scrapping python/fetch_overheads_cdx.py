import urllib.request
import json

cdx_url = "http://web.archive.org/cdx/search/cdx?url=hotspring.com/sites/default/files/images/spas/overhead/*&output=json&fl=original,timestamp&collapse=urlkey&limit=500"

req = urllib.request.Request(cdx_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=12) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    print(f"Overhead results ({len(data)-1}):")
    for row in data[1:]:
        print(" ", row[0])
    with open("D:/SPAFIT/Cover Sizer/scrapping python/wayback_overheads.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
except Exception as e:
    print(f"Error: {e}")
