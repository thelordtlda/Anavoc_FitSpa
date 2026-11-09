import fitz

doc = fitz.open("D:/SPAFIT/Cover Sizer/scrapping python/spa_manuals/american_whirlpool/AW-2018-Owner-Manual-2.pdf")
for pnum in range(50, 60):
    page = doc[pnum - 1]
    print(f"\n================ Page {pnum} ================")
    print(page.get_text()[:600])
