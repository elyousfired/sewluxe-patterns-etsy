---
name: "flat-sketch-studio"
description: "Audit, repair, redraw, and export technical flat sketches (Front + Back) to match the real pattern pieces 100%, producing clean 1800x1800 studio sketches and transparent stickers for booklets and Etsy covers."
---

# Technical Flat Sketch Studio (Audit, Repair & Sticker Export)

Goal: Ensure the Technical Flat Sketch (Front + Back) is 100% faithful to the actual pattern pieces in the PDF before generating editorial model photos (`prompt-photo-listing`), building the instruction booklet (`sewluxe-booklet` / `sewluxe-kids-booklet`), or creating Etsy listing slides (`etsy-listing-slides`).

## Why This Skill Exists
Source sketches from `PatternFast` or `Tailornova` frequently have missing details (e.g. a turtleneck collar added as a rectangle piece, a back neck slit added for kids' head clearance, wrong button count, or missing topstitching) or low-resolution artifacts. And image generation models copy every line in the flat sketch literally—if the sketch has an accidental line or wrong button count, the model photos will fail.

---

## Step 1: Pattern-vs-Sketch Anatomical Audit
Compare the extracted pattern vectors (`pdfplumber` page index 4 from the PatternFast file) against the source flat sketch:
1. **Closure & Lap Direction**:
   - Exact button count and spacing (check Size 8/10/12).
   - Lap direction: Women's & Girls' button fronts lap **Right over Left** (viewer's left over right); Men's & Boys' lap **Left over Right**.
   - Zipper: Exposed teeth vs concealed placket, exact start and stop points (collar top vs neckline).
2. **Seams & Darts**:
   - Front bust darts, waist darts, or princess seams: verify exact start/end points.
   - Back construction: Center back seam vs cut-on-fold whole back; shoulder darts; back waist darts; yoke.
3. **Neckline, Collar & Openings**:
   - Collar type (flat rounded collar, mandarin stand, convertible collar, turtleneck band, bias binding, square neck).
   - Kids woven pullovers: if a faced center-back slit + button loop was added by `sewluxe-kids-booklet` rule 2, draw the CB slit line and small loop/button on the Back view of the sketch!
4. **Sleeves, Pockets & Hem**:
   - Sleeve length, cuff vs plain hem, sleeve placket, gathered cap vs smooth set-in cap.
   - Pocket shape (square vs rounded patch corners, welt opening, in-seam pockets invisible from front).
   - Silhouette & hem shape (straight, A-line flare, peplum seam, curved shirt hem).

---

## Step 2: 4x Supersampled Vector/Raster Editing
When modifying or cleaning the sketch in Python (`PIL` / `matplotlib` / `scipy` / `opencv`):
1. **Work at 4x Supersampled Resolution** (`7200 × 7200 px` downsampled with `Image.LANCZOS` to `1800 × 1800 px`) so every new line has crisp anti-aliased edges matching the original stroke.
2. **Match Native Stroke Metrics**:
   - Measure the original sketch's outer contour width, inner seam width, and topstitching dash pattern (`#262322` or pure black).
   - Use round caps and round joins (`capstyle='round'`, `joinstyle='round'`).
   - Interior shading inside back necklines/hems: subtle light grey (`#E3E3E3` or `#EBEBEB`).
3. **Zoom Inspection**: Crop a `4x` zoom around every junction where old lines were whited out and new lines meet. Zero stubs, zero gaps, zero blurry halos.
4. **Realistic Proportions**:
   - Folded turtleneck collar: draw at `6–7 cm` visual height (not unfolded piece height).
   - Cuffs and waistbands: proportional to the bodice length of Size 10/12.

---

## Step 3: Standardized Exports
Produce 4 ready-to-use image files for the rest of the pipeline:

1. **`<Garment>_Sketch_1800.png` (`1800 × 1800 px`, pure `#FFFFFF` background)**:
   - Front view large on the left/center, Back view smaller (~72% scale) on the bottom-right, neatly balanced with generous white margin.
   - Used as the reference attachment for `prompt-photo-listing` (Model Photo Generation) and Page 2 (`Welcome`) of the Booklet.
2. **`<Garment>_Sketch_SideBySide.png` (`1600 × 1000 px`, pure `#FFFFFF` background)**:
   - Front and Back at equal scale side-by-side, bottom hems aligned.
   - Used on Slide 3 (`Technical Flat Sketch`) of `etsy-listing-slides`.
3. **`<Garment>_Sticker_Front.png` & `<Garment>_Sticker_Back.png` (Transparent RGBA)**:
   - Outer background made 100% transparent, interior garment silhouette filled pure `#FFFFFF` (`scipy.ndimage.binary_fill_holes`), `16 px` white sticker border, `4 px` accent outline (`#9C4A57` or `#A4512F`), and soft diffused drop shadow.
   - Used as floating sticker overlays on Slide 1 (`Hero Cover`) of `etsy-listing-slides`.
