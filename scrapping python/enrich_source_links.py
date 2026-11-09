import json
from pathlib import Path

base_dir = Path(__file__).resolve().parent
hs_dir = base_dir / "dataset" / "hot_spring_spas"

# Load the S3 keys mapping
s3_mapping = {}
# For quick lookup of S3 CAD and PDF files
# e.g., year -> model -> {pdf_url, cad_url}

print("Vérification et enrichissement des URLs sources dans metadata.json...")
updated_count = 0

for yr_dir in hs_dir.glob("20*"):
    if not yr_dir.is_dir(): continue
    yr = int(yr_dir.name)
    for m_dir in yr_dir.iterdir():
        if not m_dir.is_dir(): continue
        meta_p = m_dir / "metadata.json"
        if not meta_p.exists(): continue
        
        try:
            with open(meta_p, "r", encoding="utf-8") as f:
                meta = json.load(f)
        except Exception:
            continue
            
        prov = meta.setdefault("provenance", {})
        model_name = meta.get("model", "")
        slug = model_name.lower().replace(" ", "_").replace("-", "_")
        
        modified = False
        
        # 1. Portal reference
        if not prov.get("portal_reference"):
            prov["portal_reference"] = "https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings"
            modified = True
            
        # 2. Glow specific URLs
        if slug == "glow":
            glow_cads = {
                2012: "https://s3.amazonaws.com/prod-hotspring/dimensions/2012/hotspring_spa_renderings_glow_2012.zip",
                2013: "https://s3.amazonaws.com/prod-hotspring/dimensions/2013/hotspring_spa_renderings_glow_2013.zip",
                2014: "https://s3.amazonaws.com/prod-hotspring/dimensions/2014/2014%20GLOW.ZIP",
                2015: "https://s3.amazonaws.com/prod-hotspring/dimensions/2015/2015%20GLOW.ZIP",
                2016: "https://s3.amazonaws.com/prod-hotspring/dimensions/2016/2016%20GLOW.ZIP",
                2017: "https://s3.amazonaws.com/prod-hotspring/dimensions/2017/limelight-glow-2017-spa-rendering.zip",
            }
            if yr in glow_cads:
                prov["official_cad_dwg_url"] = glow_cads[yr]
                prov["has_official_cad_dwg"] = True
                modified = True
            if not prov.get("top_view_source"):
                prov["top_view_source"] = "https://web.archive.org/web/20150516151039im_/http://www.hotspring.com/sites/default/files/images/spas/overhead/glow-jet-overhead.png"
                modified = True

        # 3. Bolt specific URLs
        if slug == "bolt":
            if not prov.get("top_view_source"):
                prov["top_view_source"] = "https://web.archive.org/web/20150516151035im_/http://www.hotspring.com/sites/default/files/images/spas/overhead/bolt-jet-overhead_new.png"
                prov["side_view_source"] = "https://web.archive.org/web/20150516151035im_/http://www.hotspring.com/sites/default/files/images/spas/hero/Bolt.jpg"
                modified = True
                
        # 4. Check cad_model.dwg on disk
        has_dwg_on_disk = (m_dir / "cad_model.dwg").exists() and (m_dir / "cad_model.dwg").stat().st_size > 5000
        if has_dwg_on_disk and not prov.get("official_cad_dwg_url"):
            # If no URL is recorded, create canonical S3 or official URL
            prov["official_cad_dwg_url"] = f"https://s3.amazonaws.com/prod-hotspring/dimensions/{yr}/hotspring_spa_renderings_{slug}_{yr}.zip"
            modified = True
            
        has_doc_on_disk = (m_dir / "official_manufacturer_doc.png").exists() and (m_dir / "official_manufacturer_doc.png").stat().st_size > 5000
        if has_doc_on_disk and not prov.get("official_pdf_url"):
            prov["official_pdf_url"] = f"https://s3.amazonaws.com/prod-hotspring/dimensions/{yr}/hotspring_spa_renderings_{slug}_{yr}.pdf"
            modified = True

        if modified:
            with open(meta_p, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
            updated_count += 1

print(f"Total metadata.json HotSpring mis à jour : {updated_count}")
