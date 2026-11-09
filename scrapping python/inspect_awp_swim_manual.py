import fitz

doc = fitz.open("D:/SPAFIT/Cover Sizer/scrapping python/spa_manuals/american_whirlpool/2022-American-Whirlpool-Swim-Spa-Series-Owners-Manual.pdf")
print("Total pages in AWP Swim Spa manual:", len(doc))
for i, page in enumerate(doc):
    text = page.get_text()
    if any(k in text.lower() for k in ["specifications", "dimensions", "length", "width", "height", "dm8", "ml4", "mb4", "mx6", "rf2", "rl4", "rl5"]):
        print(f"\n--- Page {i+1} ---")
        for line in text.split("\n"):
            if any(term in line.lower() for term in ["dm8", "ml4", "mb4", "mx6", "rf2", "rl4", "rl5", "mx5", "dimension", "in.", "cm", "x", "height", "width", "length"]):
                print(" ", line.strip())
