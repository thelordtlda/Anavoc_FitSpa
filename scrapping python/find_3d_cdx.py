import requests

# Query Wayback CDX for 3D model files from bullfrogspas.com, jacuzzi.com, sundancespas.com
for domain in ['bullfrogspas.com', 'jacuzzi.com', 'sundancespas.com']:
    for ext in ['glb', 'gltf', 'obj', 'usdz', 'dwg', 'dxf', 'skp']:
        url = f"http://web.archive.org/cdx/search/cdx?url={domain}/*&output=json&filter=original:.*\\.{ext}$"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                if len(data) > 1:
                    print(f"[{domain}] Found {len(data)-1} files of type .{ext}:")
                    for row in data[1:6]:
                        print(" ", row[2])
        except Exception as e:
            print(f"Error {domain} {ext}: {e}")
