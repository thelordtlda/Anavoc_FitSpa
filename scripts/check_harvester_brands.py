from pathlib import Path

with open("scripts/wayback_generational_harvester.py", "r", encoding="utf-8") as f:
    text = f.read()

# Find BRAND_DOMAINS
start = text.find("BRAND_DOMAINS = {")
end = text.find("}", start) + 1
print(text[start:end])
