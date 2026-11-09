import urllib.request
import json
import time

def get_wayback_url(target_url, timestamp):
    api = f"https://archive.org/wayback/available?url={urllib.request.quote(target_url)}&timestamp={timestamp}"
    req = urllib.request.Request(api, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.load(resp)
            snaps = data.get('archived_snapshots', {})
            closest = snaps.get('closest')
            if closest and closest.get('available'):
                return closest.get('url')
            return None
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            time.sleep(2 * (attempt + 1))
    return None

test_targets = [
    ("http://www.hotspring.com/shop-hot-tub-models/limelight/4-person-hot-tub-glow", "20150601"),
    ("http://www.hotspring.com/shop-hot-tub-models/limelight/4-person-hot-tub-bolt", "20150601"),
    ("http://www.hotspring.com/shop-hot-tub-models/highlife/7-person-large-hot-tubs-grandee", "20150601"),
    ("http://www.hotspring.com/shop-hot-tub-models/nxt/grandee-nxt", "20150601")
]

for t_url, ts in test_targets:
    print(f"\nChecking Wayback snapshot for {t_url.split('/')[-1]} at {ts}...")
    wb_url = get_wayback_url(t_url, ts)
    print(f"  Result: {wb_url}")
    time.sleep(1)
