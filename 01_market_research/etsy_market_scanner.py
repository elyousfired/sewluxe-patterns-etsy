import os
import sys
import json
import argparse
import urllib.parse
import urllib.request

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# شجرة التصنيفات المتكاملة لباترونات الخياطة على Etsy
CATALOG_CATEGORIES = {
    "pants": {
        "folder": "01_pants",
        "label": "السراويل والبنطلونات (Pants & Trousers)",
        "queries": [
            ("wide_leg", "etsy wide leg pants pattern pdf", "wide_leg.jpg"),
            ("cargo_pants", "etsy cargo pants sewing pattern pdf", "cargo_pants.jpg"),
            ("paperbag_pants", "etsy paperbag pants sewing pattern pdf", "paperbag_pants.jpg"),
            ("pleated_pants", "etsy pleated trousers sewing pattern pdf", "pleated_pants.jpg")
        ]
    },
    "jackets_coats": {
        "folder": "02_jackets_and_coats",
        "label": "السترات والمعاطف (Jackets & Coats)",
        "queries": [
            ("tailored_blazer", "etsy tailored blazer pattern pdf", "tailored_blazer.jpg"),
            ("wool_coat", "etsy wool coat pattern pdf", "wool_coat.jpg"),
            ("jacket", "etsy jacket pattern pdf", "jacket.jpg")
        ]
    },
    "dresses": {
        "folder": "03_dresses",
        "label": "الفساتين (Dresses)",
        "queries": [
            ("slip_dress", "etsy slip dress pattern pdf", "slip_dress.jpg"),
            ("wrap_dress", "etsy wrap dress pattern pdf", "wrap_dress.jpg"),
            ("shirt_dress", "etsy linen shirt dress sewing pattern pdf", "shirt_dress.jpg")
        ]
    },
    "skirts": {
        "folder": "04_skirts",
        "label": "التنانير (Skirts)",
        "queries": [
            ("pleated_skirt", "etsy pleated skirt pattern pdf", "pleated_skirt.jpg"),
            ("slip_skirt", "etsy bias cut slip skirt pattern pdf", "slip_skirt.jpg"),
            ("wrap_skirt", "etsy wrap skirt pattern pdf", "wrap_skirt.jpg")
        ]
    },
    "tops": {
        "folder": "05_tops",
        "label": "البلوزات والقمصان (Tops & Shirts)",
        "queries": [
            ("linen_shirt", "etsy linen shirt pattern pdf", "linen_shirt.jpg"),
            ("blouse", "etsy blouse pattern pdf", "blouse.jpg")
        ]
    }
}

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def scan_category(category_key, max_items_per_query=2):
    if category_key not in CATALOG_CATEGORIES:
        print(f"Unknown category: {category_key}. Available: {list(CATALOG_CATEGORIES.keys())}")
        return

    cat_info = CATALOG_CATEGORIES[category_key]
    cat_dir = os.path.join(BASE_DIR, "categories", cat_info["folder"])
    os.makedirs(cat_dir, exist_ok=True)

    summary_file = os.path.join(cat_dir, "category_summary.json")
    category_summary = {}
    if os.path.exists(summary_file):
        try:
            with open(summary_file, "r", encoding="utf-8") as sf:
                category_summary = json.load(sf)
        except Exception:
            category_summary = {}

    print(f"\n==================================================")
    print(f"🚀 Scanning Category: {cat_info['label']}")
    print(f"📁 Target Folder: {cat_dir}")
    print(f"==================================================")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for tag, query, base_fname in cat_info["queries"]:
            print(f"\n🔍 Query: '{query}' (Tag: {tag})")
            encoded_q = urllib.parse.quote(query)
            bing_url = f"https://www.bing.com/images/search?q={encoded_q}"

            try:
                page.goto(bing_url, wait_until="domcontentloaded", timeout=25000)

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
                    }).filter(Boolean);
                }""")

                etsy_cards = [c for c in cards if "etsystatic.com" in c.get("img", "")]
                print(f"   ↳ Found total {len(cards)} cards, {len(etsy_cards)} authentic Etsy listing cards.")

                saved_for_tag = []
                for idx, c in enumerate(etsy_cards[:max_items_per_query]):
                    fname = f"{tag}_{idx+1}.jpg" if max_items_per_query > 1 else base_fname
                    out_path = os.path.join(cat_dir, fname)
                    img_url = c["img"]

                    try:
                        req = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
                        with urllib.request.urlopen(req, timeout=15) as resp, open(out_path, "wb") as out_f:
                            out_f.write(resp.read())
                        print(f"   ✅ Downloaded [{idx+1}]: {fname} ({c['title'][:45]}...)")
                        c_data = {
                            "tag": tag,
                            "rank": idx + 1,
                            "filename": fname,
                            "title": c.get("title", ""),
                            "etsy_page": c.get("page", ""),
                            "img_url": img_url
                        }
                        saved_for_tag.append(c_data)
                    except Exception as dl_err:
                        print(f"   ⚠️ Could not download {img_url}: {dl_err}")

                if saved_for_tag:
                    category_summary[tag] = saved_for_tag
                    tag_info_file = os.path.join(cat_dir, f"{tag}_info.json")
                    with open(tag_info_file, "w", encoding="utf-8") as tf:
                        json.dump(saved_for_tag, tf, indent=2, ensure_ascii=False)

            except Exception as e:
                print(f"   ❌ Error searching '{query}': {e}")

        browser.close()

    with open(summary_file, "w", encoding="utf-8") as sf:
        json.dump(category_summary, sf, indent=2, ensure_ascii=False)

    print(f"\n✨ Done category: {category_key}. Summary saved to {summary_file}")

def main():
    parser = argparse.ArgumentParser(description="Etsy Comprehensive Market Scanner")
    parser.add_argument("--category", "-c", default="pants", help="Category to scan: pants, jackets_coats, dresses, skirts, tops, or all")
    parser.add_argument("--limit", "-l", type=int, default=1, help="Number of top bestseller images to download per subcategory")
    args = parser.parse_args()

    if args.category == "all":
        for cat in CATALOG_CATEGORIES.keys():
            scan_category(cat, max_items_per_query=args.limit)
    else:
        scan_category(args.category, max_items_per_query=args.limit)

if __name__ == "__main__":
    main()
