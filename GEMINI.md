# User Language & Communication Guidelines

- **Mandatory Arabic Script**: Always communicate with the user using Arabic script (بالأحرف العربية).
- **Right-to-Left (RTL) Direction**: Always format and write responses from right to left (من اليمين إلى اليسار). Wrap responses in `<div dir="rtl" style="direction: rtl; text-align: right;">` to ensure the UI forces full RTL and right-alignment. Start sentences and lists with Arabic letters so text direction renders properly as RTL.
- **Style**: Use Moroccan Darija written in Arabic letters (الدارجة المغربية المكتوبة بالحروف العربية) or clear Modern Standard Arabic.
- **Language Invariance**: Regardless of the language the user writes in (French, English, Latin Arabizi, etc.), you MUST ALWAYS formulate your text responses in Arabic letters from right to left.
- **Technical Integrity**: Code blocks, terminal commands, file paths, and identifiers stay in their original syntax (English/programming code), but all explanations, summaries, and chat interaction must be in Arabic letters.

# Git Repository Scope & Local PC Rule (قاعدة الحفاظ على سرية المشاريع)

- **SYSTEM ONLY on GitHub**: The Git repository (`origin/master`) is strictly and exclusively reserved for core engine code, generators, shared skills, and pipeline tools (`sewluxe_core/`, engine scripts, customizations).
- **PROJECTS STRICTLY LOCAL ON PC**: All individual garment projects (`projects/`), buyer deliveries, photoshoots, flat sketches, and compiled PDF packages stay 100% locally on the user's PC (and Desktop). They MUST NEVER be committed or pushed to GitHub under any circumstances (enforced permanently via `.gitignore`).

# Mandatory Etsy Sewing Pattern Pipeline Rules (Argon Benchmark)

Whenever building a sewing pattern product package for Etsy (e.g. Odette Vest, Colette Trousers, Camille Coat, Margot Pants):

1. **Phase 0: Mandatory Pre-Production CAD & Measurement Audit Gate (STOP & REPORT)**:
   - **CRITICAL GATE & SEQUENTIAL ORDER (The Golden Sequence)**:
     1. **Sub-Step 0.1: Target Competitor Visual & Anatomical Forensics (The First Sacred Step)**:
        - BEFORE touching PatternFast or Tailornova, thoroughly scrutinize the Etsy target design's real photos and flat sketches.
        - Identify and lock the garment's true DNA: front shaping (flat/darted vs pleated), closure (side invisible zip vs front fly vs pull-on elastic), pockets (slant vs in-seam vs none), and back (clean vs welt vs yoke).
     2. **Sub-Step 0.2: Component-Locked CAD Configuration in PatternFast/Tailornova**:
        - Configure PatternFast and Tailornova using the exact locked DNA components from Sub-Step 0.1, preventing mismatched default templates.
     3. **Sub-Step 0.3: Deep Cross-Examination & Error Hunter Protocol**:
        - Piece Inventory & Stray Marks: Confirm all required garment pieces are present (Front, Back, Waistband). Detect and purge ghost pieces (e.g., zipper fly shield on side-zip, welt pockets on clean back).
        - Seam-Line & Geometry Sanity: Verify matching seam lengths (Front Inseam == Back Inseam, Front Side Seam == Back Side Seam).
        - Measurements & Ease: Compare body size chart vs. finished garment measurements. Ensure ease is realistic.
        - Instructions vs. CAD Alignment & Diagram Sourcing Rule: Keep authentic Tailornova vectors where matching 1:1; use Custom Anatomical CAD only for contradictions/missing bespoke features.
        - Intelligent Fabric Yardage: Calculate true fabric requirements using physical garment geometry for 60" and 45" widths, scaling extended sizes (4XL–10XL) to avoid shortages.
     4. **Sub-Step 0.4: Mandatory A4-First Fast Audit & Correction Protocol (Zero Token/Time Waste)**:
        - **A4-First Rule**: In the initial audit, correction, and verification phase, ALWAYS rely strictly on the **A4** format (single reference size, e.g. SIZE 0 / SIZE 8, or A4 overview) to inspect piece lists, calibration square, ghost pieces, and white-label branding.
        - DO NOT waste time, tokens, or bandwidth downloading/processing all 39-45 files across US Letter and A0 until A4 is verified and confirmed 100% clean and correct.
        - Once A4 passes 100%, batch export for US Letter, A0, Multi-Size Layered, and Projector files is unlocked.
     5. **Sub-Step 0.5: Executive Pre-Production Audit Report & Mandatory Gate**:
        - Output an executive `PRE-PRODUCTION AUDIT REPORT` to the user in Arabic script with status `[PASSED 100% MATCH]` or `[DISCREPANCIES DETECTED / ACTION REQUIRED]`.
        - **HARD STOP**: MUST WAIT for explicit user confirmation/approval before proceeding to Phase 1! Never start production on a defective pattern.

2. **NO Screenshots or Ugly Cropped PDF Snippets**:
   - NEVER take raw cropped screenshots or slices from Tailornova/PatternFast PDFs for sewing steps.
   - ALWAYS fetch authentic original vector SVGs from the Tailornova/PatternFast server (`admin.patternfast.ai/instructions_images/<hash>.svg` or API).
   - Inlined CSS classes & clean vector rendering at 300 DPI via PyMuPDF.

3. **Panel Formatting (Gold Standard)**:
   - Every step diagram MUST be constructed as an authentic framed vector panel (`make_two_panel_box`, `make_single_panel_box`, or `wrap_multi_panel_svg`).
   - Clean outer container with `#F5F2EF` rounded background (`radius=24`) and subtle border `#E2DDD8`.
   - Distinct white inner rectangles with crisp `4px` black outline (`outline=(0, 0, 0)`).
   - Large bold callout numbers in the top-left: **`1.`**, **`2.`**, **`3.`** in `Poppins-Bold` (`fill=(0, 0, 0)`).
   - Crisp vector lines with gray fill (`#E6E6E6`) for the wrong side (`wrong side`), white for right side (`right side`), and curved text arrows for labels (`understitch`, `press open`, etc.).

4. **Complete Turnkey Deliverables Suite (Do NOT rush into SEO or Shortcuts)**:
   - **Phase 0**: Pre-Production CAD & Measurement Audit Report (Wait for User Approval).
   - **Phase 1**: Market research & 1:1 Technical Flat Sketch + Photorealistic Editorial Photoshoot (3 poses).
   - **Phase 2**: PatternFast & Tailornova batch export (unlocked only after Sub-Step 0.4 A4-First audit passes): all 13–15 sizes x 3 formats (A4, US Letter, A0) = 39–45 PDFs. White-label to `SewLuxePatterns` with strict 4x4 in calibration square.
   - **Phase 3**: 16-page Luxury Booklet PDF compiled via ReportLab (`Lora` + `Poppins`, real size tables, fabric nesting, clickable QR video links on page 8, step panels 9–15, 360° Fit Gallery on page 16).
   - **Phase 3.5: Mandatory Automated Pre-Flight PDF Linter Gate (`sewluxe_booklet_linter.py`)**:
     - **CRITICAL CI/CD GATE**: MUST execute automated linter on compiled 16-page booklet PDF before presenting to user.
     - Verifies:
       1. Zero corrupted fraction bugs (`0/0"`), zero text collision typos (`trousersece`), and zero missing numbers.
       2. Finished garment chart math sanity via `sewluxe_math_engine.py` (Inseam, Outseam, Leg Sweep).
       3. Pattern Pieces Overview (Page 7) matches Page 6 Inventory 1:1 with zero ghost/stray pieces.
       4. Step diagram uniqueness (no copy-pasted panels across steps).
       5. Closure consistency (if Concealed Hook & Bar, zero button/buttonhole in step diagrams).
       6. QR codes have valid vector transform and decode properly.
       7. 360° Fit Gallery has all 3 high-res model photoshoot angles.
     - If ANY error is detected, booklet generation fails and stops until fixed.
   - **Phase 4**: Standalone Customer Delivery Guides:
     - `SewLuxe_Printing_And_Assembling_Guide.pdf` (6 pages).
     - `SewLuxe_Complete_Sewing_Tips_Guide.pdf` (11 pages, re-themed vector guide + personal notes sheet).
     - `<Garment>_Download_Hub.pdf` (1-page luxury clickable download portal).
   - **Phase 5**: Advanced Digital Formats:
     - Dedicated Projector File PDF (1" & 5cm calibration grid, wide unified canvas, 3.5pt lines, OCG layers).
     - Multi-Size Layered A0 PDF (OCG layers for all sizes).
   - **Phase 6**: 10 High-Converting Etsy Listing Slides (2000x2000 px) rendered via Playwright + Optimized Etsy SEO package.
   - Visual inspection of EVERY page and slide at high resolution before presenting to user.

# SewLuxe Permanent Knowledge & Design Memory Bank

### 1. Brand Portfolio & Project Status Tracker
- **Brand Name**: `SewLuxePatterns` (Luxury, modern, quiet-luxury indie sewing patterns for Etsy).
- **Product 1 (Margot Elastic Wide-Leg Pants)**:
  - **Status**: `COMPLETED (100%)`. All 7 project directories compiled, 5 turnkey customer delivery PDFs placed on Desktop (`C:\Users\red1e\Desktop\SewLuxe_Margot_Wide_Leg_Pants`), and committed to Git repo (`8c02884`).
  - **Key Silhouette**: Pull-on high-waist elastic casing (3.5 cm), in-seam pockets, straight-wide leg, zero pleats, zero closures, washed olive sage linen.
- **Product 2 (Colette Double-Pleated Palazzo Trousers)**:
  - **Status**: `PDF DELIVERABLES COMPLETED (100%)`. All 39 pattern PDFs across 13 sizes, 3 delivery ZIPs, 16-page luxury booklet, Multi-Size Layered A0, Projector File, and 6 customer delivery PDFs compiled and placed in `C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants`. Listing slides omitted per user instruction.
  - **Competitor Target Benchmark**: Etsy listing `1776314693` (SBModeatelier).
  - **Project Directory**: `C:\Users\red1e\Desktop\SewLuxe_Colette_Tailored_Pants`.
  - **Engine Scratch**: `C:\Users\red1e\.gemini\antigravity\scratch\etsy\colette_pants_engine`.

### 2. Tailored Trousers Construction & Design Rules (Locked Decisions)
- **Waistband Closure (القفل المخفي)**:
  - **CRITICAL**: Concealed trouser hook & bar on inside extension tab (`قفل معدني مخفي من الداخل`).
  - **Rule**: Absolutely ZERO exterior button `(+)` drawn on the front waistband in technical flat sketches, matching the seamless, smooth luxury front seen on editorial photos.
- **Belt Loops (5 Loops - Exact Placement & Dimensions)**:
  - Cut strip: **3.5 cm x 45 cm** (yielding refined **1.1 cm** finished loops, NEVER 8 cm!).
  - 2 Front loops placed **directly over the main front pleats and center pressed crease lines**.
  - 2 Side loops placed **directly over the slant pocket top corners** at side seams.
  - 1 Back loop placed **directly over the Center Back seam**.
- **Pleats & Creases**:
  - Double forward pleats on each front leg (Main pleat: 4 cm, Secondary pleat: 2.5 cm).
  - Razor-sharp pressed vertical center crease line running straight down each leg from the main pleat to the bottom hem.
- **Leg Sweep, Inseam & Hem**:
  - Ultra-wide sweeping palazzo silhouette: **60.5–96.9 cm (23 7/8" to 38 1/8") hem circumference across sizes** (defined via `universal_trouser_engine.py`).
  - Palazzo Inseam: **78.0 cm (30 3/4")** floor-length drape for 168 cm height / **75.5 cm** for 164 cm height; Outseam **104–110 cm**.
  - Deep weighted hem: **5.0 cm (2.0 in)** clean fold-up for fluid waterfall drape over shoes/sandals.
- **Fabric Specification**:
  - Washed Linen-Viscose or Tencel Melange in warm neutral sand beige / oatmeal ecru (two-tone heathered slub weave, fluid drape).
- **Video Policy**:
  - Never generate AI video MP4 via ffmpeg/scripts. User creates product video independently via Google Flow.

### 3. Master Measurement Engine (Single Source of Truth)
- **Universal Parametric Engine**: `C:\Users\red1e\.gemini\antigravity\scratch\etsy\sewluxe_core\universal_trouser_engine.py`.
- **Enforced Operational Rules**:
  1. ALL finished trouser measurements (Waist, Hips, Inseam, Outseam, Leg Sweep) and piece inventories MUST be derived directly from `TrouserSpec` via `UniversalTrouserEngine`.
  2. Zero manual hardcoding of measurement charts, and zero guess-work fractions (all fractions strictly governed by `cm_to_tailor_inches`).
  3. Pre-Flight QA Audit (`run_qa_audit()`) MUST return `[PASSED 100%]` before generating any customer booklet PDF.

### 4. Universal CAD Blueprint Engine (Tailornova Standard Pro v5.0)
- **Dedicated Engine**: `C:\Users\red1e\.gemini\antigravity\scratch\etsy\sewluxe_core\universal_cad_engine.py`.
- **Standard Blueprint Rules (Page 7 & Technical Inventories)**:
  1. **Double Seam Allowance Lines**: Every pattern piece is rendered with a 0.8pt solid cutting line (`#000000`) and a 0.4pt parallel inner stitching line (`#777777`, dashed 4, 2) offset exactly by seam allowance (1.0 cm / 3/8", and 5.0 cm / 2.0" hem).
  2. **Smooth Anatomical Splines**: True Bezier curves (`Path.curveTo`) for crotch hooks, pocket curves, and facings. Zero crude polygons or sharp polygonal angles.
  3. **Technical CAD Notches**: Authentic T-notches placed at knee, hip, pocket, and fly points.
  4. **Minimalist Apparel Typography**: Bold centered numbers (1, 2, 3...) in Helvetica-Bold, centered grainline vectors with geometric arrowheads, and clean sub-labels underneath (`Cut 2 Mirrored`).
  5. **Engineering Canvas**: Crisp white background (`#FFFFFF`), subtle technical inner border (`#D5D0C8`), and structured accessories stack. Zero AI clutter or pixelation artifacts.



