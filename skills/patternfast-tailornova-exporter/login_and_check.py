import json
import os
import shutil
from playwright.sync_api import sync_playwright

BASE_DIR = r"C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter"
CRED_PATH = os.path.join(BASE_DIR, ".credentials.json")
PROFILE_DIR = os.path.join(BASE_DIR, "browser_profile")
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
ARTIFACT_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\c675070e-91f4-406b-8086-d794cba1db24"

os.makedirs(PROFILE_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

with open(CRED_PATH, "r", encoding="utf-8") as f:
    creds = json.load(f)

pf = creds["patternfast"]

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=True,
        viewport={"width": 1440, "height": 900},
        accept_downloads=True,
    )
    page = context.new_page()
    page.goto("https://patternfast.com/login", wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(3000)

    email_in = page.locator("input[placeholder*='name@example.com'], input[type='email'], input[type='text']").first
    pass_in = page.locator("input[placeholder*='Password'], input[type='password']").first
    if email_in.is_visible() and pass_in.is_visible():
        email_in.click()
        email_in.fill(pf["email"])
        pass_in.click()
        pass_in.fill(pf["password"])
        page.wait_for_timeout(800)
        pass_in.press("Enter")
        page.wait_for_timeout(6000)

    if "/login" in page.url:
        page.goto("https://patternfast.com/designer", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(6000)

    shot_path = os.path.join(SCREENSHOT_DIR, "patternfast_designer.png")
    page.screenshot(path=shot_path)
    shutil.copy(shot_path, os.path.join(ARTIFACT_DIR, "patternfast_designer.png"))
    print("Saved screenshot:", shot_path, "| URL:", page.url)
    context.close()
