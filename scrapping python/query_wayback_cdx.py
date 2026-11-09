import urllib.request
import json
import urllib.parse

# Query CDX for hotspring.com spa images
cdx_url = "http://web.archive.org/cdx/search/cdx?url=hotspring.com/sites/default/files/images/spas/*&output=json&fl=original,timestamp,mimetype&filter=mimetype:image/.*&collapse=urlkey&limit=500"

print("Querying Wayback CDX API for hotspring.com spa images...")
req = urllib.request.Request(cdx_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    print(f"CDX returned {len(data)-1} image URLs!")
    # Show first 25
    for row in data[1:30]:
        print("  ", row[0])
except Exception as e:
    print(f"CDX error: {e}")
