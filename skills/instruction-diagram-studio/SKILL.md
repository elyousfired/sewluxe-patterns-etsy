---
name: "instruction-diagram-studio"
description: "Master skill for cleaning, repairing, and custom-drafting sewing instruction diagram panels for SewLuxePatterns booklets. Handles SVG parsing, zero-clipped-text bbox expansion, 300 DPI vector rendering, bold Poppins callout numbers (1., 2., 3., 4.), Gold Standard #F5F2EF framing, and procedural CAD drafting of missing steps."
---

# Instruction Diagram Studio (Clean, Repair & Custom CAD Drafting)

Goal: Produce flawless, ultra-clear, 300-DPI sewing step instruction panels for SewLuxe luxury booklets. Eliminates tiny floating graphics, cut-off text/borders, and lazy copy-paste screenshots. Also drafts authentic CAD diagrams from scratch whenever Tailornova lacks instructions for a specific garment feature (e.g., exposed zippers, collarless facings, tailored welt pockets).

---

## Core Principles & Hard Rules

### 0. The Mandatory Studio-First Rule (Dossier Wahd b Wahda)
**STRICT RULE**: In EVERY project, never rush into building the final booklet PDF before the instruction diagrams are ready:
1. **Dedicated Studio Folder**: Always create/use a dedicated folder (`instruction_panels_studio/`).
2. **Clean Folder Rule (Images Finales Seulement)**: The studio folder must strictly contain **ONLY the final verified images** (`Step_1.png` to `Step_8.png`). Delete all scratch/temp SVGs or PNGs immediately.
3. **Build One by One Fast**: Clean or draft every step diagram **ONE BY ONE** using fast, local Python scripts (`clean_instruction_panel.py` / `draft_missing_panel.py`).
4. **Zero Token Waste (Ma takolch les tokens)**: Never run heavy iterative LLM generation loops or repeatedly recompile the whole 16-page PDF to check an image. Write a precise local Python script, run it in 1 shot, inspect the image directly, and move to the next.
5. **Compile to PDF ONLY When All Steps Are Done**: Only after all step diagrams (1 to 8) are verified and finalized in the studio folder do you assemble them into the final `_Sewing_Instructions.pdf`.

### 1. Keep the Authentic Technique Intact (Never Over-Complicate)
- If the original Tailornova/PatternFast instruction exists for the technique: **KEEP IT**. Do not replace familiar illustrated flows with foreign artwork.
- **What to fix**:
  - Remove tiny scaling and cropped screenshot artifacts.
  - Expand viewBox / bounding boxes so zero text is cut off at the top, bottom, or sides (e.g., "circumference of the garment", "turn up", "press along foldline").
  - Render directly from the original vector SVG at 300 DPI using PyMuPDF.

### 2. Gold Standard Framing & Strict Zero-Overlap Typography
Every instruction diagram panel presented to the user or placed into a booklet must strictly adhere to the **Argon Benchmark**:
- **Outer Container**: `#F5F2EF` rounded rectangle (`radius=28` to `32`) with a subtle `#E2DDD8` border (`width=3` to `4px`).
- **Inner Panels**: 1, 2, or 4 distinct white rectangular boxes (`#FFFFFF`) with crisp `4px` black outline (`#000000`).
- **Bold Callouts**: Prominent sequential step numbers in the top-left of each panel: **`1.`**, **`2.`**, **`3.`**, **`4.`** using `Poppins-Bold` (`fill=(0, 0, 0)`).
- **Strict Zero-Overlap Rule (Lktaba ma dakhlaach f rassma)**:
  - **NO TEXT MAY EVER CROSS OR TOUCH ANY DRAWING ELEMENT, SEAM LINE, ARROW, OR PANEL BORDER**.
  - Always place text in open white space with at least 40 px safety margins from borders and lines.
  - Keep instructional labels concise and minimal (like Step 6 & Step 8) — never paste long paragraphs inside diagrams.
  - Use curved leader arrows (`marker-end="url(#arr)"`) that stop cleanly before the text and the target seam.

### 3. Procedural CAD Drafting for Missing Steps (Lkhyat khasso ifham kola haja)
Tailornova frequently generates generic instructions (e.g., shirt plackets with buttonholes for a jacket that actually has an exposed zipper, or omission of collarless neckline facings). When a garment feature is missing or mismatched:
- **YOU MUST CONSTRUCT IT FROM SCRATCH AS REAL GARMENT CAD**:
  - The illustration must look like a real garment part (e.g. realistic collarless jacket neckline, center front zipper, facing unit with shoulder joints, tailor's ham, pressing iron). Any tailor must instantly understand what pieces are being joined.
  - **Right Side of Fabric**: Clean White (`#FFFFFF`).
  - **Wrong Side of Fabric**: Neutral Gray (`#E6E6E6` or `#ECECEC`).
  - **Stitching Lines**: High-contrast dashed line (`stroke=#000000`, `stroke-width=3.2`, `dasharray=10,6`).
  - **Pins**: Silver shaft (`#777777`) with vibrant coral-red ball heads (`#E53935`) and drop shadow, placed perpendicular to seam.
  - **Clip Curves / Notches**: Red V-snips (`#D9534F`) along concave/convex allowances with callout "clip curves / snip seam allowance".
  - **Pressing**: Realistic tailor's ham (`#F4ECE1`) for 3D bust/shoulder molding + modern vector iron pressing seam allowances open ("press open").

### 4. Official API Harvesting & Dual-Box Standard (Mamnou3 Matplotlib Al-Badai)
- **THE SACRED FIRST-SOURCE RULE**: If the authentic instruction diagram already exists in Tailornova/PatternFast, **ALWAYS USE IT DIRECTLY** (cleaned, cropped, and framed). ONLY if a technique does NOT exist (or has a fatal model mismatch/contradiction) do you draft it procedurally via CAD! Never invent synthetic shapes when official vector artwork exists.
- **Official API Endpoint**:
  ```text
  GET / POST https://api.patternfast.com/api/sewing-instructions?elementIds={elem_ids}&mannequinId={man_id}&categoryCode={cat}&format=pdf
  ```
  Returns the complete 28-page official instruction PDF containing high-definition vector illustrations for all sewing steps.
- **Mandatory Text-Purge Rule (Qti3 l-ktaba l-3amiyya)**:
  - When extracting diagrams from the official PDF, render strictly below `y = 285 pt` (or auto-crop active drawing bounds) to completely purge the raw generic Tailornova bullet points that cause text collisions with callout numbers.
- **Dual-Box Extraction & Assembly**:
  - For multi-piece steps (e.g. Back + Front darts, Left + Right leg inseams), detect the vertical whitespace gap via `InstructionHarvester.split_side_by_side_pieces()`.
  - Assemble into two distinct white rectangular boxes (`#FFFFFF`) with 4px black borders inside the `#F5F2EF` container via `InstructionHarvester.build_dual_panel_box()`.
  - Top-left of Box 1: **`1.`** in `Poppins-Bold` with concise title & subtitle.
  - Top-left of Box 2: **`2.`** in `Poppins-Bold` with concise title & subtitle.
  - Zero overlapping text, zero clipped borders, 100% quiet-luxury quiet aesthetic.
- **Generic Template Contradiction Hunter (e.g. Invisible Zipper Text)**:
  - Watch out for Tailornova generic reuse bugs: e.g. using a skirt/dress center back zipper graphic (`pin back sections together`) on a trouser side seam. Always correct labels to reflect the real garment construction (`pin side seam together below zipper`).

---

## Ready-to-Use Studio Scripts

### 1. `clean_instruction_panel.py`
Located at: `C:\Users\red1e\.gemini\config\skills\instruction-diagram-studio\scripts\clean_instruction_panel.py`
- Parses any Tailornova vector SVG.
- Resolves clipped viewBox issues, strips AI/Illustrator entities.
- Crops cleanly to diagram bounds.
- Auto-detects 1-panel, 2-panel, or 4-panel configurations.
- Overlays bold **`1.`**, **`2.`**, **`3.`**, **`4.`** in `Poppins-Bold`.
- Wraps inside the `#F5F2EF` Gold Standard luxury container.
- Renders at 300 DPI high resolution.

### 2. `draft_missing_panel.py`
Located at: `C:\Users\red1e\.gemini\config\skills\instruction-diagram-studio\scripts\draft_missing_panel.py`
- Procedural CAD generator for custom steps:
  - Exposed front metal zippers.
  - Armhole / shoulder princess seams with tailor's ham molding.
  - Tailored single-welt or double-welt pockets.
  - Two-piece set-in sleeves with underarm ease.
  - Collarless jewel neck facings with understitching.
  - Jacket hem with mitered corners and hem tape.

---

## Workflow Checklist Before Presenting Any Step
1. [ ] Is the original technique respected? If available, clean it up rather than inventing new steps.
2. [ ] Is any text clipped or cut off? Verify text labels at the extreme edges.
3. [ ] Are the sequence numbers **`1.`**, **`2.`**, **`3.`**, **`4.`** large, bold, and in `Poppins-Bold`?
4. [ ] Does the diagram fill the inner panel generously without excessive empty whitespace?
5. [ ] Is the image rendered at 300 DPI?
6. [ ] Is it copied to the artifacts directory and visually inspected before sending to the user?
