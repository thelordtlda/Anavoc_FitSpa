import urllib.request
import urllib.parse
import zipfile
import io
from pathlib import Path

base_dir = Path(__file__).resolve().parent
hs_dir = base_dir / "dataset" / "hot_spring_spas"

glow_zips = [
    (2014, "https://s3.amazonaws.com/prod-hotspring/dimensions/2014/2014%20GLOW.ZIP"),
    (2015, "https://s3.amazonaws.com/prod-hotspring/dimensions/2015/2015%20GLOW.ZIP"),
    (2016, "https://s3.amazonaws.com/prod-hotspring/dimensions/2016/2016%20GLOW.ZIP"),
    (2010, "https://s3.amazonaws.com/prod-hotspring/dimensions/2010/hotspring_spa_renderings_glow_2010.zip"),
    (2011, "https://s3.amazonaws.com/prod-hotspring/dimensions/2011/hotspring_spa_renderings_glow_2011.zip"),
    (2018, "https://s3.amazonaws.com/prod-hotspring/dimensions/2018/limelight-glow-2018-spa-rendering.zip"),
]

for yr, url in glow_zips:
    target_dir = hs_dir / str(yr) / f"hot_spring_glow_{yr}"
    target_dir.mkdir(parents=True, exist_ok=True)
    out_dwg = target_dir / "cad_model.dwg"
    out_dxf = target_dir / "cad_model.dxf"
    
    print(f"Trying {yr} from {url}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = resp.read()
        print(f"  Downloaded {len(data)} bytes")
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            names = z.namelist()
            print(f"  Contents: {names}")
            dwgs = [n for n in names if n.lower().endswith(('.dwg', '.dxf'))]
            if dwgs:
                chosen = dwgs[0]
                ext = ".dwg" if chosen.lower().endswith('.dwg') else ".dxf"
                with z.open(chosen) as zf, open(target_dir / f"cad_model{ext}", "wb") as f_out:
                    f_out.write(zf.read())
                print(f"  EXTRACTED cad_model{ext} for Glow {yr}!")
    except Exception as e:
        print(f"  Failed: {e}")
