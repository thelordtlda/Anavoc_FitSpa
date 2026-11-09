import fitz

doc = fitz.open("D:/SPAFIT/Cover Sizer/scrapping python/spa_manuals/sundance_spas/2026_Sundance_Pre-Delivery-Guide.pdf")
for page_num in [15, 16, 20, 21, 22, 27, 32, 40]:
    page = doc[page_num - 1]
    print(f"\n--- Page {page_num} ---")
    print(page.get_text()[:400])
