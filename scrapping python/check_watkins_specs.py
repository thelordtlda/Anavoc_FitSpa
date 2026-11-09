from pathlib import Path

f = Path("D:/SPAFIT/Cover Sizer/scrapping python/builders_watkins.py")
if f.exists():
    text = f.read_text(encoding='utf-8')
    # search for glow and other models
    for line in text.splitlines():
        if any(k in line.lower() for k in ['glow', 'bolt', 'grandee', 'envoy', 'aria', 'sovereign', 'prodigy', 'jetsetter', 'vanguard', 'flair', 'pulse', 'gleam', 'flash', 'beam', 'pace', 'rhythm', 'relay', 'stride', 'sx', 'tx']):
            print(line[:120])
