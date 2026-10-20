import os
import sys
import json
import urllib.parse
import urllib.request
from playwright.sync_api import sync_playwright

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "bestseller_pants_5_options")
os.makedirs(OUT_DIR, exist_ok=True)

# 5 Distinct Bestseller Pants Styles on Etsy
PANTS_STYLES = [
    {
        "id": "option_1_paperbag",
        "name": "Paperbag Waist Wide Leg Trousers (الموديل الشبيه بالصورة المرفوعة)",
        "query": "etsy paperbag pants sewing pattern pdf",
        "folder": "01_paperbag_wide_leg"
    },
    {
        "id": "option_2_pleated",
        "name": "High-Waisted Tailored Pleated Trousers (السروال الكلاسيكي بالبليات)",
        "query": "etsy wide leg pants pattern pdf",
        "folder": "02_tailored_pleated"
    },
    {
        "id": "option_3_cargo",
        "name": "Straight / Wide Leg Cargo Pants (سروال الكارغو بالجياب)",
        "query": "etsy cargo pants sewing pattern pdf",
        "folder": "03_cargo_trousers"
    },
    {
        "id": "option_4_linen_lounge",
        "name": "Elastic Waist Linen Lounge / Palazzo Pants (سروال اللينين الفضفاض بالاستيك)",
        "query": "etsy linen lounge pants sewing pattern pdf",
        "folder": "04_linen_palazzo"
    },
    {
        "id": "option_5_barrel_leg",
        "name": "Barrel Leg / Horseshoe Balloon Trousers (السروال المقوس العصري)",
        "query": "etsy barrel leg pants sewing pattern pdf",
        "folder": "05_barrel_leg"
    }
]

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def fetch_top_5():
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for idx, item in enumerate(PANTS_STYLES, 1):
            print(f"\n[{idx}/5] 🔍 Searching: {item['name']}")
            style_dir = os.path.join(OUT_DIR, item["folder"])
            os.makedirs(style_dir, exist_ok=True)

            url = f"https://www.bing.com/images/search?q={urllib.parse.quote(item['query'])}"
            page.goto(url, wait_until="domcontentloaded", timeout=25000)

            try:
                btn = page.locator("#bnp_btn_accept")
                if btn.count() > 0:
                    btn.click()
            except Exception:
                pass

            try:
                page.wait_for_selector("a.iusc", timeout=6000)
            except Exception:
                pass

            page.wait_for_timeout(2000)

            cards = page.evaluate("""() => {
                const items = Array.from(document.querySelectorAll('a.iusc'));
                return items.map(a => {
                    try {
                        const m = JSON.parse(a.getAttribute('m'));
                        return {
                            title: m.t || '',
                            desc: m.desc || '',
                            img: m.murl || '',
                            page: m.purl || ''
                        };
                    } catch(e) { return null; }
                }).filter(c => c && c.img.includes('etsystatic.com'));
            }""")

            print(f"   ↳ Found {len(cards)} Etsy bestseller candidates.")

            if cards:
                top_card = cards[0]
                img_path = os.path.join(style_dir, "model_hero_photo.jpg")
                try:
                    req = urllib.request.Request(top_card["img"], headers={"User-Agent": "Mozilla/5.0"})
                    with urllib.request.urlopen(req, timeout=15) as resp, open(img_path, "wb") as f:
                        f.write(resp.read())
                    print(f"   ✅ Saved hero photo: {img_path}")
                except Exception as e:
                    print(f"   ⚠️ Could not save hero: {e}")

                # Save 2 extra slide photos if available (e.g. flat sketch or details)
                extra_imgs = []
                for extra_idx, extra_card in enumerate(cards[1:3], 1):
                    extra_path = os.path.join(style_dir, f"listing_slide_{extra_idx}.jpg")
                    try:
                        req = urllib.request.Request(extra_card["img"], headers={"User-Agent": "Mozilla/5.0"})
                        with urllib.request.urlopen(req, timeout=15) as resp, open(extra_path, "wb") as f:
                            f.write(resp.read())
                        extra_imgs.append(extra_path)
                    except Exception:
                        pass

                info = {
                    "rank": idx,
                    "style_id": item["id"],
                    "style_name": item["name"],
                    "query": item["query"],
                    "title": top_card["title"],
                    "desc_snippet": top_card.get("desc", ""),
                    "etsy_page": top_card["page"],
                    "hero_img_url": top_card["img"],
                    "hero_local_path": img_path,
                    "extra_images": extra_imgs
                }

                with open(os.path.join(style_dir, "listing_info.json"), "w", encoding="utf-8") as jf:
                    json.dump(info, jf, indent=2, ensure_ascii=False)

                results.append(info)

        browser.close()

    summary_file = os.path.join(OUT_DIR, "top_5_pants_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 All 5 Bestseller Pants Extracted! Summary: {summary_file}")
    return results

if __name__ == "__main__":
    fetch_top_5()
