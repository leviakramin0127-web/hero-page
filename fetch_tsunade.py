import urllib.request
import json
import os
import time

char_id = 2819
base_name = "tsunade"

pic_url = f"https://api.jikan.moe/v4/characters/{char_id}/pictures"
try:
    req = urllib.request.Request(pic_url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
    pic_data = json.loads(response)

    images = pic_data['data'][:5]
    for i, img_info in enumerate(images):
        img_url = img_info['jpg']['image_url']
        if 'large_image_url' in img_info['jpg']:
            img_url = img_info['jpg']['large_image_url']
        
        filename = f"assets/panels/{base_name}_{i+1}.jpg"
        img_req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(img_req, timeout=10) as resp, open(filename, 'wb') as f:
            f.write(resp.read())
        print(f"Downloaded {filename}")
except Exception as e:
    print(e)
