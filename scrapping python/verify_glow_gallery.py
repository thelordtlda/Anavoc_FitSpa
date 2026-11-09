from pathlib import Path
import json
import re

html_p = Path("D:/SPAFIT/Cover Sizer/scrapping python/universal_audit_gallery.html")
text = html_p.read_text(encoding="utf-8")

m = re.search(r'const cardsData = (\[.*?\]);', text, re.DOTALL)
if m:
    cards = json.loads(m.group(1))
    glows = [c for c in cards if c["model"].lower() == "glow"]
    print("Glow in universal_audit_gallery.html:")
    for g in glows:
        print(f"  {g['year']} {g['model']}: dims_in={g['dims_4u']['in']} | dims_ft={g['dims_4u']['ft']} | dims_cm={g['dims_4u']['cm']} | dims_mm={g['dims_4u']['mm']} | has_real={g['has_real_photo']} | has_dwg={g['has_dwg']} ({g['dwg_size']}MB)")
