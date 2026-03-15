import urllib.request
from duckduckgo_search import DDGS
import os

characters = [
    ("Makima", "Makima action figure anime"), 
    ("Yor", "Yor Forger action figure anime"), 
    ("Nezuko", "Nezuko Kamado action figure anime"), 
    ("Power", "Power Chainsaw Man action figure anime")
]
os.makedirs("assets", exist_ok=True)

with DDGS() as ddgs:
    for name, query in characters:
        print(f"Searching for {query}...")
        results = ddgs.images(query, max_results=3)
        if results:
            for res in results:
                url = res['image']
                ext = url.split('.')[-1].split('?')[0]
                if len(ext) > 4: ext = "jpg"
                filename = f"assets/{name.lower()}_figure.{ext}"
                try:
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=10) as response, open(filename, 'wb') as out_file:
                        out_file.write(response.read())
                    print(f"Downloaded {filename}")
                    break
                except Exception as e:
                    print(f"Failed to download {url}: {e}")
