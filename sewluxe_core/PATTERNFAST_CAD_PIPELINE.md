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

### Step 5: Save & Export
- Click `button.btn.primary.small.save` (`Save Design`) to persist into the user's collection.
- Trigger `Download` to export pattern files (`PDF`, `PDF-TAPE`, `DXF-AAMA`, `PLT`).
