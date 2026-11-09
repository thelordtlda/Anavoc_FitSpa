import requests
from bs4 import BeautifulSoup
import re

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}

url = "https://www.welshhottubs.co.uk/user-manuals/"
r = requests.get(url, headers=headers, timeout=15)
print("Status:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")
for a in soup.find_all("a", href=True):
    href = a["href"].strip()
    text = a.get_text(strip=True)
    if ".pdf" in href.lower() or any(k in href.lower() for k in ["whirlpool", "maax"]):
        print(f"{text} -> {href}")
