import fitz

doc = fitz.open('D:/SPAFIT/Cover Sizer/scrapping python/spa_manuals/bullfrog_spas/2024_Pre-Delivery-Guide_8_5x11_v1.pdf')
for p in [3, 4, 7, 8, 9]:
    if p < len(doc):
        print(f'=== Page {p+1} ===')
        print(doc[p].get_text())

doc_layouts = fitz.open('D:/SPAFIT/Cover Sizer/scrapping python/spa_manuals/bullfrog_spas/2024_Spa-layouts-electric-installation.pdf')
print('=== Spa Layouts PDF total pages:', len(doc_layouts))
for i, page in enumerate(doc_layouts):
    txt = page.get_text()
    if any(k in txt.lower() for k in ['s150', 's200', 's180', 'swim']):
        print(f'  Layouts Page {i+1}:')
        print(txt[:600])
