from pathlib import Path

p = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/hot_spring_spas/2010/hot_spring_grandee_2010")
print("Files in Grandee 2010:")
for f in p.iterdir():
    print(f"  {f.name} ({f.stat().st_size} bytes)")
