from pathlib import Path

harvester_path = Path("scripts/wayback_generational_harvester.py")
with open(harvester_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update BRAND_DOMAINS
old_domains = """BRAND_DOMAINS = {
    'Hot Spring Spas': [
        'hotspring.com/sites/default/files/images/spas/overhead/*',
        'hotspring.com/sites/default/files/images/spas/overhead-jets/*',
        'hotspring.com/sites/default/files/images/spas/*',
        'hotspring.com/wp-content/uploads/*',
    ],
    'Caldera Spas': [
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
    ]
}"""

new_domains = """BRAND_DOMAINS = {
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
}"""

assert old_domains in content, "old_domains not found"
content = content.replace(old_domains, new_domains)

# 2. Update verify_image with proportional aspect ratio error <= 22% and min_dist >= 9
old_verify = """    aspect = w / h
    if aspect < 0.45 or aspect > 2.2:
        return False, f"Aspect ratio invalid for spa footprint ({aspect:.2f})", None, None

    # Chromatic variance check (reject pure B&W line art / diagrams)
    var = compute_chromatic_variance(img)
    colors = len(img.convert('RGB').getcolors(maxcolors=20000) or [])
    if var < 3.0 and colors < 200:
        return False, f"Low chromatic variance/colors ({var:.1f}, {colors} colors) - likely B&W diagram", None, None

    # Compute dHash
    dh = compute_dhash(img)

    # Check collisions against existing catalog
    min_dist = 64
    closest_match = None
    for ex_dh, ex_info in existing_dhashes.items():
        dist = hamming_distance(dh, ex_dh)
        if dist < min_dist:
            min_dist = dist
            closest_match = ex_info

    if min_dist <= 4:
        return False, f"dHash collision ({min_dist} bits) with {closest_match[1]} {closest_match[2]} {closest_match[3]}", None, None"""

new_verify = """    aspect = w / h
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
        return False, f"dHash collision ({min_dist} bits < 9 bits) with {closest_match[1]} {closest_match[2]} {closest_match[3]}", None, None"""

assert old_verify in content, "old_verify not found"
content = content.replace(old_verify, new_verify)

# 3. Update call to verify_image
old_call = "valid, reason, dh, img = verify_image(content, existing_dhashes, (idx, brand, model, gen))"
new_call = "valid, reason, dh, img = verify_image(content, existing_dhashes, (idx, brand, model, gen, row.get('length_in'), row.get('width_in')))"
assert old_call in content, "old_call not found"
content = content.replace(old_call, new_call)

with open(harvester_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[OK] scripts/wayback_generational_harvester.py successfully upgraded for Batch #6!")
