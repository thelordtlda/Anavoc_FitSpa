import fitz

for name in ['2024_Pre-Delivery-Guide_8_5x11_v1.pdf', '2024_Spa-layouts-electric-installation.pdf']:
    path = f'D:/SPAFIT/Cover Sizer/scrapping python/spa_manuals/bullfrog_spas/{name}'
    doc = fitz.open(path)
    print(f'=== {name} ===')
    for i, p in enumerate(doc):
        txt = p.get_text()
        found = [l.strip() for l in txt.splitlines() if any(k in l.lower() for k in ['swim', 's150', 's200', 's180'])]
        if found:
            print(f'  Page {i+1}: {found[:3]}')
