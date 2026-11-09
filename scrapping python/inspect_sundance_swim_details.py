import fitz
import re

doc = fitz.open("D:/SPAFIT/Cover Sizer/scrapping python/spa_manuals/sundance_spas/2026_Sundance_Swim-Spas.pdf")
print("Total pages in Swim Spas manual:", len(doc))

for i, page in enumerate(doc):
    text = page.get_text()
    # Search for model names, specifications table
    if any(k in text.lower() for k in ["specifications", "stream", "surf", "dimensions", "volume", "length"]):
        for line in text.split("\n"):
            line_str = line.strip()
            if any(term in line_str.lower() for term in ["stream", "surf", "dimension", "length", "width", "height", "14", "16", "17", "19", "x", "cm", "in"]):
                if len(line_str) < 120 and len(line_str) > 3:
                    print(f"p.{i+1}: {line_str}")
