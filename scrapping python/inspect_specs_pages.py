import fitz

doc = fitz.open("D:/SPAFIT/Cover Sizer/scrapping python/spa_manuals/sundance_spas/2026_Sundance_Pre-Delivery-Guide.pdf")
for page_num in range(50, len(doc) + 1):
    page = doc[page_num - 1]
    print(f"\n==================== Page {page_num} ====================")
    text = page.get_text()
    for line in text.split("\n"):
        if any(c in line for c in ["x", "X", "\"", "cm", "in", "Radius", "radius", "Kingston", "Claremont", "Aspen", "Cameo", "Optima", "Chelsee", "Bristol", "Hamilton", "Dover", "Prado", "Peyton", "Edison"]):
            print("  ", line.strip())
