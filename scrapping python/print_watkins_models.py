import re
from pathlib import Path

f = Path("D:/SPAFIT/Cover Sizer/scrapping python/builders_watkins.py")
text = f.read_text(encoding='utf-8')
matches = re.findall(r'\{\s*"model":\s*"([^"]+)",\s*"dims":\s*\(([0-9.]+),\s*([0-9.]+),\s*([0-9.]+)\)', text)
print(f"Total model definitions in builders_watkins.py: {len(matches)}")
for m, l, w, h in matches:
    print(f"  {m:15}: {l} x {w} x {h}")
