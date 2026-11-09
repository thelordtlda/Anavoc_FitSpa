import urllib.request

url = "https://web.archive.org/web/20150516151039im_/http://www.hotspring.com/sites/default/files/images/spas/overhead/glow-jet-overhead.png"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()
    print(f"Downloaded glow overhead with im_: {len(data)} bytes, status={resp.status}")
except Exception as e:
    print(f"Error: {e}")
