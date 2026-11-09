from pathlib import Path

base_dir = Path(__file__).resolve().parent
hs_dir = base_dir / "dataset" / "hot_spring_spas"

total_models = 0
dwg_count = 0
dxf_count = 0
pdf_doc_count = 0
real_photo_count = 0

for yr_dir in hs_dir.glob("20*"):
    if not yr_dir.is_dir(): continue
    for m_dir in yr_dir.iterdir():
        if not m_dir.is_dir(): continue
        total_models += 1
        dwg = m_dir / "cad_model.dwg"
        dxf = m_dir / "cad_model.dxf"
        doc = m_dir / "official_manufacturer_doc.png"
        top = m_dir / "top_view.jpg"
        meta_p = m_dir / "metadata.json"
        
        has_real = False
        if meta_p.exists():
            import json
            with open(meta_p, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            has_real = meta.get("provenance", {}).get("has_real_photo", False)
            
        if dwg.exists() and dwg.stat().st_size > 5000:
            dwg_count += 1
        if dxf.exists() and dxf.stat().st_size > 5000:
            dxf_count += 1
        if doc.exists() and doc.stat().st_size > 5000:
            pdf_doc_count += 1
        if top.exists() and has_real:
            real_photo_count += 1

print(f"HotSpring Spas Inventory:")
print(f"  Total models across all years : {total_models}")
print(f"  Native AutoCAD DWG files      : {dwg_count}")
print(f"  DXF CAD files                 : {dxf_count}")
print(f"  Total CAD models (DWG + DXF)  : {dwg_count + dxf_count} / {total_models} ({round((dwg_count+dxf_count)/total_models*100, 1)}%)")
print(f"  Official 300 DPI Plans/PDFs   : {pdf_doc_count} / {total_models} ({round(pdf_doc_count/total_models*100, 1)}%)")
print(f"  Real Authentic Photos         : {real_photo_count}")
