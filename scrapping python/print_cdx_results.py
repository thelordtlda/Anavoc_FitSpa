import requests

cdx_url = "http://web.archive.org/cdx/search/cdx?url=hotspring.com/sites/default/files/images/spas/*&output=json&fl=original,timestamp,mimetype&filter=mimetype:image/.*&collapse=urlkey&limit=500"
r = requests.get(cdx_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
data = r.json()
print(f"Total results: {len(data)-1}")
for row in data[1:]:
    orig = row[0]
    print(orig)
