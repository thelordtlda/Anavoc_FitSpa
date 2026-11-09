#!/usr/bin/env python3
"""
wayback_generational_harvester.py
==================================
Automated, batch-capable Wayback Machine (CDX API) Harvester for authentic
historical spa overhead photos, blueprints, and generational CAD assets.

Guarantees:
- Zero Synthetic Data: Never generates parametric approximations.
- Strict Generational Isolation: Rejects any asset if dHash matches another generation.
- Chromatic Variance & Aspect Ratio verification to reject B&W diagrams or banners.
- State checkpointing in data/checkpoints/wayback_harvest_state.json.
"""

import os
import sys
import csv
import json
import time
import shutil
import io
import argparse
from urllib.parse import quote
import requests
import re
from PIL import Image

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
MASTER_CSV_PATH = os.path.join(ROOT_DIR, 'data', 'spas_master_database.csv')
CHECKPOINT_PATH = os.path.join(ROOT_DIR, 'data', 'checkpoints', 'wayback_harvest_state.json')
CACHE_DIR = os.path.join(ROOT_DIR, 'data', 'cache', 'wayback')
ARCHIVE_LOG_PATH = os.path.join(ROOT_DIR, '_ARCHIVE', 'ARCHIVE_LOG.md')

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CHECKPOINT_PATH), exist_ok=True)

# Domain and query configurations
BRAND_DOMAINS = {
    'Hot Spring Spas': [
        'hotspring.com/sites/default/files/images/spas/overhead/*',
        'hotspring.com/sites/default/files/images/spas/overhead-jets/*',
        'hotspring.com/sites/default/files/images/spas/*',
        'hotspring.com/wp-content/uploads/*',
    ],
    'Caldera Spas': [
        'calderaspas.com/sites/default/files/images/spas/overhead/*',
        'calderaspas.com/sites/default/files/images/spas/*',
        'calderaspas.com/sites/default/files/images/*',
        'calderaspas.com/sites/default/files/*',
        'calderaspas.com/wp-content/uploads/*',
    ],
    'Jacuzzi': [
        'jacuzzi.com/en-us/hot-tubs/*',
        'jacuzzi.com/wp-content/uploads/*',
        'jacuzzihottubs.com/wp-content/uploads/*',
    ],
    'Sundance Spas': [
        'sundancespas.com/wp-content/uploads/*',
        'sundancespas.com/sites/default/files/*',
    ],
    'Master Spas': [
        'masterspas.com/images/hot-tubs/*',
        'masterspas.com/images/swim-spas/*',
        'masterspas.com/wp-content/uploads/*',
    ],
    'Artesian Spas': [
        'artesianspas.com/wp-content/uploads/*',
        'artesianspas.com/images/*',
    ],
    'Coast Spas': [
        'coastspas.com/images/*',
        'coastspas.com/wp-content/uploads/*',
    ],
    'Marquis Spas': [
        'marquisspas.com/assets/*',
        'marquisspas.com/images/*',
        'marquisspas.com/wp-content/uploads/*',
    ],
    'Hydropool': [
        'hydropoolhottubs.com/images/*',
        'hydropoolhottubs.com/wp-content/uploads/*',
    ],
    'Beachcomber': [
        'beachcomberhottubs.com/*',
    ],
    'Arctic Spas': [
        'arcticspas.com/wp-content/uploads/*',
        'arcticspas.com/images/*',
    ],
    'Cal Spas': [
        'calspas.com/wp-content/uploads/*',
        'calspas.com/images/*',
    ]
}

EXCLUDE_PATTERNS = [
    'manual', 'owner', 'guide', 'warranty', 'commercial', 'logo',
    'icon', 'button', 'thumb', 'banner', 'header', 'footer', 'bg',
    'background', 'dealer', 'delivery', 'cover-card', 'accessories',
    'award', 'badge', 'ad-', 'ad_'
]


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


def load_state():
    if os.path.exists(CHECKPOINT_PATH):
        try:
            with open(CHECKPOINT_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                data.setdefault('completed_rows', [])
                data.setdefault('harvested_count', 0)
                data.setdefault('records', [])
                return data
        except Exception:
            pass
    return {
        'last_updated': None,
        'completed_rows': [],
        'harvested_count': 0,
        'records': []
    }


def save_state(state):
    state['last_updated'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    with open(CHECKPOINT_PATH, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=2)


def get_existing_dhash_index(rows):
    index = {}
    for idx, r in enumerate(rows):
        p = r.get('image_top_file')
        if p and p != 'N/A':
            local_p = os.path.join(ROOT_DIR, p.lstrip('./').replace('/', os.sep))
            if os.path.exists(local_p):
                try:
                    with Image.open(local_p) as img:
                        dh = compute_dhash(img)
                        index[dh] = (idx, r['Marque'], r['Modele'], r['Generation'], local_p)
                except Exception:
                    pass
    return index


def parse_production_window(prod_str):
    if not prod_str or prod_str == 'N/A':
        return '2005', '2026'
    parts = prod_str.split('-')
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    elif len(parts) == 1 and parts[0].strip().isdigit():
        yr = parts[0].strip()
        return str(max(2000, int(yr)-1)), str(min(2026, int(yr)+1))
    return '2005', '2026'


def clean_model_tokens(model_str):
    cleaned = model_str.replace('(NXT)', '').replace('Elite', '').strip()
    sub_models = [m.strip() for m in cleaned.split('/') if m.strip()]
    tokens = []
    for m in sub_models:
        t = ''.join(c if c.isalnum() else ' ' for c in m).lower()
        parts = t.split()
        if parts:
            tokens.append(parts[0])  # primary word e.g. "aria", "dove", "748b"
            if len(parts) > 1:
                tokens.append(''.join(parts))
    return list(dict.fromkeys(tokens))


def query_cdx_for_pattern(session, pattern, from_yr, to_yr, max_results=100):
    url = "http://web.archive.org/cdx/search/cdx"
    params = {
        'url': pattern,
        'output': 'json',
        'fl': 'original,timestamp,mimetype',
        'filter': 'mimetype:image/.*',
        'from': from_yr,
        'to': to_yr,
        'collapse': 'urlkey',
        'limit': max_results
    }
    for attempt in range(3):
        try:
            r = session.get(url, params=params, timeout=25)
            if r.status_code == 200:
                data = r.json()
                return data[1:] if len(data) > 0 else []
            elif r.status_code == 503:
                time.sleep(3 * (attempt + 1))
            else:
                return []
        except Exception:
            time.sleep(2 * (attempt + 1))
    return []


def download_image_with_retry(session, ts, orig_url):
    wb_url = f"https://web.archive.org/web/{ts}im_/{orig_url}"
    for attempt in range(3):
        try:
            r = session.get(wb_url, timeout=20)
            if r.status_code == 200 and len(r.content) > 1000:
                return r.content, wb_url
            time.sleep(2)
        except Exception:
            time.sleep(2)
    return None, None


def verify_image(content, existing_dhashes, current_row_info):
    try:
        img = Image.open(io.BytesIO(content))
    except Exception:
        return False, "Unidentified image format", None, None

    w, h = img.size
    if w < 200 or h < 200:
        return False, f"Resolution too low ({w}x{h})", None, None

    aspect = w / h
    if aspect < 0.45 or aspect > 2.2:
        return False, f"Aspect ratio invalid for spa footprint ({aspect:.2f})", None, None

    # Proportional aspect ratio check against spa physical dimensions (tolerance <= 22%)
    if len(current_row_info) >= 6:
        l_in, w_in = current_row_info[4], current_row_info[5]
        if l_in and w_in and l_in != 'N/A' and w_in != 'N/A':
            try:
                l_f = float(l_in)
                w_f = float(w_in)
                if l_f > 0 and w_f > 0:
                    spa_ratio = max(l_f, w_f) / min(l_f, w_f)
                    img_ratio = max(w, h) / min(w, h)
                    aspect_err = abs(img_ratio - spa_ratio) / spa_ratio
                    if aspect_err > 0.22:
                        return False, f"Aspect ratio error {aspect_err*100:.1f}% exceeds 22% tolerance (img={img_ratio:.2f}, spa={spa_ratio:.2f})", None, None
            except ValueError:
                pass

    # Chromatic variance check (reject pure B&W line art / diagrams)
    var = compute_chromatic_variance(img)
    colors = len(img.convert('RGB').getcolors(maxcolors=20000) or [])
    if var < 3.0 and colors < 200:
        return False, f"Low chromatic variance/colors ({var:.1f}, {colors} colors) - likely B&W diagram", None, None

    # Compute dHash
    dh = compute_dhash(img)

    # Check collisions against existing catalog (strict >= 9 bits distance required)
    min_dist = 64
    closest_match = None
    for ex_dh, ex_info in existing_dhashes.items():
        dist = hamming_distance(dh, ex_dh)
        if dist < min_dist:
            min_dist = dist
            closest_match = ex_info

    if min_dist < 9:
        return False, f"dHash collision ({min_dist} bits < 9 bits) with {closest_match[1]} {closest_match[2]} {closest_match[3]}", None, None

    return True, "PASSED", dh, img


def get_target_asset_dir(row):
    # Find existing folder from footprint_file, image_side_file, etc.
    for col in ['footprint_file', 'image_side_file', 'cad_dwg_file']:
        val = row.get(col)
        if val and val != 'N/A':
            parts = val.replace('\\', '/').split('/')
            if 'assets' in parts:
                idx = parts.index('assets')
                if len(parts) > idx + 2:
                    rel_dir = os.path.join(*parts[idx:idx+3])
                    full_dir = os.path.join(ROOT_DIR, rel_dir)
                    if os.path.exists(full_dir):
                        return full_dir, rel_dir.replace('\\', '/')

    # Fallback standard folder
    safe_brand = "".join(c for c in row['Marque'] if c.isalnum() or c in ' -_').strip()
    safe_model = "".join(c for c in row['Modele'] if c.isalnum() or c in ' -_').strip().replace(' ', '_')
    safe_gen = "".join(c for c in row['Generation'] if c.isalnum() or c in ' -_').strip().replace(' ', '_')
    folder_name = f"{safe_model}_{safe_gen}_{row['Annees_Production']}"
    rel_dir = f"assets/{safe_brand}/{folder_name}"
    full_dir = os.path.join(ROOT_DIR, 'assets', safe_brand, folder_name)
    os.makedirs(full_dir, exist_ok=True)
    return full_dir, rel_dir


def main():
    parser = argparse.ArgumentParser(description="Wayback Machine Generational Catalog Harvester")
    parser.add_argument('--brand', choices=list(BRAND_DOMAINS.keys()), help="Target specific brand")
    parser.add_argument('--limit', type=int, default=20, help="Max rows to process in this run")
    parser.add_argument('--commit', action='store_true', help="Commit downloaded assets to catalog")
    args = parser.parse_args()

    print("======================================================================")
    print("      WAYBACK MACHINE GENERATIONAL CATALOG HARVESTER (PHASE 4)        ")
    print("======================================================================")

    # 1. Load CSV
    with open(MASTER_CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Loaded {len(rows)} catalog rows.")

    # 2. Index existing dHashes
    print("Indexing existing catalog dHashes for collision prevention...")
    existing_dhashes = get_existing_dhash_index(rows)
    print(f"Indexed {len(existing_dhashes)} existing top-view photos.")

    # 3. Load checkpoint state
    state = load_state()
    print(f"Checkpoint state: {len(state['completed_rows'])} completed rows previously.")

    # 4. Filter candidate rows
    candidates = []
    for idx, r in enumerate(rows):
        if idx in state['completed_rows']:
            continue
        if args.brand and r['Marque'] != args.brand:
            continue
        if r['Marque'] not in BRAND_DOMAINS:
            continue
        has_top = bool(r.get('image_top_file') and r.get('image_top_file') != 'N/A')
        if not has_top:
            candidates.append((idx, r))

    print(f"Found {len(candidates)} candidate rows missing top-view photos.")
    if not candidates:
        print("No candidates to process. Done!")
        return

    # 5. Process candidates up to limit
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    })

    batch = candidates[:args.limit]
    print(f"\nProcessing Batch of {len(batch)} rows (limit={args.limit}, commit={args.commit})...\n")

    harvested_in_session = 0

    for idx, row in batch:
        brand = row['Marque']
        model = row['Modele']
        gen = row['Generation']
        prod = row['Annees_Production']
        from_yr, to_yr = parse_production_window(prod)
        tokens = clean_model_tokens(model)

        print(f"--> [Row {idx+2:4d}] {brand} | {model} | {gen} ({prod})")
        print(f"    Tokens: {tokens} | Window: {from_yr}-{to_yr}")

        # Check pre-compiled archive matches (e.g. Hot Spring known overheads)
        patterns = BRAND_DOMAINS.get(brand, [])
        found_asset = False

        for pattern in patterns:
            if found_asset:
                break
            time.sleep(2.0)
            cdx_results = query_cdx_for_pattern(session, pattern, from_yr, to_yr, max_results=100)
            if not cdx_results:
                continue

            # Match against tokens
            for cdx_row in cdx_results:
                orig_url, ts = cdx_row[0], cdx_row[1]
                orig_lower = orig_url.lower()

                # Filter exclusions
                if any(ex in orig_lower for ex in EXCLUDE_PATTERNS):
                    continue

                # Check if model token is in URL
                # Strict two-sided temporal bounds: start_year <= snapshot_year <= end_year
                snap_year = int(ts[:4])
                url_year_match = re.search(r'/(20[0-2][0-9])/', orig_lower)
                upload_year = int(url_year_match.group(1)) if url_year_match else snap_year
                effective_year = min(snap_year, upload_year)
                
                if effective_year < int(from_yr) or effective_year > int(to_yr):
                    continue

                # Filename model-year check (e.g. AmoreBay2015 -> 2015 model year)
                filename_only = os.path.basename(orig_url.split('?')[0]).lower()
                fn_year_match = re.search(r'(20[0-2][0-9])', filename_only)
                if fn_year_match:
                    model_year = int(fn_year_match.group(1))
                    if model_year < int(from_yr) or model_year > int(to_yr):
                        continue

                matches_token = any(f"/{tok}" in orig_lower or f"-{tok}" in orig_lower or f"_{tok}" in orig_lower or f"{tok}-" in orig_lower or f"{tok}." in orig_lower for tok in tokens)
                if not matches_token:
                    continue

                print(f"    Found candidate URL on CDX: {orig_url} ({ts})")

                # Download
                content, wb_url = download_image_with_retry(session, ts, orig_url)
                if not content:
                    print("      Download failed.")
                    continue

                # Verify
                valid, reason, dh, img = verify_image(content, existing_dhashes, (idx, brand, model, gen, row.get('length_in'), row.get('width_in')))
                if not valid:
                    print(f"      Verification REJECTED: {reason}")
                    continue

                print(f"      Verification PASSED! dHash={dh}")

                # Save asset
                full_dir, rel_dir = get_target_asset_dir(row)
                overhead_dir = os.path.join(full_dir, 'images', 'overhead')
                os.makedirs(overhead_dir, exist_ok=True)

                ext = os.path.splitext(orig_url.split('?')[0])[1].lower() or '.png'
                clean_model_name = "".join(c for c in model if c.isalnum() or c in ' -_').strip().replace(' ', '_')
                filename = f"{clean_model_name}_overhead{ext}"
                dest_full = os.path.join(overhead_dir, filename)
                rel_dest = f"./{rel_dir}/images/overhead/{filename}".replace('\\', '/')

                if args.commit:
                    with open(dest_full, 'wb') as f_out:
                        f_out.write(content)

                    # Update CSV row
                    row['image_top_file'] = rel_dest
                    row['image_top_source_url'] = wb_url
                    row['verification_status'] = 'VERIFIED_WAYBACK_HISTORICAL'
                    row['audit_notes'] = f"Wayback CDX harvested {ts}; dHash={dh}; 0 collisions"
                    row['process_timestamp'] = time.strftime('%Y-%m-%dT%H:%M:%S')

                    # Add to existing index so subsequent rows in this run don't collide
                    existing_dhashes[dh] = (idx, brand, model, gen, dest_full)
                    state['records'].append({
                        'row_idx': idx,
                        'brand': brand,
                        'model': model,
                        'gen': gen,
                        'file': rel_dest,
                        'url': wb_url,
                        'dhash': dh
                    })
                    print(f"      COMMITTED: {rel_dest}")

                found_asset = True
                harvested_in_session += 1
                break

        state['completed_rows'].append(idx)
        save_state(state)

    # Save CSV if committed
    if args.commit and harvested_in_session > 0:
        print(f"\nWriting updates to {MASTER_CSV_PATH}...")
        with open(MASTER_CSV_PATH, 'w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            writer.writerows(rows)
        print(f"Successfully committed {harvested_in_session} new authentic Wayback assets to catalog!")

    print(f"\nSession summary: {harvested_in_session} assets harvested across {len(batch)} processed rows.")


if __name__ == '__main__':
    main()
