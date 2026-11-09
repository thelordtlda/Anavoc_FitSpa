import fitz

doc = fitz.open("D:/SPAFIT/Cover Sizer/scrapping python/spa_manuals/american_whirlpool/AW-2018-Owner-Manual-2.pdf")
print("Total pages in AW 2018:", len(doc))
for i in range(len(doc)):
    page = doc[i]
    text = page.get_text()
    if any(k in text.lower() for k in ["specifications", "dimensions", "features", "overview", "layout", "footprint"]):
        print(f"Page {i+1}: {text.splitlines()[:3]}")
