import urllib.request
import json
import re

queries = [
    "hotspring.com/sites/default/files/images/spas/overhead/*",
    "hotspring.com/sites/default/files/images/spas/overhead-jets/*",
    "hotspring.com/sites/default/files/images/spas/hero/*",
    "hotspring.com/sites/default/files/images/spas/profile/*",
    "hotspring.com/sites/default/files/images/spas/exterior/*",
    "hotspring.com/sites/default/files/images/spas/*"
]

all_images = {}

for q in queries:
    cdx_url = f"http://web.archive.org/cdx/search/cdx?url={q}&output=json&fl=original,timestamp,mimetype&filter=mimetype:image/.*&collapse=urlkey&limit=1000"
    print(f"Querying {q}...")
    try:
        req = urllib.request.Request(cdx_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        print(f"  Got {len(data)-1} results")
        for row in data[1:]:
            orig, ts, mime = row[0], row[1], row[2]
            all_images[orig] = ts
    except Exception as e:
        print(f"  Error: {e}")

print(f"\nTotal unique spa images discovered: {len(all_images)}")

# Save to json file
with open("D:/SPAFIT/Cover Sizer/scrapping python/wayback_hotspring_images.json", "w", encoding="utf-8") as f:
    json.dump(all_images, f, indent=2)

# Print overheads
print("\n--- Overheads found ---")
for url in sorted(all_images.keys()):
    if 'overhead' in url.lower():
        print(" ", url.split('/')[-1])

print("\n--- Heroes found ---")
for url in sorted(all_images.keys()):
    if 'hero' in url.lower():
        print(" ", url.split('/')[-1])
