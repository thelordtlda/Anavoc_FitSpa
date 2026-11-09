import urllib.request
import re
from bs4 import BeautifulSoup
from collections import defaultdict

HEADERS = {'User-Agent': 'Mozilla/5.0'}
url = "https://www.hotspring.com/learning-center/hot-tubs-sizes-and-renderings"
req = urllib.request.Request(url, headers=HEADERS)
with urllib.request.urlopen(req, timeout=30) as resp:
    html = resp.read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')

# Look for accordion or tab containers
# In Elementor, tabs have title and content
tab_titles = soup.find_all('div', class_=re.compile(r'tab-title|accordion-item|elementor-tab-title'))
print(f"Found {len(tab_titles)} tab titles")

all_a = soup.find_all('a', href=True)
print(f"Total links on page: {len(all_a)}")

# Group links by year pattern in URL or text
by_year = defaultdict(list)
for a in all_a:
    href = a['href']
    txt = a.get_text(strip=True)
    # find year 2000-2026
    m = re.search(r'20(0[2-9]|1[0-9]|2[0-6])', href)
    if not m:
        m = re.search(r'20(0[2-9]|1[0-9]|2[0-6])', txt)
    if m:
        yr = m.group(0)
        by_year[yr].append((txt, href))

for yr in sorted(by_year.keys()):
    print(f"\n=== Year {yr} ({len(by_year[yr])} links) ===")
    for t, h in by_year[yr][:6]:
        print(f"  [{t}] {h}")
    if len(by_year[yr]) > 6:
        print(f"  ... and {len(by_year[yr]) - 6} more")
