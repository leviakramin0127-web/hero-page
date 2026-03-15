import urllib.request
import urllib.parse
import re
import os

queries = {
    'makima': 'Makima action figure anime',
    'yor': 'Yor Forger action figure anime',
    'nezuko': 'Nezuko Kamado action figure anime',
    'power': 'Power Chainsaw Man action figure anime'
}
os.makedirs('assets', exist_ok=True)
for name, q in queries.items():
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        matches = re.findall(r'//external-content\.duckduckgo\.com/iu/\?u=([^&"\'\\]+)', html)
        if matches:
            img_url = urllib.parse.unquote(matches[0])
            print(f"Downloading {name} from {img_url}")
            try:
                req_img = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_img, timeout=10) as resp, open(f'assets/{name}_figure.jpg', 'wb') as f:
                    f.write(resp.read())
            except Exception as e:
                print(f"Failed {name}: {e}")
        else:
            print(f"No image found for {name}")
    except Exception as e:
         print(f"Search failed for {name}: {e}")
