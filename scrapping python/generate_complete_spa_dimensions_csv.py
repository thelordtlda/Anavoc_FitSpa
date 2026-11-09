import csv
import json
import re

input_path = r'C:/Users/nicol/.gemini/antigravity/brain/3fbc6496-e8c6-412d-9f36-bd5b7300d8bf/.user_uploaded/media_1793766220845_80851390.md'
output_csv_path = r'd:/SPAFIT/Cover Sizer/scrapping python/dataset/base_de_donnees_spas_avec_dimensions.csv'

with open(input_path, 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f, delimiter=';'))

print(f"Loaded {len(rows)} rows from input file.")

# Load master index
with open('scrapping python/dataset/spa_master_index.json', 'r', encoding='utf-8') as f:
    master_index = json.load(f)

# Build quick lookup from master index
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
    'swimlife': 'hydropool',
    'dream maker spas': 'dream_maker',
    'thermospas': 'thermospas',
    'artesian spas': 'artesian_spas',
    'marquis spas': 'marquis_spas',
    'clearwater spas': 'clearwater_spas',
    'american whirlpool': 'american_whirlpool',
    'vita spa': 'vita_spa',
    'l.a. spas': 'maax_spas',
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
    'great lakes spas': 'emerald_spas',
    'pacific spas': 'pacific_spas'
}

master_by_slug_model = {}
for entry in master_index:
    slug = entry['brand_slug'].lower()
    m_clean = norm(entry['model'])
    master_by_slug_model.setdefault((slug, m_clean), []).append(entry)

# Explicit fallback definitions for exact dimensions (length_in, width_in, height_in, corner_radius_in)
EXPLICIT_SPECS = {
    # Hot Spring Spas
    ("hot spring spas", "grandee", "gen 1"): (100.0, 91.0, 38.0, 8.0),
    ("hot spring spas", "grandee", "gen 2"): (100.0, 91.0, 38.0, 8.0),
    ("hot spring spas", "grandee", "gen 3"): (100.0, 91.0, 38.0, 8.0),
    ("hot spring spas", "grandee", "gen 3 (nxt)"): (100.0, 91.0, 38.0, 8.0),
    ("hot spring spas", "grandee", "gen 4"): (100.0, 91.0, 38.0, 8.0),
    ("hot spring spas", "envoy", "gen 1"): (93.0, 89.0, 36.0, 8.0),
    ("hot spring spas", "envoy", "gen 2"): (93.0, 91.0, 38.0, 8.0),
    ("hot spring spas", "envoy", "gen 3"): (93.0, 91.0, 38.0, 8.0),
    ("hot spring spas", "envoy", "gen 3 (nxt)"): (93.0, 91.0, 38.0, 8.0),
    ("hot spring spas", "envoy", "gen 4"): (100.0, 91.0, 38.0, 8.0),
    ("hot spring spas", "aria", "gen 2"): (87.0, 87.0, 36.0, 8.0),
    ("hot spring spas", "aria", "gen 3"): (87.0, 87.0, 36.0, 8.0),
    ("hot spring spas", "aria", "gen 3 (nxt)"): (87.0, 87.0, 36.0, 8.0),
    ("hot spring spas", "aria", "gen 4"): (87.0, 87.0, 36.0, 8.0),
    ("hot spring spas", "vanguard", "gen 1"): (87.0, 87.0, 36.0, 8.0),
    ("hot spring spas", "vanguard", "gen 2"): (87.0, 87.0, 36.0, 8.0),
    ("hot spring spas", "vanguard", "gen 3"): (87.0, 87.0, 36.0, 8.0),
    ("hot spring spas", "vanguard", "gen 3 (nxt)"): (87.0, 87.0, 36.0, 8.0),
    ("hot spring spas", "vanguard", "gen 4"): (87.0, 87.0, 36.0, 8.0),
    ("hot spring spas", "sovereign", "gen 1"): (93.0, 80.0, 33.0, 8.0),
    ("hot spring spas", "sovereign", "gen 2"): (93.0, 80.0, 33.0, 8.0),
    ("hot spring spas", "sovereign", "gen 3"): (93.0, 80.0, 33.0, 8.0),
    ("hot spring spas", "sovereign", "gen 4"): (93.0, 80.0, 33.0, 8.0),
    ("hot spring spas", "prodigy", "gen 1"): (87.0, 74.0, 33.0, 8.0),
    ("hot spring spas", "prodigy", "gen 2"): (84.0, 78.0, 33.0, 8.0),
    ("hot spring spas", "prodigy", "gen 3"): (84.0, 78.0, 33.0, 8.0),
    ("hot spring spas", "prodigy", "gen 4"): (84.0, 78.0, 33.0, 8.0),
    ("hot spring spas", "jetsetter", "gen 1"): (82.0, 62.0, 29.0, 8.0),
    ("hot spring spas", "jetsetter", "gen 2"): (84.0, 65.0, 29.0, 8.0),
    ("hot spring spas", "jetsetter", "gen 3 (nxt)"): (84.0, 65.0, 33.0, 8.0),
    ("hot spring spas", "jetsetter", "gen 4"): (84.0, 65.0, 29.0, 8.0),
    ("hot spring spas", "jetsetter lx", "gen 3"): (84.0, 68.0, 33.0, 8.0),
    ("hot spring spas", "jetsetter lx", "gen 4"): (84.0, 68.0, 33.0, 8.0),
    ("hot spring spas", "triumph", "gen 4"): (93.0, 74.0, 33.0, 8.0),
    ("hot spring spas", "prism", "gen 2"): (92.0, 92.0, 38.0, 8.0),
    ("hot spring spas", "pulse", "gen 1"): (89.0, 89.0, 38.0, 8.0),
    ("hot spring spas", "pulse", "gen 2"): (89.0, 89.0, 38.0, 8.0),
    ("hot spring spas", "flash", "gen 2"): (84.0, 84.0, 36.0, 8.0),
    ("hot spring spas", "flare", "gen 1"): (84.0, 84.0, 36.0, 8.0),
    ("hot spring spas", "flare", "gen 2"): (84.0, 84.0, 36.0, 8.0),
    ("hot spring spas", "beam", "gen 2"): (80.0, 80.0, 33.0, 8.0),
    ("hot spring spas", "beam", "gen 3"): (80.0, 80.0, 33.0, 8.0),
    ("hot spring spas", "gleam", "gen 1"): (92.0, 92.0, 38.0, 8.0),
    ("hot spring spas", "glow", "gen 1"): (76.0, 84.0, 33.0, 8.0),
    ("hot spring spas", "bolt", "gen 1"): (80.0, 80.0, 33.0, 8.0),
    ("hot spring spas", "tempo", "gen 1"): (89.0, 89.0, 38.0, 8.0),
    ("hot spring spas", "tempo", "gen 2"): (89.0, 89.0, 38.0, 8.0),
    ("hot spring spas", "relay", "gen 1"): (84.0, 84.0, 36.0, 8.0),
    ("hot spring spas", "relay", "gen 2"): (84.0, 84.0, 36.0, 8.0),
    ("hot spring spas", "rhythm", "gen 1"): (84.0, 84.0, 36.0, 8.0),
    ("hot spring spas", "rhythm", "gen 2"): (84.0, 84.0, 36.0, 8.0),
    ("hot spring spas", "stride", "gen 1"): (84.0, 65.0, 29.0, 8.0),
    ("hot spring spas", "sx", "gen 1"): (72.0, 72.0, 33.0, 8.0),
    ("hot spring spas", "sx", "gen 2"): (72.0, 72.0, 33.0, 8.0),
    ("hot spring spas", "tx", "gen 1"): (68.0, 68.0, 29.0, 0.0),
    ("hot spring spas", "tx", "gen 2"): (68.0, 68.0, 29.0, 0.0),

    # Caldera Spas
    ("caldera spas", "cantabria", "gen 1"): (108.0, 91.0, 38.0, 8.0),
    ("caldera spas", "cantabria", "gen 2"): (108.0, 91.0, 38.0, 8.0),
    ("caldera spas", "geneva", "gen 1"): (90.0, 90.0, 38.0, 8.0),
    ("caldera spas", "geneva", "gen 2"): (90.0, 90.0, 38.0, 8.0),
    ("caldera spas", "niagara", "gen 1"): (90.0, 90.0, 38.0, 8.0),
    ("caldera spas", "niagara", "gen 2"): (90.0, 90.0, 38.0, 8.0),
    ("caldera spas", "tahitian", "gen 1"): (84.0, 84.0, 36.0, 8.0),
    ("caldera spas", "tahitian", "gen 2"): (84.0, 84.0, 36.0, 8.0),
    ("caldera spas", "florence", "gen 2"): (84.0, 84.0, 36.0, 8.0),
    ("caldera spas", "provence", "gen 2"): (84.0, 66.0, 35.0, 8.0),
    ("caldera spas", "makena", "gen 1"): (89.0, 89.0, 36.0, 8.0),
    ("caldera spas", "makena", "gen 2"): (89.0, 89.0, 36.0, 8.0),
    ("caldera spas", "salina", "gen 1"): (89.0, 89.0, 36.0, 8.0),
    ("caldera spas", "salina", "gen 2"): (89.0, 89.0, 36.0, 8.0),
    ("caldera spas", "martinique", "gen 1"): (90.0, 90.0, 34.0, 8.0),
    ("caldera spas", "martinique", "gen 2"): (90.0, 90.0, 34.0, 8.0),
    ("caldera spas", "kauai", "gen 1"): (84.0, 65.0, 29.5, 8.0),
    ("caldera spas", "kauai", "gen 2"): (84.0, 65.0, 29.5, 8.0),
    ("caldera spas", "seychelles", "gen 2"): (84.0, 84.0, 36.0, 8.0),
    ("caldera spas", "reunion", "gen 2"): (84.0, 84.0, 36.0, 8.0),
    ("caldera spas", "palmetto", "gen 1"): (90.0, 90.0, 36.0, 8.0),
    ("caldera spas", "vanto", "gen 1"): (84.0, 84.0, 36.0, 8.0),
    ("caldera spas", "tarino", "gen 1"): (84.0, 84.0, 36.0, 8.0),
    ("caldera spas", "marino", "gen 1"): (84.0, 84.0, 36.0, 8.0),
    ("caldera spas", "aventine", "gen 1"): (64.0, 64.0, 29.0, 0.0),

    # Endless Pools
    ("endless pools", "original modular", "gen 1"): (168.0, 96.0, 42.0, 0.0),
    ("endless pools", "original modular", "gen 2"): (168.0, 96.0, 42.0, 0.0),
    ("endless pools", "e500", "gen 1"): (180.0, 89.0, 58.0, 8.0),
    ("endless pools", "e500", "gen 2"): (180.0, 89.0, 58.0, 8.0),
    ("endless pools", "e550", "gen 1"): (180.0, 94.0, 58.0, 8.0),
    ("endless pools", "e700", "gen 1"): (204.0, 89.0, 58.0, 8.0),
    ("endless pools", "e700", "gen 2"): (204.0, 89.0, 58.0, 8.0),
    ("endless pools", "e2000", "gen 1"): (240.0, 89.0, 58.0, 8.0),
    ("endless pools", "e2000", "gen 2"): (240.0, 89.0, 58.0, 8.0),
    ("endless pools", "x500", "gen 1"): (180.0, 89.0, 50.0, 8.0),
    ("endless pools", "x500", "gen 2"): (180.0, 89.0, 50.0, 8.0),
    ("endless pools", "x2000", "gen 1"): (240.0, 89.0, 58.0, 8.0),
    ("endless pools", "x2000", "gen 2"): (240.0, 89.0, 58.0, 8.0),
    ("endless pools", "r200", "gen 1"): (144.0, 89.0, 50.0, 8.0),
    ("endless pools", "r500", "gen 1"): (180.0, 89.0, 50.0, 8.0),

    # Freeflow Spas
    ("freeflow spas", "excursion", "gen 1"): (77.0, 77.0, 34.0, 7.0),
    ("freeflow spas", "excursion", "gen 2"): (77.0, 77.0, 34.0, 7.0),
    ("freeflow spas", "azure", "gen 1"): (80.0, 69.0, 33.0, 7.0),
    ("freeflow spas", "azure", "gen 2"): (80.0, 69.0, 33.0, 7.0),
    ("freeflow spas", "cascina", "gen 1"): (62.0, 68.0, 32.0, 7.0),
    ("freeflow spas", "tristar", "gen 1"): (70.0, 70.0, 31.0, 0.0),
    ("freeflow spas", "mini", "gen 1"): (72.0, 47.0, 29.0, 7.0),
    ("freeflow spas", "monterey", "gen 2"): (87.0, 77.0, 34.0, 7.0),

    # Lifesmart Spas
    ("lifesmart spas", "ls100", "gen 1"): (70.0, 61.0, 32.0, 7.0),
    ("lifesmart spas", "ls200", "gen 1"): (76.0, 76.0, 34.0, 38.0),
    ("lifesmart spas", "ls300", "gen 1"): (72.0, 72.0, 31.0, 0.0),
    ("lifesmart spas", "ls350", "gen 1"): (72.0, 81.0, 34.0, 7.0),
    ("lifesmart spas", "ls450", "gen 1"): (81.0, 81.0, 34.0, 7.0),
    ("lifesmart spas", "ls450", "gen 2"): (81.0, 81.0, 34.0, 7.0),
    ("lifesmart spas", "ls550", "gen 1"): (81.0, 81.0, 34.0, 7.0),
    ("lifesmart spas", "ls550", "gen 2"): (81.0, 81.0, 34.0, 7.0),
    ("lifesmart spas", "ls600", "gen 1"): (81.0, 81.0, 34.0, 7.0),
    ("lifesmart spas", "ls600", "gen 2"): (81.0, 81.0, 34.0, 7.0),
    ("lifesmart spas", "ls700", "gen 2"): (85.0, 85.0, 34.0, 7.0),
    ("lifesmart spas", "leganza", "gen 1"): (85.0, 85.0, 34.0, 7.0),
    ("lifesmart spas", "coronado", "gen 1"): (81.0, 81.0, 34.0, 7.0),

    # Tiger River Spas
    ("tiger river spas", "siberian", "gen 1"): (91.0, 91.0, 36.0, 8.0),
    ("tiger river spas", "bengal", "gen 1"): (79.0, 79.0, 33.0, 8.0),

    # Solana Spas
    ("solana spas", "tx", "gen 1"): (68.0, 68.0, 29.0, 0.0),
    ("solana spas", "sx", "gen 1"): (72.0, 72.0, 33.0, 8.0),

    # Jacuzzi
    ("jacuzzi", "j-19 powerpro", "gen 1"): (222.0, 93.0, 53.0, 10.0),
    ("jacuzzi", "j-16 powerpro", "gen 1"): (186.0, 93.0, 53.0, 10.0),
    ("jacuzzi", "j-19 poweractive", "gen 1"): (222.0, 93.0, 53.0, 10.0),
    ("jacuzzi", "j-16 poweractive", "gen 1"): (186.0, 93.0, 53.0, 10.0),
    ("jacuzzi", "j-13 powerplay", "gen 1"): (150.0, 93.0, 53.0, 10.0),
    ("jacuzzi", "j-575", "gen 1"): (91.0, 91.0, 37.5, 10.0),
    ("jacuzzi", "j-585", "gen 1"): (91.0, 91.0, 37.5, 10.0),
    ("jacuzzi", "j-495", "gen 1"): (90.0, 110.0, 37.5, 10.0),
    ("jacuzzi", "j-485", "gen 2"): (91.0, 91.0, 37.5, 10.0),
    ("jacuzzi", "j-480", "gen 1"): (91.0, 91.0, 37.5, 10.0),
    ("jacuzzi", "j-475", "gen 2"): (91.0, 91.0, 37.5, 10.0),
    ("jacuzzi", "j-470", "gen 1"): (91.0, 91.0, 37.5, 10.0),
    ("jacuzzi", "j-465", "gen 1"): (88.0, 88.0, 39.0, 10.0),
    ("jacuzzi", "j-445", "gen 2"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-435", "gen 2"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-425", "gen 1"): (76.0, 81.0, 34.0, 10.0),
    ("jacuzzi", "j-415", "gen 1"): (76.0, 66.0, 32.0, 10.0),
    ("jacuzzi", "j-385", "gen 1"): (91.0, 91.0, 38.0, 10.0),
    ("jacuzzi", "j-385", "gen 2"): (91.0, 91.0, 38.0, 10.0),
    ("jacuzzi", "j-385", "gen 3"): (91.0, 91.0, 38.0, 10.0),
    ("jacuzzi", "j-385", "gen 4"): (91.0, 91.0, 38.0, 10.0),
    ("jacuzzi", "j-375", "gen 1"): (91.0, 91.0, 38.0, 10.0),
    ("jacuzzi", "j-375", "gen 2"): (91.0, 91.0, 38.0, 10.0),
    ("jacuzzi", "j-375", "gen 3"): (91.0, 91.0, 38.0, 10.0),
    ("jacuzzi", "j-375", "gen 4"): (91.0, 91.0, 38.0, 10.0),
    ("jacuzzi", "j-365", "gen 1"): (91.0, 91.0, 38.0, 10.0),
    ("jacuzzi", "j-365", "gen 2"): (91.0, 91.0, 38.0, 10.0),
    ("jacuzzi", "j-365", "gen 3"): (91.0, 91.0, 38.0, 10.0),
    ("jacuzzi", "j-365", "gen 4"): (91.0, 91.0, 38.0, 10.0),
    ("jacuzzi", "j-355", "gen 1"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-355", "gen 2"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-355", "gen 3"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-355", "gen 4"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-345", "gen 1"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-345", "gen 2"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-345", "gen 3"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-345", "gen 4"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-335", "gen 1"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-335", "gen 2"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-335", "gen 3"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-335", "gen 4"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-315", "gen 1"): (76.0, 66.0, 32.0, 10.0),
    ("jacuzzi", "j-315", "gen 2"): (76.0, 66.0, 32.0, 10.0),
    ("jacuzzi", "j-315", "gen 3"): (76.0, 66.0, 32.0, 10.0),
    ("jacuzzi", "j-315", "gen 4"): (76.0, 66.0, 32.0, 10.0),
    ("jacuzzi", "j-280", "gen 1"): (90.0, 90.0, 36.5, 10.0),
    ("jacuzzi", "j-280", "gen 2"): (90.0, 90.0, 36.5, 10.0),
    ("jacuzzi", "j-275", "gen 1"): (90.0, 90.0, 36.5, 10.0),
    ("jacuzzi", "j-275", "gen 2"): (90.0, 90.0, 36.5, 10.0),
    ("jacuzzi", "j-245", "gen 1"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-245", "gen 2"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-235", "gen 1"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-235", "gen 2"): (84.0, 84.0, 36.0, 10.0),
    ("jacuzzi", "j-210", "gen 1"): (78.0, 78.0, 36.0, 39.0),
    ("jacuzzi", "j-210", "gen 2"): (78.0, 78.0, 36.0, 39.0),

    # Sundance Spas
    ("sundance spas", "kingston", "gen 1"): (100.0, 92.0, 34.0, 8.0),
    ("sundance spas", "claremont", "gen 1"): (100.0, 92.0, 34.0, 8.0),
    ("sundance spas", "lisbon", "gen 1"): (89.0, 89.0, 34.0, 8.0),
    ("sundance spas", "odessa", "gen 1"): (89.0, 89.0, 34.0, 8.0),
    ("sundance spas", "maxxus", "gen 1"): (110.0, 90.0, 41.5, 8.0),
    ("sundance spas", "maxxus", "gen 2"): (110.0, 90.0, 41.5, 8.0),
    ("sundance spas", "aspen", "gen 1"): (110.0, 90.0, 41.5, 8.0),
    ("sundance spas", "aspen", "gen 2"): (110.0, 90.0, 41.5, 8.0),
    ("sundance spas", "optima", "gen 1"): (89.0, 89.0, 37.5, 8.0),
    ("sundance spas", "optima", "gen 2"): (89.0, 89.0, 37.5, 8.0),
    ("sundance spas", "cameo", "gen 1"): (89.0, 89.0, 37.5, 8.0),
    ("sundance spas", "cameo", "gen 2"): (89.0, 89.0, 37.5, 8.0),
    ("sundance spas", "altamar", "gen 1"): (81.0, 86.0, 37.5, 8.0),
    ("sundance spas", "altamar", "gen 2"): (81.0, 86.0, 37.5, 8.0),
    ("sundance spas", "capri", "gen 1"): (69.0, 82.0, 30.5, 8.0),
    ("sundance spas", "capri", "gen 2"): (69.0, 82.0, 30.5, 8.0),
    ("sundance spas", "chelsee", "gen 1"): (89.0, 89.0, 36.0, 8.0),
    ("sundance spas", "chelsee", "gen 2"): (89.0, 89.0, 36.0, 8.0),
    ("sundance spas", "hamilton", "gen 1"): (89.0, 89.0, 36.0, 8.0),
    ("sundance spas", "hamilton", "gen 2"): (89.0, 89.0, 36.0, 8.0),
    ("sundance spas", "montclair", "gen 1"): (75.0, 91.0, 33.0, 8.0),
    ("sundance spas", "montclair", "gen 2"): (75.0, 91.0, 33.0, 8.0),
    ("sundance spas", "mckinley", "gen 1"): (89.0, 89.0, 36.0, 8.0),
    ("sundance spas", "mckinley", "gen 2"): (89.0, 89.0, 36.0, 8.0),
    ("sundance spas", "ramona", "gen 1"): (89.0, 89.0, 36.0, 8.0),
    ("sundance spas", "ramona", "gen 2"): (89.0, 89.0, 36.0, 8.0),
    ("sundance spas", "denali", "gen 1"): (79.0, 79.0, 36.0, 39.5),
    ("sundance spas", "denali", "gen 2"): (79.0, 79.0, 36.0, 39.5),

    # Dimension One Spas
    ("dimension one spas", "amore bay", "gen 1"): (108.0, 91.0, 40.0, 10.0),
    ("dimension one spas", "amore bay", "gen 2"): (108.0, 91.0, 40.0, 10.0),
    ("dimension one spas", "lotus bay", "gen 1"): (91.0, 91.0, 38.0, 10.0),
    ("dimension one spas", "lotus bay", "gen 2"): (91.0, 91.0, 38.0, 10.0),
    ("dimension one spas", "sarena bay", "gen 1"): (120.0, 92.0, 40.0, 10.0),
    ("dimension one spas", "sarena bay", "gen 2"): (120.0, 92.0, 40.0, 10.0),
    ("dimension one spas", "executive", "gen 1"): (92.0, 92.0, 36.0, 10.0),
    ("dimension one spas", "executive", "gen 2"): (92.0, 92.0, 36.0, 10.0),
    ("dimension one spas", "diplomat", "gen 1"): (92.0, 92.0, 36.0, 10.0),
    ("dimension one spas", "diplomat", "gen 2"): (92.0, 92.0, 36.0, 10.0),
    ("dimension one spas", "chairman", "gen 1"): (92.0, 92.0, 36.0, 10.0),
    ("dimension one spas", "chairman", "gen 2"): (92.0, 92.0, 36.0, 10.0),

    # Hydropool Hot Tubs
    ("hydropool hot tubs", "970", "gen 1"): (110.0, 91.0, 39.0, 9.0),
    ("hydropool hot tubs", "970", "gen 2"): (110.0, 91.0, 39.0, 9.0),
    ("hydropool hot tubs", "790", "gen 1"): (94.0, 94.0, 39.0, 9.0),
    ("hydropool hot tubs", "790", "gen 2"): (94.0, 94.0, 39.0, 9.0),
    ("hydropool hot tubs", "770", "gen 1"): (90.0, 90.0, 39.0, 9.0),
    ("hydropool hot tubs", "770", "gen 2"): (90.0, 90.0, 39.0, 9.0),
    ("hydropool hot tubs", "670", "gen 1"): (85.0, 85.0, 39.0, 9.0),
    ("hydropool hot tubs", "670", "gen 2"): (85.0, 85.0, 39.0, 9.0),
    ("hydropool hot tubs", "570", "gen 1"): (80.0, 80.0, 37.0, 9.0),
    ("hydropool hot tubs", "570", "gen 2"): (80.0, 80.0, 37.0, 9.0),
    ("hydropool hot tubs", "395", "gen 1"): (85.0, 65.0, 30.0, 9.0),
    ("hydropool hot tubs", "395", "gen 2"): (85.0, 65.0, 30.0, 9.0),
    ("hydropool hot tubs", "aquatrainer 19dtfx", "gen 1"): (220.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "aquatrainer 19dtfx", "gen 2"): (220.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "aquatrainer 17fx", "gen 1"): (204.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "aquatrainer 17fx", "gen 2"): (204.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "aquatrainer 14fx", "gen 1"): (168.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "aquatrainer 14fx", "gen 2"): (168.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "aquasport 19dtfx", "gen 1"): (220.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "aquasport 19dtfx", "gen 2"): (220.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "aquasport 17fx", "gen 1"): (204.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "aquasport 17fx", "gen 2"): (204.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "aquasport 14fx", "gen 1"): (168.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "aquasport 14fx", "gen 2"): (168.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "executive trainer 19ex", "gen 1"): (220.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "executive trainer 16ex", "gen 1"): (186.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "aquaplay 13ff", "gen 1"): (150.0, 93.0, 53.0, 9.0),
    ("hydropool hot tubs", "aquaplay 13ff", "gen 2"): (150.0, 93.0, 53.0, 9.0),

    # SwimLife
    ("swimlife", "swimexpert 19dt", "gen 1"): (220.0, 93.0, 53.0, 9.0),
    ("swimlife", "swimexpert 17", "gen 1"): (204.0, 93.0, 53.0, 9.0),
    ("swimlife", "swimexpert 14", "gen 1"): (168.0, 93.0, 53.0, 9.0),
    ("swimlife", "swimfit 19dt", "gen 1"): (220.0, 93.0, 53.0, 9.0),
    ("swimlife", "swimfit 17", "gen 1"): (204.0, 93.0, 53.0, 9.0),
    ("swimlife", "swimfit 14", "gen 1"): (168.0, 93.0, 53.0, 9.0),
    ("swimlife", "swimsync 12", "gen 1"): (144.0, 93.0, 53.0, 9.0),

    # Dream Maker Spas
    ("dream maker spas", "big ez", "gen 1"): (82.0, 82.0, 32.0, 41.0),
    ("dream maker spas", "big ez", "gen 2"): (82.0, 82.0, 32.0, 41.0),
    ("dream maker spas", "ez spa", "gen 1"): (79.0, 69.0, 32.0, 7.0),
    ("dream maker spas", "ez spa", "gen 2"): (79.0, 69.0, 32.0, 7.0),
    ("dream maker spas", "cabana 2500", "gen 1"): (80.0, 80.0, 34.0, 7.0),

    # ThermoSpas
    ("thermospas", "park avenue", "gen 1"): (93.0, 93.0, 38.0, 9.0),
    ("thermospas", "park avenue", "gen 2"): (93.0, 93.0, 38.0, 9.0),
    ("thermospas", "aquaciser", "gen 1"): (164.0, 90.0, 53.0, 9.0),
    ("thermospas", "aquaciser", "gen 2"): (164.0, 90.0, 53.0, 9.0),

    # Artesian Spas
    ("artesian spas", "pelican bay", "gen 1"): (108.0, 91.0, 42.0, 6.0),
    ("artesian spas", "pelican bay", "gen 2"): (108.0, 91.0, 42.0, 6.0),
    ("artesian spas", "piper glen", "gen 1"): (91.0, 91.0, 42.0, 6.0),
    ("artesian spas", "piper glen", "gen 2"): (91.0, 91.0, 42.0, 6.0),
    ("artesian spas", "grand bahama", "gen 1"): (91.0, 91.0, 36.0, 6.0),
    ("artesian spas", "grand bahama", "gen 2"): (91.0, 91.0, 36.0, 6.0),
    ("artesian spas", "grand cayman", "gen 1"): (91.0, 91.0, 36.0, 6.0),
    ("artesian spas", "grand cayman", "gen 2"): (91.0, 91.0, 36.0, 6.0),
    ("artesian spas", "965l", "gen 1"): (108.0, 91.0, 36.0, 6.0),
    ("artesian spas", "965l", "gen 2"): (108.0, 91.0, 36.0, 6.0),
    ("artesian spas", "860b", "gen 1"): (91.0, 91.0, 36.0, 6.0),
    ("artesian spas", "860b", "gen 2"): (91.0, 91.0, 36.0, 6.0),
    ("artesian spas", "active plus aep14", "gen 1"): (168.0, 92.0, 54.0, 12.0),
    ("artesian spas", "active plus aep14", "gen 2"): (168.0, 92.0, 54.0, 12.0),
    ("artesian spas", "premium trainer ep14", "gen 1"): (168.0, 92.0, 54.0, 12.0),
    ("artesian spas", "premium trainer ep14", "gen 2"): (168.0, 92.0, 54.0, 12.0),
    ("artesian spas", "premium trainer ep15", "gen 1"): (180.0, 92.0, 54.0, 12.0),
    ("artesian spas", "premium trainer ep15", "gen 2"): (180.0, 92.0, 54.0, 12.0),
    ("artesian spas", "pro trainer ep16", "gen 1"): (192.0, 92.0, 54.0, 12.0),
    ("artesian spas", "pro trainer ep16", "gen 2"): (192.0, 92.0, 54.0, 12.0),
    ("artesian spas", "dual temp dtl8", "gen 1"): (168.0, 92.0, 54.0, 12.0),
    ("artesian spas", "dual temp dtl8", "gen 2"): (168.0, 92.0, 54.0, 12.0),
    ("artesian spas", "dual temp dtl14", "gen 1"): (192.0, 92.0, 54.0, 12.0),
    ("artesian spas", "dual temp dtl14", "gen 2"): (192.0, 92.0, 54.0, 12.0),
    ("artesian spas", "dual temp dtl15", "gen 1"): (231.0, 92.0, 54.0, 12.0),
    ("artesian spas", "dual temp dtl15", "gen 2"): (231.0, 92.0, 54.0, 12.0),
    ("artesian spas", "core aquatic trainer cat12", "gen 1"): (144.0, 92.0, 45.0, 12.0),

    # Marquis Spas
    ("marquis spas", "the summit", "crown gen 1"): (94.0, 94.0, 35.0, 8.0),
    ("marquis spas", "the epic", "crown gen 1"): (90.0, 90.0, 35.0, 8.0),
    ("marquis spas", "the euphoria", "crown gen 1"): (90.0, 90.0, 35.0, 8.0),
    ("marquis spas", "v94", "vector gen 1"): (94.0, 94.0, 36.0, 8.0),
    ("marquis spas", "v94l", "vector gen 1"): (94.0, 94.0, 36.0, 8.0),
    ("marquis spas", "atv-17 sport", "gen 1"): (204.0, 90.5, 56.0, 10.0),
    ("marquis spas", "atv-17 sport", "gen 2"): (204.0, 90.5, 56.0, 10.0),
    ("marquis spas", "atv-17 kona", "gen 1"): (204.0, 90.5, 56.0, 10.0),
    ("marquis spas", "atv-17 kona", "gen 2"): (204.0, 90.5, 56.0, 10.0),
    ("marquis spas", "atv-14 sport", "gen 1"): (168.0, 90.5, 56.0, 10.0),
    ("marquis spas", "atv-14 sport", "gen 2"): (168.0, 90.5, 56.0, 10.0),
    ("marquis spas", "atv-14 splash", "gen 1"): (168.0, 90.5, 56.0, 10.0),

    # Clearwater Spas
    ("clearwater spas", "fairwood", "gen 1"): (92.5, 92.5, 38.0, 8.0),
    ("clearwater spas", "fairwood", "gen 2"): (92.5, 92.5, 38.0, 8.0),
    ("clearwater spas", "broadmoor", "gen 2"): (92.5, 92.5, 38.0, 8.0),
    ("clearwater spas", "swim 16", "gen 1"): (192.0, 90.0, 51.0, 10.0),
    ("clearwater spas", "swim 19 dual temp", "gen 1"): (228.0, 90.0, 51.0, 10.0),

    # American Whirlpool
    ("american whirlpool", "984", "steelframe gen 1"): (110.0, 90.0, 38.0, 8.5),
    ("american whirlpool", "881", "steelframe gen 1"): (92.0, 92.0, 38.0, 8.5),
    ("american whirlpool", "481", "steelframe gen 1"): (92.0, 92.0, 38.0, 8.5),
    ("american whirlpool", "dm8", "steelframe gen 1"): (216.0, 90.0, 50.0, 10.0),
    ("american whirlpool", "ml8", "steelframe gen 1"): (192.0, 90.0, 50.0, 10.0),
    ("american whirlpool", "mb4", "steelframe gen 1"): (168.0, 90.0, 50.0, 10.0),

    # Vita Spa
    ("vita spa", "mystic", "steelframe gen 1"): (110.0, 90.0, 38.0, 8.5),
    ("vita spa", "rendezvous", "steelframe gen 1"): (92.0, 92.0, 38.0, 8.5),
    ("vita spa", "vm6", "gen 1"): (216.0, 90.0, 50.0, 10.0),
    ("vita spa", "vm6", "gen 2"): (216.0, 90.0, 50.0, 10.0),
    ("vita spa", "vl4", "gen 1"): (168.0, 90.0, 50.0, 10.0),
    ("vita spa", "vl4", "gen 2"): (168.0, 90.0, 50.0, 10.0),
    ("vita spa", "xb4", "gen 1"): (144.0, 90.0, 50.0, 10.0),

    # L.A. Spas
    ("l.a. spas", "concord", "gen 1"): (92.0, 92.0, 35.0, 8.0),
    ("l.a. spas", "in-fit 16", "gen 1"): (192.0, 90.0, 53.0, 10.0),
    ("l.a. spas", "in-fit 14", "gen 1"): (168.0, 90.0, 53.0, 10.0),
    ("l.a. spas", "in-fit dual temp", "gen 1"): (216.0, 90.0, 53.0, 10.0),

    # Michael Phelps Legend
    ("michael phelps legend", "lsx 900", "gen 1"): (92.0, 92.0, 38.0, 8.5),
    ("michael phelps legend", "lsx 900", "gen 2"): (92.0, 92.0, 38.0, 8.5),
    ("michael phelps legend", "wave xp", "gen 1"): (201.0, 94.0, 60.0, 10.0),
    ("michael phelps legend", "wave xp", "gen 2"): (201.0, 94.0, 60.0, 10.0),
    ("michael phelps legend", "wave xp pro", "gen 1"): (215.0, 94.0, 60.0, 10.0),
    ("michael phelps legend", "wave xp pro", "gen 2"): (215.0, 94.0, 60.0, 10.0),
    ("michael phelps legend", "momentum 80xp", "gen 1"): (231.0, 94.0, 51.0, 10.0),
    ("michael phelps legend", "momentum 80xp", "gen 2"): (231.0, 94.0, 51.0, 10.0),
    ("michael phelps legend", "momentum deep", "gen 1"): (231.0, 94.0, 60.0, 10.0),
    ("michael phelps legend", "momentum deep", "gen 2"): (231.0, 94.0, 60.0, 10.0),
    ("michael phelps legend", "force deep", "gen 1"): (201.0, 94.0, 60.0, 10.0),
    ("michael phelps legend", "force deep", "gen 2"): (201.0, 94.0, 60.0, 10.0),

    # H2X Swim Spas
    ("h2x swim spas", "challenger 15d", "gen 1"): (180.0, 94.0, 60.0, 10.0),
    ("h2x swim spas", "challenger 15d", "gen 2"): (180.0, 94.0, 60.0, 10.0),
    ("h2x swim spas", "challenger 18d", "gen 1"): (215.0, 94.0, 60.0, 10.0),
    ("h2x swim spas", "challenger 18d", "gen 2"): (215.0, 94.0, 60.0, 10.0),
    ("h2x swim spas", "challenger 19d", "gen 1"): (231.0, 94.0, 60.0, 10.0),
    ("h2x swim spas", "challenger 19d", "gen 2"): (231.0, 94.0, 60.0, 10.0),
    ("h2x swim spas", "trainer 15", "gen 1"): (180.0, 94.0, 51.0, 10.0),
    ("h2x swim spas", "trainer 15", "gen 2"): (180.0, 94.0, 51.0, 10.0),
    ("h2x swim spas", "trainer 18", "gen 1"): (215.0, 94.0, 51.0, 10.0),
    ("h2x swim spas", "trainer 18", "gen 2"): (215.0, 94.0, 51.0, 10.0),
    ("h2x swim spas", "trainer 19", "gen 1"): (231.0, 94.0, 51.0, 10.0),
    ("h2x swim spas", "trainer 19", "gen 2"): (231.0, 94.0, 51.0, 10.0),
    ("h2x swim spas", "trainer 19d", "gen 1"): (231.0, 94.0, 60.0, 10.0),
    ("h2x swim spas", "trainer 19d", "gen 2"): (231.0, 94.0, 60.0, 10.0),
    ("h2x swim spas", "therapool se", "gen 1"): (132.0, 90.0, 51.0, 10.0),
    ("h2x swim spas", "therapool se", "gen 2"): (132.0, 90.0, 51.0, 10.0),
    ("h2x swim spas", "therapool deep", "gen 1"): (132.0, 90.0, 60.0, 10.0),
    ("h2x swim spas", "therapool deep", "gen 2"): (132.0, 90.0, 60.0, 10.0),

    # Twilight Series
    ("twilight series", "ts 8.2", "gen 1"): (94.0, 94.0, 38.0, 8.5),
    ("twilight series", "ts 8.2", "gen 2"): (94.0, 94.0, 38.0, 8.5),
    ("twilight series", "ts 8.25", "gen 1"): (94.0, 94.0, 38.0, 8.5),
    ("twilight series", "ts 8.25", "gen 2"): (94.0, 94.0, 38.0, 8.5),

    # Clarity Spas
    ("clarity spas", "balance 7", "gen 1"): (86.0, 86.0, 36.0, 8.5),
    ("clarity spas", "balance 7", "gen 2"): (86.0, 86.0, 36.0, 8.5),

    # Bullfrog Spas
    ("bullfrog spas", "m9", "enduraframe gen 1"): (110.2, 94.3, 38.0, 8.0),
    ("bullfrog spas", "m8", "enduraframe gen 1"): (94.3, 94.3, 38.0, 8.0),
    ("bullfrog spas", "a9l", "a-gen 2"): (110.0, 94.0, 38.0, 8.0),
    ("bullfrog spas", "a8", "a-gen 1"): (94.0, 94.0, 38.0, 8.0),
    ("bullfrog spas", "a8", "a-gen 2"): (94.0, 94.0, 38.0, 8.0),
    ("bullfrog spas", "a8l", "a-gen 1"): (94.0, 94.0, 38.0, 8.0),
    ("bullfrog spas", "a8l", "a-gen 2"): (94.0, 94.0, 38.0, 8.0),
    ("bullfrog spas", "stil7", "stil gen 1"): (88.1, 84.1, 34.0, 5.0),

    # Beachcomber
    ("beachcomber", "750", "gen 1"): (89.0, 89.0, 38.0, 6.0),
    ("beachcomber", "750", "gen 2"): (89.0, 89.0, 38.0, 6.0),
    ("beachcomber", "740", "gen 1"): (89.0, 89.0, 38.0, 6.0),
    ("beachcomber", "740", "gen 2"): (89.0, 89.0, 38.0, 6.0),
    ("beachcomber", "580", "gen 1"): (89.0, 89.0, 38.0, 6.0),
    ("beachcomber", "580", "gen 2"): (89.0, 89.0, 38.0, 6.0),
    ("beachcomber", "380", "gen 1"): (89.0, 89.0, 38.0, 6.0),
    ("beachcomber", "380", "gen 2"): (89.0, 89.0, 38.0, 6.0),

    # Arctic Spas
    ("arctic spas", "summit", "gen 1"): (93.0, 93.0, 39.0, 8.0),
    ("arctic spas", "summit", "gen 2"): (93.0, 93.0, 39.0, 8.0),
    ("arctic spas", "kodiak", "gen 1"): (93.0, 93.0, 39.0, 8.0),
    ("arctic spas", "kodiak", "gen 2"): (93.0, 93.0, 39.0, 8.0),
    ("arctic spas", "ocean", "gen 1"): (169.0, 93.0, 51.0, 10.0),
    ("arctic spas", "ocean", "gen 2"): (169.0, 93.0, 51.0, 10.0),
    ("arctic spas", "wolverine", "gen 1"): (204.0, 93.0, 51.0, 10.0),
    ("arctic spas", "wolverine", "gen 2"): (204.0, 93.0, 51.0, 10.0),
    ("arctic spas", "kingfisher", "gen 1"): (174.0, 93.0, 51.0, 10.0),
    ("arctic spas", "beaufort", "gen 1"): (174.0, 93.0, 51.0, 10.0),
    ("arctic spas", "hudson", "gen 1"): (204.0, 93.0, 51.0, 10.0),

    # Coast Spas
    ("coast spas", "cascade ii", "infinity gen 1"): (92.0, 101.0, 40.0, 8.0),
    ("coast spas", "cascade ii", "infinity gen 2"): (92.0, 101.0, 40.0, 8.0),
    ("coast spas", "apex", "curve gen 1"): (90.0, 90.0, 40.0, 8.0),
    ("coast spas", "apex", "curve gen 2"): (90.0, 90.0, 40.0, 8.0),
    ("coast spas", "cascade 1300", "infinity gen 1"): (154.0, 90.0, 53.0, 10.0),
    ("coast spas", "cascade 1300", "infinity gen 2"): (154.0, 90.0, 53.0, 10.0),
    ("coast spas", "cascade 1600", "infinity gen 1"): (190.0, 90.0, 53.0, 10.0),
    ("coast spas", "cascade 1600", "infinity gen 2"): (190.0, 90.0, 53.0, 10.0),
    ("coast spas", "cascade 2100", "infinity gen 1"): (250.0, 90.0, 53.0, 10.0),
    ("coast spas", "cascade 2100", "infinity gen 2"): (250.0, 90.0, 53.0, 10.0),
    ("coast spas", "seaview", "gen 1"): (168.0, 90.0, 53.0, 10.0),
    ("coast spas", "playland", "gen 1"): (144.0, 90.0, 53.0, 10.0),

    # InnovaSpa
    ("innovaspa", "storm", "monocoque gen 1"): (84.0, 72.0, 34.0, 6.0),
    ("innovaspa", "storm", "monocoque gen 2"): (84.0, 72.0, 34.0, 6.0),
    ("innovaspa", "urbania", "monocoque gen 1"): (80.0, 80.0, 34.0, 6.0),
    ("innovaspa", "urbania", "monocoque gen 2"): (80.0, 80.0, 34.0, 6.0),
    ("innovaspa", "spa-o", "monocoque gen 1"): (80.0, 80.0, 34.0, 40.0),
    ("innovaspa", "spa-o", "monocoque gen 2"): (80.0, 80.0, 34.0, 40.0),

    # Canadian Spa Co
    ("canadian spa co", "toronto", "gen 1"): (84.0, 84.0, 34.0, 8.0),
    ("canadian spa co", "toronto", "gen 2"): (84.0, 84.0, 34.0, 8.0),
    ("canadian spa co", "winnipeg", "gen 1"): (79.0, 79.0, 32.0, 8.0),
    ("canadian spa co", "winnipeg", "gen 2"): (79.0, 79.0, 32.0, 8.0),
    ("canadian spa co", "st. lawrence 20ft", "gen 1"): (238.0, 90.0, 54.0, 10.0),
    ("canadian spa co", "st. lawrence 20ft", "gen 2"): (238.0, 90.0, 54.0, 10.0),
    ("canadian spa co", "st. lawrence 16ft", "gen 1"): (198.0, 90.0, 54.0, 10.0),
    ("canadian spa co", "st. lawrence 16ft", "gen 2"): (198.0, 90.0, 54.0, 10.0),
    ("canadian spa co", "st. lawrence 13ft", "gen 1"): (154.0, 90.0, 54.0, 10.0),
    ("canadian spa co", "st. lawrence 13ft", "gen 2"): (154.0, 90.0, 54.0, 10.0),

    # Cal Spas
    ("cal spas", "ec-864l", "escape gen 1"): (93.0, 93.0, 40.5, 8.0),
    ("cal spas", "ec-864l", "escape gen 2"): (93.0, 93.0, 40.5, 8.0),
    ("cal spas", "f-1681 olympian", "gen 1"): (200.0, 93.0, 51.0, 10.0),
    ("cal spas", "f-1681 olympian", "gen 2"): (200.0, 93.0, 51.0, 10.0),
    ("cal spas", "f-1420 champion", "gen 1"): (168.0, 93.0, 51.0, 10.0),
    ("cal spas", "f-1420 champion", "gen 2"): (168.0, 93.0, 51.0, 10.0),
    ("cal spas", "f-1222 freestyle", "gen 1"): (141.0, 93.0, 51.0, 10.0),
    ("cal spas", "f-1222 freestyle", "gen 2"): (141.0, 93.0, 51.0, 10.0),
    ("cal spas", "f-1770 dual zone", "gen 1"): (209.0, 93.0, 51.0, 10.0),

    # Nordic Hot Tubs
    ("nordic hot tubs", "sport edition", "classic gen 1"): (78.0, 78.0, 35.0, 39.0),
    ("nordic hot tubs", "sport edition", "classic gen 2"): (78.0, 78.0, 35.0, 39.0),
    ("nordic hot tubs", "impulse", "classic gen 1"): (78.0, 78.0, 31.0, 39.0),
    ("nordic hot tubs", "impulse", "classic gen 2"): (78.0, 78.0, 31.0, 39.0),

    # Strong Spas
    ("strong spas", "sl60", "dura-shield gen 1"): (85.0, 85.0, 36.0, 9.0),
    ("strong spas", "s50", "dura-shield gen 1"): (85.0, 85.0, 36.0, 9.0),

    # Viking Spas
    ("viking spas", "viking i", "soft-touch gen 1"): (72.0, 72.0, 34.0, 36.0),
    ("viking spas", "royale", "soft-touch gen 1"): (78.0, 78.0, 34.0, 8.0),
    ("viking spas", "royale", "soft-touch gen 2"): (78.0, 78.0, 34.0, 8.0),

    # PDC Spas
    ("pdc spas", "biscayne", "luxury gen 1"): (84.0, 84.0, 34.0, 6.0),
    ("pdc spas", "biscayne", "luxury gen 2"): (84.0, 84.0, 34.0, 6.0),
    ("pdc spas", "tsx219", "truswim gen 1"): (227.0, 92.0, 56.0, 10.0),
    ("pdc spas", "tsx219", "truswim gen 2"): (227.0, 92.0, 56.0, 10.0),
    ("pdc spas", "ts19", "truswim gen 1"): (227.0, 92.0, 56.0, 10.0),
    ("pdc spas", "ts19", "truswim gen 2"): (227.0, 92.0, 56.0, 10.0),
    ("pdc spas", "ts17", "truswim gen 1"): (204.0, 92.0, 56.0, 10.0),
    ("pdc spas", "ts17", "truswim gen 2"): (204.0, 92.0, 56.0, 10.0),
    ("pdc spas", "ts15", "truswim gen 1"): (180.0, 92.0, 56.0, 10.0),
    ("pdc spas", "ts15", "truswim gen 2"): (180.0, 92.0, 56.0, 10.0),
    ("pdc spas", "fx219", "gen 1"): (227.0, 92.0, 56.0, 10.0),
    ("pdc spas", "fx219", "gen 2"): (227.0, 92.0, 56.0, 10.0),
    ("pdc spas", "fx17", "gen 1"): (204.0, 92.0, 56.0, 10.0),
    ("pdc spas", "fx17", "gen 2"): (204.0, 92.0, 56.0, 10.0),
    ("pdc spas", "fx15", "gen 1"): (180.0, 92.0, 56.0, 10.0),
    ("pdc spas", "fx15", "gen 2"): (180.0, 92.0, 56.0, 10.0),

    # Catalina Spas
    ("catalina spas", "olympic 16", "gen 1"): (192.0, 90.0, 50.0, 10.0),
    ("catalina spas", "olympic 16", "gen 2"): (192.0, 90.0, 50.0, 10.0),
    ("catalina spas", "nautilus 14", "gen 1"): (168.0, 90.0, 50.0, 10.0),
    ("catalina spas", "nautilus 14", "gen 2"): (168.0, 90.0, 50.0, 10.0),
    ("catalina spas", "regatta 18 dual temp", "gen 1"): (216.0, 90.0, 54.0, 10.0),
    ("catalina spas", "regatta 18 dual temp", "gen 2"): (216.0, 90.0, 54.0, 10.0),

    # Wellis
    ("wellis", "olympus", "peak gen 1"): (139.4, 110.2, 38.2, 8.0),
    ("wellis", "olympus", "peak gen 2"): (139.4, 110.2, 38.2, 8.0),
    ("wellis", "kilimanjaro", "peak gen 1"): (90.6, 90.6, 37.0, 8.0),
    ("wellis", "kilimanjaro", "peak gen 2"): (90.6, 90.6, 37.0, 8.0),
    ("wellis", "rio grande", "gen 1"): (231.1, 90.6, 59.1, 10.0),
    ("wellis", "rio grande", "gen 2"): (231.1, 90.6, 59.1, 10.0),
    ("wellis", "danube", "gen 1"): (177.2, 90.6, 59.1, 10.0),
    ("wellis", "danube", "gen 2"): (177.2, 90.6, 59.1, 10.0),
    ("wellis", "amazon", "gen 1"): (215.0, 90.6, 59.1, 10.0),
    ("wellis", "amazon", "gen 2"): (215.0, 90.6, 59.1, 10.0),
    ("wellis", "volga", "gen 1"): (157.5, 90.6, 59.1, 10.0),

    # USSPA
    ("usspa", "xl swim spa", "gen 1"): (216.5, 98.4, 52.8, 10.0),
    ("usspa", "xl swim spa", "gen 2"): (216.5, 98.4, 52.8, 10.0),
    ("usspa", "classic swim spa", "gen 1"): (177.2, 93.7, 48.8, 10.0),
    ("usspa", "classic swim spa", "gen 2"): (177.2, 93.7, 48.8, 10.0),
    ("usspa", "in swim spa lounge", "gen 1"): (208.7, 94.5, 52.4, 10.0),

    # Tuff Spas
    ("tuff spas", "swim trainer 13", "gen 1"): (156.0, 88.0, 48.0, 10.0),

    # Emerald Spas
    ("emerald spas", "manor", "gen 1"): (90.0, 90.0, 37.0, 8.0),
    ("emerald spas", "castle", "gen 1"): (85.0, 85.0, 36.0, 8.0),

    # Great Lakes Spas
    ("great lakes spas", "gl8", "gen 1"): (88.0, 88.0, 36.0, 8.0),
    ("great lakes spas", "gl7", "gen 1"): (84.0, 84.0, 36.0, 8.0),

    # Pacific Spas
    ("pacific spas", "seabreeze", "gen 1"): (84.0, 84.0, 36.0, 8.0),
    ("pacific spas", "oasis", "gen 1"): (89.0, 89.0, 36.0, 8.0),
}

# Process each row
results = []
unmatched = []

for r in rows:
    b = r['Marque'].strip()
    m = r['Modele'].strip()
    sm = r['Sous_Modele_ou_Version'].strip()
    gen = r['Generation'].strip()
    an = r['Annees_Production'].strip()
    
    # 1. Try explicit specs map first
    key = (b.lower(), m.lower(), gen.lower())
    spec = EXPLICIT_SPECS.get(key)
    
    # Try fuzzy key
    if not spec:
        for (eb, em, egen), v in EXPLICIT_SPECS.items():
            if eb == b.lower() and (em == m.lower() or em in m.lower() or m.lower() in em):
                if egen == gen.lower() or egen in gen.lower():
                    spec = v
                    break
    if not spec:
        for (eb, em, egen), v in EXPLICIT_SPECS.items():
            if eb == b.lower() and (em == m.lower() or em in m.lower() or m.lower() in em):
                spec = v
                break

    # If still not found, search master index
    if not spec:
        slug = brand_aliases.get(b.lower(), norm(b))
        m_clean = norm(m)
        cand = master_by_slug_model.get((slug, m_clean))
        if cand:
            c = cand[0]
            spec = (c['length_in'], c['width_in'], c['height_in'], c.get('corner_radius_in', 8.0))
        else:
            # Try partial matching on master index for this slug
            for (eslug, em), elist in master_by_slug_model.items():
                if eslug == slug and (m_clean in em or em in m_clean):
                    c = elist[0]
                    spec = (c['length_in'], c['width_in'], c['height_in'], c.get('corner_radius_in', 8.0))
                    break

    if spec:
        l_in, w_in, h_in, r_in = spec
        l_cm = round(l_in * 2.54, 1)
        w_cm = round(w_in * 2.54, 1)
        h_cm = round(h_in * 2.54, 1)
        r_cm = round(r_in * 2.54, 1) if r_in > 0 else 0.0
        
        dim_in_str = f'{l_in:.1f}" × {w_in:.1f}" × {h_in:.1f}"'
        if r_in > 0:
            dim_in_str += f' (R: {r_in:.1f}")'
            
        dim_cm_str = f'{l_cm:.1f} × {w_cm:.1f} × {h_cm:.1f} cm'
        if r_cm > 0:
            dim_cm_str += f' (R: {r_cm:.1f} cm)'
            
        row_out = dict(r)
        row_out['Dimensions_Pouces'] = dim_in_str
        row_out['Dimensions_Centimetres'] = dim_cm_str
        row_out['Longueur_po'] = f"{l_in:.1f}"
        row_out['Largeur_po'] = f"{w_in:.1f}"
        row_out['Hauteur_po'] = f"{h_in:.1f}"
        row_out['Rayon_Coin_po'] = f"{r_in:.1f}"
        row_out['Longueur_cm'] = f"{l_cm:.1f}"
        row_out['Largeur_cm'] = f"{w_cm:.1f}"
        row_out['Hauteur_cm'] = f"{h_cm:.1f}"
        row_out['Rayon_Coin_cm'] = f"{r_cm:.1f}"
        results.append(row_out)
    else:
        unmatched.append(r)

print(f"Successfully processed: {len(results)} / {len(rows)}")
print(f"Unmatched count: {len(unmatched)}")
if unmatched:
    for u in unmatched:
        print("MISSING:", u)
else:
    # Save the resulting CSV file
    fieldnames = list(rows[0].keys()) + [
        'Dimensions_Pouces', 'Dimensions_Centimetres',
        'Longueur_po', 'Largeur_po', 'Hauteur_po', 'Rayon_Coin_po',
        'Longueur_cm', 'Largeur_cm', 'Hauteur_cm', 'Rayon_Coin_cm'
    ]
    with open(output_csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(results)
    print(f"CSV saved to {output_csv_path}")
