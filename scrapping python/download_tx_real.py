import urllib.request
from PIL import Image
from pathlib import Path

url = "https://www.hotspring.com/wp-content/uploads/2025/04/tx-a-spot-overhead-2025.jpg"
out_p = Path("D:/SPAFIT/Cover Sizer/scrapping python/test_tx_real.jpg")
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = resp.read()

out_p.write_bytes(data)
img = Image.open(out_p)
print(f"Downloaded TX real overhead: {img.size}, format={img.format}, bytes={len(data)}")
