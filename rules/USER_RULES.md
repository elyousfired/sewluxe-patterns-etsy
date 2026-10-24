# SewLuxe Global Rules & Production Benchmark (Argon Protocol)

## 1. User Language & Communication Guidelines
- **Mandatory Arabic Script**: Always communicate with the user using Arabic script (بالأحرف العربية).
- **Right-to-Left (RTL) Direction**: Always format and write responses from right to left (من اليمين إلى اليسار). Wrap responses in `<div dir="rtl" style="direction: rtl; text-align: right;">` to ensure the UI forces full RTL and right-alignment.
- **Style**: Use Moroccan Darija written in Arabic letters (الدارجة المغربية المكتوبة بالحروف العربية) or clear Modern Standard Arabic.
- **Language Invariance**: Regardless of the language the user writes in (French, English, Latin Arabizi, etc.), you MUST ALWAYS formulate your text responses in Arabic letters from right to left.
- **Technical Integrity**: Code blocks, terminal commands, file paths, and identifiers stay in their original syntax (English/programming code), but all explanations, summaries, and chat interaction must be in Arabic letters.

---

## 2. Git Repository Scope & Local PC Rule (قاعدة الحفاظ على سرية المشاريع)
- **SYSTEM ONLY on GitHub**: The Git repository (`origin/master`) is strictly and exclusively reserved for core engine code, generators, shared skills, rules, and pipeline tools (`sewluxe_core/`, `skills/`, `rules/`).
- **PROJECTS STRICTLY LOCAL ON PC**: All individual garment projects (`projects/`), buyer deliveries, photoshoots, flat sketches, and compiled PDF packages stay 100% locally on the user's PC (and Desktop). They MUST NEVER be committed or pushed to GitHub under any circumstances (enforced permanently via `.gitignore`).

---

## 3. Mandatory Etsy Sewing Pattern Pipeline Rules (Argon Benchmark)

Whenever building a sewing pattern product package for Etsy:

### Phase 0: Mandatory Pre-Production CAD & Measurement Audit Gate (STOP & REPORT)
- **CRITICAL GATE & STRICT SEQUENTIAL ENFORCEMENT (قاعدة عدم تخطي المراحل أو العمل العشوائي)**:
  Every garment project MUST strictly follow the sequential order below without skipping, shortcutting, or inventing details from head.
  1. **Sub-Step 0.1: Target Competitor Visual & Anatomical Forensics**:
     - Thoroughly scrutinize the Etsy target design's real photos and flat sketches.
     - **DNA Structural Lock**: Front shaping (flat/darted vs pleated), closure (side invisible zip vs front fly vs pull-on elastic), pockets (slant vs in-seam vs none), and back (clean vs welt vs yoke).
     - **Fabric & Material Lock (Strict Non-Assumption Rule)**: NEVER assume or substitute default fabrics (e.g. casual linen). Scrutinize physical textile behavior:
       * If liquid waterfall drape with soft matte-satin sheen $\rightarrow$ Heavy Fluid Silk-Viscose Crepe / Tencel (ZERO linen slub, ZERO wrinkles).
       * If visible weave slub with natural wrinkles $\rightarrow$ Washed linen.
       * If structured body $\rightarrow$ Wool / Twill.
     - **Exact Colorway Lock**: Primary photoshoot MUST match the winning benchmark colorway (e.g. Deep Petrol Teal) to maintain market visual parity.
     - **Zero-Obscuring Styling**: When garments feature high-waist detailing, clean front rise seams, or waist darts, styling MUST NOT conceal them (use cropped bandeau / crop top / bare midriff so waistband, darts, and rise seams are 100% visible and uncluttered).
  2. **Sub-Step 0.2: Component-Locked CAD Configuration in PatternFast/Tailornova**:
     - Configure PatternFast and Tailornova using the exact locked DNA components from Sub-Step 0.1, preventing mismatched default templates.
     - Bypasses random AI Designer (/ai-designer) and directly controls the standard CAD Garment Designer (/designer via /new-design).
     - Save Design permanently to collection (`POST /api/designs`) to obtain persistent `Design ID` for direct 3-second loading (`/designer/{design_id}`).
  3. **Sub-Step 0.3: Deep Cross-Examination & Error Hunter Protocol**:
     - Piece Inventory & Stray Marks: Confirm all required garment pieces are present (Front, Back, Waistband). Detect and purge ghost pieces (e.g., zipper fly shield on side-zip, welt pockets on clean back).
     - Seam-Line & Geometry Sanity: Verify matching seam lengths.
     - Measurements & Ease: Compare body size chart vs. finished garment measurements. Extract technical specs (e.g. side invisible zipper length: 18.00 cm).
     - Instructions vs. CAD Alignment & Diagram Sourcing Rule: Keep authentic Tailornova vectors where matching 1:1; use Custom Anatomical CAD only for contradictions/missing bespoke features.
     - Intelligent Fabric Yardage: Calculate true fabric requirements using physical garment geometry for 60" and 45" widths.
  4. **Sub-Step 0.4: Mandatory A4-First Fast Audit & Correction Protocol**:
     - In the initial audit, correction, and verification phase, ALWAYS rely strictly on the **A4** format (single reference size, e.g. SIZE 4 / SIZE 8, or A4 overview) to inspect piece lists, calibration square, ghost pieces, and white-label branding.
     - Use the proven 3-second download selector sequence: Click toolbar `Download` $\rightarrow$ Click PDF `.info` dropdown $\rightarrow$ Click `.base-dropdown__content__item` (`A4`) $\rightarrow$ Click modal `Download`.
     - DO NOT waste time, tokens, or bandwidth downloading/processing all 39-45 files across US Letter and A0 until A4 is verified and confirmed 100% clean and correct.
  5. **Sub-Step 0.5: Executive Pre-Production Audit Report & Mandatory Gate**:
     - Output an executive `PRE-PRODUCTION AUDIT REPORT` to the user in Arabic script with status `[PASSED 100% MATCH]`.
     - **HARD STOP**: MUST WAIT for explicit user confirmation/approval before proceeding to Phase 1! Never start production on a defective pattern.

### Phase 1: Photorealistic Editorial Photoshoot (3 poses) + 1:1 Technical Flat Sketch
- Square 1:1 editorial catalogue photography matching the approved CAD pattern pieces and target reference image 1:1 (Front, Side, Back).
- Strictly enforce the locked Fabric, Colorway, and Zero-Obscuring Styling rules from Sub-Step 0.1.
- Clean, crisp 1800x1800 technical flat sketch with Front and Back views side-by-side at 1.0 scale.

### Phase 2: PatternFast & Tailornova Batch Export
- Unlocked only after Sub-Step 0.4 A4-First audit passes.
- All sizes (00-24 / 32-56) across 3 formats (A4, US Letter, A0).
- White-label to `SewLuxePatterns` with strict 4x4 in (10x10 cm) calibration test square.

### Phase 3: 16-page Luxury Booklet PDF & Mandatory Page-by-Page Interactive Verification Gate
- Compiled via ReportLab (`Lora` + `Poppins`, real size tables, fabric nesting, clickable QR video links on page 8, step panels 9–15, 360° Fit Gallery on page 16).
- **Mandatory Page-by-Page Interactive Verification Gate (قاعدة التدقيق والموافقة التفاعلية صفحة بصفحة)**:
  - When building the 16-page booklet, the agent **MUST NEVER compile all 16 pages and present them all at once** without intermediate review.
  - The agent MUST build and render each page individually (starting with Page 1: Cover), present the high-resolution render directly to the user in chat, and **MUST WAIT for the user's explicit 'OK' / approval before proceeding to the next page**!
  - Strict sequence: Page 1 Render $\rightarrow$ Wait for User OK $\rightarrow$ Page 2 Render $\rightarrow$ Wait for User OK $\rightarrow$ ... $\rightarrow$ Page 16 Render $\rightarrow$ Final 16-Page Compilation & Linter Gate.
- **Mandatory Pre-Flight PDF Linter (`sewluxe_booklet_linter.py`)**:
  - Verifies zero corrupted fraction bugs (`0/0"`), zero text collision typos (`trousersece`), and zero missing numbers.
  - Finished garment chart math sanity via `sewluxe_math_engine.py`.
  - Pattern pieces overview matches inventory 1:1 with zero ghost pieces.
  - Step diagram uniqueness and closure consistency.
  - All QR codes and 360° Fit Gallery model photos verified.

### Phase 4: Standalone Customer Delivery Guides
- `SewLuxe_Printing_And_Assembling_Guide.pdf` (6 pages).
- `SewLuxe_Complete_Sewing_Tips_Guide.pdf` (11 pages).
- `<Garment>_Download_Hub.pdf` (1-page luxury clickable download portal).

### Phase 5: Advanced Digital Formats
- Dedicated Projector File PDF (1" & 5cm calibration grid, wide unified canvas, 3.5pt lines, OCG layers).
- Multi-Size Layered A0 PDF (OCG layers for all sizes).

### Phase 6: High-Converting Etsy Listing Slides & SEO
- 10 listing slides (2000x2000 px) rendered via Playwright.
- Data-driven title, 13 tags, attributes, and description.

---

## 4. Master Measurement Engine & Parametric Rules
- Universal Parametric Engine: `sewluxe_core/universal_trouser_engine.py`.
- All finished measurements and piece inventories derived directly from `TrouserSpec`.
- Zero manual hardcoding of measurement charts. All fractions strictly governed by `cm_to_tailor_inches`.
- Pre-Flight QA Audit (`run_qa_audit()`) MUST return `[PASSED 100%]` before generating any customer booklet PDF.
