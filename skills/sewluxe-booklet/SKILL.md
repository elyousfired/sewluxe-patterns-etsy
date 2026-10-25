---
name: "sewluxe-booklet"
description: "Build a SewLuxePatterns sewing-instruction booklet PDF (Elsie house style) from pattern files, source instructions, sketch and model photo. Booklet only, no SEO or listing."
---

# SewLuxePatterns booklet

Deliverable: ONE PDF booklet, `<Garment-Name>_Sewing-Instructions.pdf`. No Etsy SEO, no listing, no website post unless the user asks. Reply in the user's own language, short. If the user gives no name, pick a short feminine name in the Elsie style (e.g. Margot Coat, Eloise Coat, Rachel Jacket, Nora Turtleneck Top) and tell him he can rename it.

The booklet exists to prevent bad reviews: every step must be impossible to misunderstand for someone who has never made this garment.

## Fast Ready-to-Use Scripts (Self-Contained in Skill)
- **Mandatory Studio-First Diagram Pipeline**: Always extract and prepare all authentic instruction step panels in `instruction_panels_studio/` directly from the active garment's Tailornova PDF before generating the booklet.
- **SVG Diagram Cleaner & 300-DPI Renderer**: `C:\Users\red1e\.gemini\config\skills\instruction-diagram-studio\scripts\clean_instruction_panel.py` — Auto-crops to active diagram bounds, expands viewBox for zero clipped text, auto-detects grid panels, overlays bold Poppins numbers (`1.`, `2.`, `3.`, `4.`), and wraps in `#F5F2EF` luxury container.
- **Procedural CAD Generator for Missing Steps (ONLY when missing from Tailornova)**: `C:\Users\red1e\.gemini\config\skills\instruction-diagram-studio\scripts\draft_missing_panel.py` — Use ONLY if the garment model has an invented/custom feature missing from Tailornova.
- **Automated Booklet Quality Gate & Master Auditor**: `C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\scripts\audit_booklet_quality.py` — Automated 39-point quality auditor that inspects all 16 pages for page count, 1:1 cover geometry, zero cross-garment contamination, real pieces 1..N, mask='auto' transparency, dead whitespace, clickable links, QR vector codes, and dual showcase model matching before delivering to user.
- **Pattern Piece & Spec Extractor**: `C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\scripts\extract_booklet_data_template.py`.

### 0.0 MANDATORY LAW: Zero Project Contamination & Strict Project Autonomy
- **NEVER reuse, borrow, or copy assets, diagrams, schematics, or scripts from past project folders** (e.g. `Lila_Lounge_Pants`, `Audrey_Tailored_Pants`, `Celeste_Pleated_Pants`, `SewLuxe_Production_System\projects\...`).
- **Every project MUST be 100% self-contained and generated directly and exclusively from ITS OWN authentic Tailornova/PatternFast files**:
  - `pieces_overview.png`: MUST be extracted directly from **Page 3 of the active garment's Tailornova instructions PDF** at 300 DPI. NEVER draw simplified rectangles or schematics when authentic CAD vector pattern pieces already exist!
  - `Step_*.png`: MUST be extracted directly from **Pages 11+ of the active garment's Tailornova instructions PDF** at 300 DPI.
  - **Procedural CAD Drafting is ONLY for Missing Techniques**: If and ONLY if a garment model has a custom feature not present in the Tailornova instructions (e.g. custom cargo pocket, belt sash), draft it using CAD. If the feature already exists in Tailornova, ALWAYS use the authentic original vector diagram!

### 0.1 THE 5 ARGON BOOKLET VISUAL RULES (MANDATORY ZERO-DEFECT QUALITY LAWS)
1. **Rule 1: Clean High-Fashion Cover (Zero Competitor Graphics)**:
   - NEVER paste raw seller listing slides, orange banners, or competitor thumbnails with external text (e.g. "US Letter-A4-A0 Sewing Pattern", "XS to 5XL") onto Page 1.
   - ALWAYS crop and use clean authentic model photography (`margot_cover_clean.jpg`) with crisp white framing, paired with an overlapping authentic flat sketch sticker (`flat_sketch_transparent.png`, `mask='auto'`).
2. **Rule 2: Zero Text Collision & Dynamic Flow (Page 5 & All Tip Boxes)**:
   - In all `draw_tip_box` and callout components, NEVER hardcode static box heights (e.g. `height=44`). ALWAYS compute dynamic height: `w, h = p.wrap(width - 24, 200)` and `box_h = max(height, h + 28.0)`.
   - Title must sit at `y - 13.5` and body text must draw strictly below the title (`y - 13.5 - 5 - h`) with ample breathing room.
   - All notion items, checklists, and markings must decrement dynamically (`ry -= (h + spacing)`).
3. **Rule 3: Clean Authentic Pieces Overview & Dynamic Markings (Page 7)**:
   - Extract the authentic pieces overview diagram exclusively from Page 3 of the active garment's Tailornova PDF at 300 DPI. Overwrite any old files to ensure zero third-party logos (`Tailornova`, etc.).
   - On the right column ("Understanding Pattern Markings"), every bulleted paragraph must compute its dynamic wrapped height and decrement `ry -= (h + 10)`. Zero overlapping text lines.
4. **Rule 4: Complete Instruction Step Diagrams (Pages 13 & 14 - Zero Half-Sliced Boxes)**:
   - Every step diagram panel must be complete with zero cut-off boxes or half-visible drawings.
   - When a step contains multiple pictures (e.g. Waistband Casing & Elastic insertion with 6 pictures):
     - Split cleanly into two logical pages:
       - **Page 13**: Step 5 (Waistband Casing Prep, Pics 1 & 2 only, complete, uncapped).
       - **Page 14**: Step 6 (Attaching Waistband & Threading Elastic, Pics 3 to 6 only, complete, uncapped).
5. **Rule 5: Standalone Final Celebration Page (Page N - Zero Step Cramming)**:
   - The final page (Page N: 16, 18, 20, 24...) MUST be a 100% standalone celebration, styling, and garment care page (`Y O U   M A D E   I T` / `Enjoy Your Garment!`).
   - The final sewing step MUST sit on **Page N-1** with its own complete diagram. NEVER cram sewing steps or instructions onto the celebration page!
   - Page N features a luxury dual showcase (clean model photo + flat sketch back), curated styling tips, fabric care guidelines, and the Etsy customer support help box.
6. **Rule 6: Strict Drawing-Only Bbox (Zero Raw PDF Text Inside Diagram Panels)**:
   - When extracting instruction step panels (`Step_*.png`) from Tailornova/PatternFast, NEVER clip or include the raw instruction text paragraphs printed above the diagrams (e.g. `Step 1:... - Pin the pocket pieces...`).
   - The script must always locate `max_text_y = max(block[3] for block in text_blocks)` and start the diagram crop strictly below the text (`y0 >= max_text_y + 5`), so the exported PNG contains EXCLUSIVELY the authentic framed vector boxes (`1.`, `2.`, `3.`...) and exactly ZERO duplicate text.
7. **Rule 7: Flexible Dynamic Pagination (Adaptive 16+ Pages — Zero Artificial Page-Capping)**:
   - The booklet is **NOT rigidly fixed to 16 pages**. 16 pages is only the natural minimum for simple garments (e.g. relaxed pants with 6–7 steps).
   - For complex garments (e.g. cargo trousers with extra flap/patch pockets, blazers, lined trench coats, or garments with 8 to 14 steps), the booklet **MUST dynamically expand to 18, 20, 22, 24+ pages**!
   - **MANDATORY LAW**: Every sewing step or multi-part step gets its OWN dedicated, spacious, complete page. NEVER compress, squish, combine, or truncate steps just to hit 16 pages! The total pages are dynamically computed as: `Total Pages = 8 (Front Matter) + M (Dedicated Step Pages) + 1 (Standalone Celebration Outro)`.
8. **Rule 8: Automated Gap Detection (Pieces vs. Steps Reconciliation)**:
   - Always execute an automated cross-audit between the CAD pattern pieces list and the instruction steps (`Missing Pieces = Total CAD Pieces - Pieces Covered in Steps`).
   - If any piece or feature (e.g. Cargo pockets, flap pieces, drawstring eyelets, belt loops, sash belt) exists in the pattern but is omitted from Tailornova source instructions, procedurally draft the missing step via `instruction-diagram-studio` (`draft_missing_panel.py`) and insert it into the logical assembly sequence.
   - **Zero Orphaned Pieces**: Every piece in the cutting layout MUST have a dedicated, illustrated sewing step showing how it is prepped and assembled.
9. **Rule 9: The Autonomous Forensic Quality Gate (Gemini Standard - Zero User-Reported Defects)**:
   - **MANDATORY LAW**: The assistant MUST NEVER present a completed booklet to the user before running an autonomous, multi-layered forensic self-audit that eliminates all defects that a sharp human or AI reviewer would catch.
   - **4 Mandatory Forensic Self-Audit Checks**:
     1. **Sewing Order 1:1 Synchronization**: Cross-examine the Page 6 Roadmap table against Pages 9–15 step titles and phase badges. Step numbers, titles, and operations must match 100% with zero discrepancies.
     2. **Garment DNA vs. Diagram Contradiction Gate**: Inspect every step diagram and bullet text against the locked DNA from Phase 0. If the garment is side-zip / seamless flat front, ensure zero buttons, zero buttonholes, and zero fly fronts are drawn or described in diagrams. If Tailornova vector artwork contains generic options (e.g. buttonhole on left, hook & eye on right), the generic contradiction MUST be purged and the authentic closure centered.
     3. **Table Geometry & Number Integrity Gate**: For trousers, ensure Table 1 has no BUST column. Verify that all body and finished garment measurements fit comfortably within column widths with zero text wrapping, zero Russian/corrupted glyphs, and zero fraction truncation.
     4. **Visual Typography & Typo Hunt**: Inspect bottom protocol cards to guarantee clean TTF rendering without encoding artifacts or corrupted bullet symbols. Scan all headings and captions across all pages for spelling typos (e.g. 'Left' vs 'Lett').
10. **Rule 10: The Master Couturier Persona & The 5 Sacred Tailoring Questions (بروتوكول عقلية المعلم الخياط)**:
    - **Couturier Persona Law**: The assistant must NEVER operate simply as a passive script-runner. On EVERY model (past, present, and future), the assistant MUST adopt the rigorous persona of a **Master Bespoke Couturier & Patternmaker (المعلم الخياط المحترف)**.
    - **Online Verification & Industry Standards**: For any tailoring technique, closure construction, pocket insertion, or seam sequence, the assistant must conduct online technical research (`search_web`) or verify authoritative tailoring literature before drafting code.
    - **The 5 Sacred Master Tailor Questions (الأسئلة الخمسة الإلزامية صفحة بصفحة)**:
      Before declaring ANY garment, page, or booklet ready, the assistant MUST critically ask itself:
      1. **Measurements & Ease (واش القياسات صحيحة ومنطقية؟)**: Is the ease mathematically and anatomically appropriate for the fabric and silhouette? Are body measurements vs. finished garment dimensions 100% coherent? Are all table cells, inches, and fractions fully visible with zero column-width clipping?
      2. **Technical Instructions (واش النص والتعليمات مفهومين وصحيحين؟)**: Does the text describe the EXACT piece being assembled without generic boilerplate? Are instructions 100% synchronized with the Page 6 Roadmap? Zero typos, zero clipped text, zero missing numbers.
      3. **Engineering Diagrams (واش الرسومات كطابق الباطرون 100%؟)**: Are all drawings strictly representing the actual garment pieces? Have generic/conflicting options (e.g. buttonholes on seamless side-zip pants) been purged and authentic bespoke methods centered? Zero ghost pieces, correct notches, correct seam allowances.
      4. **Visual Photoshoots (واش تصاور الموديل كطابقو الباطرون 1:1؟)**: Does the model's garment match the CAD pattern in waistband, pockets, closures, and drape? Zero stray details that don't exist in the pattern.
      5. **Physical Tailoring Craftsmanship (واش هاد الخدمة صحيحة وتقنية وتقدر تتخيط فـ الواقع؟)**: If a professional tailor took this booklet into an atelier with scissors and fabric, would they execute it flawlessly without getting stuck or ruining materials?
11. **Rule 11: The Multilayer Inspection Framework (4 Couches Motatabi3a - The Gemini Audit Standard)**:
    - **MANDATORY FINAL GATE BEFORE PUBLICATION**:
      The assistant must execute `master_tailor_audit.py` implementing the 4 consecutive inspection layers:
      1. **Couche 1: Math & Spec Cross-Checking (Vérification Handasiya w Hisabiya)**:
         - Any measurement on one page must match all other pages 1:1 (Features vs Measurements vs Inventory vs CAD Specs).
         - Metric-to-Imperial Recalculation ($cm / 2.54 \rightarrow$ nearest 1/8"): Cross-check every row of Table 1. If hips are $87.8\text{ cm}$, recalculate $87.8 / 2.54 = 34.56'' = 34\ 1/2''$. Flag leading-digit truncations immediately (e.g. `14 1/2"` instead of `34 1/2"`).
      2. **Couche 2: Layout & Typography Render Inspection (OCR & Bounding Boxes)**:
         - Inspect every table cell and paragraph for text-clipping, digit truncation, and unrendered characters (`!5/8`, `3г`, `chm`).
         - Detect line overlap collisions and typos (`Left` vs `Lett`).
      3. **Couche 3: Industrial Sewing & Tailoring Protocol Logic**:
         - Assembly Order: Darts before seams, pressing directions toward anatomical center.
         - Roadmap 1:1 Synchronization: Compare Page 6 Roadmap titles word-for-word against step pages (Pages 9–15).
      4. **Couche 4: Visual CAD & Diagram Rigor**:
         - Verify grainlines parallel to selvedge, notches, and fold lines.
         - Purge generic Tailornova contradictions (buttons/buttonholes on seamless side-zip pants).
         - Verify vector QR codes (Page 8) and 3-angle model photography (Page 16).
    - **Embedded Auditor System Persona**:
      `Role: Senior Haute-Couture Technical Auditor & Patternmaker QA Engineer.`
      `Task: Conduct a forensic, pixel-level, and mathematical cross-audit of the sewing instruction booklet and CAD specs before publication.`
      `Gate: Deliverable is REJECTED and MUST NOT be presented until all 4 layers pass with 100% Zero Defects.`

### 0. The Golden Read-First Principle ("System Khasso Yaqra 3aad Ya'raf Chno Ydiir")
**MANDATORY CORE LAW**: In EVERY single phase of the pipeline, the assistant and all scripts MUST **READ and PARSE the authentic source files first** before writing a single line of code, text, table, or diagram:
1. **Strict 1:1 PatternFast/Tailornova Garment Model Recipe Matching**:
   - Before drafting any booklet or instructions, the system MUST inspect the EXACT components selected in PatternFast:
     - Waistband: `Elastic Casing` vs `Contoured Waistband` vs `Facing`.
     - Closure: `No closure / Pull-on` vs `Fly Zipper` vs `Side Zipper` vs `Button Front`.
     - Pockets: `Inseam Side Pockets` vs `Slanted Welt` vs `Patch Pockets` vs `No Pockets`.
     - Pleats/Darts: `Gathered` vs `Darts` vs `Front Pleats`.
   - **ZERO Contamination**: If the pattern has NO zipper, the instructions and diagrams MUST NEVER mention or draw a zipper fly! If the pattern has NO darts, NEVER mention darts!
2. **Category-Driven Size Chart Ease Engine (MANDATORY)**:
   - For **Pull-on / Elastic Waist Bottoms**:
     - Standard Letter Range: `XXS, XS, S, M, L, XL, XXL` (mapped to US 00–18).
     - Standard Grading Step: Exactly `5 cm (2 in)` per size on Body Waist and Body Hip.
     - **MANDATORY Hip Ease**: `Finished Hip = Body Hip + (10 to 14 cm)`. This is mathematically required so the garment pulls over hips without a zipper!
     - **MANDATORY Relaxed Waist**: `Finished Relaxed Waist = Body Waist - (2 to 4 cm)` so elastic grips snugly.
   - For **Tailored / Structured Bottoms (With Zipper)**:
     - Hip Ease is `3 to 5 cm` only.
3. **Content-Based Semantic Search Rule (Zero Hardcoded Page Indices Across All Phases)**:
   - NEVER assume or hardcode specific page numbers (e.g. "page 2 has the pieces", "page 3 has specs", "step 2 is always welt"). Pattern page layouts vary drastically across garments (jackets vs coats vs pants vs dresses).
   - In EVERY phase, the parser must scan all pages of the document dynamically using semantic keyword anchor matching:
     - Search `Pattern pieces:` to locate the pieces list wherever it falls.
     - Search `Pattern Specs` or `Pattern Measurements` to locate the measurements table.
     - Search `Cutting And Marking Instructions` or `Pattern Layout` to locate the yardage and nesting layouts.
     - Search `Step \d+:` to extract instruction text and diagrams in true chronological sequence.
4. **Never Assume or Fill Blindly (Mamnou' Ta'mar lkhwa)**: Never invent measurements, pieces, allowances, or techniques. Always extract the real ground-truth data from the anchor-located sections.
5. **Phase 1: Read Garment Anatomy First**: Read the exact component IDs, silhouette, closures, and pockets directly from the API response before formulating the design brief or flat sketch.
6. **Phase 2: Read Pattern Specs First**: Run `extract_booklet_data_template.py` on the downloaded pattern PDFs to inspect:
   - The EXACT piece names and cut counts.
   - The EXACT finished measurements per size (Waist, Hips, Inseam, Leg Opening).
   - The EXACT seam allowance and hem allowance.
7. **Phase 3: Read Source Instructions First**: Read the exact step flow and original vector SVG diagrams from Tailornova/PatternFast. Match them piece-by-piece to the pattern before drafting booklet pages.
8. **Phase 4: Synthesize Based on Real Data Only**: Only after reading and verifying all data sources does the system generate `design_manifest.json` and compile the booklet PDF.

- **Mandatory Garment Manifest Architecture (`design_manifest.json`)**:
  - NEVER hardcode garment titles, garment types, or specific design features (e.g. "Colette", "Wide-leg", "Vest") inside the booklet generator script.
  - ALWAYS generate and read a project-level `design_manifest.json` defining `garment_name`, `garment_type` (Trousers, Skirt, Jacket, Dress, etc.), `silhouette`, `closure`, `pockets`, and `palette_theme`.
  - All covers, running headers, footers, overview paragraphs, and page 16 styling sections MUST dynamically derive from this manifest.
  - **Procedural Subtitle Generation Rule (La tasta'mil jomal mahfouda)**:
    - Never hardcode fixed sentences for the cover subtitle.
    - The assistant must dynamically synthesize the subtitle for the specific garment by analyzing its real components (Fit/Rise + Silhouette + Category + Front/Dart details + Pocket types + Closure mechanism).
    - Example of synthesis logic:
      - Trousers with darts and welt: "[Rise] tailored [leg cut] trousers with [front details], [pocket types], and [closure]."
      - Jacket: "[Fit] [length] jacket with [neckline/collar], [pocket style], and [closure]."
      - Dress: "[Silhouette] [length] dress with [neckline], [sleeves], and [waist/skirt details]."
    - Store the synthesized result dynamically in `manifest["subtitle"]` so ReportLab renders it automatically.
  - **Page 2 Dynamic Architecture Rule (Welcome & Flat Sketch)**:
    - **Authentic Server Flat Sketch (Zero Token Waste)**: Never redraw or generate the flat sketch from scratch using AI or prompts. The technical flat sketch ALREADY exists on the PatternFast server (`svgFront` and `svgBack` returned directly by the API `/categories/{code}/update-design`). The script must automatically combine and render them directly to a transparent, tightly cropped 300-DPI PNG (`flat_sketch_transparent.png`) in under 2 seconds.
    - **Dynamic Welcome Intro**: The welcome paragraph on Page 2 must be procedurally constructed from `{manifest['full_title']}`, `{manifest['suggested_fabrics']}`, `{manifest['silhouette']}`, and its specific front/back closure details. Never reuse older garment text.
    - **Dynamic Design Features & Exact Hem Depth**: The bulleted list under "Design features" must read directly from `manifest["features"]` array so it exactly reflects the actual garment components. Always verify the true hem depth against the pattern spec (e.g. `2 cm (3/4 in)` for pants) instead of hardcoding arbitrary values like 3 cm.
    - **What is Included List**: Include all real formats provided: multi-size PDFs (A4, US Letter, A0 Copyshop), layered PDF functionality, projector capability, and the interactive video hub reference.
    - **Conditional Dynamic Metadata Callout Box (Only if Space Permits)**:
      - The script must measure available vertical space below "What is included" (`y_inc - bottom_margin`).
      - ONLY if remaining space >= 60 pt: render a clean, subtle callout box with dynamic garment metadata derived from the manifest:
        - `Skill Level`: dynamically set based on complexity (e.g. beginner for elastic waist / no zipper; confident beginner/intermediate for fly zipper, welt pockets, or tailored collars).
        - `Estimated Sewing Time`: realistic estimate based on garment type (e.g. 2–3 hours for skirt/tote, 4–6 hours for tailored trousers, 7–9 hours for lined jacket/coat).
        - `Drafting Height & Adjustment Note`: e.g. "Drafted for height 168 cm (5'6\") with lengthen/shorten lines."
      - If vertical space is tight (< 60 pt), do NOT render the box to avoid page overflow.
  - **Page 3 Dynamic Architecture Rule (Before You Begin Checklist)**:
    - **Zero Hardcoded Checklist Sentences**: Never paste static checklist sentences from past projects. The checklist points must be procedurally assembled based on the active garment's real construction:
      - `Size & Ease Point`: Synthesize dynamic text citing the garment's target ease (e.g. for trousers: waist ease 1.5–2.5 cm and hip ease 4–6 cm; for jackets: bust ease 8–12 cm; for knits: negative/zero ease). Never mention pleats if the pattern has darts, and vice versa.
      - `Length Check Point`: Dynamically reference the specific adjustment zone for that garment type:
        - Trousers: "along the knee line on Pants Front and Back".
        - Jackets/Coats: "between the waist and hem, or along the sleeve bicep line".
        - Skirts: "along the lengthen/shorten line at mid-thigh".
      - `Markings Point`: Dynamically list ONLY the markings that truly exist on the pattern pieces (e.g. front waist darts, welt pocket lines, notches, zipper stop circles). Do NOT list pleats, vents, or collar notches if the garment has none.
      - `Allowances Point`: Read the exact seam allowance (e.g. `1 cm / 3/8 in`) and exact hem allowance (e.g. `2 cm / 3/4 in`) from the real pattern specs. Never guess or write ranges like "2 to 3 cm".
      - `Key Techniques Point`: Dynamically highlight the 1–2 most critical steps of that specific garment (e.g. "welt pockets and fly zipper" for tailored trousers; "collar stand and set-in sleeves" for blazers; "invisible zipper and neckline facing" for dresses).
      - `Pressing Box`: Dynamically mention only the features present (e.g. "Press every dart, seam, and pocket" instead of mentioning non-existent pleats).
  - **Page 4 Dynamic Architecture Rule (Size Charts & Measurements)**:
    - **Category-Adaptive Body Measurement Columns**: Never display irrelevant body measurements.
      - **Bottoms (Pants, Trousers, Shorts, Skirts)**: Columns MUST be `[US SIZE, WAIST cm, HIPS cm, WAIST in, HIPS in]`. Do NOT include Bust columns for bottoms as it confuses buyers.
      - **Tops, Jackets, Coats, Vests**: Columns MUST be `[US SIZE, BUST cm, WAIST cm, BUST in, WAIST in]`.
      - **Full-Body Garments (Dresses, Jumpsuits, Overalls)**: Columns MUST be `[US SIZE, BUST cm, WAIST cm, HIPS cm, BUST in, WAIST in, HIPS in]`.
    - **100% Real Pattern Measurements (Finished Garment Table)**:
      - NEVER reuse measurement numbers from previous project files or hardcoded arrays.
      - Values in the Finished Garment Measurements table MUST be dynamically calculated directly from the active garment's real PatternFast specs (`booklet_size_data.json` extracted from the actual generated pattern files):
        - For pants: read real `Waist * 2`, `Hips * 2`, real `Bottom opening * 2` (leg opening), and real `Inseam length` / `Pants side seam length`.
        - For jackets/tops: read real `Bust * 2`, `Waist * 2`, `Center back length`, and `Sleeve length`.
        - For skirts: read real `Waist * 2`, `Hips * 2`, and `Skirt length`.
    - **Dynamic Footnote Synthesis**:
      - Procedurally generate the footnote based on the garment's real features:
        - If pants/skirt with pleats: "Finished measurements measured with pleats closed."
        - If pants/skirt without pleats: "Finished measurements include design ease for a comfortable fit."
        - Waistband height: cite the exact height from specs (e.g. `3 cm / 1 1/8 in`).
        - Never mention pleats if the pattern has darts, and vice versa.
  - **Page 5 Dynamic Architecture Rule (Fabric & Notions)**:
    - **100% Real Piece Numbers (Zero Blind Guessing)**:
      - NEVER hardcode piece numbers for lining (e.g. "Pieces 6 and 9") or interfacing (e.g. "Waistband 3, Fly 7, Welt 8").
      - The script MUST dynamically parse the active pattern's piece list:
        - Identify all pieces designated as `LINING` (e.g. for Audrey: Pieces 7, 8, 10, 11) and reference their exact numbers.
        - Identify all pieces designated as `FUSIBLE INTERFACING` (e.g. for Audrey: Pieces 3, 6, 9) and reference their exact numbers.
    - **Authentic Fabric Requirements (Smart Geometric Sanity Logic)**:
      - NEVER blindly trust raw algorithmic yardage numbers from Tailornova/PatternFast.
      - Calculate and verify the true fabric requirement using physical garment geometry for both standard fabric widths:
        - **60" (150 cm) Width**: Check if largest pieces (e.g. Front & Back) can sit side-by-side or must be stacked along the grainline. Account for waistband, pocket bags, hem allowances, and a +10% fabric shrinkage/cutting buffer.
        - **45" (115 cm) Width**: Pieces must almost always be stacked lengthwise. Calculate: `(2 × Garment Outseam/Length) + Waistband/Facings + Hem + 10% Buffer`.
      - Ensure yardage scales logically across size tiers:
        - Tier 1: Sizes `US 00–06` (XXS–S)
        - Tier 2: Sizes `US 08–14` (M–L)
        - Tier 3: Sizes `US 16–22` (XL–4XL)
      - Provide both Metric (Meters to nearest 0.1 m) and Imperial (Yards to nearest 1/8 yd).
      - If the garment requires pocket lining or fusible interfacing, compute and cite the exact yardage required separately.
    - **Dynamic Notions List**:
      - Read closure requirements directly from the active garment's specs:
        - Zipper: cite the real `Fly zipper length` from specs (e.g. `23 cm / 9 in` or `18 cm / 7 1/8 in`).
        - Buttons: cite the real button count and diameter (e.g. 1 button of 10 mm / 3/8 in for pants; 6 buttons for jackets).
        - Elastic: cite waistband elastic width if an elastic band was selected.
        - Thread and specialized tools (zipper foot, buttonhole foot, tailor's ham, pressing cloth).
  - **Page 6 Dynamic Architecture Rule (Pattern Pieces & Cutting Table)**:
    - **100% Authentic Pattern Pieces Table**:
      - NEVER copy a static 10-piece table from an older garment.
      - The script MUST dynamically parse the active pattern's Page 2 specification sheet (`Pattern pieces:`) and generate the exact table rows:
        - Exact piece index (`1` to `N`).
        - Exact piece name as printed on the pattern (e.g. `PANTS FRONT`, `POCKET FACING`, `POCKET BAG BIG LINING`).
        - Exact material (`Main fabric`, `Lining fabric`, `Fusible interfacing`).
        - Exact cut count (e.g. `2 (a mirrored pair)`, `1 on fold`, `1 + 1 interfacing`).
    - **Dynamic Cutting Tips**:
      - Procedurally generate tips based on the active piece list:
        - If pieces require interfacing: dynamically reference their exact real numbers (e.g. Pieces 3, 6, 9).
        - If asymmetric cuts exist (e.g. `CUT ON LEFT FRONT` for fly extension): cite the exact piece number where the note appears.
        - Pocket welt reinforcement: cite exact welt piece numbers and real slit dimensions.
    - **Dynamic Sewing Order at a Glance (9-Cell Grid)**:
      - Procedurally populate the grid using the active garment's real step names:
        - If garment has darts without pleats: Cell 1 MUST be "Front & back waist darts" (NEVER mention pleats).
        - Cells 2 to 9 must reflect the exact sewing sequence of the active project (e.g. Pockets, Zipper fly, Inseams, Crotch, Side seams, Waistband, Hem, Finishing).
  - **Page 7 Dynamic Architecture Rule (Pieces & Markings)**:
    - **Authentic Pieces Overview Vector Diagram (Zero Missing/Blank Images)**:
      - NEVER leave the diagram area blank or rely on hardcoded missing image paths.
      - The script MUST locate and extract the authentic pattern pieces layout vector graphic directly from the downloaded instructions PDF (searching dynamically for the overview page by scanning for multiple piece names e.g. `PANTS FRONT`, `PANTS BACK`, `WAISTBAND`, `MAIN FABRIC`).
      - Automatically crop out the Bootstrap/PatternFast header logo using vector drawing bounding boxes (`d['rect']` where `y0 > 120`).
      - Render and save the clean vector graphic at 300 DPI (`pattern_pieces_overview.png`).
      - Draw a clean `#F5F2EF` container with `#E2DDD5` subtle border around it, fitting it harmoniously on the left side of Page 7 (`width=245 pt`, `height=410 pt`, `keepAspectRatio=True`).
    - **100% Dynamic Pattern Pieces Key (Pieces 1 to N)**:
      - NEVER hardcode 10 pieces or copy names from a past project.
      - The side legend ("Pattern pieces key") MUST be populated directly from the parsed pattern pieces list (`pieces_list`) extracted from the source PDF's `Pattern pieces:` anchor:
        - Automatically format each piece entry: bold piece number, clean title-cased name, and cut count/material indicator.
        - Support any number of pieces ($1$ to $N$, whether $8$, $11$, $14$, or $20$) dynamically without layout overflow.
    - **Dynamic Markings Explanation**:
      - Procedurally explain ONLY the markings that actually exist on the active garment's pieces:
        - **Darts**: If the garment has waist/bust darts, explain: `"Dart fold lines & tips: Fold along center line, align legs, and sew tapering precisely to the punch dot."`
        - **Pleats**: If the garment has pleats, explain: `"Pleat fold lines: Fold along the indicated arrows toward the side seam / center front as directed."`
        - **Zipper Fly**: If fly front zipper exists, explain: `"Center front line & Circle stop: Marks the finished center front and the exact bottom stop point of the zipper."`
        - **Welt Pockets**: If welt pockets exist, explain: `"Welt placement lines: Mark the precise parallel stitching lines and triangular cut lines for the welt opening."`
        - **Button & Buttonhole**: If closure includes buttons, explain: `"Button markings: Crosses indicate button placement; horizontal/vertical bars mark buttonhole length."`
        - **Universal Markings**: Always explain Notches (small triangles/ticks for seam matching), Grainline arrows (parallel to fabric selvage), and Hem foldline (exact finished fold depth).
      - NEVER display explanations for markings that do not exist on the current garment (e.g. no pleat explanations when only darts are present).
  - **Page 8 Dynamic Architecture Rule (Helpful Video Guides Hub)**:
    - **100% Dynamic Feature-to-Video Selection (Zero Irrelevant Techniques)**:
      - NEVER copy-paste hardcoded video titles (e.g. NEVER show "Sewing front pleats & darts" when the garment has only darts and no pleats).
      - The script MUST inspect the active project's `design_manifest.json` and parsed pieces/steps to dynamically select the 4 key tailoring techniques:
        - If waist darts without pleats: video title MUST be `"Sewing waist darts"`.
        - If pleats exist: `"Sewing front pleats"`.
        - If slanted side pockets exist: `"Slanted front trouser pockets"`.
        - If single-welt pocket exists: `"Single-welt back pockets"`.
        - If fly front zipper exists: `"Trouser zipper fly & waistband"`.
        - If jackets/blazers: select tailored collar stand, welt pockets, set-in sleeves, or lining bagging.
        - If dresses: select invisible zipper, neck facings, or gathered skirts.
    - **Dynamic Step Cross-Referencing (Never Guess Step Numbers)**:
      - NEVER hardcode `"Used in Step X"` strings.
      - The script MUST dynamically query the actual chronological step sequence generated for Pages 9–16:
        - Finds the exact step number(s) where that technique is taught (e.g. scans for keyword matches like "dart", "pocket", "fly", "welt").
        - Automatically formats the subtitle: `"Used in Step {found_step}"` or `"Used in Steps {step_a} and {step_b}"`.
    - **Functional Multi-Format Links (Clickable + QR)**:
      - Every video card must feature a sharp ReportLab vector QR code (scannable via mobile camera) pointing to the verified YouTube URL.
      - Every card must feature a prominent, clickable blue/accent link `"Watch the video"` directly opening the video in browser when clicked inside the PDF.
    - **Dynamic Header & Footer Text**:
      - Intro text dynamically injects `{manifest['garment_type']}`: `"Short video tutorials for the key tailoring techniques used in these {manifest['garment_type'].lower()}..."`
      - Footnote dynamically cites `{manifest['full_title']}`: `"Videos are made by independent creators and may use slightly different seam allowances. Always follow the measurements in this guide for the {manifest['full_title']}."`
  - **Phase 1.5: Custom Steps & Pattern Gap Architecture (Invented & Missing Techniques)**:
    - **The Gap Detector**: When a garment features a design component, accessory, or pocket invented or customized by the designer that does NOT exist in Tailornova source instructions (e.g. 3D cargo pockets, custom belt sash, waistband tabs, ankle cuff slits):
      - **Manifest Declaration (`custom_steps`)**: Declare the technique cleanly in `design_manifest.json` under `"custom_steps"` array:
        `{"step_title": "...", "insert_after": "...", "target_pieces": [...], "cad_template": "...", "instructions": [...]}`.
      - **Procedural CAD Panel Drafting**: Call `instruction-diagram-studio\scripts\draft_missing_panel.py` to draft clean, true-to-scale vector panels with right/wrong side shading (`#E6E6E6` / `#FFFFFF`), dashed stitch lines, curved press arrows, and `#F5F2EF` Gold Standard framing.
      - **Seamless Step Insertion**: The booklet generator reads `manifest["custom_steps"]`, chronologically injects them into the instruction sequence at the exact specified position, assigns a sequential step number, maps the authentic piece citations, and updates the Page 6 "Sewing order at a glance" grid dynamically.
  - **Pages 9–15 Dynamic Architecture Rule (Chronological Sewing Instructions)**:
    - **The Sacred First-Source Rule (Al-Masdar Al-Awwal)**:
      - If the authentic instruction diagram already exists in Tailornova/PatternFast, **ALWAYS USE IT DIRECTLY** (cleaned, cropped, and framed into Argon Gold Standard #F5F2EF container).
      - ONLY if a bespoke technique does NOT exist (or has a fatal model mismatch/contradiction) do you draft it procedurally via CAD!
      - NEVER draw crude synthetic polygonal shapes in Python/Matplotlib/PIL when official vector artwork exists.
    - **Generic Template Contradiction Hunter**:
      - Inspect authentic Tailornova diagrams for generic template reuse bugs (e.g. using a skirt/dress center-back zipper graphic saying "pin back sections together" on a side-zip trouser). Always correct labels to reflect real garment anatomy ("pin side seam together below zipper").
    - **100% Faithful Step Extraction from Source Instructions (Zero Inventions & Zero Leftovers)**:
      - NEVER copy sewing step texts from another pattern or hardcode non-existent features (e.g. NEVER write "Sew the front pleats" when the pattern has darts; NEVER describe pocket types not in the pattern).
      - The script MUST dynamically parse the source instructions PDF/JSON by locating `Step \d+:` anchors:
        - Extract the authentic title (e.g. `Sewing Darts On Pants`, `Sewing Slanted Welt Pockets`, `Sewing Zipper Fly`, `Sewing Pockets`, `Sewing Pants Inseams`, `Sewing Crotch Seam`, `Sewing Pants Side Seams`, `Setting Waistband`, `Hem`).
        - Extract the authentic step instructions text directly from the source.
    - **Dynamic Step Header & Pieces Cited (100% Authentic Piece Mapping)**:
      - NEVER guess or hardcode piece numbers in the step header context or body text (e.g. NEVER cite "Pocket Lining (6)" when Piece 6 is actually "Fly Interfacing").
      - The script MUST dynamically map the pieces required for each step by cross-referencing the parsed step topic with the authentic pattern pieces list:
        - Slanted Front Pockets: MUST cite `Pieces 1, 4, 7 and 8` (Pants Front, Pocket Facing, Pocket Bag Big Lining, Pocket Bag Small Lining).
        - Back Welt Pockets: MUST cite `Pieces 2, 9, 10 and 11` (Pants Back, Back Pocket Welt, Back Inner Pocket Bag, Back Outer Pocket Bag).
        - Zipper Fly: MUST cite `Pieces 1, 5 and 6` (Pants Front, Fly Facing, Fly Interfacing).
        - Waistband: MUST cite `Piece 3` (Waistband main + interfacing).
      - Step header context line MUST accurately state: `"Pieces [mapped numbers] · pictures 1–N"`.
      - All mentions of pieces within the instructional text MUST cite the authentic name and number matching the pattern pieces key.
    - **Mandatory Linkage with Argon Gold-Standard Studio Panels (Zero Number Mismatch & Zero Double-Numbering)**:
      - Each sewing page MUST embed its corresponding clean, 300 DPI framed vector panel from `instruction_panels_studio/` (`Step_1_Darts.png`, `Step_2_Welt_Pocket.png`, etc.) with `#F5F2EF` container and bold Poppins numbers (`1.`, `2.`, `3.`, `4.`).
      - NEVER allow double or overlapping numbers (e.g. bold numbers colliding with existing numbers inside the raw vector diagram). Clean and suppress internal duplicate numbers so only the clear, prominent outer panel callouts remain.
      - **100% Exact Match Between Text Picture Citations and Panel Numbers**:
        - Every `(picture N)` cited in the instructional text MUST have an exact corresponding numbered sub-panel in the diagram.
        - If the text cites `pictures 1–2`, the panel MUST contain exactly sub-panels `1.` and `2.`.
        - NEVER have stray sub-panel numbers (e.g. 3. and 4.) displayed in the diagram that are never mentioned or explained in the text.
        - Single-diagram steps must be presented as a single clean framed panel without arbitrary phantom numbers.
      - **100% Strict Diagram-to-Step Content Alignment (Zero Mismatched Panels)**:
        - NEVER place a crotch seam or inseam diagram on a Side Seams page, and vice versa!
        - The script MUST dynamically verify that each diagram panel strictly portrays the operation being taught on that page:
          - Side Seams page MUST display the outer side seam assembly diagram with pins along outer leg edges.
          - Crotch/Inseam page MUST display the inner leg / crotch curve reinforcement diagram.
          - Pocket steps MUST display the respective pocket construction diagrams (welt vs slanted slash).
          - Waistband step MUST display waistband folding and attachment diagrams.
          - Hem step MUST display hem turning and blind/machine stitching diagrams.
      - **One Major Step Per Page Rule (Zero Squashed / Double-Step Pages)**:
        - NEVER squeeze two major tailoring operations onto a single page (e.g. NEVER combine Waistband and Hem on the same page).
        - Waistband attachment (Step 7) MUST have its own dedicated page (Page 14) with full-size 5-panel diagram and beginner tip.
        - Hemming (Step 8) MUST have its own dedicated page (Page 15) with clean hemline diagram and exact hem depth read from the pattern spec (`2 cm / 3/4 in`, never vague ranges like "2 to 3 cm").
        - This preserves the perfect 16-page luxury rhythm: Cover (1), Welcome (2), Checklist (3), Sizes (4), Fabric (5), Cutting (6), Pieces (7), Videos (8), Steps 1–7 (Pages 9–15), Final Page (16).
    - **Context-Aware Video Help & Beginner Tips (Rule 15 - The Hardest Steps Require a Tip Box)**:
      - Video Help line ONLY appears if a relevant video exists for that specific technique (referencing Page 8).
      - Beginner Tip Box is MANDATORY for all high-risk tailoring techniques:
        - **Single-Welt Pocket (Highest Risk)**: MUST include `"Beginner tip: the trickiest step"` detailing the 45° corner slash technique: *"When slashing the pocket opening, clip diagonally into the corners right up to the last stitch without cutting the thread. Too shallow causes puckers; cutting the stitch causes the pocket corner to fray."*
        - **Fly Zipper (High Risk)**: MUST include `"Beginner tip: perfect zipper curve"`: *"Keep the center front seam firmly machine-basted shut until after you have topstitched the curved J-stitch. Make sure the loose fly shield is folded completely out of the way so it is not accidentally caught in the curved topstitching."*
        - **Darts**: MUST instruct to tie thread tails by hand at the tip rather than backstitching.
        - **Waistband**: MUST instruct how to ease the body into the waistband without tucks.
  - **Page 16 Dynamic Architecture Rule (Enjoy Your Garment & Care)**:
    - **Dynamic Garment Title**: Kicker `"Y O U   M A D E   I T"`, Title `"Enjoy Your {manifest['garment_name']}!"` (or `{manifest['full_title']}`).
    - **Dual Front & Back Model Showcase (Zero Mismatched or Duplicate Photos)**:
      - NEVER display the same photo twice side-by-side!
      - **CRITICAL GARMENT-MATCH AUDIT**: The system must NEVER pick a random or outdated photo from another garment model (e.g. NEVER place leisure elasticated pants with flap pockets next to a tailored dart pants photo).
      - Left image MUST be the authentic Front view photo of THIS EXACT garment; Right image MUST be the authentic Back view photo showing the rear details (back darts, welt pockets, back yoke).
      - **Automatic Fallback Rule**: If an authentic back view photo of THIS EXACT garment does NOT exist yet, the system must NEVER guess or use another garment's photo. Instead, it must automatically fallback to embedding the authentic clean technical flat sketches (`flat_sketch_front.png` on the left, `flat_sketch_back.png` on the right, or authentic front photo + authentic back flat sketch) so the visual presentation is 100% faithful to the pattern pieces.
    - **Dynamic Styling Ideas (Zero Forbidden Feature Mentions)**:
      - NEVER mention design features that do not exist (e.g. NEVER mention "double pleats" on a garment with darts; NEVER mention "belt loops" if not drafted).
      - Procedurally generate 3–4 styling recommendations strictly tailored to `{manifest['garment_type']}`, `{manifest['silhouette']}`, and real waist/pocket details:
        - Pants with darts: *"Tucked in with a fine-ribbed cream knit top or silk blouse to showcase the clean high waistline, front darts, and tailored waistband."*
        - Pants casual: *"With a relaxed linen button-down shirt and leather loafers for effortless office-to-weekend tailoring."*
        - Seasonal: *"Sewn in brushed wool twill for autumn and winter, or in washed heavy linen for warm summer days."*
        - Layering: *"Paired with a cropped cardigan or structured blazer that hits right at the high waist."*
    - **Dynamic Fabric Care**:
      - Care instructions must strictly match `{manifest['suggested_fabrics']}` (e.g. Wool: dry clean or gentle hand wash cold with wool detergent, lay flat to dry, press with steam cloth; Linen/Cotton: machine wash gentle, warm iron while damp).
    - **Support & Store Branding**:
      - SewLuxePatterns Etsy shop support box with friendly customer service guarantee, review invitation, and copyright protection notice.

## Inputs (ask only for what is missing)
- Garment name.
- Pattern files: the user sends the A4 zip only (A0 and US Letter exist on their side; the booklet always lists A4 · US Letter · A0). Each size = separate PDF from PatternFast.
- Source instructions (Tailornova ZIPs with steps.md + SVG diagrams, or a PDF) = technique source only, often WRONG for the real pattern or missing a technique (e.g. no collar step). Write missing techniques by hand and draw their diagrams.
- Technical flat sketch (front + back) and model photo (white studio background). If the model photo is missing, build the cover and last page with the sketch and say so; rebuild when he sends the photo (keep the photo path as a parameter of the build script).
- Do NOT need: PatternFast "Pattern specs"/"Body specs" PDFs (often from another design), size-chart screenshots (body sizes are inside each pattern file).
- A reference booklet (e.g. the Elsie / Vivienne jacket) = design reference only. READ IT FULLY (every page at readable resolution, not only a low-res montage) and list its layout elements, boxes, tips and per-step features before building; reproduce the style, never its content.
- If the garment needs a part the pattern does not contain (e.g. a turtleneck collar as a rectangle), the booklet adds it: a piece number, a cutting table per size computed from the pattern (e.g. neckline length + 2 x seam allowance), a piece-figure entry, and its own steps and diagrams. The sketch must then show it: redraw the sketch on the same canvas and stroke as his original (front large + back small, 1800x1800) and give him the image.

## Hard rules (from Client Issues Log + Booklet Redo List)
1. Pattern files are the truth. Check every piece, number, name, cut count, mark, seam allowance and hem against the pattern before writing. Source instructions are often wrong (e.g. "flap pocket" when pattern has a welt, "convertible collar" when pattern has a stand, a center back seam when the back is cut whole, darts the source forgets, wrong hem depth, cuff steps for a pattern with no cuff).
2. Same piece numbers and names as the pattern sheet everywhere.
3. Every step must be sewable in that order (no step closes an edge a later step needs).
4. Hidden/built-in pieces get their own explanation + diagram.
5. Seam allowance stated only after measuring it; one value per measurement across the whole booklet.
6. Every mark (notches, lines, circles, boxes, FOLD labels, stray labels such as ZIP on a garment without zipper) explained somewhere.
7. Every "picture N" reference has a real numbered picture; no cut-off sentences; pages in order; the page number printed on the cover for the videos must match the real page.
8. Pictures must match the garment (same collar, button count, pockets, one-piece vs seamed back). Never reuse a drawing or panel that shows a different garment; cut such panels out.
9. Always include "Before You Begin" checklist (test square, size choice with ease, length, markings, allowances, scrap test, trickiest technique tip) and finished garment measurements.
10. Hem suited to fabric (wool coat = folded hem, not narrow hem).
11. NEVER any reference to internal tools, PatternFast, or Tailornova: text, images, file metadata. grep the final PDF text (and `strings` for metadata). No channel names for videos, and no leftovers from the previous garment's name.
12. Correct level: Beginner / Confident beginner / Intermediate.
13. **Thick fabric = size-up note, always.** Whenever the garment is made in a thick fabric (pre-quilted fabric, coating, boiled wool, fleece, sherpa, heavy sweater knit, etc.), the "Choose your size" line in Before You Begin must say: if the fabric is thick (for quilted: more than 5 mm / 3/16 in) or the garment will be worn over a warm sweater, choose one size up. Also add a fabric-specific tip box (e.g. for quilted: walking foot, 3-3.5 mm stitch, trim batting out of seam allowances, clips not pins, press through a cloth without flattening the quilting) and repeat "trim the batting" in the relevant steps.
14. **Letter sizes table under the body chart, always.** Directly under the Body measurements table on the Size Charts page, add a 2-row table (header row in the dark table style with the US sizes, second row on the tint background labelled LETTER) with this mapping: 00 = XXS, 0 = XS, 2 = XS, 4 = S, 6 = S, 8 = M, 10 = M, 12 = L, 14 = L, 16 = XL, 18 = 2XL, 20 = 3XL, 22 = 4XL. Add "Letter sizes are a guide only" in the footnote, and mention "sizes US 00 to 22 (XXS to 4XL)" in What is included. Keep the Size Charts on ONE page (shorten the intro/footnotes if it overflows).
15. **Beginner tip in every difficult step, always.** For each step ask: "what would a beginner get wrong here, and what bad review would it cause?" Every step where the answer is non-trivial (collars, necklines, set-in sleeves, underarm matching, hems on knits, buttonholes, zippers, pockets, plackets, ruffles, linings, bound edges...) ends with a tip box titled "Beginner tip" (the single hardest step of the garment: "Beginner tip: the trickiest step") stating the typical mistake, the visible symptom (wavy, twisted, puckered, too tight), how to avoid it and how to fix it (unpick and re-pin, steam, re-sew slower). 2-4 concrete sentences, no vague advice. Trivial steps (e.g. final press) need no tip. Keep a "Video help:" line wherever a video exists.
16. **Knit/stretch garments:** state the minimum stretch required and a simple stretch test in Before You Begin when the neckline or hem must pass over the head or body (e.g. 10 cm must stretch to 16 cm = 60%); recommend needles (ballpoint/stretch 75/11-80/12), stitches (serger or stretch/narrow zigzag about 3 mm long) and a twin-needle hem; check that neckline length x stretch passes a head (about 56 cm) and flag it to the user if the pattern neckline is too small.
17. **Adaptive Luxury Color Palette System (Anti-Copy-Paste Architecture):**
    **NEVER** use the exact same color palette across all booklets! Each garment receives its own bespoke color identity dynamically selected from the 4 official Haute Couture themes based on the garment's fabric type and color:

    - **Theme 1: L'Édition Parisienne (Parisian Midnight Navy)**
      - `PRIMARY = #162536`, `SECONDARY = #2B4C6F`, `PAGE_BG = #FBFBF9`, `TABLE_HEAD = #162536`, `TABLE_ALT = #EEF3F8`, `RULE_LINE = #D5E0EB`, `TEXT_BODY = #151C24`, `MUTED = #5A6B7C`
      - *Garment Match*: Cool tones, classic tailored blazers, suits, denim, navy garments, crisp outerwear with silver hardware.
    
    - **Theme 2: Atelier Botanique (Imperial Forest Emerald)**
      - `PRIMARY = #1C3831`, `SECONDARY = #365E54`, `PAGE_BG = #FAF9F5`, `TABLE_HEAD = #1C3831`, `TABLE_ALT = #EFF5F2`, `RULE_LINE = #D8E3DE`, `TEXT_BODY = #16221E`, `MUTED = #546A63`
      - *Garment Match*: British heritage wools, tweeds, greens, olive, khaki, country outerwear, structured utility tailoring.

    - **Theme 3: Maison Minimaliste (Couture Noir & Warm Cashmere)**
      - `PRIMARY = #1C1B1A`, `SECONDARY = #7D6C5E`, `PAGE_BG = #FAF8F5`, `TABLE_HEAD = #1C1B1A`, `TABLE_ALT = #F3ECE3`, `RULE_LINE = #E2DDD5`, `TEXT_BODY = #1A1918`, `MUTED = #6E6862`
      - *Garment Match*: The Row / Totême "Quiet Luxury" aesthetic, camel trousers, trench coats, linen dresses, minimalist jackets, monochrome outfits.

    - **Theme 4: Haute Berry & Plum Noir (Bordeaux & Blackberry Tweed)**
      - `PRIMARY = #381822`, `SECONDARY = #613342`, `PAGE_BG = #FAF7F8`, `TABLE_HEAD = #381822`, `TABLE_ALT = #F5ECF0`, `RULE_LINE = #E5D6DC`, `TEXT_BODY = #24161C`, `MUTED = #6E545F`
      - *Garment Match*: Deep wine/plum tweed, berry wool, velvet, rich evening outerwear.

## Reading the PatternFast pattern files
- Pages 1-4 are A4 (test square, piece list, specs). A0 file: pages 5+ are A0 tiles; A4 file: tiles 5+. Tile label "r/c": FIRST number = row. The zip may contain a sub-folder and __MACOSX: flatten it.
- Text on pages 1-3 (`pdftotext`, use -layout to see wrapped cut counts): piece list with cut counts, "Seam Allowance: 1 (3/8 in)", `Size: Height, Bust, Waist, Hips` (body chart for that size), specs such as Waist, (Low) hips, Hemline sweep (circumferences are HALF: multiply by 2), Center back length to hem, Sleeve length (sleeve piece only; a cuff adds its own width), Collar length, Neckline length (when front and back are drawn whole it is the full neckline circumference = front arc + back arc), Front buttons quantity (check every size: it changes for large sizes), zipper length (often a template leftover), placket width.
- Vector data: `pdfplumber` page index 4 contains the WHOLE layout (objects outside the page box are still listed). Curves with linewidth > 4 = cutting outlines; small straight pieces may be `rect` objects with linewidth 5 (add them). Linewidth ~3 curves with >100 pts = stitching line; 2-pt lines = notches/grainlines/fold lines/marks; 70-pt circles = buttons, dart points or ease dots; 6-pt short lines = buttonholes (check orientation: horizontal vs vertical). Notches are also part of the cut outline itself.
- Map outline to piece number: digit labels (also reversed text for rotated labels) - big digits (size >= 40) for the main pieces, smaller sizes (>= 11) for the rest; ignore the "Cut 1/2" digits. Assign each label to the SMALLEST outline that contains it; assign inner marks to the smallest containing outline too. Fallback for unmatched outlines: sort by area; sanity-check swaps (e.g. a thin strip must be taller than wide) for every size.
- Units: 1 pt = 2.54/72 cm. Measure SA = distance stitch line to cut line (KD-tree nearest distance, median), hem = distance at the hem (not the lowest point of a curve). Check which pieces are drawn whole ("Cut 1" symmetric, or a piece with a FOLD label that is already drawn full): tell the user to cut single layer / NOT on a fold. Asymmetric fronts (right/left "Cut 1"): cut single layer, right side up. Sleeve cap length minus armhole lengths = ease (check per size).
- Back neckline arc per size from the stitch line; front arc = spec neckline length minus back (front detection fails on some sizes).
- Collars/stands: compare collar neck-edge length (center to end) with half back neck + front neck arc; they usually end at the center-front mark, not the front edge. Plackets: the CF is the middle of the finished placket.
- Pocket boxes: measure the box (upper/lower or welt/bag lines, 1.5 cm apart), welt/flap sizes, pocket bag SA; check whether the box crosses a princess seam (part of it on the center front) -> sew the princess seam first.
- Fabric: rasterise cut polygons at 1 cm (dilate 1 cell), nest with FFT overlap test (rotation 0/180 only, mirrored copy for cut 2) on 150 cm and 115 cm, trying all orderings of the pieces (one greedy order can be 20% worse); take the running max per size group (00-6, 8-14, 16-22), add ~8%, round up to 0.1 m and to 1/8 yd. Lining and interfacing the same way (interfacing 90 cm wide).
- Pieces figure: draw all pieces for size 12 from vectors with matplotlib (cut line solid #2b2b2b, stitch line grey dashed, marks: grainline arrows, CF/CB dash-dot, ease circles; do not redraw notches already in the outline), number in accent color + name and cut count under each piece (wrap long names on two lines); extra rectangles (e.g. collar) drawn at the same scale.
- Flag to the user (one line each): A0 exports that waste sheets, source-spec PDFs that belong to another design, stray labels printed on the pattern (e.g. ZIP) that the booklet tells buyers to ignore.

## Diagrams
- Reuse source-instruction drawings only when they match: Tailornova SVGs render with headless Chromium (playwright, viewport from the viewBox, page.goto file://, screenshot) because cairosvg is not installable; PDFs: crop at 250 dpi. Trim white margins. Drop or cut out panels that show another garment or a wrong technique. If a crop has no numbers, add "N." in Liberation Sans Bold top-left of each panel.
- Draw new diagrams with matplotlib in the same look: 4x3 in panels (2x2 grid for a 4-picture step), black frame, bold "N." top-left, wavy garment edges, white = right side, #e3e3e3 = wrong side, dashed stitching, Liberation Sans 7.5 pt labels with curved arrows (keep labels clear of arrows), 300 dpi. Note "shown straight for clarity" when simplified. A dart/marking diagram can be drawn straight from the piece vectors. Cross-section panels are the clearest for attaching bands/collars.
- Collar-stand pictures 1-4 from the Elsie booklet can be reused for any rounded mandarin stand.
- Button step: use the technical sketch front (composite RGBA on white).
- Editing the sketch: whiteout the old line, draw new lines on a 4x supersampled RGBA layer in the sketch's own stroke colour and width with round caps, and check a 4x zoom of every junction (no stubs). Keep proportions realistic: a folded turtleneck collar looks right at about 6-7 cm of visual height, not the full finished height.

## House style (Elsie / Odette Vest, approved)
Reference booklet saved locally at: `C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\references\odette_vest\Odette-Vest_Sewing-Instructions.pdf` (16 pages, with all 5 model photos and flat sketch in the same folder).
reportlab (platypus with page templates works well), A4 (`595.28 × 841.89 pt`), margins `51 pt`.
Fonts directory on Windows: `C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts\` (`Poppins-Regular.ttf`, `Poppins-Medium.ttf`, `Poppins-Bold.ttf`, `Poppins-Italic.ttf`, `Lora-Regular.ttf`, `Lora-Bold.ttf`, `Lora-Italic.ttf`).
Colors: accent `#9C4A57`, ink `#262322`, grey `#6b6b6b`, tip/grid tint `#F6EDEB`, table alt row `#FBF7F5`, table header `#262322` with white text, lines `#dcdcdc`, cover bg `#F9F9F9`.
- Cover: accent bar `17 pt` at top; letter-spaced kicker `"SEWING PATTERN · INSTRUCTION BOOKLET"` (Poppins Medium 7.4, accent); garment name Lora 50-58 (first word(s)) + garment type letter-spaced Poppins Medium 16 (e.g. `"Odette"` / `"V E S T"`); Lora Italic 11 two-line description; square model photo `400-430 pt` (Photo 1 Front); accent rule; 4 columns SIZES / LEVEL / SEAM ALLOWANCE / FORMATS (labels Poppins Medium 5.8 accent, values Poppins 8.4); `"HELPFUL VIDEO GUIDES INCLUDED · CLICKABLE LINKS AND QR CODES ON PAGE 8"`; `"SewLuxePatterns"` Lora Italic accent.
- Inner pages: header `"GARMENT NAME · SEWING GUIDE"` left, `"SIZES US 00–22"` right (Poppins 6.6 grey) + line; footer line, `"SewLuxePatterns"` Lora Italic 9.5 accent left, page number Poppins 8.0 grey right.
- Section start: small accent kicker (uppercase letter-spaced Poppins Medium 7.6), title Lora 29, short accent rule `110 pt`.
- Welcome page (Page 2): intro paragraph (Poppins 9.6/14.6), then 2-column row: Flat Sketch on left (`width=250 pt`, `x=51..301`) and `"Design features"` (`Poppins Medium 10.2` accent heading + bullet list at `x=313..544`) on right; below: `"What is included"` bullet list.
- Body Poppins 9.6/14.6; h3 Poppins Medium 10.2 accent; bullets indent 15.
- Step header: accent circle `r=15` with white number (Poppins Medium 12), title Lora 18.5, right-aligned grey context (`"Front and Back · pictures 1–2"`, Poppins 7.4), grey line under. Keep each step (header + text + video line + picture + tip) together on one page.
- Tip box: tint background `#F6EDEB`, `2.2 pt` accent bar on the left, Poppins Medium 8.8 accent title + Poppins Regular 8.6 body.
- Pictures sit in a light-grey framed box, centered, with black inner frame (`1 pt`) around each panel and bold `"1."`, `"2."` top-left.
- Last page (`"Enjoy Your <Garment>"`): final sewing step at top if needed, then kicker `"Y O U  M A D E  I T"` + title `"Enjoy Your <Garment>"` (Lora 29), **two square model photos side-by-side** (`185 × 185 pt` each: Photo 1 Front at `x=57`, Photo 2 Back at `x=303.6`), `"Styling ideas"` bullets, `"Care"`, `"Need help?"` tip box mentioning the Etsy shop, and `© SewLuxePatterns` personal-use footer line.
- Metadata: Title `"<Name> - Sewing Instructions"`, Author/Creator/Producer `"SewLuxePatterns"`, Subject `"<Name> sewing pattern instructions"` (setProducer, then rewrite with pypdf to be sure).

Page order: 1 Cover · 2 Welcome ("Meet the …": intro, sketch + Design features, What is included, skill-level box) · 3 Before You Begin (checkbox table + pressing/fabric tip) · 4 Size Charts (body cm + in to nearest 1/8; LETTER sizes table XXS-4XL; finished measurements cm + in) · 5 Fabric & Notions (suggested fabrics, requirements table 150/115, notions, printing & assembling) · 6 Pattern Pieces & Cutting (table #/piece/cut from/cut, cutting table for any extra piece, cutting tips, "Sewing order at a glance" tint grid) · 7 Pieces & Markings (pieces figure + what every mark means) · 8 Helpful Video Guides (2x3 grid, reportlab QR + clickable "Watch the video") · Sewing Instructions (one step per technique, "Video help:" line and "Beginner tip" box where rule 15 applies) · last page "Enjoy Your …" (photo, styling ideas, care, "Need help?" tip mentioning the Etsy shop SewLuxePatterns, © personal-use line).
Printing text: A4/US Letter tiles numbered like 1/1, 1/2; pages with the same first number form one row; A0 to a copy shop at 100%.

## Video library (verified; reuse)
- Sewing darts: https://www.youtube.com/watch?v=Y3rAmHE7CZs
- Mandarin collar stand: https://www.youtube.com/watch?v=Dz3e7Z9BIEU
- Understitching a facing: https://www.youtube.com/watch?v=iZWStGOHQlg
- Perfect buttonholes: https://www.youtube.com/watch?v=FaX8MWwvlmc
- Easing and setting in a sleeve: https://www.youtube.com/watch?v=9E1_NcRrDB8
- Hemming a curved flounce: https://www.youtube.com/watch?v=m0IfvjDV8tE
- Sewing princess seams: https://www.youtube.com/watch?v=rZvkl2069sQ
- Single welt pocket: https://www.youtube.com/watch?v=Ir9fYOxXSYc
- Welt pocket with flap: https://www.youtube.com/watch?v=XodoUXVsXhY
- Attaching a rounded (flat) collar: https://www.youtube.com/watch?v=2gLmvkiVB1Q
- Sewing a convertible collar: https://www.youtube.com/watch?v=iT_FdKq7x8o
- Sewing a front button placket: https://www.youtube.com/watch?v=DPpF3kAP_oo
- Shortening/installing a separating zipper: https://www.youtube.com/watch?v=cSnesIxeIrM
- Continuous bound sleeve placket: https://www.youtube.com/watch?v=Xsx8CZ8-r1A
- Bias binding on a jacket: https://www.youtube.com/watch?v=MwNoDTTVsJM
- Sewing a turtleneck collar: https://www.youtube.com/watch?v=oUiZ_mZnJB8
- Turtleneck top for beginners: https://www.youtube.com/watch?v=BPc_VA3eqyw
- Sewing knits and stretch fabrics on a regular machine: https://www.youtube.com/watch?v=UvudD3Rqqy4
- Best stitches for knit side seams: https://www.youtube.com/watch?v=f3f0lEBdNTQ
- Hemming knits with a twin needle: https://www.youtube.com/watch?v=jd7sOXVkAN4
New technique: a web search restricted to youtube.com to get URLs, then confirm the video exists with page fetch on `https://www.youtube.com/oembed?url=<video url>&format=json` (curl from the shell is blocked). Show technique names only, never channel names.

## Workflow (keep it lean)
1. Unzip the pattern (A4); read pages 1-3 text of every size into specs JSON.
2. Read the source instructions once and note what does not match the pattern or is missing. Read the reference booklet fully (all pages) and list its features.
3. Extract vector pieces (all sizes), measure SA/hem, marks, special pieces; nest fabric.
4. Crop reusable drawings; draw only the diagrams that are missing or wrong; redraw the sketch if the garment gains a part.
5. Write text + build PDF in one script (reuse the previous booklet's build script as the template); apply rule 15 to every step; render pages at 50 dpi in a montage to check overflow; fix; check one dense page at 80-110 dpi.
6. **Automated Quality Gate & Self-Healing Loop (Mandatory Final Inspection)**:
   - Run `python audit_booklet_quality.py <pdf_path> design_manifest.json audit_report.json`.
   - The auditor automatically evaluates all 39 points (page count, 1:1 Odette cover geometry, cross-garment contamination, real pieces 1..N, mask='auto' transparency, dead whitespace, clickable links, vector QR codes, and dual showcase model matching).
   - If any `[FAIL]` is detected, the assistant MUST read `audit_report.json`, parse the specific failing pages/rules, automatically patch the build script to fix the cause, and re-run until `RESULT: [PASS] 100% PRISTINE` is achieved before showing anything to the user.
7. Deliver the PDF to the user (attach it in the chat). Reply in the user's language: what was corrected versus the source instructions, and anything the user must check (missing format files, source-spec mismatch, A0 layout waste, missing model photo, stray labels, risky neckline).