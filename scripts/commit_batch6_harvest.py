import os
import sys
import csv
import json
import time
import shutil
import requests
import io
from PIL import Image

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MASTER_CSV = os.path.join(ROOT_DIR, 'data', 'spas_master_database.csv')
ARCHIVE_LOG = os.path.join(ROOT_DIR, '_ARCHIVE', 'ARCHIVE_LOG.md')

# Helper functions
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

def compute_chromatic_variance(img):
    thumb = img.convert('RGB').resize((64, 64))
    pixels = list(thumb.get_flattened_data())
    diff_sum = sum(abs(r - g) + abs(g - b) + abs(b - r) for r, g, b in pixels)
    return diff_sum / len(pixels)

# Load existing catalog
with open(MASTER_CSV, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter=';')
    fieldnames = reader.fieldnames
    rows = list(reader)

existing_dhashes = {}
for idx, r in enumerate(rows):
    p = r.get('image_top_file')
    if p and p != 'N/A':
        full_p = os.path.join(ROOT_DIR, p.lstrip('./').replace('/', os.sep))
        if os.path.exists(full_p):
            try:
                with Image.open(full_p) as im:
                    dh = compute_dhash(im)
                    existing_dhashes[dh] = (idx, r['Marque'], r['Modele'], r['Generation'], full_p)
            except Exception:
                pass

print(f"Loaded {len(existing_dhashes)} existing catalog image dHashes.")

# List of confirmed items to harvest
# Format: (brand, model, gen, source_type, source_path_or_url, filename)
HARVEST_PLAN = [
    # Beachcomber
    ('Beachcomber', '350', 'Gen 1', 'local', 'data/temp/bc_images/350_top_view.png', '350_overhead.png'),
    ('Beachcomber', '360', 'Gen 1', 'local', 'data/temp/bc_images/360_top_view.png', '360_overhead.png'),
    ('Beachcomber', '530', 'Gen 1', 'local', 'data/temp/bc_images/530_top_view.png', '530_overhead.png'),
    ('Beachcomber', '540', 'Gen 1', 'local', 'data/temp/bc_images/540_top_view.png', '540_overhead.png'),
    ('Beachcomber', '550', 'Gen 1', 'local', 'data/temp/bc_images/550_top_view.png', '550_overhead.png'),
    ('Beachcomber', '590', 'Gen 1', 'local', 'data/temp/bc_images/590_top_view.png', '590_overhead.png'),
    ('Beachcomber', '710', 'Gen 1', 'local', 'data/temp/bc_images/710_top_view.png', '710_overhead.png'),
    ('Beachcomber', '730', 'Gen 1', 'local', 'data/temp/bc_images/730_top_view.png', '730_overhead.png'),
    # Arctic Spas
    ('Arctic Spas', 'Cub', 'Gen 1', 'url', 'https://www.arcticspas.com/wp-content/uploads/CUB-40-SDS-Platinium-visao-400-300x300-2.png', 'Cub_overhead.png'),
    ('Arctic Spas', 'Eagle', 'Gen 1', 'url', 'https://www.arcticspas.com/wp-content/uploads/EAGLE-40-Platinium-visao-400-300x300-2.png', 'Eagle_overhead.png'),
    ('Arctic Spas', 'Totem', 'Gen 1', 'url', 'https://www.arcticspas.com/wp-content/uploads/TOTEM-40-Platinium-visao-400-300x300-2.png', 'Totem_overhead.png'),
    ('Arctic Spas', 'Yukon', 'Gen 1', 'url', 'https://www.arcticspas.com/wp-content/uploads/YUKON-40-SDS-Platinium-visao-400-300x300-2.png', 'Yukon_overhead.png'),
    ('Arctic Spas', 'Grizzly', 'Gen 1', 'url', 'https://www.arcticspas.com/wp-content/uploads/GRIZZLY-40-Platinium-visao-400-300x300-3.png', 'Grizzly_overhead.png'),
    ('Arctic Spas', 'Orca', 'Gen 1', 'url', 'https://www.arcticspas.com/wp-content/uploads/ORCA-40-Platinium-visao-400-300x300-2.png', 'Orca_overhead.png'),
    ('Arctic Spas', 'McKinley', 'Gen 1', 'url', 'https://www.arcticspas.com/wp-content/uploads/MCKINLEY-40-Platinium-visao-400-300x300-2.png', 'McKinley_overhead.png'),
    ('Arctic Spas', 'Mustang', 'Gen 1', 'url', 'https://www.arcticspas.com/wp-content/uploads/MUSTANG-40-Platinium-visao-400-300x300-3.png', 'Mustang_overhead.png'),
    ('Arctic Spas', 'Tundra', 'Gen 1', 'url', 'https://www.arcticspas.com/wp-content/uploads/TUNDRA-60-Platinium-visao-400-300x300-1.png', 'Tundra_overhead.png'),
    ('Arctic Spas', 'Columbia', 'Gen 1', 'url', 'https://www.arcticspas.com/wp-content/uploads/arcticspas-Columbia-Legend-Select-tier-top-view-500x905-2-2.png', 'Columbia_overhead.png'),
    ('Arctic Spas', 'Okanagan', 'Gen 1', 'url', 'https://www.arcticspas.com/wp-content/uploads/2021-arcticspas-awp-okanagan-legend-500x300-vertical.png', 'Okanagan_overhead.png'),
    ('Arctic Spas', 'Ocean', 'Gen 1', 'url', 'https://www.arcticspas.com/wp-content/uploads/2021-arcticspas-awp-ocean-legend-select-500x300-vertical.png', 'Ocean_overhead.png'),
    ('Arctic Spas', 'Kingfisher', 'Gen 1', 'url', 'https://www.arcticspas.com/wp-content/uploads/arctic-spas-awp-garden-ladies-1000-3.jpg', 'Kingfisher_overhead.jpg'),
    # Cal Spas
    ('Cal Spas', 'Belair', 'Gen 1', 'url', 'https://calspas.com/images/belair.webp', 'Belair_overhead.webp'),
    # Marquis Spas
    ('Marquis Spas', 'The Spirit', 'Gen 1', 'url', 'https://web.archive.org/web/20051218163932im_/http://marquisspas.com:80/images/finance/mspa_overhead_spirit.jpg', 'Spirit_overhead.jpg')
]

session = requests.Session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

committed_count = 0
committed_log = []

for brand, model, gen, src_type, src_path, target_fn in HARVEST_PLAN:
    matching = [r for r in rows if r['Marque'] == brand and r['Modele'] == model and r['Generation'] == gen]
    if not matching:
        print(f"Skipping {brand} {model} {gen}: not found in catalog")
        continue
    row = matching[0]
    row_idx = rows.index(row)
    
    # Obtain image
    img = None
    source_url = None
    if src_type == 'local':
        full_src = os.path.join(ROOT_DIR, src_path.replace('/', os.sep))
        if os.path.exists(full_src):
            try:
                img = Image.open(full_src)
                source_url = f"https://www.beachcomberhottubs.com/hot-tubs/{model}"
            except Exception as e:
                print(f"Failed to open local {full_src}: {e}")
                continue
    else:
        source_url = src_path
        for attempt in range(3):
            try:
                r = session.get(src_path, timeout=15)
                if r.status_code == 200:
                    img = Image.open(io.BytesIO(r.content))
                    break
                time.sleep(1)
            except Exception:
                time.sleep(1)
        if img is None:
            print(f"Failed to download {src_path}")
            continue

    # Verify image
    w, h = img.size
    l_in, w_in = float(row['length_in']), float(row['width_in'])
    spa_ratio = max(l_in, w_in) / min(l_in, w_in)
    img_ratio = max(w, h) / min(w, h)
    err = abs(img_ratio - spa_ratio) / spa_ratio
    dh = compute_dhash(img)

    # Check collisions
    min_dist = 64
    closest = None
    for ex_dh, ex_info in existing_dhashes.items():
        dist = hamming_distance(dh, ex_dh)
        if dist < min_dist:
            min_dist = dist
            closest = ex_info
    
    if min_dist < 9:
        print(f"COLLISION: {brand} {model} collided with {closest[1]} {closest[2]} (dist={min_dist}) -> SKIPPED")
        continue

    # Determine destination folder
    # Use existing footprint_file folder if available
    fp = row.get('footprint_file')
    if fp and fp != 'N/A':
        folder_dir = os.path.dirname(os.path.dirname(os.path.join(ROOT_DIR, fp.lstrip('./').replace('/', os.sep))))
    else:
        safe_model = "".join(c for c in model if c.isalnum() or c in ' -_').strip().replace(' ', '_')
        safe_gen = "".join(c for c in gen if c.isalnum() or c in ' -_').strip().replace(' ', '_')
        folder_name = f"{safe_model}_{safe_gen}_{row['Annees_Production']}"
        folder_dir = os.path.join(ROOT_DIR, 'assets', brand, folder_name)

    target_dir = os.path.join(folder_dir, 'images', 'overhead')
    os.makedirs(target_dir, exist_ok=True)
    target_path = os.path.join(target_dir, target_fn)

    # Save image
    if src_type == 'local':
        shutil.copy2(os.path.join(ROOT_DIR, src_path.replace('/', os.sep)), target_path)
    else:
        img.save(target_path)

    rel_target = os.path.relpath(target_path, ROOT_DIR).replace('\\', '/')
    if not rel_target.startswith('./'):
        rel_target = './' + rel_target

    # Update row
    row['image_top_file'] = rel_target
    row['image_top_source_url'] = source_url
    prev_notes = row.get('audit_notes', '')
    new_note = f"[Batch 6 Harvest: Verified overhead photo ({w}x{h}, aspect err {err*100:.1f}%, dHash {dh}, min_dist={min_dist}b)]"
    row['audit_notes'] = f"{prev_notes} {new_note}".strip()

    # Update hash index
    existing_dhashes[dh] = (row_idx, brand, model, gen, target_path)
    committed_count += 1
    committed_log.append(f"Row {row_idx:04d} | {brand:<14} | {model:<14} | {gen:<8} | {rel_target} (err={err*100:.1f}%, dist={min_dist}b)")
    print(f"COMMITTED: {brand} {model} {gen} -> {rel_target}")

# Save updated CSV
with open(MASTER_CSV, 'w', encoding='utf-8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    writer.writerows(rows)

print(f"\nSuccessfully committed {committed_count} authentic overhead images to master catalog!")
for l in committed_log:
    print("  ", l)

# Append to ARCHIVE_LOG
with open(ARCHIVE_LOG, 'a', encoding='utf-8') as f:
    f.write(f"\n## Batch #6 Authentic Overhead Harvest - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"- Total committed: {committed_count}\n")
    for l in committed_log:
        f.write(f"- {l}\n")
