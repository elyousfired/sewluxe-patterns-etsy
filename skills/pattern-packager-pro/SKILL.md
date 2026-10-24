---
name: "pattern-packager-pro"
description: "Clean, white-label, and upgrade PatternFast/Tailornova pattern PDFs (A4, US Letter, A0) into a pro Etsy delivery package: strip logos/metadata, build a Multi-Size Layered PDF (OCG layers), generate a Projector File PDF, package ZIP archives, and build a clickable Etsy Download Sheet PDF."
---

# Pattern Packager Pro (White-Label + Layered PDF + Projector + Etsy Delivery)

Goal: Turn raw single-size PatternFast / Tailornova exports into an industry-leading Etsy pattern package that rivals top indie pattern houses. Never ship raw PatternFast files or metadata to buyers.

## Deliverables
1. **Cleaned Individual Size PDFs** (`A4`, `US Letter`, `A0`) with all PatternFast/Tailornova logos, headers, watermarks, stray labels, and metadata completely removed and replaced with shop branding.
2. **Multi-Size Layered PDF (`A4`, `US Letter`, `A0`)** using PDF Optional Content Groups (`OCG` layers via `pikepdf` / `pymupdf`) so buyers can toggle individual sizes on/off in Adobe Acrobat Reader and grade between sizes.
3. **Dedicated Projector File PDF** (`<Garment-Name>_Projector-Layered.pdf`) with wide 50 cm margins, thick high-contrast cut/stitch lines, calibration grid layer, and toggleable size layers.
4. **Organized ZIP Archives** ready for cloud upload (`Google Drive` / `Dropbox`):
   - `<Garment-Name>-A4-Print-at-Home.zip`
   - `<Garment-Name>-US-Letter-Print-at-Home.zip`
   - `<Garment-Name>-A0-Copyshop.zip`
   - `<Garment-Name>-Projector-File.zip`
5. **Etsy Instant Download Sheet PDF** (`<Garment-Name>_Download-Your-Pattern.pdf`): A sleek 1-page branded PDF (under 2 MB) uploaded directly to Etsy alongside the Instruction Booklet, containing clickable buttons to download the ZIP packs.

---

## Hard Rules (Zero-Trace, Audit & Accuracy)
0. **Mandatory Phase 0 Pre-Production Audit Gate (A4-First Protocol)**: Before cleaning or packaging, you MUST cross-examine all CAD pieces, matching seam lengths (Front vs. Back inseams/side seams), and ease allowances relying strictly on the **A4** format first (single reference size, e.g. SIZE 0 / SIZE 8, or A4 overview) to prevent wasting time and tokens on flawed batches. Generate a `PRE-PRODUCTION AUDIT REPORT` in Arabic script for the user and WAIT for approval before launching batch operations across US Letter and A0.
1. **Zero Trace of Generators**: Scan all text streams (`pdftotext`), vector objects, embedded images (`pdfimages`), PDF Info dictionary, and XMP metadata (`strings`) for `PatternFast`, `Tailornova`, or internal generation tools. Strip and overwrite `Author`, `Creator`, `Producer`, and `Title` with the shop brand (`SewLuxePatterns` or the user's configured brand name).
2. **Calibration Square Integrity**: Never scale or shift page geometry when cleaning headers or merging layers. The test square on Page 1 must remain strictly **4 in × 4 in (101.5 mm × 101.5 mm)** at 100% scale (`288 pt × 288 pt`).
3. **Stray Mark Cleanup**: If the booklet audit (`sewluxe-booklet` or `sewluxe-kids-booklet`) flagged stray template labels on the pattern (e.g., `ZIP` printed on a button-front garment, or wrong spec sheets on pages 1–3), strip those text elements from the content stream before packaging.
4. **File Naming Convention**:
   - Individual sizes (Adult): `<Garment-Name>_<Format>_Size-US-00-XXS.pdf` ... `Size-US-22-4XL.pdf`
   - Individual sizes (Kids): `<Garment-Name>_<Format>_Size-2.pdf` ... `Size-16.pdf` (fix colon filenames like `2:91.pdf` -> `Size-2.pdf`)
   - Multi-size layered: `<Garment-Name>_<Format>_ALL-SIZES-LAYERED.pdf`

---

## Step 1: White-Label & Clean Individual Pattern PDFs
- **Ready-to-Run White-Label Script**: `C:\Users\red1e\.gemini\config\skills\pattern-packager-pro\scripts\whitelabel_patternfast_pdfs.py` (and integrated inside `patternfast-tailornova-exporter\download_all_template.py`).
- Reference cleaned pattern packs for `Odette Vest` are saved locally at:
- `A0`: `C:\Users\red1e\.gemini\config\skills\pattern-packager-pro\references\example_A0\A0\` (`SIZE 00.pdf` .. `SIZE 22.pdf`, pages 1–4 `595.28 × 841.89 pt`, pages 5+ `2383.94 × 3370.39 pt` true A0).
- `US Letter`: `C:\Users\red1e\.gemini\config\skills\pattern-packager-pro\references\example_zip2\US Letter\` (`SIZE 00.pdf` .. `SIZE 22.pdf`, pages 1–4 `595.28 × 841.89 pt`, pages 5+ `612.0 × 792.0 pt` true US Letter).
- `A4`: `C:\Users\red1e\.gemini\config\skills\pattern-packager-pro\references\example_A4\A4\` (`SIZE 00.pdf` .. `SIZE 22.pdf`, all pages `595.28 × 841.89 pt` true A4).

Procedure:
1. Flatten any nested folders or `__MACOSX` entries when processing source ZIPs; when packaging final ZIPs (`A4.zip`, `US Letter.zip`, `A0.zip`), put the 13 PDFs (`SIZE 00.pdf` .. `SIZE 22.pdf`) inside `A4/`, `US Letter/`, and `A0/`.
2. Inspect pages 1–4 (spec/overview pages) and pages 5+ (pattern tiles):
   - Strip the `PatternFast` logo vector/image block from the top center of Pages 1–4 (`y < 70 pt`).
   - Stamp the exact centered two-line brand header at the top of Pages 1–4:
     - Line 1: `<Shop Name>` (e.g. `SewLuxePatterns`) in `Helvetica-Bold`, `20.0 pt`, color `#1f1f1f` (`RGB 0.1216, 0.1216, 0.1216`), centered at `y = 29.0..56.5 pt` from top (`Tm: 1 0 0 1 214.83 791.54`).
     - Line 2: `SEWING PATTERNS` in `Helvetica`, `7.5 pt`, color `#666666` (`RGB 0.4, 0.4, 0.4`), centered at `y = 54.3..64.6 pt` from top (`Tm: 1 0 0 1 262.285 779.54`).
   - Clear PDF metadata (`Title`, `Author`, `Subject`, `Keywords` = empty or shop brand; `Creator`/`Producer` = `PDFKit` or shop brand, zero trace of `PatternFast`).
   - Verify tile numbering (`1/1`, `1/2` ... on pages 5+ in `Helvetica-Bold 36pt #cccccc` at `bbox=[56.7, 44.0, 106.7, 93.6]`).

## Step 2: Build the Multi-Size Layered PDF (OCG Layers)
Using `pymupdf` (`fitz`) or `pikepdf`:
1. Create an Optional Content Group (`OCG`) for each size in ascending order:
   - Adult: `US 00 (XXS)`, `US 0 (XS)`, `US 2 (XS)`, `US 4 (S)`, `US 6 (S)`, `US 8 (M)`, `US 10 (M)`, `US 12 (L)`, `US 14 (L)`, `US 16 (XL)`, `US 18 (2XL)`, `US 20 (3XL)`, `US 22 (4XL)`.
   - Kids: `Size 2` through `Size 16`.
2. Create a locked/always-visible base layer: `00 - Calibration Square, Tile Grid & Legend`.
3. Assign distinct, high-readability stroke colors + dash patterns per size (cycling through a colorblind-safe palette: Deep Navy, Crimson, Forest Green, Royal Purple, Burnt Orange, Teal, Magenta, Charcoal) so buyers printing in B&W or color can still distinguish adjacent sizes when grading.
4. Ensure each size's piece outlines, stitching lines, notches, grainlines, and size labels belong to that size's OCG layer.

## Step 3: Build the Dedicated Projector File PDF
 sewists using ceiling/table projectors need specific geometry:
1. Extract the full un-tiled vector layout from the `A0` / page-index-4 master layout for each size.
2. Place all pieces on a single unified artboard with **50 cm (1417 pt) margins** on all four sides so pieces near the edge can be centered under the projector lens.
3. Increase stroke weights for projection visibility:
   - Cutting lines: `3.5 pt` solid (distinct high-contrast color per size layer + option for dark/light background).
   - Stitching lines: `2.0 pt` dashed.
   - Grainlines, fold lines, and notches: `2.5 pt` with large `18 pt` piece labels oriented horizontally.
4. Add two toggleable calibration layers at the top of the OCG list:
   - `Calibration Grid - Inches (1" x 1" grid + 4"x4" square)`
   - `Calibration Grid - Metric (5cm x 5cm grid + 10cm x 10cm square)`

## Step 4: Generate the Etsy Download Sheet PDF
Because Etsy restricts digital listings to 5 files (max 20 MB each), build `<Garment-Name>_Download-Your-Pattern.pdf` in `ReportLab` (1 page, A4, matching the Elsie house style):
- Header: `<Garment Name> · Digital Pattern Download Hub`
- Short welcome note + thumbnail of the garment cover & flat sketch.
- **4 Clickable Download Buttons** (styled rounded rectangles with embedded `linkAbsolute` URLs — use placeholders `#LINK-A4`, `#LINK-LETTER`, `#LINK-A0`, `#LINK-PROJECTOR` or the user's Google Drive folder link):
  1. `Download A4 Print-at-Home Pack (Layered + Single Sizes)`
  2. `Download US Letter Print-at-Home Pack (Layered + Single Sizes)`
  3. `Download A0 Copyshop Pack (Layered + Single Sizes)`
  4. `Download Projector File (Layered PDF)`
- Quick 3-step printing reminder (`1. Open in free Adobe Acrobat Reader on a computer`, `2. Print Page 1 at 100% / Actual Size and measure the 4"x4" square`, `3. Toggle your size layer using the Layers icon on the left panel`).
- Footer: Support message ("Need help downloading or printing? Message us on Etsy anytime!") + Shop name.
