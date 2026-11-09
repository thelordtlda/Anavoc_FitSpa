import json
from pathlib import Path

user_raw_list = [
    'American Whirlpool', 'Aqua-Living', 'Aquaterra Spas', 'Aquatica', 'Arctic Spas',
    'Artesian Elite', 'Artesian Garden Spas', 'Artesian Island Spa', 'Artesian Island Spa Elite',
    'Artesian South Seas', 'Artesian Spas', 'Asgard', 'Aspen', 'Barefoot', 'Beachcomber',
    'BeWell', 'Bullfrog', 'Bullfrog ', 'Cal Spas', 'Caldera', 'Cantabria', 'Catalina',
    'Coast Spa', 'Coast Spas', 'Dimension One Spas', 'Dr. Wellness', 'Dream Maker',
    'Dynasty Spas', 'Evolution Spas', 'Fisher Spas', 'Four Winds Spas', 'Garden Leisure',
    'Glacier spas', 'HotSpring', 'Hydropool', 'Hydropool ', 'HydroTher', 'Integrity Spas',
    'Jacuzzi', 'Just Spas', 'MAAX Spas', 'Marquis', 'Marquise', 'Master Spas',
    'Mira Hot Tubs', 'Multi', 'Northern Bay', 'Passion Spa', 'PDC Spas', 'Platinum Spas',
    'Premier Outdoor Spas', 'Premium Leisure', 'Premium Leisure Go Spas', 'Riptide',
    'Royal Spa', 'Saratoga Spas', 'Saundance', 'Shorline', 'Signature Spas Platinum',
    'Signature Swim Spas', 'Spa Alina', 'Sparelax', 'Strong Spas', 'Sundance', 'Sundance ',
    'Sunrans Chineese', 'Swim Spa', 'Swim Spa Int\'l', 'Swim spa Plus', 'Swim Spa solutions',
    'Swim Spas Denver', 'SwimLife swim spas', 'Tahiti Elite', 'Tendance & Spa', 'ThermoSpas',
    'TidalFit', 'Treesse', 'Trevi', 'Trévi', 'Trevi ', 'Tropical Seas Spas', 'Vita Spa',
    'Vortex', 'Water Day - Spa', 'WELLIS', 'Wellis', 'World of Spa', 'Beach Collection',
    'Palmbeach Collection', 'Daytona Beach Collection', 'TT', 'ZEN', 'Celebrity Elite',
    'Celebrity Standard', 'Crown', 'Premium', 'Vector', 'Eternity'
]

index_path = Path("D:/SPAFIT/Cover Sizer/scrapping python/dataset/spa_master_index.json")
with open(index_path, "r", encoding="utf-8") as f:
    data = json.load(f)

dataset_brands = set(x["brand"] for x in data)

missing = [b for b in user_raw_list if b not in dataset_brands]

print(f"Total entries in user list: {len(user_raw_list)}")
print(f"Distinct brand keys in dataset: {len(dataset_brands)}")
print(f"Missing count: {len(missing)}")
if missing:
    print("Missing:", missing)
else:
    print("RESULT: 100% OF THE 98 USER-REQUESTED ENTRIES ARE PRESENT AND VERIFIED IN THE DATASET!")

swim_count = sum(1 for x in data if "swim" in x.get("spafit_notes", "").lower() or "swim" in x.get("series", "").lower() or "swim" in x.get("model", "").lower())
print(f"Total records in dataset: {len(data)}")
print(f"  - Hot Tubs: {len(data) - swim_count}")
print(f"  - Swim Spas: {swim_count}")
