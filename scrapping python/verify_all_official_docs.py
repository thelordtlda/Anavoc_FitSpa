import fitz
from pathlib import Path
import json

base_dir = Path(__file__).resolve().parent
hs_dir = base_dir / "dataset" / "hot_spring_spas"
manuals_dir = base_dir / "spa_manuals" / "hotspring"

# Ensure all PDFs are converted to high-res PNG for thumbnail/previews
print("Vérification des plans officiels 300 DPI...")
rendered_count = 0

for yr_dir in hs_dir.glob("20*"):
    if not yr_dir.is_dir(): continue
    for m_dir in yr_dir.iterdir():
        if not m_dir.is_dir(): continue
        doc_p = m_dir / "official_manufacturer_doc.png"
        
        # If already exists and good size, skip
        if doc_p.exists() and doc_p.stat().st_size > 10000:
            continue
            
        # Look for matching pdf in spa_manuals or target folder
        pdf_files = list(m_dir.glob("*.pdf"))
        if not pdf_files and manuals_dir.exists():
            mod_slug = m_dir.name.replace("hot_spring_", "").replace(f"_{yr_dir.name}", "")
            candidates = list(manuals_dir.glob(f"*{mod_slug}*{yr_dir.name}*.pdf"))
            if candidates:
                pdf_files = candidates
                
        if pdf_files:
            pdf_path = pdf_files[0]
            try:
                doc = fitz.open(pdf_path)
                page = doc[0]
                pix = page.get_pixmap(dpi=200) # 200-300 dpi
                pix.save(str(doc_p))
                print(f"Rendu officiel créé pour {m_dir.name} ({doc_p.stat().st_size} octets)")
                rendered_count += 1
            except Exception as e:
                print(f"Erreur rendu {pdf_path}: {e}")

print(f"Total nouveaux rendus officiels créés : {rendered_count}")
