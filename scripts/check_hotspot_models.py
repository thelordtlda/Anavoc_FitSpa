import requests
import re

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}
for m in ['propel', 'strobe', 'tempo']:
    url = f'https://www.hotspring.com/shop/hot-spot/{m}'
    r = requests.get(url, headers=headers, timeout=10)
    print(m, 'status:', r.status_code)
    if r.status_code == 200:
        all_imgs = re.findall(r'https?://[^\s"\'<>]+\.(?:png|jpg|jpeg|webp)', r.text)
        overheads = [c for c in set(all_imgs) if 'overhead' in c.lower() or 'top' in c.lower()]
        for o in overheads[:5]:
            print(" ", o)
