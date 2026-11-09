from pathlib import Path
from test_builders import test_sundance, test_awp, test_maax

BASE_DIR = Path("D:/SPAFIT/Cover Sizer/scrapping python")

def check_mapping(brand_slug, specs, img_prefix=""):
    img_dir = BASE_DIR / "images" / brand_slug
    fp_dir = BASE_DIR / "dataset" / brand_slug / "extracted_footprints"
    fps = list(fp_dir.glob("*.png"))
    
    missing_top = []
    missing_side = []
    missing_fp = []
    
    for item in specs:
        m = item["model"]
        m_norm = m.lower().replace(" ", "").replace("-", "")
        # search folder
        cand_dirs = [
            img_dir / m_norm,
            img_dir / m.lower(),
            img_dir / m_norm.replace("powerpool", "powerpool_"),
            img_dir / f"powerpool_{m_norm.replace('powerpool', '')}",
            img_dir / f"stream{m_norm.replace('stream', '')}",
            img_dir / f"surf{m_norm.replace('surf', '')}",
        ]
        found_dir = None
        for cd in cand_dirs:
            if cd.exists():
                found_dir = cd
                break
                
        has_top = bool(found_dir and list(found_dir.glob("top_view.*")))
        has_side = bool(found_dir and list(found_dir.glob("side_view.*")))
        
        if not has_top:
            missing_top.append(f"{m} ({item['year']})")
        if not has_side:
            missing_side.append(f"{m} ({item['year']})")
            
    print(f"\n[{brand_slug.upper()}] Total specs: {len(specs)}")
    print(f"  Missing top views: {len(missing_top)} {missing_top[:5]}")
    print(f"  Missing side views: {len(missing_side)} {missing_side[:5]}")

check_mapping("sundance_spas", test_sundance())
check_mapping("american_whirlpool", test_awp())
check_mapping("maax_spas", test_maax())
