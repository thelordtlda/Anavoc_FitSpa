from pathlib import Path
import json
import re

html_p = Path("D:/SPAFIT/Cover Sizer/scrapping python/universal_audit_gallery.html")
text = html_p.read_text(encoding="utf-8")

m = re.search(r'const cardsData = (\[.*?\]);', text, re.DOTALL)
if m:
    cards = json.loads(m.group(1))
    print(f"Total cards in HTML: {len(cards)}")
    
    # Grandee 2026
    g26 = [c for c in cards if c["model"].lower() == "grandee" and c["year"] == 2026]
    if g26:
        print("\n--- Grandee 2026 Source Links ---")
        for k in ['top_src', 'side_src', 'pdf_src', 'dwg_src', 'portal_ref']:
            print(f"  {k:12}: {g26[0].get(k)}")

    # Glow 2014
    glow14 = [c for c in cards if c["model"].lower() == "glow" and c["year"] == 2014]
    if glow14:
        print("\n--- Glow 2014 Source Links ---")
        for k in ['top_src', 'side_src', 'pdf_src', 'dwg_src', 'portal_ref']:
            print(f"  {k:12}: {glow14[0].get(k)}")

    # Bolt 2015
    bolt15 = [c for c in cards if c["model"].lower() == "bolt" and c["year"] == 2015]
    if bolt15:
        print("\n--- Bolt 2015 Source Links ---")
        for k in ['top_src', 'side_src', 'pdf_src', 'dwg_src', 'portal_ref']:
            print(f"  {k:12}: {bolt15[0].get(k)}")
