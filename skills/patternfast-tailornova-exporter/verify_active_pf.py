import json
import os
import shutil
import subprocess
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter"
CRED_PATH = os.path.join(BASE_DIR, ".credentials.json")
PROFILE_DIR = os.path.join(BASE_DIR, "browser_profile_active")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
ARTIFACT_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\c675070e-91f4-406b-8086-d794cba1db24"

os.makedirs(PROFILE_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

with open(CRED_PATH, "r", encoding="utf-8") as f:
    creds = json.load(f)

pf = creds["patternfast"]

login_file = r"C:\Users\red1e\.gemini\antigravity\brain\c675070e-91f4-406b-8086-d794cba1db24\scratch\login_active.json"
with open(login_file, "w", encoding="utf-8") as f:
    json.dump({"email": pf["email"], "password": pf["password"]}, f)


def curl_json(method, url, headers=None, data_file=None):
    cmd = [
        "curl.exe", "-s", "-X", method, url,
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "-H", "Accept: application/json"
    ]
    if headers:
        for k, v in headers.items():
            cmd.extend(["-H", f"{k}: {v}"])
    if data_file:
        cmd.extend(["-H", "Content-Type: application/json; charset=UTF-8", "--data-binary", f"@{data_file}"])
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="ignore")
    try:
        return json.loads(res.stdout)
    except Exception:
        return {"raw": res.stdout[:1000]}


login_resp = curl_json("POST", "https://patternfast.com/api/user/login", data_file=login_file)
token = login_resp.get("token")
print("1. API Login Token Present:", bool(token))
auth_hdr = {"Authorization": f"Bearer {token}", "X-Requested-With": "XMLHttpRequest"}

user_info = curl_json("GET", "https://patternfast.com/api/user/current", headers=auth_hdr)
print("2. Active User Info:", json.dumps(user_info, indent=2)[:1000])

collections = curl_json("GET", "https://patternfast.com/api/collections", headers=auth_hdr)
print("3. Collections:", json.dumps(collections, indent=2)[:1000])

# Also log in inside Playwright persistent context and open /designer
with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=True,
        viewport={"width": 1440, "height": 900},
        accept_downloads=True,
    )
    page = context.new_page()
    page.goto("https://patternfast.com/login", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(2500)

    email_in = page.locator("input[placeholder*='name@example.com'], input[type='email'], input[type='text']").first
    pass_in = page.locator("input[placeholder*='Password'], input[type='password']").first
    if email_in.is_visible() and pass_in.is_visible():
        email_in.click()
        email_in.fill(pf["email"])
        pass_in.click()
        pass_in.fill(pf["password"])
        page.wait_for_timeout(500)
        pass_in.press("Enter")
        page.wait_for_timeout(5000)

    page.goto("https://patternfast.com/designer", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(6000)

    shot_path = os.path.join(SCREENSHOT_DIR, "patternfast_active_designer.png")
    page.screenshot(path=shot_path)
    shutil.copy(shot_path, os.path.join(ARTIFACT_DIR, "patternfast_active_designer.png"))
    print("4. Saved Playwright Designer Screenshot | URL:", page.url)
    context.close()
