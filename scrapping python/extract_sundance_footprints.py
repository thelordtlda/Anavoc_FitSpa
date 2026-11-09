import os
from pathlib import Path
from schematic_extractor import SchematicExtractor

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")
MANUALS_DIR = BASE_DIR / "spa_manuals" / "sundance_spas"

def extract_all_sundance():
    extractor = SchematicExtractor()
    pdfs = [
        "2026_Sundance_Pre-Delivery-Guide.pdf",
        "2026_Sundance_Swim-Spas.pdf",
        "2025_Sundance_980-Series.pdf",
        "2026_Sundance_880-Series.pdf",
        "2026_Sundance_780-Series.pdf",
        "2026_Sundance_680-Series.pdf",
        "2018_Sundance_Select-Series.pdf",
        "2023_Sundance_Splash-Series.pdf"
    ]
    
    total_footprints = []
    for pdf_name in pdfs:
        p = MANUALS_DIR / pdf_name
        if p.exists():
            print(f"\nProcessing {pdf_name}...")
            res = extractor.extract_from_pdf(p, brand="Sundance Spas")
            total_footprints.extend(res)
            print(f"Extracted {len(res)} footprints from {pdf_name}")
            
    print(f"\n=== Total Sundance Footprints Extracted: {len(total_footprints)} ===")

if __name__ == "__main__":
    extract_all_sundance()
