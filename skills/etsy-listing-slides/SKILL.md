---
name: "etsy-listing-slides"
description: "Generate all 10 high-converting Etsy listing images (2000x2000 px) and a 10-second Etsy listing video (MP4) from the approved model photos, technical flat sketch, and booklet specs using Playwright and ffmpeg."
---

# Etsy Listing Slides & Video Builder (10 Images + MP4 Video)

Goal: Automatically build a complete, cohesive 10-image Etsy visual funnel (`2000x2000 px` JPGs, quality 95) plus a 10–12 second Etsy Listing Video (`1080x1080 px` MP4) so the user never has to manually lay out slides in Canva.

## Inputs
- **5 Approved Model Photos** (from `prompt-photo-listing`: 1 Front, 2 Back, 3 Three-Quarter, 4 Extra Pose, 5 Lifestyle).
- **Technical Flat Sketch** (Front + Back, transparent PNG stickers from `flat-sketch-studio` or extracted from the sketch).
- **Generated Booklet PDF** (from `sewluxe-booklet` or `sewluxe-kids-booklet`) to extract exact tables (Body Measurements, Letter Sizes, Finished Measurements, Fabric Requirements, Notions, Skill Level, Design Features) and render page previews.

---

## House Visual Style (Elsie / SewLuxe Etsy Aesthetic)
- **Canvas**: `2000 × 2000 px` (1:1 Square, crisp thumbnail visibility on Etsy search mobile & desktop).
- **Typography**: `Lora` (Regular, Bold, Italic for headings/garment names) + `Poppins` (Regular, Medium, SemiBold for badges, tables, callouts).
- **Color Palette**:
  - Primary Accent: `#9C4A57` (Dusty Rose / Burgundy) or harmonized with the garment's editorial palette
  - Ink / Dark Text: `#262322`
  - Warm Cream Background: `#FAF6F4` / `#F6EDEB`
  - Table Alternating Row: `#FBF7F5`
  - Crisp White Cards: `#FFFFFF` with subtle soft drop shadow (`0 12px 32px rgba(38,35,34,0.08)`).
- **Rendering Engine**: HTML/CSS templates rendered at `2000x2000` viewport via headless Chromium (`Playwright`) for pixel-perfect typography, tables, and badges. Visually inspect every generated slide before delivering.
- **Ready-to-Run Playwright Template Script**: `C:\Users\red1e\.gemini\config\skills\etsy-listing-slides\scripts\build_etsy_slides_template.py` — Uses embedded base64 `Lora` and `Poppins` fonts (`<meta charset="utf-8">`) and `flat_sketch_transparent.png` to render all `2000x2000` slides in ~8 seconds!

---

## The 10-Slide Conversion Funnel

### Slide 1: The Hero Cover (`01_Cover.jpg`)
Designed to maximize CTR (Click-Through Rate) in crowded Etsy search results:
- **Left 58%**: Approved Model Photo 1 (Front view, tight head-to-mid-thigh framing).
- **Right 42%**: Warm cream panel (`#FAF6F4`) with:
  - Top Kicker: `PDF SEWING PATTERN` (`Poppins Medium`, letter-spaced, accent `#9C4A57`).
  - Garment Title: e.g. `Rachel` (`Lora` 110px) + `JACKET` (`Poppins Medium` letter-spaced).
  - Overlapping Technical Flat Sketch Sticker (Front large + Back smaller, white fill, crisp outline, soft shadow) bridging the photo and panel.
  - Key Value Badges (stacked clean pills):
    - `SIZES US 00–22 (XXS–4XL)` (or `KIDS SIZES 2–16`)
    - `SKILL LEVEL: CONFIDENT BEGINNER` (with scissors icon — must strictly match the booklet!)
    - `A4 · US LETTER · A0 · PROJECTOR`
    - `ILLUSTRATED GUIDE + VIDEO TUTORIALS`
  - Bottom Ribbon: `INSTANT DIGITAL DOWNLOAD` + Shop Brand Name (`Lora Italic`).

### Slide 2: Back & 3/4 Angles + Feature Callouts (`02_Angles_Details.jpg`)
- Split 2-column showcase of **Model Photo 2 (Back)** and **Model Photo 3 (3/4 View)**.
- Header: `THOUGHTFUL CONSTRUCTION DETAILS`.
- 4–5 clean floating callout pills pointing to real pattern features (e.g., `Mandarin Collar Stand`, `Exposed Brass Zipper`, `Shaped Waist Darts`, `Full Circular Peplum Hem`, `Relaxed Everyday Ease`).

### Slide 3: Technical Flat Sketch & Design Features (`03_Technical_Sketch.jpg`)
*Crucial trust builder on Etsy — proves the pattern is genuinely drafted and not an AI fake.*
- Large, crystal-clear **Front & Back Technical Flat Sketches** centered on a subtle dot-grid studio card.
- Left column: **Design Features** (`✔` bullet list matching the booklet).
- Right column: **Pattern Specifications** (`Seam Allowances Included`, exact hem depths, closure specs, number of pattern pieces, `Layered PDF + Individual Sizes`).

### Slide 4: Size Chart & Finished Garment Measurements (`04_Size_Chart.jpg`)
- Header: `SIZE CHART & FINISHED MEASUREMENTS`.
- Top Table: **Body Measurements** (`US 00–22` with `XXS–4XL` Letter row directly underneath, or Kids `2–6` & `7–16`) in both **Inches** and **Centimeters**.
- Bottom Table: **Finished Garment Measurements** (Bust/Chest, Waist, Hips, Back Length, Sleeve Length) + clear note on **Ease** ("Includes X cm / Y in of comfortable wearing ease at the bust/waist").

### Slide 5: Fabric Requirements & Notions (`05_Fabric_Notions.jpg`)
- Header: `FABRIC & NOTIONS GUIDE`.
- Main Table: **Fabric Yardage / Meterage** per size group for `150 cm (60")` and `115 cm (45")` widths (plus Lining / Interfacing if applicable).
- Bottom Left Card: **Suggested Fabrics** (`✔` list from booklet + thick-fabric size-up note if applicable).
- Bottom Right Card: **Required Notions** (exact button count, zipper length, elastic width, thread, needle type).

### Slide 6: What You Will Receive (`06_What_You_Receive.jpg`)
- Header: `EVERYTHING INCLUDED IN YOUR DOWNLOAD`.
- Visual mockup showing fanned pages of the **Instruction BookletCover + Inner Pages**, tiled `A4 / US Letter` sheets, large `A0` copyshop sheet, and `Projector / Layered PDF` icons.
- 6 Icon Feature Cards:
  1. `Illustrated Step-by-Step Booklet`
  2. `Print-at-Home A4 & US Letter`
  3. `A0 Copyshop Large Format`
  4. `Multi-Size Layered PDF & Projector File`
  5. `QR & Clickable Video Tutorials`
  6. `Beginner Tips on Every Tricky Step`

### Slide 7: Inside the Instruction Booklet (`07_Inside_Booklet.jpg`)
- Header: `CLEAR, BEGINNER-FRIENDLY INSTRUCTIONS`.
- Renders 4 actual pages from the generated `<Garment>_Sewing-Instructions.pdf` (`Page 3 Before You Begin`, `Page 7 Pieces & Markings`, `Page 8 Video Guides`, and a dense `Sewing Step` page with vector diagrams and a `Beginner Tip` box).
- Highlights: *"Every step illustrated with clear technical diagrams + troubleshooting tips."*

### Slide 8: Extra Pose & Styling Inspiration (`08_Styling_Pose.jpg`)
- Features **Model Photo 4 (Extra Pose / Detail movement)** on the left (65% width).
- Right panel: `SEW IT YOUR WAY` — 3 curated fabric & color mood combinations + wardrobe styling ideas from the booklet's final page.

### Slide 9: Lifestyle Editorial & Techniques Covered (`09_Lifestyle_Skills.jpg`)
- Features **Model Photo 5 (Lifestyle)** on the right (65% width).
- Left panel: `SKILLS YOU WILL LEARN` — lists the core sewing techniques covered in the booklet + notes that video guides are included for each technique.

### Slide 10: How Instant Digital Download Works (`10_How_To_Download.jpg`)
- Header: `HOW INSTANT DOWNLOAD WORKS`.
- 4-step visual timeline:
  1. **Purchase & Download**: Access your files immediately via `Etsy > Purchases and Reviews` on your computer browser.
  2. **Choose Your Format**: Print at home (`A4` or `US Letter`), send `A0` to a local print shop, or project directly onto fabric.
  3. **Select Your Size Layer**: Open in free Adobe Acrobat Reader, toggle your size layer on, and print Page 1 at `100% Actual Size` to check the `4" × 4"` square.
  4. **Cut & Sew with Confidence**: Follow the step-by-step illustrated booklet and scan the QR codes for video help!
- Clear disclaimer box at bottom: `💻 DIGITAL PRODUCT ONLY — No physical garment or paper pattern will be shipped.`

---

## Step 2: Etsy Listing Video (`11_Listing_Video.mp4`)
Etsy boosts listings with video in search rankings and plays them automatically on hover/mobile:
- **Specs**: `1080 × 1080 px` (or `1200 × 1200 px`), `30 fps`, `10–12 seconds` duration, H.264 `.mp4`, no audio track needed.
- **Storyboard** (built with `ffmpeg` / `PIL` frame interpolation):
  - `0.0s – 3.0s`: Smooth slow zoom-in (`1.00x -> 1.06x`) on **Slide 1 (Hero Cover)** or **Photo 1** with subtle floating badge `PDF Sewing Pattern · Sizes XXS–4XL`.
  - `3.0s – 6.0s`: Crossfade to **Technical Flat Sketch (Front & Back)** drawing/revealing alongside **Photo 2 (Back)** & **Photo 3 (3/4)**.
  - `6.0s – 9.0s`: Smooth pan across **Inside the Booklet pages** (showing crisp diagrams, QR video guides, and size chart).
  - `9.0s – 11.5s`: Crossfade to **Photo 5 (Lifestyle)** with end card overlay: `Print at Home (A4/Letter) · Copyshop (A0) · Projector`.

## Quality Checks Before Delivery
- Verify all 10 images at full resolution: no text clipping, no overlapping stickers, skill level matches the booklet 100%, button count and features match the pattern, zero mention of internal generation tools, PatternFast, or Tailornova.
