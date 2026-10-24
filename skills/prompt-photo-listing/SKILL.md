---
name: "prompt-photo-listing"
description: "Autonomously generate ultra-realistic 1:1 editorial catalogue model photos for a SewLuxePatterns listing from a flat sketch (front, back, 3/4, extra pose, lifestyle): square 1:1, garment-first framing, researched fabric and color, realistic human model, relaxed real-life fit, garment matching the pattern."
---

# Editorial Model Photo Studio (SewLuxePatterns)

Goal: Autonomously generate complete, cohesive, 100% photorealistic editorial model photos that look like a genuine high-fashion photoshoot on the FIRST try via the internal `image-generator` studio subagent (zero external tools, zero manual copy-pasting).

### Autonomous Generation Mode (Default & Mandatory):
- The assistant directly drives the photo generation process using the internal `image-generator` subagent.
- Formulate precise, studio-grade prompts matching the authentic garment construction (silhouette, seams, closure, pockets, hem, ease).
- Directly generate and verify:
  1. **Photo 1: Front Hero View** (relaxed stance, one hand in pocket, full trousers).
  2. **Photo 2: Side / Three-Quarter Angle** (45° angle, side seam, pocket opening, clean drape).
  3. **Photo 3: Back View** (clean back silhouette, gathered waist casing, center back seam).
  4. **Photo 4: Extra Pose / Detail Movement** (natural candid movement, fabric folds).
  5. **Photo 5: Lifestyle Editorial** (50mm, blurred natural environment).
- Inspect every generated photo against the technical flat sketch (waistband, pockets, length, silhouette) before presenting to the user.

## Inputs
- Technical flat sketch (front + back). Required.
- Pattern files and/or booklet if available: use them to confirm button count per size, darts, seams, pockets, length, silhouette, and the EASE (finished waist vs body waist) so the fit in the photo matches the real garment.
- Garment name if chosen (vintage feminine names: Florence Jacket, Elsie Jacket, Rachel Jacket, Clara Vest...).
- The user's previous listing covers and competitor listings (Etsy) if he shares them (or ask for the covers before choosing a color). Previous covers are the reference for what NOT to repeat and for the series look. Competitors are the reference for how the product is shown (fit, outfit, backdrop) and for what to stand out from.

## Previous listings (update this list after every new listing)
| Listing | Garment | Fabric | Color | Backdrop | Styling |
|---|---|---|---|---|---|
| Florence Jacket | collarless boxy jacket, 7 gold buttons, bust darts | boucle | plum / aubergine | light grey | cream pencil skirt |
| Elsie Jacket | mandarin stand, 7 gold buttons, peplum | wool | chocolate brown | white | cream full skirt |
| Vivienne Jacket | mandarin stand, exposed gold zipper, peplum | wool | deep teal | warm beige | cream trousers |
| Audrey Jacket | mandarin stand, exposed brass zipper, NO peplum, darts front + back | wool crepe | deep burnt olive | white paper | cream trousers |
| Clara / Odette Vest | sleeveless pre-quilted vest, V-neck, 6 ivory buttons, princess seams, 2 patch pockets | matte diamond-quilted cotton blend | spiced terracotta clay | pale sage | ecru linen shirt (sleeves rolled), wide-leg cream linen trousers |
| Colette Trousers | high-waisted wide-leg full-length trousers, double front pleats, slanted side pockets, back single-welt pockets, 1-button waistband + zipper fly | matte brushed wool-linen twill suiting | warm camel tan | pale powder blue | fitted ecru cream long-sleeve fine-ribbed knit top tucked in |

Reference photos (1 Front, 2 Back, 3 Three-Quarter, 4 Extra Pose, 5 Lifestyle) + Flat Sketch for `Odette Vest` are saved locally at: `C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\references\odette_vest\`.

## Fixed format (all 5 prompts)
- **Square 1:1.**
- **Garment-first framing**: the garment fills about 65-75% of the image. Jacket/top/blouse/vest: from the top of the head to mid-thigh. Dress/coat/skirt: from the top of the head to just below the hem (crop the feet). Never a full room or a full-body shot with lots of floor and wall. The photo goes on the left of a listing cover next to the title and sketch, so the garment must read clearly at small size.
- **Plain seamless backdrop** for prompts 1-4: evenly lit, softly out of focus, NO room, NO floor line, NO window shadows, NO furniture, NO props.
- Prompt 5 (lifestyle) keeps the same tight framing with a strongly blurred real background.
- If the user asks for a specific backdrop (e.g. white), use it in prompts 1-4 even if it repeats.

## Step 1: Read the garment exactly
Write two lists from the sketch/pattern:
- MUST HAVE: neckline/collar, closure + EXACT button count (and button size/style) or zipper (exposed or hidden, metal color, from where to where), darts (where, direction), seams that exist (center back seam, yokes, princess seams only if real), pockets or none (patch pocket shape, rounded corners, over a seam?), sleeve type and length, garment length, silhouette, hem shape, which front laps over (women: right over left).
- MUST NOT HAVE: features the pattern does not have that image models add by default. Always consider: vertical front seams / princess lines, waist darts, nipped waist, pockets, collar, lapels, belt, vents, extra buttons, braid trim, fringe, chains (boucle/tweed!), contrast piping or binding, lining showing, peplum/ruffle, pocket flaps, hood, zipper.

## Step 1b: Check against the previous listings
- If the new garment is close to an older one (same collar, same closure), name the difference in the prompt with capital NO (e.g. Audrey vs Vivienne: "NO peplum, NO ruffle, NO flared skirt at the waist: the jacket continues smoothly in one piece from the bust to the hem."). Repeat it in every prompt.
- Its color must be clearly different from every listing in the table, and especially from the most similar garment (not burgundy next to plum, not olive-teal next to teal).

## Step 1c: Competitor Reference & Fabric Forensics (Mandatory Non-Assumption Rule)
- **1:1 Fabric & Textile Lock**: NEVER assume or substitute default fabrics (e.g. casual linen slub). Strictly scrutinize the target Etsy photo for physical textile behavior:
  * Liquid waterfall drape with soft matte-satin sheen $\rightarrow$ Heavy Fluid Silk-Viscose Crepe / Tencel (ZERO linen slub, ZERO wrinkles).
  * Visible weave slub with natural relaxed creases $\rightarrow$ Washed pure linen.
  * Stiff, structured body $\rightarrow$ Cotton twill, canvas, or suiting wool.
- **1:1 Exact Colorway Lock**: Photoshoot 1-3 MUST match the winning benchmark listing's exact colorway (e.g. Deep Petrol Teal) to maintain proven market appeal.
- **Zero-Obscuring Styling**: When the garment features high-waisted tailoring, clean front rise seams, or vertical waist darts, styling MUST NEVER cover them (use cropped bandeau / crop top / bare midriff so the entire waistband, darts, and front rise seam are 100% visible and unobscured).

## Wording that works on the first try
Always include these sentences, adapted to the garment:
- For any garment whose front has no vertical seams: "The front panels are one smooth continuous piece of fabric below the bust darts: NO vertical seams, NO princess lines, NO waist darts." (Plain "no princess seams" was not enough: faint vertical lines kept appearing.)
- When the front HAS long waist darts: "These two waist darts are the ONLY vertical lines on the front: they do NOT reach the shoulder or the armhole."
- When the front HAS princess seams: "Each front has one long curved princess seam rising from the armhole to the hem, clearly visible as a seam line (also through quilting); these are the ONLY vertical seams on the front." Repeat it in the back prompt with the exact back construction (e.g. one center back seam + two princess seams).
- For a flared or straight body: "Below the bust the jacket falls straight with a very slight flare toward the hem; it does NOT curve in at the waist."
- Button count: "exactly N buttons" and describe their spacing ("evenly spaced from just below the V-neck point to just above the hem").
- Exposed zipper: "EXPOSED <metal> metal separating zipper ... the zipper teeth are fully visible on the outside, sitting right at the front edges with no placket or flap covering them."
- Repeat the MUST NOT HAVE list with capital NO in every prompt, including prompts 4 and 5.

## RELAXED REAL-LIFE FIT (always; learned from Clara Vest)
Image models make garments look glued to the body (corset waist, peplum flare), which does not match real patterns (ease 10-16 cm at the waist) or what competitors show (relaxed, boxy). Put this in EVERY prompt, adapted: "Fit: relaxed and comfortable, NOT tight. The <garment> does not hug the waist or squeeze the body, there is a little ease between the fabric and the body, it falls from the shoulders to the hem with only a very slight A-line flare, and it does NOT look like a corset or a peplum. Natural soft creases at the <buttons, waist, pockets> and a slight natural gap at the armholes." Only for a deliberately fitted garment (check the pattern ease) soften this.

## Step 2: Research fabric and color (every listing)
Run web searches (several in one go) and page fetch the best hits: current season women's color trends (Trendalytics, Style of Eurasia, Mango, Pantone, WGSN...) and the fabric that suits this garment and is trending. Choose:
- ONE fabric matching the pattern's weight/drape, with concrete texture words (nubby looped boucle, matte wool crepe with fine pebbly grain, crisp slubby linen, matte pre-quilted cotton blend with soft diamond quilting...). For quilted garments: matte, lightly puffed, thread in the same color, NOT a shiny puffer, NO horizontal channel quilting.
- ONE trend color with a precise name that suits the vintage look and is NOT in the Previous listings table.
- Styling that keeps the series look: cream/ecru bottoms (trousers or skirt), small gold or pearl earrings, vintage-inspired hair (soft waves, curls). For casual garments (vests, shirts, casual jackets) use the relaxed outfit: ecru linen shirt with sleeves rolled to the elbows (collar visible at the neckline) and wide-leg cream linen trousers, one hand loosely in a pocket. Competitors use casual outfits; our photos must feel the same.
- ONE plain backdrop tone that contrasts with the garment, rotating between listings unless the user names one, and differing from competitors (they mostly use beige/white): white paper, off-white, very light warm grey, soft pale cream, pale blush, pale sage, pale powder blue.
Tell the user in one or two short lines what you chose and why, with sources.

## Step 2b: Competitor check (when the user shares competitor listings)
Look at fit, outfit, backdrop and framing. Say in the user's language what they do (e.g. boxy, relaxed, casual outfit) and what must change in our prompts. Do not copy their patchwork/binding if the pattern does not have it.

## Step 3: The 5 prompts
1. Front: front view, shoulders very slightly turned, one hand loosely in a pocket (if any) or arms relaxed a little away from the body so side seams and sleeves show, garment closed.
2. Back: back to camera, head turned slightly so a bit of profile shows; describe the back construction exactly (e.g. one center back seam, two princess seams) and its MUST NOT list (no vents, no back pleat, no yoke...).
3. Three-quarter: 45 degrees, looking back to camera, one hand lightly at the hem; shows the side seam, pocket, sleeve and silhouette.
4. Extra pose: natural movement in the same backdrop (adjusting a cuff, fingertips at a button or zipper pull, looking down, small step). Real knuckles and fingernails. No props.
5. Lifestyle: vintage-themed place (cobblestone street, bookshop front, cafe terrace, autumn park, flower market), candid, 50mm f/2, background strongly blurred, still head to mid-thigh.

Every prompt contains, in this order:
1. Reference line. Prompt 1: "Use the attached technical flat sketch as the exact garment reference." Prompts 2-5: "Using the attached photo as the reference for the model and the <garment> (keep the exact same woman, face, hairstyle, makeup, <fabric>, <color> and <closure>)" + "and the attached flat sketch for the construction" in prompts 2-3.
2. "Square 1:1 fashion catalogue photograph."
3. Garment: type, fabric + texture, color, MUST HAVE, the Fit block, then the first-try wording and the MUST NOT list.
4. Model (prompt 1 in full; others say "same woman") and outfit.
5. Pose.
6. Framing line: "Framing: tight, from the top of the head to mid-thigh; the <garment> fills most of the frame; minimal background around the model."
7. Backdrop line. White: "Background: real white seamless paper backdrop in a photo studio, clean white with a very soft natural tonal falloff toward the edges and a faint soft shadow beside the model, evenly lit, softly out of focus. NO room, NO floor, NO window shadows, NO props. Not a digital pure-white cutout." Other tones: "Background: plain seamless <tone> backdrop, evenly lit and softly out of focus. NO room, NO floor, NO window shadows, NO props." (lifestyle: the scene, strongly blurred.)
8. Realism block (below).

## Realistic model (avoid the glossy AI look)
Earlier covers (Elsie, Vivienne) looked too smooth and too perfect. In prompt 1 always describe the model as:
"a natural-looking woman in her early 30s, ordinary real person rather than a supermodel, slightly asymmetric face, soft <eye color> eyes, light freckles, <vintage hair, slightly imperfect, a few strands out of place>, minimal makeup with a soft nude lip. Calm, relaxed expression, faint natural smile."
Avoid: "beautiful", "flawless", "glamorous", bold red lips, perfect glossy curls.

## Realism block
"Make it look like a real photograph by a professional fashion photographer: full-frame camera, 85mm lens, f/4, soft directional light from the left, realistic shadows on the body, true-to-life colors. Natural skin texture with visible pores, light freckles, fine baby hairs at the hairline and a few flyaway hairs, slight under-eye texture, no airbrushed or plastic skin, no doll-like face. The <garment> looks home-sewn by a skilled sewist and actually worn: real <fabric> texture with tiny surface grain, natural creases at the <elbows, closure, waist, pockets>, real fabric weight, <buttons / zipper teeth> with small natural differences in shine. No perfect symmetry, no glow, no oversaturated colors, no CGI look, no text, no logo, no watermark."
(lifestyle: 50mm, f/2, natural overcast daylight, subtle film grain, slightly imperfect framing. Pose 4: add "real knuckles and fingernails".)

After the prompts: one short line on what to attach to each prompt, and ask the user to send photo 1 back for review.

## Review a returned photo
Zoom on the garment before answering (crop + contrast/brighten with PIL; faint seams hide in textured fabric). When the user sends two options, compare and choose one. Check:
- Format: square, tight, garment fills most of the frame, plain backdrop.
- Pattern match: button count or zipper, neckline, darts, princess seams visible (also under pockets down to the hem), NO extra vertical seams, pocket shape and position, collar, trims, piping/binding the pattern does not have (commonly invented on necklines and armholes), length, silhouette (no nipped waist if the pattern flares, no peplum if the pattern has none), sleeve length, lap direction.
- Fit: relaxed, not corset-tight, hem not a peplum (the most common failure).
- Realism: skin texture, no glossy/plastic face, fabric grain visible, natural creases.
If something is wrong, give an EDIT prompt in the same chat: "Edit this exact photo. Keep the same woman, face, hair, makeup, pose, lighting, framing, <styling> and background exactly as they are. Only change the <garment>: <fix 1>, <fix 2>. Keep <darts, buttons/zipper, neckline, sleeves, texture, color> identical." Only suggest an edit when the flaw matters; tiny natural asymmetries are fine.
Never accept a photo for the listing or the booklet cover that shows a feature the pattern does not have. When a booklet exists, put the approved photo 1 on its cover and last page.

## Never
- Never mention internal tools, artificial generation, or software names in text meant for the listing or booklet.
- Never reuse a color from the Previous listings table, nor the same color + fabric + backdrop combination.
- Never a wide studio/room shot.
- Never a tight, corset-like or peplum look unless the pattern really has it.