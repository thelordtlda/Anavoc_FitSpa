#!/usr/bin/env python3
"""
simulate_git_scope.py
Simulates what git would track when given our standard .gitignore rules,
measures total size, and counts remaining occurrences of 'spafit'.
"""

import os
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

IGNORE_DIRS = {
    '.venv', 'temp', '_ARCHIVE', 'temp_test', '__pycache__', '.git', 'cache',
    'checkpoints', '_SPAFIT_CAD', 'scrapping_legacy', 'redundant_assets'
}

IGNORE_FILES = {
    'assets.zip', 'Cover Sizer.rar'
}

TEXT_EXTENSIONS = {
    '.js', '.html', '.css', '.json', '.csv', '.md', '.py', '.txt', '.yaml', '.yml'
}

def simulate():
    tracked = []
    total_bytes = 0
    over_50mb = []
    over_100mb = []
    spafit_occurrences = {}

    for dirpath, dirnames, filenames in os.walk(ROOT):
        # Prune ignored directory trees
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS]

        rel_dir = os.path.relpath(dirpath, ROOT)

        for f in filenames:
            if f in IGNORE_FILES or f.endswith(('.zip', '.rar', '.7z', '.STEP', '.step', '.stp')):
                continue

            fp = os.path.join(dirpath, f)
            rel_fp = os.path.join(rel_dir, f) if rel_dir != '.' else f
            try:
                sz = os.path.getsize(fp)
                total_bytes += sz
                tracked.append((rel_fp, sz))
                if sz > 100 * 1024 * 1024:
                    over_100mb.append((rel_fp, sz / (1024 * 1024)))
                elif sz > 50 * 1024 * 1024:
                    over_50mb.append((rel_fp, sz / (1024 * 1024)))

                ext = os.path.splitext(f)[1].lower()
                if ext in TEXT_EXTENSIONS:
                    with open(fp, 'r', encoding='utf-8', errors='ignore') as fh:
                        txt = fh.read()
                    matches = len(re.findall(r'spafit', txt, re.IGNORECASE))
                    if matches > 0:
                        spafit_occurrences[rel_fp] = matches
            except Exception as e:
                pass

    print("=" * 80)
    print("           SIMULATION DE LA PORTÉE DU DÉPÔT GIT AVEC .GITIGNORE")
    print("=" * 80)
    print(f"Fichiers inclus dans Git           : {len(tracked)}")
    print(f"Poids total sur disque             : {total_bytes / (1024*1024):.2f} Mo ({total_bytes / (1024*1024*1024):.2f} Go)")
    print(f"Fichiers bloquants (> 100 Mo)      : {len(over_100mb)}")
    for f, sz in over_100mb:
        print(f"  ❌ {f} ({sz:.2f} Mo)")
    print(f"Fichiers avec alerte GitHub (> 50 Mo): {len(over_50mb)}")
    for f, sz in over_50mb:
        print(f"  ⚠️ {f} ({sz:.2f} Mo)")

    print(f"\nFichiers contenant le mot 'SPAFIT' : {len(spafit_occurrences)} fichiers")
    print(f"Total des mentions 'SPAFIT'        : {sum(spafit_occurrences.values())}")
    for f, c in sorted(spafit_occurrences.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"  - {f:50} : {c:5d} mentions")
    if len(spafit_occurrences) > 15:
        print(f"  ... et {len(spafit_occurrences) - 15} autres fichiers.")

if __name__ == '__main__':
    simulate()
