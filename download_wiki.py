import urllib.request
import json
import os

url = "https://en.wikipedia.org/w/api.php?action=query&titles=Makima|Yor_Forger|Nezuko_Kamado|List_of_Chainsaw_Man_characters&prop=pageimages&format=json&pithumbsize=800"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
os.makedirs('assets', exist_ok=True)

try:
    response = urllib.request.urlopen(req).read().decode('utf-8')
    data = json.loads(response)
    pages = data['query']['pages']
    
    mapping = {
        'Makima': 'makima',
        'Yor Forger': 'yor',
        'Nezuko Kamado': 'nezuko',
        'List of Chainsaw Man characters': 'power'
    }
    
    for page_id, info in pages.items():
        title = info.get('title')
        if title in mapping and 'thumbnail' in info:
            img_url = info['thumbnail']['source']
            name = mapping[title]
            print(f"Downloading {name} from {img_url}")
            img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(img_req, timeout=10) as resp, open(f'assets/{name}_figure.jpg', 'wb') as f:
                f.write(resp.read())
                
    # Fallbacks for ones that might fail (just generic hotlinks that are widely available)
    fallbacks = {
        'makima': 'https://upload.wikimedia.org/wikipedia/en/thumb/0/08/Makima_from_Chainsaw_Man_anime.png/220px-Makima_from_Chainsaw_Man_anime.png',
        'power': 'https://upload.wikimedia.org/wikipedia/en/thumb/9/9f/Power_from_Chainsaw_Man_anime.png/220px-Power_from_Chainsaw_Man_anime.png'
    }
    for name, f_url in fallbacks.items():
        if not os.path.exists(f'assets/{name}_figure.jpg') or os.path.getsize(f'assets/{name}_figure.jpg') == 0:
            print(f"Using fallback for {name}")
            img_req = urllib.request.Request(f_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(img_req, timeout=10) as resp, open(f'assets/{name}_figure.jpg', 'wb') as f:
                f.write(resp.read())

except Exception as e:
    print(f"Error: {e}")
