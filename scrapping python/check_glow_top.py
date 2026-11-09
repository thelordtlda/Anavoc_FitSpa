from pathlib import Path
from PIL import Image

p = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/hot_spring_spas/2010/hot_spring_glow_2010/top_view.jpg")
if p.exists():
    img = Image.open(p)
    print(f"glow 2010 top_view.jpg: format={img.format}, size={img.size}, mode={img.mode}, bytes={p.stat().st_size}")
else:
    print("Does not exist!")
