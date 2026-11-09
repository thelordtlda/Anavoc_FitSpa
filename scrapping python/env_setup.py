#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module A : env_setup.py
Configuration et installation des dépendances du pipeline de scraping et extraction de spas.
"""

import sys
import subprocess
import os
from pathlib import Path

REQUIRED_PACKAGES = [
    "requests",
    "beautifulsoup4",
    "playwright",
    "pypdf",
    "pymupdf",
    "pillow",
    "opencv-python",
    "pydantic"
]

def get_target_python():
    """Détermine l'exécutable Python à utiliser (.venv local ou c:\\python314\\python.exe)."""
    script_dir = Path(__file__).resolve().parent
    venv_python = script_dir / ".venv" / "Scripts" / "python.exe"
    
    if venv_python.exists():
        return str(venv_python)
    if os.path.exists(r"c:\python314\python.exe"):
        return r"c:\python314\python.exe"
    return sys.executable

def install_packages(python_exe: str):
    print(f"[SETUP] Utilisation de l'exécutable Python : {python_exe}")
    
    # 1. Mise à jour de pip
    print("[SETUP] Mise à niveau de pip...")
    subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], check=False)
    
    # 2. Installation des packages requis
    print(f"[SETUP] Installation des packages requis : {', '.join(REQUIRED_PACKAGES)}")
    cmd = [python_exe, "-m", "pip", "install"] + REQUIRED_PACKAGES
    res = subprocess.run(cmd, check=True)
    if res.returncode == 0:
        print("[SETUP] Packages installés avec succès.")
    else:
        print(f"[ERREUR] Échec de l'installation des packages (code {res.returncode})")
        sys.exit(res.returncode)

    # 3. Installation des navigateurs Playwright (Chromium)
    print("[SETUP] Installation du navigateur Chromium pour Playwright...")
    try:
        pw_res = subprocess.run([python_exe, "-m", "playwright", "install", "chromium"], check=True)
        if pw_res.returncode == 0:
            print("[SETUP] Playwright Chromium installé avec succès.")
    except Exception as e:
        print(f"[AVERTISSEMENT] Erreur lors de playwright install chromium : {e}")

    # 4. Vérification finale des imports
    print("[SETUP] Vérification des modules installés...")
    test_code = """
import requests
import bs4
import fitz
import PIL
import cv2
import pydantic
import pypdf
import playwright
print("Tous les modules ont été importés avec succès !")
"""
    verify_res = subprocess.run([python_exe, "-c", test_code], capture_output=True, text=True)
    print(verify_res.stdout)
    if verify_res.stderr:
        print(f"[STDERR]: {verify_res.stderr}")

if __name__ == "__main__":
    py_target = get_target_python()
    install_packages(py_target)
