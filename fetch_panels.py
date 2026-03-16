import urllib.request
import urllib.parse
import json
import os
import time

characters = [
    "Tsunade Senju",
    "Makima",
    "Yor Forger",
    "Nezuko Kamado",
    "Power"
]

os.makedirs('assets/panels', exist_ok=True)

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        response = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
        return json.loads(response)
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

for char in characters:
    print(f"Fetching data for {char}...")
    # Search for character
    search_url = f"https://api.jikan.moe/v4/characters?q={urllib.parse.quote(char)}&limit=1"
    search_data = fetch_json(search_url)
    
    if search_data and search_data.get('data'):
        char_id = search_data['data'][0]['mal_id']
        # Fetch pictures
        pic_url = f"https://api.jikan.moe/v4/characters/{char_id}/pictures"
        pic_data = fetch_json(pic_url)
        
        if pic_data and pic_data.get('data'):
            images = pic_data['data'][:5] # Get up to 5 images
            base_name = char.split()[0].lower()
            for i, img_info in enumerate(images):
                img_url = img_info['jpg']['image_url']
                if 'large_image_url' in img_info['jpg']:
                     img_url = img_info['jpg']['large_image_url']
                
                filename = f"assets/panels/{base_name}_{i+1}.jpg"
                try:
                    img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(img_req, timeout=10) as resp, open(filename, 'wb') as f:
                        f.write(resp.read())
                    print(f"Downloaded {filename}")
                except Exception as e:
                    print(f"Failed to download {img_url}: {e}")
        else:
             print(f"No pictures found for {char}")
    else:
        print(f"Character {char} not found on Jikan.")
        
    time.sleep(1) # Rate limit protection for Jikan API
