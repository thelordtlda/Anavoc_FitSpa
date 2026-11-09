from pathlib import Path

f = Path("D:/SPAFIT/Cover Sizer/scrapping python/create_alphabetical_audit_gallery.py")
text = f.read_text(encoding='utf-8')
for line in text.splitlines():
    if any(k in line for k in ['badge_photo', 'has_photo', 'Photo Réelle', 'has_real_photo']):
        print(line[:120])
