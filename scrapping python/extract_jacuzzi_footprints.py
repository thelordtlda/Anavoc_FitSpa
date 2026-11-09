import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")
sys.path.insert(0, str(BASE_DIR))

from schematic_extractor import SchematicExtractor

def main():
    manuals_dir = BASE_DIR / "spa_manuals" / "jacuzzi"
    output_dir = BASE_DIR / "dataset"
    extractor = SchematicExtractor(output_root=output_dir)
    
    pdf_files = list(manuals_dir.glob("*.pdf"))
    print(f"=== EXTRACTING SCHEMATICS FROM {len(pdf_files)} JACUZZI MANUALS ===")
    
    total_extracted = 0
    for pdf_path in sorted(pdf_files):
        print(f"\nProcessing {pdf_path.name}...")
        results = extractor.extract_from_pdf(pdf_path, brand="jacuzzi")
        print(f"  -> Extracted {len(results)} schematic pages.")
        total_extracted += len(results)
        for r in results:
            print(f"     Page {r.get('page_number', '?')}: {Path(r['footprint_path']).name}")
            
    print(f"\n[DONE] Total schematics extracted: {total_extracted}")

if __name__ == "__main__":
    main()
