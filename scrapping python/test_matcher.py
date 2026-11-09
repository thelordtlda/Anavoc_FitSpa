import csv
import json
import re

input_path = r'C:/Users/nicol/.gemini/antigravity/brain/3fbc6496-e8c6-412d-9f36-bd5b7300d8bf/.user_uploaded/media_1793766220845_80851390.md'

with open(input_path, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

with open('scrapping python/dataset/spa_master_index.json', 'r', encoding='utf-8') as f:
    master_index = json.load(f)

# Build a lookup index by (brand_clean, model_clean)
def norm(s):
    return re.sub(r'[^a-zA-Z0-9]', '', str(s).lower())

brand_aliases = {
    'hot spring spas': 'hot_spring_spas',
    'caldera spas': 'caldera_spas',
    'endless pools': 'endless_pools',
    'freeflow spas': 'freeflow_spas',
    'lifesmart spas': 'lifesmart_spas',
    'tiger river spas': 'tiger_river_spas',
    'solana spas': 'solana_spas',
    'jacuzzi': 'jacuzzi',
    'sundance spas': 'sundance_spas',
    'dimension one spas': 'dimension_one_spas',
    'hydropool hot tubs': 'hydropool',
    'swimlife': 'hydropool', # SwimLife swim spas made by Hydropool
    'dream maker spas': 'dream_maker',
    'thermospas': 'thermospas',
    'artesian spas': 'artesian_spas',
    'marquis spas': 'marquis_spas',
    'clearwater spas': 'clearwater_spas',
    'american whirlpool': 'american_whirlpool',
    'vita spa': 'vita_spa',
    'l.a. spas': 'maax_spas', # LA Spas acquired by MAAX
    'michael phelps legend': 'master_spas',
    'h2x swim spas': 'master_spas',
    'twilight series': 'master_spas',
    'clarity spas': 'master_spas',
    'bullfrog spas': 'bullfrog_spas',
    'beachcomber': 'beachcomber',
    'arctic spas': 'arctic_spas',
    'coast spas': 'coast_spas',
    'innovaspa': 'innovaspa',
    'canadian spa co': 'canadian_spa_co',
    'cal spas': 'cal_spas',
    'nordic hot tubs': 'nordic_hot_tubs',
    'strong spas': 'strong_spas',
    'viking spas': 'viking_spas',
    'pdc spas': 'pdc_spas',
    'catalina spas': 'catalina',
    'wellis': 'wellis',
    'usspa': 'usspa',
    'tuff spas': 'tuff_spas',
    'emerald spas': 'emerald_spas',
    'great lakes spas': 'emerald_spas', # Great Lakes Spas made by Emerald
    'pacific spas': 'pacific_spas'
}

master_by_slug = {}
for entry in master_index:
    slug = entry['brand_slug'].lower()
    master_by_slug.setdefault(slug, []).append(entry)

matched = []
unmatched = []

for i, r in enumerate(rows):
    b = r['Marque'].strip()
    m = r['Modele'].strip()
    sm = r['Sous_Modele_ou_Version'].strip()
    gen = r['Generation'].strip()
    slug = brand_aliases.get(b.lower(), norm(b))
    
    entries = master_by_slug.get(slug, [])
    # Find match
    m_norm = norm(m)
    found = None
    for e in entries:
        em_norm = norm(e['model'])
        if m_norm == em_norm or m_norm in em_norm or em_norm in m_norm:
            found = e
            break
            
    if found:
        matched.append((r, found))
    else:
        unmatched.append(r)

print(f"Matched directly against master_index: {len(matched)}")
print(f"Unmatched: {len(unmatched)}")

by_unmatched_brand = {}
for r in unmatched:
    by_unmatched_brand.setdefault(r['Marque'], []).append(r)

for b, r_list in by_unmatched_brand.items():
    print(f"\nUnmatched Brand: {b} ({len(r_list)})")
    for r in r_list:
        print(f"  {r['Modele']} | {r['Sous_Modele_ou_Version']} | {r['Generation']}")
