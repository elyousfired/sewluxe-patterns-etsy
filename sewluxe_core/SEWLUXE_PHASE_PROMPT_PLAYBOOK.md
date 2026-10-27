# SewLuxe Master Pipeline - Complete Phase-by-Phase Prompt Playbook
# دليل برومبتات ومراحل العمل الإلزامية خطوة بخطوة للـ AI (Argon Benchmark)

> **⚠️ CRITICAL IMMUTABLE SYSTEM LAW (قاعدة النظام الأساسية):**
> The AI Assistant must NEVER operate blindly as a passive script-runner.
> In EVERY single phase below, the AI MUST strictly follow its assigned **Action Prompt**,
> adopt the **Master Bespoke Couturier Persona**, execute the **Forensic Self-Audit**,
> and respect the **Gate Condition** before moving to the next phase.

---

## 📍 Phase 0: Mandatory Pre-Production CAD, Textile Forensics & Instruction Audit Gate
* **Goal**: Lock the garment DNA, calculate physical textile specifications, harvest and refine official instructions, inspect the reference A4 calibration test square, and secure user approval before touching production.
* **AI Action Prompt (شنو يدير الـ AI بالتفصيل)**:
  1. **Sub-Step 0.1 (Visual Forensics)**: Analyze target design photos across the 4 DNA Pillars: Front (darts/pleats), Closure (pull-on, side invisible zip, fly), Pockets (slant, in-seam, none), Back (clean darts, welt, yoke).
  2. **Sub-Step 0.1b (Textile Forensics)**: Research optimal fabric (GSM, composition, drape, stretch %, bolt width 60" & 45", pre-wash shrinkage %, needles, interfacing).
  3. **Sub-Step 0.2 (In-Account CAD)**: Create live design in user's PatternFast account (`POST /api/designs`, collection 750) and export authentic 300 DPI vector flat sketch (Front + Back).
  4. **Sub-Step 0.3 (Instruction Sourcing & Audit)**: Fetch official instructions and SVGs via `/api/sewing-instructions`. Pass them through `SewLuxeTailoringLibrary.audit_and_refine_instructions()` to purge ghost buttons/steps, upgrade to Haute-Couture terminology, and inject bespoke recipes.
  5. **Sub-Step 0.4 (A4-First Fast Audit)**: Audit Page 1 of the reference A4 pattern PDF via `audit_a4_calibration_test_square()`. Verify exactly $10.00\text{ cm} \times 10.00\text{ cm}$ ($\le 0.5\%$ tolerance) and ruler warning text.
  6. **Sub-Step 0.5 (Executive Report & Sketch)**: Output executive report in Arabic script with DNA Table, Textile Audit Card, Refined Instructions summary, and direct display of the 2D Technical Flat Sketch.
* **Master Tailor Self-Audit**:
  * Did I pull the authentic vector sketch from PatternFast (not draw it manually)?
  * Are the instructions 100% purged of conflicting generic options (e.g. zero buttonholes on side-zip)?
  * Is the A4 calibration square mathematically certified?
* **Gate Condition**: 🛑 **MANDATORY HARD STOP**. WAIT for the user's explicit **"OK"** on both the report and the visual flat sketch!

---

## 📍 Phase 1: Photorealistic Editorial Model Photoshoot & 1:1 Sketch Verification
* **Goal**: Produce 3 high-fashion, true-to-life editorial catalogue model photos that match the approved CAD pattern 1:1.
* **AI Action Prompt**:
  1. Use the approved 2D Flat Sketch from Phase 0 as the **Immutable Visual Anchor**.
  2. Prompt the image generator using the exact locked textile properties (GSM, fabric slub/weave, colorway, and fluid waterfall drape).
  3. Strictly apply **Zero-Obscuring Styling** (cropped top/bandeau so waistband, pleats, and rise seams are 100% visible).
  4. Generate the **3 Sacred Angles**:
     - Angle 1: Front View (waistband, pleats, drape over shoes).
     - Angle 2: Side / 3/4 View (slant pocket opening, side seam line, leg sweep width).
     - Angle 3: Back View (back shaping darts, clean waistband).
* **Master Tailor Self-Audit**:
  * Does the garment on the model match the CAD pattern in waistband, pockets, closures, and silhouette 1:1 with zero stray details?
* **Gate Condition**: 🛑 **HARD STOP**. Present the 3 photos to the user. WAIT for explicit user approval!

---

## 📍 Phase 2: Mass Batch Pattern Export & White-Labeling
* **Goal**: Export and white-label all 13 sizes across all 3 global paper formats.
* **AI Action Prompt**:
  1. Execute batch export via `PatternFastAccountEngine.batch_export_all_sizes()` across Adult US 00–22 (13 sizes) x 3 formats (A4, US Letter, A0) = 39 pattern PDFs.
  2. White-label all files: purge PatternFast/Tailornova logos and embed `SewLuxePatterns` luxury headers.
  3. Verify $10.00\text{ cm} \times 10.00\text{ cm}$ ($4.00'' \times 4.00''$) calibration square on Page 1 of every single file.
  4. Package into 3 organized customer ZIP archives:
     - `SewLuxe_<Garment>_Size_US_00-22_A4.zip`
     - `SewLuxe_<Garment>_Size_US_00-22_US_Letter.zip`
     - `SewLuxe_<Garment>_Size_US_00-22_A0_CopyShop.zip`
* **Master Tailor Self-Audit**:
  * Are all 39 files accounted for with zero missing sizes?
* **Gate Condition**: Automated verification (39/39 files present and verified).

---

## 📍 Phase 2.5: The Pre-PDF Master Text Blueprint, Dynamic Page Planning & Tailor Self-Audit Gate
* **Goal**: Prevent wasted tokens and PDF compilation errors by drafting the entire booklet as text and tables first, planning instruction pages dynamically, and getting user sign-off.
* **AI Action Prompt**:
  1. **Adopt Master Tailor Persona**: Inspect the garment data (piece count, closure complexity, pocket type).
  2. **Devise Dynamic Page Allocation Plan (Pages 9–N)**:
     - Do NOT use a rigid template. Allocate pages based on step complexity:
     - Complex steps (Slanted Pocket, Hook & Bar Waistband) get dedicated full pages with 4-panel breakdown (`1.`, `2.`, `3.`, `4.`).
     - Simple connected steps (Inseams + Crotch) are paired harmoniously.
  3. **Draft Complete Text & Tables**:
     - Page 4: Body Size Chart (US 00–22, Bust/Waist/Hips in cm & inches).
     - Page 5: Finished Garment Measurements Table with wearing ease check and exact tailor fractions ($cm / 2.54 \rightarrow$ nearest 1/8").
     - Page 6: Piece Inventory & Cutting Layout.
     - Pages 9–N: Complete step-by-step sewing instructions with Haute-Couture terminology.
  4. **The Master Tailor Self-Audit**: Ask the 5 Sacred Tailor Questions:
     - Are measurements mathematically coherent?
     - Are fractions ($1/2''$, $3/8''$, $5/8''$) accurate without clipping?
     - Is the sewing sequence physically executable in an atelier without fabric damage?
* **Gate Condition**: 🛑 **MANDATORY HARD STOP**. Present the Text Blueprint and Page Plan in chat. WAIT for the user's explicit **"OK"**!

---

## 📍 Phase 3: Luxury Illustrated Instruction Booklet PDF Compilation
* **Goal**: Build the binary luxury PDF booklet via ReportLab based on the approved Text Blueprint.
* **AI Action Prompt**:
  1. Compile PDF via `UniversalBookletBuilder` (`Lora` + `Poppins` fonts).
  2. Render authentic pieces overview on Page 7.
  3. Embed verified clickable QR codes on Page 8.
  4. Build Gold Standard `#F5F2EF` framed 300 DPI vector panels for Pages 9–N following the exact approved Page Allocation Plan from Phase 2.5.
  5. Place the 3 approved model photos into the 360° Fit Gallery on Page N.
* **Master Tailor Self-Audit**:
  * Does the booklet layout match the approved Text Blueprint 1:1?
* **Gate Condition**: Automated transition to Phase 3.5.

---

## 📍 Phase 3.5: Mandatory Pre-Flight PDF Linter Gate (`sewluxe_booklet_linter.py`)
* **Goal**: Perform pixel-level and text-level automated forensic inspection before showing the PDF to the user.
* **AI Action Prompt**:
  1. Execute `sewluxe_booklet_linter.py` on the compiled booklet PDF.
  2. Verify:
     - Zero fraction errors (`0/0"`), zero text collisions (`trousersece`), zero missing digits.
     - Finished garment math sanity (Inseam, Outseam, Leg Sweep).
     - Step diagram uniqueness (zero duplicate panels).
     - Closure consistency (zero buttons/buttonholes if concealed hook/bar or side-zip).
     - QR codes decode cleanly.
     - 360° Fit Gallery has all 3 high-res model angles.
* **Gate Condition**: Automated CI/CD gate. Must return `[PASSED 100% Zero Defect]`.

---

## 📍 Phase 4: Standalone Customer Delivery Guides
* **Goal**: Compile standalone support documents that guarantee 5-star Etsy customer reviews.
* **AI Action Prompt**:
  1. Compile `SewLuxe_Printing_And_Assembling_Guide.pdf` (6 pages, 100% scaling, 10x10 cm square check, edge-trimming vs overlap).
  2. Compile `SewLuxe_Complete_Sewing_Tips_Guide.pdf` (11 pages, re-themed vector guide + atelier notes sheet).
  3. Compile `<Garment>_Download_Hub.pdf` (1-page luxury clickable download portal).
* **Gate Condition**: Verify files generated and links work.

---

## 📍 Phase 5: Advanced Digital Formats
* **Goal**: Deliver pro formats for tech-savvy home sewists.
* **AI Action Prompt**:
  1. Generate dedicated Projector File PDF (thick 3.5pt lines, high contrast, 1" and 5cm calibration grids, wide unified canvas, OCG layers).
  2. Generate Multi-Size Layered A0 PDF (individual OCG layer for every size from 00 to 22).
* **Gate Condition**: Verify layer visibility toggles correctly in Adobe Acrobat.

---

## 📍 Phase 6: High-Converting Etsy Listing Slides & SEO
* **Goal**: Complete Etsy commercial package ready for instant listing.
* **AI Action Prompt**:
  1. Render 10 square listing slides (2000x2000 px) via Playwright:
     - Slide 1: Cover Hero (editorial model + sketch badge + logo).
     - Slide 2: Style Variations / Key Features.
     - Slide 3: 1:1 Technical Flat Sketch (Front + Back with callouts).
     - Slide 4: Size Chart & Finished Garment Measurements.
     - Slide 5: Fabric Recommendations, GSM & Yardage.
     - Slide 6: What's Included in Download (Booklet, Formats, Guides).
     - Slide 7: Printing & Assembly Overview (A4, Letter, A0, Projector).
     - Slide 8: Customer Support & Beginner Friendly Promise.
     - Slide 9: 360° Editorial Angle Showcase.
     - Slide 10: Brand Story & Shop Value Proposition.
  2. Generate optimized Etsy SEO:
     - High-converting Title (under 140 chars).
     - Exactly 13 multi-word Etsy tags.
     - Category, attributes, and structured listing description.
* **Gate Condition**: Final Review & Delivery to User PC.
