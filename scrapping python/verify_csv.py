import csv

output_csv_path = r'd:/SPAFIT/Cover Sizer/scrapping python/dataset/base_de_donnees_spas_avec_dimensions.csv'
with open(output_csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    header = next(reader)
    print("Header fields:", header)
    rows = list(reader)
    print(f"Total data rows: {len(rows)}")
    print("\n--- First 5 rows ---")
    for r in rows[:5]:
        print(f"{r[1]} | {r[5]} | {r[6]} | {r[7]} | {r[10]} | {r[11]}")
    print("\n--- Sample mid rows ---")
    for r in rows[200:205]:
        print(f"{r[1]} | {r[5]} | {r[6]} | {r[7]} | {r[10]} | {r[11]}")
    print("\n--- Last 5 rows ---")
    for r in rows[-5:]:
        print(f"{r[1]} | {r[5]} | {r[6]} | {r[7]} | {r[10]} | {r[11]}")
