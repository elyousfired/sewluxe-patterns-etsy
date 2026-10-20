import os
import sys
import json
import urllib.parse
import urllib.request
from typing import Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# UTF-8 encoding support
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

app = FastAPI(title="SewLuxe Etsy Market Intelligence Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESEARCH_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
STATIC_DIR = os.path.join(BASE_DIR, "static")
IMAGES_DIR = os.path.join(STATIC_DIR, "images")
os.makedirs(IMAGES_DIR, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
PROJECT_ROOT = os.path.abspath(os.path.join(RESEARCH_DIR, ".."))
SELECTED_FILE = os.path.join(PROJECT_ROOT, "selected_pattern.json")

# المطابقة الدقيقة 1:1 مع تصنيفات PatternFast من الصورة المرفوعة
PATTERNFAST_CATEGORIES = {
    "jackets": {
        "id": "jackets",
        "title_en": "Jackets",
        "title_ar": "السترات والمعاطف (Jackets)",
        "badge": "Active",
        "icon_svg": "jacket",
        "desc": "Blazers, Trench Coats, Wool Coats, Cropped Jackets",
        "queries": [
            {"tag": "tailored_blazer", "name": "Tailored Blazer", "q": "etsy tailored blazer pattern pdf"},
            {"tag": "wool_coat", "name": "Classic Wool Coat", "q": "etsy wool coat pattern pdf"},
            {"tag": "trench_coat", "name": "Tailored Trench Coat", "q": "etsy trench coat pattern pdf"},
            {"tag": "cropped_jacket", "name": "Cropped Jacket", "q": "etsy cropped jacket pattern pdf"},
            {"tag": "casual_jacket", "name": "Casual Everyday Jacket", "q": "etsy jacket pattern pdf"}
        ]
    },
    "dresses": {
        "id": "dresses",
        "title_en": "Dresses",
        "title_ar": "الفساتين (Dresses)",
        "badge": "Active",
        "icon_svg": "dress",
        "desc": "Slip Dresses, Wrap Dresses, Linen Shirt Dresses, Midi Dresses",
        "queries": [
            {"tag": "slip_dress", "name": "Bias Cut Slip Dress", "q": "etsy slip dress pattern pdf"},
            {"tag": "wrap_dress", "name": "Classic Wrap Dress", "q": "etsy wrap dress pattern pdf"},
            {"tag": "shirt_dress", "name": "Linen Shirt Dress", "q": "etsy linen shirt dress sewing pattern pdf"},
            {"tag": "midi_dress", "name": "Tiered Midi Dress", "q": "etsy midi dress pattern pdf"},
            {"tag": "summer_dress", "name": "Summer Linen Sundress", "q": "etsy linen dress pattern pdf"}
        ]
    },
    "tops": {
        "id": "tops",
        "title_en": "Tops",
        "title_ar": "البلوزات والقمصان (Tops)",
        "badge": "Active",
        "icon_svg": "top",
        "desc": "Button-Up Shirts, Puff Sleeve Blouses, Wrap Tops",
        "queries": [
            {"tag": "linen_shirt", "name": "Relaxed Button-Up Shirt", "q": "etsy linen shirt pattern pdf"},
            {"tag": "blouse", "name": "Classic Tailored Blouse", "q": "etsy blouse pattern pdf"},
            {"tag": "puff_sleeve", "name": "Puff Sleeve Blouse", "q": "etsy puff sleeve top pattern pdf"},
            {"tag": "wrap_top", "name": "Tie-Front Wrap Top", "q": "etsy wrap top pattern pdf"},
            {"tag": "peplum_top", "name": "Peplum Blouse", "q": "etsy peplum top pattern pdf"}
        ]
    },
    "jumpsuits": {
        "id": "jumpsuits",
        "title_en": "Jumpsuits",
        "title_ar": "الجمبسوت والسالوبيت (Jumpsuits)",
        "badge": "Active",
        "icon_svg": "jumpsuit",
        "desc": "Wide Leg Jumpsuits, Linen Overalls, Boiler Suits",
        "queries": [
            {"tag": "wide_leg_jumpsuit", "name": "Wide Leg Linen Jumpsuit", "q": "etsy wide leg jumpsuit pattern pdf"},
            {"tag": "wrap_jumpsuit", "name": "Tie Waist Wrap Jumpsuit", "q": "etsy wrap jumpsuit pattern pdf"},
            {"tag": "boiler_suit", "name": "Utility Boiler Suit Overalls", "q": "etsy boiler suit pattern pdf"},
            {"tag": "sleeveless_jumpsuit", "name": "Summer Sleeveless Jumpsuit", "q": "etsy jumpsuit sewing pattern pdf"},
            {"tag": "dungarees", "name": "Casual Linen Overalls", "q": "etsy overalls pattern pdf"}
        ]
    },
    "pants": {
        "id": "pants",
        "title_en": "Pants",
        "title_ar": "السراويل والبنطلونات (Pants)",
        "badge": "Active",
        "icon_svg": "pants",
        "desc": "Paperbag Trousers, Wide Leg, Cargo, Tailored Pleated, Barrel Leg",
        "queries": [
            {"tag": "paperbag_pants", "name": "Paperbag Wide-Leg Pants", "q": "etsy paperbag pants sewing pattern pdf"},
            {"tag": "wide_leg", "name": "Wide Leg Trousers", "q": "etsy wide leg pants pattern pdf"},
            {"tag": "cargo_pants", "name": "Utility Cargo Pants", "q": "etsy cargo pants sewing pattern pdf"},
            {"tag": "pleated_pants", "name": "Tailored Pleated Trousers", "q": "etsy tailored pleated trousers sewing pattern pdf"},
            {"tag": "barrel_leg", "name": "Barrel Leg Balloon Pants", "q": "etsy barrel leg pants sewing pattern pdf"}
        ]
    },
    "skirts": {
        "id": "skirts",
        "title_en": "Skirts",
        "title_ar": "التنانير (Skirts)",
        "badge": "Active",
        "icon_svg": "skirt",
        "desc": "Pleated Skirts, Bias Cut Slip Skirts, Wrap Skirts, A-Line",
        "queries": [
            {"tag": "pleated_skirt", "name": "Pleated Midi Skirt", "q": "etsy pleated skirt pattern pdf"},
            {"tag": "slip_skirt", "name": "Bias Cut Silk/Linen Slip Skirt", "q": "etsy bias cut slip skirt pattern pdf"},
            {"tag": "wrap_skirt", "name": "Tie-Waist Wrap Skirt", "q": "etsy wrap skirt pattern pdf"},
            {"tag": "a_line_skirt", "name": "High-Waist A-Line Skirt", "q": "etsy a line skirt pattern pdf"},
            {"tag": "tiered_skirt", "name": "Boho Tiered Maxi Skirt", "q": "etsy tiered skirt pattern pdf"}
        ]
    },
    "sweatshirts": {
        "id": "sweatshirts",
        "title_en": "Sweatshirts",
        "title_ar": "السويت شيرت والهودي (Sweatshirts)",
        "badge": "Active",
        "icon_svg": "sweatshirt",
        "desc": "Raglan Sweatshirts, Oversized Hoodies, Crewneck Pullovers",
        "queries": [
            {"tag": "raglan_sweatshirt", "name": "Classic Raglan Sweatshirt", "q": "etsy raglan sweatshirt pattern pdf"},
            {"tag": "hoodie", "name": "Oversized Cozy Hoodie", "q": "etsy hoodie pattern pdf"},
            {"tag": "crewneck", "name": "Relaxed Crewneck Pullover", "q": "etsy crewneck sweatshirt pattern pdf"},
            {"tag": "cropped_hoodie", "name": "Cropped Fleece Hoodie", "q": "etsy cropped hoodie pattern pdf"},
            {"tag": "quarter_zip", "name": "Half-Zip Sweatshirt", "q": "etsy zip sweatshirt pattern pdf"}
        ]
    },
    "tshirts": {
        "id": "tshirts",
        "title_en": "T-Shirts",
        "title_ar": "التيشرتات (T-Shirts)",
        "badge": "Active",
        "icon_svg": "tshirt",
        "desc": "Boxy Tees, Relaxed Crewneck T-Shirts, V-Neck T-Shirts",
        "queries": [
            {"tag": "boxy_tee", "name": "Boxy Oversized T-Shirt", "q": "etsy boxy t shirt pattern pdf"},
            {"tag": "classic_tee", "name": "Classic Everyday Crewneck Tee", "q": "etsy t shirt pattern pdf"},
            {"tag": "v_neck_tee", "name": "Relaxed V-Neck T-Shirt", "q": "etsy v neck t shirt pattern pdf"},
            {"tag": "drop_shoulder_tee", "name": "Drop Shoulder Tee", "q": "etsy drop shoulder t shirt pattern pdf"},
            {"tag": "fitted_tee", "name": "Fitted Rib Knit Tee", "q": "etsy fitted tee pattern pdf"}
        ]
    }
}

import re

class DirectUrlRequest(BaseModel):
    url: str

class SelectModelRequest(BaseModel):
    category_id: str
    rank: int
    title: str
    image_url: str
    etsy_url: str
    style_name: str
    features: List[str] = []

def run_playwright_scan(cat_id: str) -> List[Dict[str, Any]]:
    if cat_id not in PATTERNFAST_CATEGORIES:
        return []

    cat_cfg = PATTERNFAST_CATEGORIES[cat_id]
    from playwright.sync_api import sync_playwright

    results = []
    cat_img_dir = os.path.join(IMAGES_DIR, cat_id)
    os.makedirs(cat_img_dir, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for idx, q_info in enumerate(cat_cfg["queries"][:5], 1):
            q_text = q_info["q"]
            tag = q_info["tag"]
            name = q_info["name"]

            url = f"https://www.bing.com/images/search?q={urllib.parse.quote(q_text)}"
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                try:
                    btn = page.locator("#bnp_btn_accept")
                    if btn.count() > 0:
                        btn.click()
                except Exception:
                    pass

                try:
                    page.wait_for_selector("a.iusc", timeout=5000)
                except Exception:
                    pass

                page.wait_for_timeout(1800)

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

                for c in cards:
                    # check duplicate
                    key = c['title'][:25].lower()
                    if any(key in r['title'].lower() for r in results):
                        continue

                    img_filename = f"{tag}_{len(results)+1}.jpg"
                    local_img_path = os.path.join(cat_img_dir, img_filename)
                    web_img_path = f"/static/images/{cat_id}/{img_filename}"

                    try:
                        req = urllib.request.Request(c["img"], headers={"User-Agent": "Mozilla/5.0"})
                        with urllib.request.urlopen(req, timeout=10) as resp, open(local_img_path, "wb") as f:
                            f.write(resp.read())
                    except Exception:
                        web_img_path = c["img"]

                    results.append({
                        "rank": len(results) + 1,
                        "tag": tag,
                        "style_name": name,
                        "title": c["title"],
                        "desc": c.get("desc", ""),
                        "etsy_url": c["page"],
                        "image_url": web_img_path,
                        "original_image": c["img"]
                    })

                    if len(results) >= 5:
                        break

            except Exception as e:
                print(f"Error scanning query {q_text}: {e}")

            if len(results) >= 5:
                break

        browser.close()

    cache_path = os.path.join(RESEARCH_DIR, f"results_{cat_id}.json")
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    return results

@app.get("/api/categories")
def get_categories():
    return [
        {
            "id": cat_id,
            "title_en": cfg["title_en"],
            "title_ar": cfg["title_ar"],
            "badge": cfg["badge"],
            "icon": cfg["icon_svg"],
            "desc": cfg["desc"]
        }
        for cat_id, cfg in PATTERNFAST_CATEGORIES.items()
    ]

@app.get("/api/results/{category_id}")
def get_category_results(category_id: str):
    if category_id not in PATTERNFAST_CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found")

    cache_path = os.path.join(RESEARCH_DIR, f"results_{category_id}.json")
    if os.path.exists(cache_path):
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if data:
                    return {"category": category_id, "results": data, "cached": True}
        except Exception:
            pass

    # For pants, check if bestseller options exist
    if category_id == "pants":
        bestsellers_summary = os.path.join(RESEARCH_DIR, "bestseller_pants_5_options", "top_5_pants_summary.json")
        if os.path.exists(bestsellers_summary):
            try:
                with open(bestsellers_summary, "r", encoding="utf-8") as f:
                    b_data = json.load(f)
                    formatted = []
                    for item in b_data:
                        formatted.append({
                            "rank": item.get("rank", 1),
                            "tag": item.get("style_id", ""),
                            "style_name": item.get("style_name", ""),
                            "title": item.get("title", ""),
                            "desc": item.get("desc_snippet", ""),
                            "etsy_url": item.get("etsy_page", ""),
                            "image_url": item.get("hero_img_url", ""),
                            "original_image": item.get("hero_img_url", "")
                        })
                    return {"category": category_id, "results": formatted, "cached": True}
            except Exception:
                pass

    return {"category": category_id, "results": [], "cached": False}

@app.post("/api/scan/{category_id}")
def trigger_scan(category_id: str):
    if category_id not in PATTERNFAST_CATEGORIES:
        raise HTTPException(status_code=404, detail="Category not found")

    print(f"Triggering fresh scan for: {category_id}")
    results = run_playwright_scan(category_id)
    return {"category": category_id, "results": results, "count": len(results)}

@app.post("/api/select")
def select_model(payload: SelectModelRequest):
    data = payload.model_dump()
    with open(SELECTED_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return {"status": "success", "message": "تم اختيار الموديل بنجاح!", "data": data}

@app.get("/api/selected")
def get_selected_model():
    if os.path.exists(SELECTED_FILE):
        try:
            with open(SELECTED_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None
    return None

DIRECT_DIR = os.path.join(IMAGES_DIR, "direct")
os.makedirs(DIRECT_DIR, exist_ok=True)

@app.post("/api/scan-url")
def scan_direct_etsy_url(payload: DirectUrlRequest):
    url = payload.url.strip()
    m_id = re.search(r'/listing/(\d+)', url) or re.search(r'listing_id=(\d+)', url) or re.search(r'^(\d+)$', url)

    if not m_id:
        raise HTTPException(status_code=400, detail="لم نتمكن من استخراج رقم المنتج (Listing ID) من هذا الرابط. يرجى إدخال رابط Etsy صحيح.")

    lid = m_id.group(1)
    
    # استعلام مباشر وحقيقي من سيرفر Etsy الرسمي عبر واجهة AJAX العامة (100% Authentic Data)
    api_url = f"https://www.etsy.com/api/v3/ajax/public/listings/{lid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Accept": "application/json"
    }

    data = None
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"Etsy API direct fetch failed for {lid}: {e}")

    if data and "title" in data:
        full_title = data.get("title", "")
        shop_name = data.get("shop_name", "Etsy Shop")
        desc = data.get("description", "") or data.get("generated_summary", "")
        currency = data.get("currency_symbol") or "$"
        price_val = data.get("price") or ""
        price_str = f"{currency}{price_val}" if price_val else ""
        images_list = data.get("images", [])
        tags = data.get("tags", [])
        category_name = data.get("category_name", "")

        hero_cdn = images_list[0] if images_list else "https://placehold.co/600x750/FAF8F5/1C1B1A?text=Pattern+Image"
        
        # حفظ الصورة محلياً لضمان السرعة الفائقة وعدم الانقطاع
        local_img_filename = f"listing_{lid}.jpg"
        local_img_disk = os.path.join(DIRECT_DIR, local_img_filename)
        web_img_path = f"/static/images/direct/{local_img_filename}"
        
        if not os.path.exists(local_img_disk) and images_list:
            try:
                img_req = urllib.request.Request(hero_cdn, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(img_req, timeout=10) as img_resp, open(local_img_disk, "wb") as f_out:
                    f_out.write(img_resp.read())
            except Exception as img_err:
                print(f"Could not cache image locally: {img_err}")
                web_img_path = hero_cdn
        elif not os.path.exists(local_img_disk):
            web_img_path = hero_cdn

        # تخمين التصنيف الأنسب من الكلمات المفتاحية
        matched_cat = "pants"
        lower_t = (full_title + " " + " ".join(tags)).lower()
        if "dress" in lower_t:
            matched_cat = "dresses"
        elif "jacket" in lower_t or "coat" in lower_t or "blazer" in lower_t:
            matched_cat = "jackets"
        elif "top" in lower_t or "shirt" in lower_t or "blouse" in lower_t:
            matched_cat = "tops"
        elif "jumpsuit" in lower_t or "overall" in lower_t or "romper" in lower_t:
            matched_cat = "jumpsuits"
        elif "skirt" in lower_t:
            matched_cat = "skirts"
        elif "sweatshirt" in lower_t or "hoodie" in lower_t:
            matched_cat = "sweatshirts"
        elif "t-shirt" in lower_t or "tee" in lower_t:
            matched_cat = "tshirts"

        result = {
            "listing_id": lid,
            "title": full_title,
            "clean_title": full_title[:50] + "..." if len(full_title) > 50 else full_title,
            "shop_name": shop_name,
            "price": price_str,
            "etsy_url": f"https://www.etsy.com/listing/{lid}",
            "image_url": web_img_path,
            "original_image": hero_cdn,
            "desc": desc,
            "gallery_images": images_list,
            "tags": tags[:8],
            "category_id": matched_cat,
            "style_name": f"{full_title.split(',')[0].split('-')[0].strip()} ({shop_name})"
        }
        return {"status": "success", "data": result}

    # في حالة نادرة لم يجب السيرفر، استخدام البديل الاحتياطي
    m_slug = re.search(r'/listing/\d+/([^/?]+)', url)
    slug = m_slug.group(1) if m_slug else ""
    clean_title = slug.replace("-", " ").title() if slug else f"Etsy Pattern #{lid}"
    q = f"{slug.replace('-', ' ')} {lid} etsy" if slug else f"etsy listing {lid} pattern pdf"

    from playwright.sync_api import sync_playwright
    cards = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        b_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(q)}"
        try:
            page.goto(b_url, wait_until="domcontentloaded", timeout=20000)
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
        except Exception as e:
            print("Direct URL scan fallback error:", e)
        browser.close()

    hero_img = cards[0]["img"] if cards else "https://placehold.co/600x750/FAF8F5/1C1B1A?text=Pattern+Image"
    full_title = cards[0]["title"] if cards and cards[0]["title"] else f"{clean_title} (PDF Pattern)"
    desc = cards[0]["desc"] if cards else "Direct Etsy listing analyzed by SewLuxe Intelligence Engine."
    gallery = [c["img"] for c in cards[1:5]] if len(cards) > 1 else []

    result = {
        "listing_id": lid,
        "title": full_title,
        "clean_title": clean_title,
        "shop_name": "Etsy Seller",
        "price": "",
        "etsy_url": f"https://www.etsy.com/listing/{lid}" if lid else url,
        "image_url": hero_img,
        "original_image": hero_img,
        "desc": desc,
        "gallery_images": gallery,
        "tags": [],
        "category_id": "pants",
        "style_name": clean_title
    }

    return {"status": "success", "data": result}

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def get_dashboard():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h1>Dashboard Loading...</h1>")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
