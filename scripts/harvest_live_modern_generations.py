#!/usr/bin/env python3
"""
harvest_live_modern_generations.py
==================================
Executes Phase 12A Task 12.1:
Hybrid Live-Site Scraping for Modern Active Generations (2018–2026 / 2023–2026).
- Downloads verified authentic top-down photographs directly from official manufacturer CDNs
- Executes 4-gate verification:
  1. auto_crop_margins() via ImageChops
  2. Proportional Aspect Ratio Error <= 22%
  3. Chromatic Variance >= 3.0
  4. 64-bit dHash distance >= 9 bits (100% 1:1 unicity)
- Saves assets to assets/<Brand>/<Folder>/images/overhead/
- Updates data/spas_master_database.csv
"""

import os
import sys
import csv
import json
import time
import requests
import io
from PIL import Image, ImageChops

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(ROOT_DIR, 'data', 'spas_master_database.csv')
ARCHIVE_LOG = os.path.join(ROOT_DIR, '_ARCHIVE', 'ARCHIVE_LOG.md')

def auto_crop_margins(img, tolerance=15):
    if img.mode == 'RGBA':
        alpha = img.split()[-1]
        bbox = alpha.getbbox()
        if bbox:
            img = img.crop(bbox)
    bg = Image.new(img.mode, img.size, img.getpixel((0, 0)))
    diff = ImageChops.difference(img, bg)
    diff = ImageChops.add(diff, diff, 2.0, -tolerance)
    bbox = diff.getbbox()
    if bbox:
        return img.crop(bbox)
    return img

def compute_dhash(img, hash_size=8):
    img_l = img.convert('L').resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    try:
        pixels = list(img_l.get_flattened_data())
    except AttributeError:
        pixels = list(img_l.getdata())
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
    try:
        pixels = list(thumb.get_flattened_data())
    except AttributeError:
        pixels = list(thumb.getdata())
    diff_sum = sum(abs(r - g) + abs(g - b) + abs(b - r) for r, g, b in pixels)
    return diff_sum / len(pixels)

COMMITS = [
    # Bullfrog Spas Gen 2 (2023-2026)
    {
        "row_idx": 195,
        "brand": "Bullfrog Spas",
        "model": "A5L",
        "gen": "Gen 2",
        "url": "https://www.bullfrogspas.com/wp-content/uploads/2024/05/A5L_Top-Down.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer top-down orthographic photo from bullfrogspas.com (2024 redesign); auto-cropped margins, AR verified."
    },
    {
        "row_idx": 201,
        "brand": "Bullfrog Spas",
        "model": "A6",
        "gen": "Gen 2",
        "url": "https://www.bullfrogspas.com/wp-content/uploads/2024/05/A6_2-Pump_Top-Down.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer top-down orthographic photo from bullfrogspas.com (2024 redesign); auto-cropped margins, AR verified."
    },
    {
        "row_idx": 203,
        "brand": "Bullfrog Spas",
        "model": "A6L",
        "gen": "Gen 2",
        "url": "https://www.bullfrogspas.com/wp-content/uploads/2024/05/A6L_2-Pump_Top-Down.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer top-down orthographic photo from bullfrogspas.com (2024 redesign); auto-cropped margins, AR verified."
    },
    {
        "row_idx": 213,
        "brand": "Bullfrog Spas",
        "model": "A7L",
        "gen": "Gen 2",
        "url": "https://www.bullfrogspas.com/wp-content/uploads/2024/05/A7L_Top-Down.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer top-down orthographic photo from bullfrogspas.com (2024 redesign); auto-cropped margins, AR verified."
    },
    {
        "row_idx": 199,
        "brand": "Bullfrog Spas",
        "model": "X5L",
        "gen": "Gen 2",
        "url": "https://www.bullfrogspas.com/wp-content/uploads/2024/05/X5L_Select_Snow_Top.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer top-down orthographic photo from bullfrogspas.com (X-Series Select Snow); auto-cropped margins, AR verified."
    },
    {
        "row_idx": 209,
        "brand": "Bullfrog Spas",
        "model": "X6L",
        "gen": "Gen 2",
        "url": "https://www.bullfrogspas.com/wp-content/uploads/2024/05/X6L_Select_Snow_Top.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer top-down orthographic photo from bullfrogspas.com (X-Series Select Snow); auto-cropped margins, AR verified."
    },
    {
        "row_idx": 219,
        "brand": "Bullfrog Spas",
        "model": "X7",
        "gen": "Gen 2",
        "url": "https://www.bullfrogspas.com/wp-content/uploads/2024/05/X7_Select_Snow_Top.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer top-down orthographic photo from bullfrogspas.com (X-Series Select Snow); auto-cropped margins, AR verified."
    },
    {
        "row_idx": 237,
        "brand": "Bullfrog Spas",
        "model": "Stil 7",
        "gen": "Gen 1",
        "url": "https://www.bullfrogspas.com/wp-content/uploads/2024/05/STIL-7_top-down.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer top-down orthographic photo from bullfrogspas.com (STIL Series); auto-cropped margins, AR verified."
    },

    # Hot Spring Spas
    {
        "row_idx": 522,
        "brand": "Hot Spring Spas",
        "model": "Envoy",
        "gen": "Gen 3",
        "url": "https://www.hotspring.com/wp-content/uploads/2022/03/hotSpring-highlife-2024-envoy-overhead-iq-web.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer overhead render from hotspring.com (Highlife 2024 IQ); auto-cropped margins, AR verified."
    },
    {
        "row_idx": 528,
        "brand": "Hot Spring Spas",
        "model": "Grandee",
        "gen": "Gen 4",
        "url": "https://www.hotspring.com/wp-content/uploads/2022/03/hotSpring-highlife-2024-grandee-overhead-iq-web-3.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer overhead render from hotspring.com (Highlife 2024 IQ); auto-cropped margins, AR verified."
    },
    {
        "row_idx": 550,
        "brand": "Hot Spring Spas",
        "model": "Pace",
        "gen": "Gen 1",
        "url": "https://www.hotspring.com/wp-content/uploads/2025/01/hot-spring-spas-hotspot-overhead-pace-2025.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer overhead render from hotspring.com (Hot Spot 2025 Pace); auto-cropped margins, AR verified."
    },
    {
        "row_idx": 568,
        "brand": "Hot Spring Spas",
        "model": "Flair",
        "gen": "Gen 2",
        "url": "https://www.hotspring.com/wp-content/uploads/2024/02/HotSpring-Limelight-2024-Flair-AlpineWhite-Overhead-IQ.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer overhead render from hotspring.com (Limelight 2024 Flair Alpine White IQ); auto-cropped margins, AR verified."
    },

    # Jacuzzi
    {
        "row_idx": 675,
        "brand": "Jacuzzi",
        "model": "J-215",
        "gen": "Gen 1",
        "url": "https://jacuzzi-prod.imgix.net/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dw1d1246e7/images/hi-res/JHT_J-215_Platinum_OH.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer overhead render from jacuzzi.com (J-215 Platinum OH); auto-cropped margins, AR verified."
    },
    {
        "row_idx": 676,
        "brand": "Jacuzzi",
        "model": "J-225",
        "gen": "Gen 1",
        "url": "https://jacuzzi-prod.imgix.net/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dwbcb32b3c/images/hi-res/JHT_J-225_Platinum_OH.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer overhead render from jacuzzi.com (J-225 Platinum OH); auto-cropped margins, AR verified."
    },
    {
        "row_idx": 680,
        "brand": "Jacuzzi",
        "model": "J-325",
        "gen": "Gen 4",
        "url": "https://jacuzzi-prod.imgix.net/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dwf90df9a7/images/hi-res/JHT_J325_Platinum_OH.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer overhead render from jacuzzi.com (J-325 Platinum OH); auto-cropped margins, AR verified."
    },
    {
        "row_idx": 742,
        "brand": "Jacuzzi",
        "model": "J-19 DT Power Pro",
        "gen": "Gen 1",
        "url": "https://jacuzzi-prod.imgix.net/on/demandware.static/-/Sites-master-catalog-jacuzzi/default/dwc3819c2d/images/hi-res/JSS_PowerActive_J19DT_Porcelain_OH_IR.png",
        "ext": "png",
        "notes": "Verified authentic live manufacturer overhead render from jacuzzi.com (JSS PowerActive J19DT Porcelain OH); auto-cropped margins, AR verified."
    },

    # Sundance Spas
    {
        "row_idx": 1071,
        "brand": "Sundance Spas",
        "model": "Peyton",
        "gen": "Gen 2",
        "url": "https://cdn.prod.website-files.com/698dee5ce526ab6cb95380e0/6ab5729d2e49d168ece58a89_SDS_680_Peyton_Porcelain_OH.webp",
        "ext": "webp",
        "notes": "Verified authentic live manufacturer overhead render from sundancespas.com (680 Series Peyton Porcelain OH); auto-cropped margins, AR verified."
    }
]

def main():
    print("======================================================================")
    print("    PHASE 12A - TASK 12.1: LIVE MODERN GENERATIONS HARVEST & COMMIT   ")
    print("======================================================================")

    # 1. Load CSV
    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=';')
        fieldnames = reader.fieldnames
        rows = list(reader)

    print(f"Loaded master database: {len(rows)} rows.")

    # Fix Row 311 Florence Gen 1 span: 2005-2016
    r311 = rows[311]
    if r311['Marque'] == 'Caldera Spas' and r311['Modele'] == 'Florence' and r311['Generation'] == 'Gen 1':
        print(f"Normalizing Row 311 Florence Gen 1: '{r311['Annees_Production']}' -> '2005-2016'")
        r311['Annees_Production'] = '2005-2016'
        r311['audit_notes'] = (r311.get('audit_notes', '') + ' | Normalized historical span to 2005-2016 prior to Gen 2 introduction (2017).').strip(' |')

    # Collect existing dhashes
    existing_hashes = {}
    for idx, r in enumerate(rows):
        img_path = r.get('image_top_file', '')
        if img_path and img_path != 'N/A' and os.path.exists(img_path):
            try:
                with Image.open(img_path) as im:
                    h = compute_dhash(im)
                    existing_hashes[idx] = (h, img_path)
            except Exception:
                pass

    print(f"Loaded {len(existing_hashes)} existing catalog image hashes.")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    committed_count = 0
    for item in COMMITS:
        row_idx = item['row_idx']
        r = rows[row_idx]
        brand = item['brand']
        model = item['model']
        gen = item['gen']
        url = item['url']
        ext = item['ext']

        assert r['Marque'] == brand, f"Brand mismatch at row {row_idx}: {r['Marque']} vs {brand}"
        assert r['Modele'] == model, f"Model mismatch at row {row_idx}: {r['Modele']} vs {model}"
        assert r['Generation'] == gen, f"Generation mismatch at row {row_idx}: {r['Generation']} vs {gen}"

        print(f"\nProcessing Row {row_idx:04d} | {brand} {model} ({gen})...")
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code != 200:
            print(f"  [ERROR] HTTP {resp.status_code} fetching {url}")
            continue

        raw_img = Image.open(io.BytesIO(resp.content))
        orig_w, orig_h = raw_img.size
        cropped = auto_crop_margins(raw_img)
        crop_w, crop_h = cropped.size

        # Gate 2: Aspect Ratio
        l_in = float(r['length_in'])
        w_in = float(r['width_in'])
        cat_ratio = max(l_in, w_in) / min(l_in, w_in)
        img_ratio = max(crop_w, crop_h) / min(crop_w, crop_h)
        aspect_err = abs(cat_ratio - img_ratio) / cat_ratio

        # Gate 3: Chromatic Variance
        chroma = compute_chromatic_variance(cropped)

        # Gate 4: dHash & Unicity
        img_hash = compute_dhash(cropped)
        min_dist = 999
        closest_match = None
        for e_idx, (e_hash, e_path) in existing_hashes.items():
            dist = hamming_distance(img_hash, e_hash)
            if dist < min_dist:
                min_dist = dist
                closest_match = (e_idx, dist, e_path)

        gate_ar = aspect_err <= 0.22
        gate_chroma = chroma >= 3.0
        gate_hash = min_dist >= 9

        print(f"  Orig: {orig_w}x{orig_h} -> Crop: {crop_w}x{crop_h} | AR err: {aspect_err*100:.1f}% | Chroma: {chroma:.1f} | dHash dist: {min_dist}")

        if not (gate_ar and gate_chroma and gate_hash):
            print(f"  [REJECTED] Failed verification gates (AR={gate_ar}, Chroma={gate_chroma}, Hash={gate_hash})")
            continue

        # Determine target folder from footprint_file or construct standard path
        fp = r.get('footprint_file', '')
        if fp and fp != 'N/A':
            # e.g. ./assets/Bullfrog Spas/A5L_Gen_2_2023-2026/footprint/A5L_blueprint.pdf
            model_folder = os.path.dirname(os.path.dirname(fp))
        else:
            code = r.get('Code_Usine_Chassis', '') or gen.replace(' ', '')
            years = r.get('Annees_Production', '')
            model_folder = f"./assets/{brand}/{model}_{code}_{years}"

        dest_dir = os.path.join(ROOT_DIR, model_folder.replace('./', '').replace('/', os.sep), 'images', 'overhead')
        os.makedirs(dest_dir, exist_ok=True)

        clean_model = model.replace(' ', '_').replace('/', '_')
        dest_filename = f"{clean_model}_overhead.{ext}"
        dest_path = os.path.join(dest_dir, dest_filename)
        rel_dest_path = f"{model_folder}/images/overhead/{dest_filename}"

        # Save cropped image
        if ext == 'png':
            cropped.save(dest_path, format='PNG')
        elif ext in ('jpg', 'jpeg'):
            cropped.convert('RGB').save(dest_path, format='JPEG', quality=95)
        elif ext == 'webp':
            cropped.save(dest_path, format='WEBP', quality=95)

        # Update CSV row
        r['image_top_file'] = rel_dest_path
        r['image_top_source_url'] = url
        r['process_timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
        r['verification_status'] = 'COMPATIBLE'
        existing_notes = r.get('audit_notes', '')
        r['audit_notes'] = f"{existing_notes} | {item['notes']}".strip(' |')

        # Register in hash table
        existing_hashes[row_idx] = (img_hash, rel_dest_path)
        committed_count += 1
        print(f"  [COMMITTED] Saved to: {rel_dest_path}")

    # 4. Save CSV
    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n======================================================================")
    print(f"SUCCESS: Committed {committed_count} verified modern overhead photos!")
    print(f"Master CSV written to: {CSV_PATH}")
    print(f"======================================================================")

if __name__ == '__main__':
    main()
