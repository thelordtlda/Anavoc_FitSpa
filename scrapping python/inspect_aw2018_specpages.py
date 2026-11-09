import fitz

doc = fitz.open("D:/SPAFIT/Cover Sizer/scrapping python/spa_manuals/american_whirlpool/AW-2018-Owner-Manual-2.pdf")
for pnum in range(14, 25):
    page = doc[pnum - 1]
    print(f"\n================ Page {pnum} ================")
    text = page.get_text()
    for line in text.split("\n"):
        if any(c in line for c in ["x", "X", "\"", "cm", "in", "Model", "481", "471", "881", "280", "151", "101", "Dimension", "dimension"]):
            print("  ", line.strip())
