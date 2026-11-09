import urllib.request
import pypdf # or fitz if available

pdf_url = "https://s3.amazonaws.com/prod-hotspring/dimensions/2017/limelight-glow-2017-spa-rendering.pdf"
req = urllib.request.Request(pdf_url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = resp.read()
    print(f"Downloaded PDF: {len(data)} bytes")
    # check text in pdf
    import pypdf
    import io
    reader = pypdf.PdfReader(io.BytesIO(data))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    print("PDF Text Preview:")
    for line in text.splitlines():
        if any(w in line.lower() for w in ['dimension', 'glow', 'width', 'length', 'height', '76', '84', '6\'', '7\'']):
            print("  ", line)
except Exception as e:
    print(f"Error: {e}")
