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
    page.wait_for_timeout(4000)

    # Inspect Vuex store or window state
    vue_state = page.evaluate("""() => {
        let store = null;
        const app = document.querySelector('#app') || document.querySelector('[id*="app"]');
        if (app && app.__vue__ && app.__vue__.$store) {
            store = app.__vue__.$store;
        } else if (window.__store) {
            store = window.__store;
        }
        
        if (store) {
            const modules = Object.keys(store.state || {});
            return {
                modules,
                currentCategory: store.state.category || store.state.currentCategory || (store.state.designer ? store.state.designer.category : null),
                design: store.state.design ? Object.keys(store.state.design) : null
            };
        }
        return 'No Vue store found directly on #app';
    }""")
    print("Vue store info:", vue_state)

    ctx.close()
