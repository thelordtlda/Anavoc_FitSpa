import fitz

doc = fitz.open('D:/SPAFIT/Cover Sizer/scrapping python/spa_manuals/bullfrog_spas/2024_Spa-layouts-electric-installation.pdf')
print(f'Total pages: {len(doc)}')
for i, page in enumerate(doc):
    txt = page.get_text()
    title = [l.strip() for l in txt.splitlines() if l.strip()][:3]
    print(f'Page {i+1}: {title}')
