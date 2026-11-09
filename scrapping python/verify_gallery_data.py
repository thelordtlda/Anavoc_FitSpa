from pathlib import Path
import json
import re

html_p = Path("D:/SPAFIT/Cover Sizer/scrapping python/universal_audit_gallery.html")
text = html_p.read_text(encoding="utf-8")

# Extract cardsData JSON
m = re.search(r'const cardsData = (\[.*?\]);', text, re.DOTALL)
if m:
    cards = json.loads(m.group(1))
    print(f"Total cards in HTML: {len(cards)}")
    
    # Check Glow
    glows = [c for c in cards if c["model"].lower() == "glow"]
    print(f"\nGlow cards ({len(glows)}):")
    for g in glows[:3]:
        print(f"  {g['year']} {g['model']}: dims={g['dims_4u']} | has_real={g['has_real_photo']} | has_dwg={g['has_dwg']}")
        
    # Check TX
    txs = [c for c in cards if c["model"].lower() == "tx"]
    print(f"\nTX cards ({len(txs)}):")
    for t in txs[:3]:
        print(f"  {t['year']} {t['model']}: dims={t['dims_4u']} | has_real={t['has_real_photo']} | has_dwg={t['has_dwg']}")
        
    # Check Grandee 2010
    g2010 = [c for c in cards if c["model"].lower() == "grandee" and c["year"] == 2010]
    print(f"\nGrandee 2010:")
    if g2010:
        print(f"  dims={g2010[0]['dims_4u']} | has_real={g2010[0]['has_real_photo']} | has_dwg={g2010[0]['has_dwg']} | dwg_size={g2010[0]['dwg_size']}MB")
