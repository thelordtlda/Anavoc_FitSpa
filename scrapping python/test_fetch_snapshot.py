import requests

# Test fetching a snapshot page
snapshot_url = "https://web.archive.org/web/20150516151035/http://www.hotspring.com/hot-tub-models"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}
try:
    r = requests.get(snapshot_url, headers=headers, timeout=20)
    print(f"Status code: {r.status_code}, Length: {len(r.text)}")
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')
    print(f"Total img tags: {len(images)}")
    for img in images:
        src = img.get('src', '')
        if any(k in src.lower() for k in ['spa', 'overhead', 'hero', 'model']):
            print(" ", src)
except Exception as e:
    print(f"Error: {e}")
