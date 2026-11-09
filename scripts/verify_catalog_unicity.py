import os
import csv
from PIL import Image

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MASTER_CSV = os.path.join(ROOT_DIR, 'data', 'spas_master_database.csv')

def compute_dhash(img, hash_size=8):
    img_l = img.convert('L').resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = list(img_l.get_flattened_data())
    diff = []
    for row in range(hash_size):
        for col in range(hash_size):
            left = pixels[row * (hash_size + 1) + col]
            right = pixels[row * (hash_size + 1) + col + 1]
            diff.append(left > right)
    val = 0
    for b in diff:
        val = (val << 1) | (1 if b else 0)
    return f"{val:016x}"

def hamming_distance(h1, h2):
    return bin(int(h1, 16) ^ int(h2, 16)).count('1')

with open(MASTER_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    rows = list(reader)

print(f"Total rows in catalog: {len(rows)}")

top_rows = [r for r in rows if r.get('image_top_file') and r.get('image_top_file') != 'N/A']
print(f"Rows with linked image_top_file: {len(top_rows)}")

unique_paths = set(r['image_top_file'] for r in top_rows)
print(f"Unique image_top_file paths: {len(unique_paths)}")

dhashes = {}
collisions = []
missing_files = []

for idx, r in enumerate(top_rows):
    p = r['image_top_file']
    full_p = os.path.join(ROOT_DIR, p.lstrip('./').replace('/', os.sep))
    if not os.path.exists(full_p):
        missing_files.append((r['Marque'], r['Modele'], p))
        continue
    try:
        with Image.open(full_p) as im:
            dh = compute_dhash(im)
            if dh in dhashes:
                other_idx, other_m, other_g = dhashes[dh]
                collisions.append((r['Marque'], r['Modele'], r['Generation'], other_m, other_g, dh))
            else:
                dhashes[dh] = (idx, f"{r['Marque']} {r['Modele']}", r['Generation'])
    except Exception as e:
        print(f"Error opening {p}: {e}")

print(f"Unique dHashes: {len(dhashes)}")
print(f"Missing local image files: {len(missing_files)}")
print(f"Exact dHash collisions: {len(collisions)}")
if collisions:
    for c in collisions:
        print("  COLLISION:", c)

# Check DWG unicity
dwg_rows = [r for r in rows if r.get('cad_dwg_file') and r.get('cad_dwg_file') != 'N/A']
unique_dwgs = set(r['cad_dwg_file'] for r in dwg_rows)
print(f"Rows with linked cad_dwg_file: {len(dwg_rows)}")
print(f"Unique cad_dwg_file paths: {len(unique_dwgs)}")

# Check DXF unicity
dxf_rows = [r for r in rows if r.get('cad_dxf_file') and r.get('cad_dxf_file') != 'N/A']
unique_dxfs = set(r['cad_dxf_file'] for r in dxf_rows)
print(f"Rows with linked cad_dxf_file: {len(dxf_rows)}")
print(f"Unique cad_dxf_file paths: {len(unique_dxfs)}")
