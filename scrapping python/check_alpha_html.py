from pathlib import Path
import re

p = Path("D:/SPAFIT/Cover Sizer/scrapping python/audit_gallery_hotspring_alphabetical.html")
text = p.read_text(encoding="utf-8")

# Find block for Grandee 2010
m = re.search(r'<span class="card-year">2010</span>\s*<span class="card-series">Grandee.*?</div>\s*</div>', text, re.DOTALL)
if m:
    print("Grandee 2010 in alphabetical HTML:")
    print(m.group(0)[:500])
else:
    print("Not found in alphabetical HTML")
