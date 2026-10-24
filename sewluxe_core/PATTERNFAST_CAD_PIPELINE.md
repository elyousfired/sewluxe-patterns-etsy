# PatternFast CAD Native Automation Pipeline

## Overview
This document outlines the standard operating procedure (SOP) for configuring and extracting sewing patterns and technical flat sketches from **PatternFast** (`patternfast.com`) without using the automated/random AI Designer.

---

## 1. AI Designer vs Parametric CAD Designer

| Feature | AI Designer (`/ai-designer/*`) | Garment Designer (`/designer`) |
| :--- | :--- | :--- |
| **URL Route** | `https://patternfast.com/ai-designer/<garment>` | `https://patternfast.com/new-design` $\rightarrow$ `/designer` |
| **Selection Type** | 10 static AI-generated presets (Design 1-10) | 100% Parametric Component Selection |
| **Component Control**| Rigid combinations (cannot customize closures/pleats) | Full control over Silhouettes, Waist Bands, Pockets |
| **Direct SVG Linework** | May contain ghost pieces / mismatched templates | Authentic CAD linework matching pattern pieces 1:1 |
| **Etsy Production** | ❌ **PROHIBITED** (leads to non-matching patterns) | ✅ **MANDATORY STANDARD** |

---

## 2. Standard 5-Step Workflow

### Step 1: Initialize Garment in `/new-design`
- Navigate to `https://patternfast.com/new-design`.
- Select the garment category (e.g. `Pants`, `Tops`, `Dresses`, `Jackets`).
- Click `Next`.

### Step 2: Lock Size Chart & Standard Base Size
- Open `.base-dropdown` $\rightarrow$ `Size chart`.
- Select standard sizing: `US/CAN Standard Women, 00-22` (or `EU Standard Women`).
- Select reference base size: `Size 4` (or `Size 36`).
- Click `Create`. The browser loads the full CAD workspace at `https://patternfast.com/designer`.

### Step 3: Parametric Component Selection
1. **Silhouettes**:
   - Click `Silhouettes` in the left sidebar menu (loads 480+ silhouettes).
   - Use internal search input (`input[placeholder*='Search']`).
   - Example search: `Floor Length` $\rightarrow$ Click `Wide Leg Floor Length`.
2. **Waist Bands**:
   - Click `Waist Bands` in the left sidebar.
   - For clean front with side closure: Select `Waistband Side Button`.
   - For classic front button & fly: Select `Waistband Front Button`.
3. **Pockets**:
   - Click `Pockets` in the left sidebar.
   - For clean hip lines: Ensure `No Front Pockets` is selected.

### Step 4: Authentic Vector Extraction & Normalization
- The Flat Sketch canvas contains `<svg id="both">`.
- In live preview, PatternFast scales the back view to $0.7$ and shifts it behind the front view.
- `PatternFastCADEngine.process_and_render_sketch()` automatically:
  1. Isolates `<g class="front-view">` and `<g class="back-view">`.
  2. Resets the Back view `transform` (normalizing scale from $0.7$ to $1.0$).
  3. Renders both views side-by-side at 300 DPI on a clean $1800 \times 1800$ white canvas.

### Step 5: Save & Persistent Design ID
- Click `button.btn.primary.small.save` (`Save Design`) or `POST /api/designs` to persist into the user's collection.
- PatternFast returns a persistent `Design ID` (e.g. `10593`).
- **Instant Reload Flow**: Instead of re-doing steps 1-3 (25s), navigate directly to `https://patternfast.com/designer/{design_id}` which loads in ~3 seconds.

---

## 3. High-Speed Pattern Download Engine

### The PDF Sub-Format Selector Sequence
In PatternFast's download modal, the Download button is disabled by default for `PDF` until a specific paper format is selected from the nested dropdown.

**Automated Playwright Sequence**:
1. Click toolbar Download:
   ```python
   page.locator("button.btn.secondary.small:has-text('Download')").first.click()
   ```
2. Expand the PDF info dropdown:
   ```python
   pdf_block = page.locator(".selected-block").filter(has_text="PDF").first
   pdf_block.locator(".info").first.click()
   ```
3. Select paper format (`A4`, `LETTER`, `A0`):
   ```python
   page.locator(".base-dropdown__content__item").filter(has_text=format_name).first.click()
   ```
4. Confirm download button is enabled and trigger download:
   ```python
   with page.expect_download(timeout=60000) as dl_info:
       page.locator(".download-pattern-modal button.btn.primary.one").first.click()
   download = dl_info.value
   download.save_as(target_path)
   ```

---

## 4. Phase 0 Gate: A4-First Fast Audit Protocol
Never download all 39-45 files across Letter and A0 until A4 is verified!
1. Download reference size in **A4** (e.g. Size 4 / Size 8).
2. **Page 1 Audit**: Test square calibration (10 cm x 10 cm / 4 in x 4 in).
3. **Page 2 Audit**: Piece inventory & technical specifications:
   - Pants Front (Cut 2 Mirrored)
   - Pants Back (Cut 2 Mirrored)
   - Waistband (Cut 1 Main, Cut 1 Interfacing)
   - Technical closure specs (e.g. Left Side Invisible Zipper: 18.00 cm / 7 1/8 in)
   - Zero ghost pieces (no fly shield, no welt pocket pieces).
4. **Page 4 Audit**: Piece layout sanity & seam alignments.
5. **Pre-Production Audit Report**: Present report in chat, **HARD STOP** for explicit user approval before Phase 1.
