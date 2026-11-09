import fitz # PyMuPDF
import urllib.request
import io

pdf_url = "https://s3.amazonaws.com/prod-hotspring/dimensions/2017/limelight-glow-2017-spa-rendering.pdf"
req = urllib.request.Request(pdf_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=15) as resp:
    data = resp.read()

doc = fitz.open(stream=data, filetype="pdf")
print("Page count:", len(doc))
for i, page in enumerate(doc):
    text = page.get_text()
    print(f"--- Page {i+1} ---")
    print(text)
