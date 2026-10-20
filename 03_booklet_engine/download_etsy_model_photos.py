import os
import urllib.request
import json

def download_model_photos():
    out_dir = r"C:\Users\red1e\.gemini\antigravity\scratch\etsy\03_booklet_engine\model_photos"
    os.makedirs(out_dir, exist_ok=True)
    
    url = "https://www.etsy.com/api/v3/ajax/public/listings/4325463054"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
    data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode("utf-8"))
    images = data.get("images", [])
    
    print(f"Downloading {len(images)} authentic model photos from Etsy listing 4325463054...")
    downloaded = []
    for idx, img_url in enumerate(images):
        dest = os.path.join(out_dir, f"model_photo_{idx+1}.jpg")
        img_req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(img_req, timeout=20) as resp, open(dest, "wb") as f:
            f.write(resp.read())
        sz = os.path.getsize(dest)
        print(f"  [OK] Saved model_photo_{idx+1}.jpg ({sz // 1024} KB)")
        downloaded.append(dest)
        
    return downloaded

if __name__ == "__main__":
    download_model_photos()
