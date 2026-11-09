import json

with open("D:/SPAFIT/Cover Sizer/scrapping python/awp_scraped_specs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for item in data[:15]:
    print(f"Model: {item['slug']} -> 3D: {item['dim_3d']} | 2D: {item['dim_2d']} | Imgs: {len(item['images'])}")
    if item['images']:
        print("  Img:", item['images'][0])
