import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"
}

r = requests.get("https://www.maaxspas.com/new-brands-page/", headers=headers, timeout=15)
soup = BeautifulSoup(r.text, "html.parser")
print("Status:", r.status_code)
for a in soup.find_all("a", href=True):
    print("  ", a.get_text(strip=True), "->", a["href"])
