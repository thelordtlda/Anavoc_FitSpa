from pathlib import Path

glow_2017_doc = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/hot_spring_spas/2017/hot_spring_glow_2017/official_manufacturer_doc.png")
print("Exists:", glow_2017_doc.exists(), "Size:", glow_2017_doc.stat().st_size if glow_2017_doc.exists() else 0)

glow_2010_doc = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/hot_spring_spas/2010/hot_spring_glow_2010/official_manufacturer_doc.png")
print("Exists:", glow_2010_doc.exists(), "Size:", glow_2010_doc.stat().st_size if glow_2010_doc.exists() else 0)
