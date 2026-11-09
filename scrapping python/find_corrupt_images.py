import os
import cv2
from pathlib import Path

DATASET = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset")

corrupt_files = []
total_images = 0

for root, dirs, files in os.walk(DATASET):
    for f in files:
        if f.endswith((".png", ".jpg", ".webp", ".jpeg")):
            total_images += 1
            p = Path(root) / f
            if p.stat().st_size < 100:
                corrupt_files.append((str(p.relative_to(DATASET)), f"too small: {p.stat().st_size} bytes"))
            else:
                # Test read for non-png or small files
                if f.endswith(".webp") or p.stat().st_size < 10000:
                    im = cv2.imread(str(p))
                    if im is None:
                        corrupt_files.append((str(p.relative_to(DATASET)), "cv2 decode failed"))

print(f"Total images audited: {total_images}")
print(f"Corrupted or invalid images: {len(corrupt_files)}")
for c in corrupt_files[:20]:
    print("  ", c)
