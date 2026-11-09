import requests
import json
from pathlib import Path

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")

domains = ["americanwhirlpool.com", "maaxspas.com"]
results = {}

for domain in domains:
    print(f"Querying Wayback CDX for {domain}...")
    url = f"http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&fl=original,timestamp,mimetype&filter=mimetype:application/pdf&collapse=urlkey&limit=100"
    try:
        r = requests.get(url, timeout=20)
        if r.status_code == 200:
            data = r.json()
            if len(data) > 1:
                header = data[0]
                rows = [dict(zip(header, row)) for row in data[1:]]
                results[domain] = rows
                print(f"  Found {len(rows)} PDF archives for {domain}!")
            else:
                print(f"  0 PDF found for {domain}")
        else:
            print(f"  Status {r.status_code}")
    except Exception as e:
        print(f"  Error on {domain}: {e}")

with open(BASE_DIR / "cdx_pdf_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\nCDX search completed!")
