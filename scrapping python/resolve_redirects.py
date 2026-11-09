import requests

url1 = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQEPemHBjPT6p_wqmTNhAIqm6IJRRtzz0h4pShJ6404N-eBhbZyyypOyiEpea9Xu9npWWGc8TjOzvztoPofbh5qdLrRpesincwgu_z92Svm2phb8Pk5JeLCPiJ9h7PIDeFikzKzIkEZz6PwQV0aVJtzg21zp41lRSauLSB2MAP85lEKh6auvD37zRZC6aoXlWxPSCdrvbdbxC8rP91b4NlsV6cRN"
url2 = "https://vertexaisearch.cloud.google.com/grounding-api-redirect/AUZIYQFb3KGtrp9Ah8RY8jaqeJV64W0D8C4CtubhE2dkkeUftiqELzb759g5ZfK7u_eKCVbjsQORIk3uxyq2dP1IKQTcQlrW3ofR7_cvJF_2AbBKukSr_zYfJwYqDvyRU3H2Kqg9xeVwHEhdDFz2bdkD_5O7VsHXch1aWUh_y-6B5svh6MJ81IUdUIIv69sTpqwa8xKI97k6ZipyBx5XbGuurU8Xoaw0"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}

for u in [url1, url2]:
    try:
        r = requests.head(u, headers=headers, allow_redirects=True, timeout=10)
        print("Resolved to:", r.url)
    except Exception as e:
        print("Error:", e)
