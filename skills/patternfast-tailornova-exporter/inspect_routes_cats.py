import json
import os
from playwright.sync_api import sync_playwright

BASE_DIR = r"C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter"
PROFILE_DIR = os.path.join(BASE_DIR, "browser_profile_berop")

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(
        user_data_dir=PROFILE_DIR,
        headless=True,
        viewport={"width": 1440, "height": 900}
    )
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://patternfast.com/designer", wait_until="domcontentloaded", timeout=45000)
    page.wait_for_timeout(3000)

    routes_and_cats = page.evaluate("""() => {
        const app = document.querySelector('#app').__vue__;
        const store = app.$store;
        const router = app.$router;
        
        return {
            currentRoute: router.currentRoute.path,
            routes: router.options.routes.map(r => ({ path: r.path, name: r.name })),
            designCategoryPrefixes: store.state.designCategoryPrefixes,
            mannequinCategories: store.state.mannequinCategories
        };
    }""")
    print("Routes & categories:")
    print("Current route:", routes_and_cats.get("currentRoute"))
    print("Category prefixes:", routes_and_cats.get("designCategoryPrefixes"))
    print("Mannequin categories:", routes_and_cats.get("mannequinCategories"))
    print("\nRoutes count:", len(routes_and_cats.get("routes", [])))
    for r in routes_and_cats.get("routes", [])[:20]:
        print(" ", r)

    ctx.close()
