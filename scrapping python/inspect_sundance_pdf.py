import fitz
import re
from pathlib import Path

manuals_dir = Path("D:/SPAFIT/Cover Sizer/scrapping python/spa_manuals/sundance_spas")

pre_del = manuals_dir / "2026_Sundance_Pre-Delivery-Guide.pdf"
if pre_del.exists():
    doc = fitz.open(pre_del)
    print(f"2026 Pre-Delivery Guide: {len(doc)} pages")
    for i, page in enumerate(doc):
        text = page.get_text()
        first_line = text.split("\n")[0] if text else ""
        # Check for dimensions or models
        matches = re.findall(r"\b(Kingston|Claremont|Lisbon|Odessa|Aspen|Maxxus|Cameo|Optima|Cameo|Altamar|Marin|Capri|Chelsee|Hamilton|Bristol|Hanover|Montclair|Dover|Prado|Lucia|Peyton|Denali|Tacoma|Ramona|Edison|Verve)\b", text, re.I)
        if matches or "dimension" in text.lower() or "specification" in text.lower():
            unique_models = list(set(matches))
            print(f"Page {i+1}: {unique_models} | {first_line[:60]}")

swim_pdf = manuals_dir / "2026_Sundance_Swim-Spas.pdf"
if swim_pdf.exists():
    doc_swim = fitz.open(swim_pdf)
    print(f"\n2026 Swim Spas Manual: {len(doc_swim)} pages")
    for i, page in enumerate(doc_swim):
        text = page.get_text()
        if any(w in text.lower() for w in ["dimension", "specifications", "length", "width"]):
            lines = [l.strip() for l in text.split("\n") if any(k in l.lower() for k in ["length", "width", "height", "dimension", "swim", "ft", "x", "model", "series"]) and len(l.strip()) < 80]
            print(f"Swim Page {i+1}: {lines[:5]}")
