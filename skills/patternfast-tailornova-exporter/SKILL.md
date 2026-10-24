---
name: "patternfast-tailornova-exporter"
description: "Automatically log into PatternFast and open Tailornova Designer, apply the exact same garment model and design components on both sites, download the Pattern PDFs (A4, US Letter, A0 across all sizes) + Flat Sketch from PatternFast, and download the matching Sewing Instructions PDF from Tailornova."
---

# PatternFast + Tailornova Synchronized Exporter

> [!IMPORTANT]
> ### 🚨 Mandatory Golden Operational Rules (User Directives)
> 1. **Ultra-Fast Execution (السرعة القصوى وعدم تضييع التوكنز)**:
>    - Always use fast API endpoints (`https://patternfast.com/api/...`, `https://api.patternfast.com/api/...`) and direct batch python scripts (`download_all_template.py`).
>    - Do NOT waste tokens or stall on slow, repetitive manual UI clicks. Act decisively and return results within seconds.
> 2. **Strict 1:1 Model Match & Immediate User Alert (التطابق الصارم والتنبيه الفوري عند أي اختلاف)**:
>    - Every single garment element (Silhouette, Waistband, Closure, Pleats, Pockets, Collar/Neckline, Sleeves) MUST match 100% identically between PatternFast and Tailornova.
>    - **CRITICAL**: If any model or component in PatternFast does NOT have an exact 1:1 match in Tailornova (or vice versa), you **MUST IMMEDIATELY NOTIFY THE USER IN CHAT** and explain the exact difference before taking any further action. Never proceed silently or assume approximations!

Goal: Given a garment design recipe (Category, Silhouette, Neckline/Collar, Closure, Sleeves, Pockets, Length, Fit), automatically configure the **exact same garment** on both **PatternFast** (`https://patternfast.com/designer`) and **Tailornova** (`https://tailornova.com/designer`), and download:
1. **From PatternFast**:
   - The **Pattern PDFs / ZIPs** (`A4`, `US Letter`, `A0` across all sizes: Adult `US 00–22` or Kids `2–6` & `7–16`).
   - The **Technical Flat Sketch** (Front + Back) and `Design details` string.
2. **From Tailornova (`https://tailornova.com/designer`, no login needed)**:
   - Configure the **exact same garment category and component options** as selected in PatternFast.
   - Open the **`SEWING`** tab in the top toolbar and export/print the **Sewing Instructions PDF** (containing the step-by-step instructions and technical diagrams).

---

## Saved Credentials, Persistent Browser Profile & Fast Batch Engine
- **Credentials File**: `C:\Users\red1e\.gemini\config\skills\patternfast-tailornova-exporter\.credentials.json`
  - Active PatternFast primary account: `berop37791@playfine.com` (`Elyousfi1993@`)
  - Backup account: `lefavoy394@proguidex.com`
- **Persistent Browser Profile**: `C:\Users\red1e\.gemini\antigravity\scratch\etsy\browser_profile_berop`
- **Fast 3-Second Loader & Core CAD Engine**: `C:\Users\red1e\.gemini\antigravity\scratch\etsy\sewluxe_core\patternfast_cad_engine.py`
  - Once a design is created and saved (`POST /api/designs`), PatternFast assigns a persistent `Design ID` (e.g. `10593`).
  - **Instant Reload**: Navigating directly to `https://patternfast.com/designer/{design_id}` bypasses the 25s setup flow and loads the workspace in ~3 seconds.
- **Fast Pattern Download Selector Sequence**:
  - In PatternFast's Download modal, the Download button is disabled by default for PDF because PDF requires selecting a sub-format.
  - The exact automated selector sequence is:
    1. Click toolbar Download: `page.locator("button.btn.secondary.small:has-text('Download')").first.click()`
    2. Expand PDF format dropdown: `page.locator(".selected-block").filter(has_text="PDF").locator(".info").first.click()`
    3. Select target paper format: `page.locator(".base-dropdown__content__item").filter(has_text=format_name).first.click()` (`A4`, `LETTER`, or `A0`)
    4. Confirm download button is enabled and trigger: `with page.expect_download() as dl: page.locator(".download-pattern-modal button.btn.primary.one").first.click()`

---

## Step-by-Step Synchronized Workflow

### Step 1: Define the Exact Garment Recipe
Before clicking on either site, write down the exact component selections so both sites match 100%:
- **Division**: `Womenswear`, `Menswear`, `Girlswear (2–6)`, `Junior Girls (7–16)`, `Boyswear (2–6)`, or `Junior Boys (7–16)`.
- **Category**: `Dresses`, `Tops`, `Jackets`, `Coats`, `Vests`, `Pants`, `Skirts`, `Sweatshirts`, `T-Shirts`, `Jumpsuits`, etc.
- **Components**:
  - `Silhouette` & `Length` (e.g., Above Knee, Hip Length, Cropped, Straight, Peplum, Trapeze)
  - `Neckline` / `Collar` (e.g., Mandarin Stand, Round Jewel Neck, Square Neck, Convertible Collar, V-Neck)
  - `Closure` (Front Buttons, Exposed Zipper, Back Buttoned Seam, None)
  - `Sleeves` & `Cuffs` (Long Set-in Sleeve, Bishop Sleeve with Cuff, Sleeveless, Short Sleeve)
  - `Pockets` / `Ruffles` / `Belts` / `Lining` / `Neckline Facing`
  - `Seam Allowance`: `1 cm (3/8 in)`

### Step 2: Export Patterns & Flat Sketch from PatternFast
1. Open `https://patternfast.com/designer` using `browser_profile_active`.
2. Select the Division, Category, and exact Components from Step 1.
3. Verify the **Flat Sketch** (Front + Back) and **Flat Pattern** preview on the right; save the high-res Flat Sketch image.
4. Click **`Download ↓`** (or call `/cat/download-pdf` / batch export across the full size range) to download:
   - `A4` ZIP/PDFs (all sizes)
   - `US Letter` ZIP/PDFs (all sizes)
   - `A0` ZIP/PDFs (all sizes)

### Step 3: Export Matching Sewing Instructions from Tailornova
1. Open `https://tailornova.com/designer` (no account login required).
2. In the *"Create new masterpiece"* modal (or `DESIGN > New`), select the **exact same Division and Category**.
3. In the left/component menus, click the **exact same component options** (`Silhouette`, `Neckline`, `Closure`, `Sleeves`, `Pockets`, `Lining`, `Facing`) and confirm that the Tailornova `TECHNICAL SKETCH (BOTH)` matches the PatternFast `Flat Sketch` 100%.
4. Click **`SEWING`** in the top toolbar (`DESIGN | UNDO | REDO | SPECS | EASE | SEWING | YARDAGE | HELP | DOWNLOAD`).
5. Wait for all sewing steps and SVG diagrams to load, then click Print / Save as PDF (or `page.pdf()` / extract raw SVGs + text) to save `Tailornova_Source_Instructions.pdf` into the project's `raw/` folder.

### Step 3.5: Mandatory Pre-Production CAD & Measurement Audit (Phase 0 Gate - A4-First Protocol)
> [!CRITICAL]
> **MANDATORY AUDIT GATE & A4-FIRST PROTOCOL BEFORE PROCEEDING**:
> Before mass batch downloads, you MUST perform an automated pre-flight audit relying strictly on the **A4** format first (single reference size, e.g. SIZE 0 / SIZE 8, or A4 overview) to prevent wasting time and tokens on defective batches:
> 1. **A4-First Inspection**: Inspect A4 Page 2 (Piece Inventory) and Page 4 (Piece Layout). Cross-reference pieces with the garment DNA. Detect and purge ghost pieces (e.g. fly shield on side zip).
> 2. **Piece Count & Inventory**: Flag any missing pieces (e.g. pocket bag, facing) or rogue pieces.
> 3. **Seam Length Symmetry**: Verify matching seams (Front Inseam == Back Inseam, Side Seams match).
> 4. **Measurements & Ease**: Verify finished garment measurements against body size chart for realistic ease.
> 5. **Step-by-Step Alignment**: Confirm that every step in the instructions corresponds 1:1 with CAD pieces and notches.
> 6. **Output Audit Report**: Present the report in chat (Status: PASSED or DISCREPANCY DETECTED) and **WAIT for user approval** before launching full batch downloads across US Letter and A0!

### Step 4: Hand Off to Production Skills
Once Phase 0 is approved by the user, pass the validated assets to:
1. [`flat-sketch-studio`](../flat-sketch-studio/SKILL.md) (verify sketch & export stickers)
2. [`sewluxe-booklet`](../sewluxe-booklet/SKILL.md) (build the 16-page luxury illustrated booklet)
3. [`pattern-packager-pro`](../pattern-packager-pro/SKILL.md) (clean logos, build Multi-Size Layered PDF + Projector File + Download Hub)
4. [`prompt-photo-listing`](../prompt-photo-listing/SKILL.md) & [`etsy-listing-slides`](../etsy-listing-slides/SKILL.md) & [`seo-listing-etsy`](../seo-listing-etsy/SKILL.md).
