import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONTS_DIR = r"C:\Users\red1e\.gemini\config\skills\sewluxe-booklet\fonts"
OUT_PDF = r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants\07_Customer_Delivery_Guide\SewLuxe_Essential_Sewing_Tips_Guide.pdf"
BRAIN_PDF = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\SewLuxe_Essential_Sewing_Tips_Guide.pdf"

# Register Fonts
pdfmetrics.registerFont(TTFont("Lora-Regular", os.path.join(FONTS_DIR, "Lora-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Lora-Bold", os.path.join(FONTS_DIR, "Lora-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Lora-Italic", os.path.join(FONTS_DIR, "Lora-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Regular", os.path.join(FONTS_DIR, "Poppins-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Medium", os.path.join(FONTS_DIR, "Poppins-Medium.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Bold", os.path.join(FONTS_DIR, "Poppins-Bold.ttf")))

# Color Palette (Matching SewLuxe Gold Standard)
C_PRIMARY = HexColor("#2D3728")
C_SECONDARY = HexColor("#58694B")
C_ACCENT = HexColor("#9BB08B")
C_BG_WARM = HexColor("#FAF8F5")
C_BORDER = HexColor("#E2DDD5")
C_TEXT = HexColor("#1A1918")
C_MUTED = HexColor("#6E6862")
C_WHITE = HexColor("#FFFFFF")

PAGE_W, PAGE_H = A4
MARGIN_L = 40
MARGIN_R = 40
MARGIN_T = 45
MARGIN_B = 45
USABLE_W = PAGE_W - MARGIN_L - MARGIN_R

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        self.saveState()
        
        # Draw running header on pages > 1
        if self._pageNumber > 1:
            self.setFont("Lora-Italic", 9)
            self.setFillColor(C_MUTED)
            self.drawString(MARGIN_L, PAGE_H - 30, "SewLuxePatterns · Essential Sewing Tips & Master Tailor Techniques")
            self.setFont("Poppins-Medium", 8)
            self.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 30, "PRO GARMENT FINISHES")
            self.setStrokeColor(C_BORDER)
            self.setLineWidth(0.75)
            self.line(MARGIN_L, PAGE_H - 35, PAGE_W - MARGIN_R, PAGE_H - 35)

        # Draw running footer on all pages
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.75)
        self.line(MARGIN_L, 35, PAGE_W - MARGIN_R, 35)

        self.setFont("Lora-Italic", 8.5)
        self.setFillColor(C_MUTED)
        self.drawString(MARGIN_L, 22, "SewLuxePatterns © 2026 · Personal Home Sewing License")

        self.setFont("Poppins-Medium", 8.5)
        self.drawRightString(PAGE_W - MARGIN_R, 22, f"Page {self._pageNumber} of {total_pages}")
        
        self.restoreState()

def build_pdf():
    os.makedirs(os.path.dirname(OUT_PDF), exist_ok=True)
    os.makedirs(os.path.dirname(BRAIN_PDF), exist_ok=True)

    doc = SimpleDocTemplate(
        OUT_PDF,
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
    )

    styles = getSampleStyleSheet()

    # Custom typography styles
    st_cover_brand = ParagraphStyle(
        "CoverBrand", fontName="Lora-Italic", fontSize=20, leading=24, textColor=C_SECONDARY, alignment=1
    )
    st_cover_title = ParagraphStyle(
        "CoverTitle", fontName="Lora-Bold", fontSize=28, leading=34, textColor=C_PRIMARY, alignment=1
    )
    st_cover_sub = ParagraphStyle(
        "CoverSub", fontName="Poppins-Regular", fontSize=11.5, leading=17, textColor=C_MUTED, alignment=1
    )
    st_section_h1 = ParagraphStyle(
        "SectionH1", fontName="Lora-Bold", fontSize=19, leading=24, textColor=C_PRIMARY, spaceAfter=4
    )
    st_section_sub = ParagraphStyle(
        "SectionSub", fontName="Lora-Italic", fontSize=11, leading=15, textColor=C_MUTED, spaceAfter=14
    )
    st_card_title = ParagraphStyle(
        "CardTitle", fontName="Lora-Bold", fontSize=12.5, leading=16, textColor=C_PRIMARY, spaceAfter=4
    )
    st_body = ParagraphStyle(
        "BodyDark", fontName="Poppins-Regular", fontSize=9.2, leading=14.0, textColor=C_TEXT
    )
    st_body_bold = ParagraphStyle(
        "BodyBold", fontName="Poppins-Bold", fontSize=9.2, leading=14.0, textColor=C_TEXT
    )
    st_th = ParagraphStyle(
        "TableHead", fontName="Poppins-Bold", fontSize=9.2, leading=14.0, textColor=C_WHITE
    )

    story = []

    # ==========================================
    # PAGE 1: COVER & THE GOLDEN RULE OF PRESSING
    # ==========================================
    story.append(Spacer(1, 10))
    story.append(Paragraph("SewLuxePatterns", st_cover_brand))
    story.append(Spacer(1, 8))
    story.append(Paragraph("Essential Sewing Tips &<br/>Master Tailor Techniques", st_cover_title))
    story.append(Spacer(1, 8))
    story.append(Paragraph("A comprehensive companion guide for professional finishes, crisp pressing, and stress-free garment construction", st_cover_sub))
    story.append(Spacer(1, 20))

    # Golden Rule Box
    golden_content = [
        [
            Paragraph("⭐ THE GOLDEN RULE: PRESSING IS 50% OF SEWING", ParagraphStyle("GRHead", fontName="Poppins-Bold", fontSize=11, leading=14, textColor=C_WHITE)),
        ],
        [
            Paragraph(
                "The single biggest difference between a 'homemade-looking' garment and a high-end designer boutique piece is <b>pressing technique</b>.<br/><br/>"
                "• <b>Never sew across an unpressed seam:</b> Every seam must be pressed flat as stitched (to meld threads into fibers), then pressed open or to one side <i>before</i> crossing it with another seam.<br/>"
                "• <b>Press, don't iron:</b> Lift and lower the iron firmly onto the fabric with gentle steam. Sliding the iron back and forth stretches delicate bias grainlines and distorts pattern shapes.<br/>"
                "• <b>Use a Tailor's Clapper:</b> After applying steam to linen or wool, immediately press a flat hardwood block (tailor's clapper) firmly onto the seam for 5 seconds. The wood absorbs the heat and moisture, locking in razor-sharp, flat edges with zero shine.",
                ParagraphStyle("GRBody", fontName="Poppins-Regular", fontSize=9.2, leading=14.0, textColor=HexColor("#F5F2EF"))
            )
        ]
    ]
    t_golden = Table(golden_content, colWidths=[USABLE_W])
    t_golden.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 15),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBELOW', (0,0), (-1,0), 1, C_SECONDARY),
    ]))
    story.append(t_golden)
    story.append(Spacer(1, 18))

    # Needle & Thread Quick Reference Table
    story.append(Paragraph("Essential Needle & Thread Selection Chart", st_card_title))
    story.append(Spacer(1, 6))

    needle_data = [
        [
            Paragraph("Fabric Type", st_th),
            Paragraph("Recommended Needle", st_th),
            Paragraph("Thread Type", st_th),
            Paragraph("Stitch Length", st_th),
        ],
        [
            Paragraph("<b>Washed Linen & Blends</b>", st_body),
            Paragraph("Universal or Jeans 80/12 – 90/14", st_body),
            Paragraph("100% Polyester all-purpose (Gutermann)", st_body),
            Paragraph("2.6 – 3.0 mm (straight stitch)", st_body),
        ],
        [
            Paragraph("<b>Cotton Twill & Poplin</b>", st_body),
            Paragraph("Universal 75/11 – 80/12", st_body),
            Paragraph("All-purpose polyester or cotton thread", st_body),
            Paragraph("2.4 – 2.6 mm", st_body),
        ],
        [
            Paragraph("<b>Rayon, Viscose & Tencel</b>", st_body),
            Paragraph("Microtex / Sharp 70/10 – 80/12", st_body),
            Paragraph("Fine polyester thread", st_body),
            Paragraph("2.2 – 2.5 mm (prevents puckers)", st_body),
        ],
        [
            Paragraph("<b>Lightweight Wool Suiting</b>", st_body),
            Paragraph("Universal 80/12", st_body),
            Paragraph("Polyester or silk thread", st_body),
            Paragraph("2.5 – 2.8 mm", st_body),
        ],
    ]
    t_needle = Table(needle_data, colWidths=[130, 140, 145, USABLE_W - 415])
    t_needle.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), C_WHITE),
        ('BACKGROUND', (0,1), (-1,-1), C_BG_WARM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_needle)

    story.append(PageBreak())

    # ==========================================
    # PAGE 2: FABRIC PREPARATION & CUTTING
    # ==========================================
    story.append(Paragraph("1. Fabric Preparation & Cutting Precision", st_section_h1))
    story.append(Paragraph("Setting the foundation for accurate fit, straight grainlines, and clean edges", st_section_sub))

    p2_box = [
        [
            Paragraph("<b>Pre-Washing & Grainline Squaring</b>", st_card_title),
            Paragraph("<b>Directional Stay-Stitching</b>", st_card_title)
        ],
        [
            Paragraph(
                "• <b>Shrinkage Control:</b> Natural fibers (linen, cotton, viscose) shrink 4% to 8% during their first wash! Always machine wash and tumble dry your yardage using the same settings you plan to use for the finished garment before cutting a single piece.<br/><br/>"
                "• <b>Find True Crossgrain:</b> Snip 1 cm into the selvedge, gently catch one horizontal crosswise thread, and pull it across the width. Cut along the resulting visible pull-line for a 100% square cutting baseline.<br/><br/>"
                "• <b>Parallel Grainline:</b> Always measure both the top and bottom of pattern grainline arrows to the selvedge with a ruler. If pieces are even 1 cm off-grain, trouser legs will twist around your shins when walking!",
                st_body
            ),
            Paragraph(
                "• <b>What is Stay-Stitching?</b> Stay-stitching is a permanent row of straight stitches sewn through a single layer of fabric within the seam allowance (typically 6 mm / 1/4 in from the raw edge) to prevent curved edges from stretching out of shape during handling.<br/><br/>"
                "• <b>Where to Apply:</b> Essential on curved waistline edges, necklines, armholes, and bias-cut pocket openings.<br/><br/>"
                "• <b>Direction Matters:</b> Always stitch from the highest point down toward the center to avoid distorting the natural symmetry of the garment.<br/><br/>"
                "• <b>Stitch Length:</b> Use a shorter stitch length (1.8 – 2.0 mm) for maximum stability.",
                st_body
            )
        ]
    ]
    t_p2 = Table(p2_box, colWidths=[USABLE_W/2, USABLE_W/2])
    t_p2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_WARM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p2)
    story.append(Spacer(1, 16))

    # Cutting & Transferring Notches Box
    cutting_box = [
        [
            Paragraph("<b>Mastering Cutting Tools & Transferring Notches</b>", ParagraphStyle("CH", fontName="Poppins-Bold", fontSize=11, leading=15, textColor=C_PRIMARY))
        ],
        [
            Paragraph(
                "• <b>Rotary Cutter vs Shears:</b> A 45 mm rotary cutter on a self-healing mat keeps delicate linen completely flat while cutting, eliminating the lift and distortion caused by traditional scissors.<br/>"
                "• <b>Pattern Weights:</b> Use flat weights instead of pins when cutting lightweight wovens. Pinning causes small ripples that lead to millimeter inaccuracies across long trouser seams.<br/>"
                "• <b>Notch Transferring:</b> Never cut deep notches into your garment! Cut a tiny <b>3 mm (1/8 in) snip</b> into the raw seam allowance edge, or mark with a water-soluble fabric pen. Deep cuts weaken high-stress seams and cannot be undone.<br/>"
                "• <b>Fusible Interfacing Strips:</b> Apply lightweight 1 cm wide fusible interfacing strips along pocket openings and waistband foldlines. This reinforces high-wear areas and prevents pocket gaping.",
                st_body
            )
        ]
    ]
    t_cutting = Table(cutting_box, colWidths=[USABLE_W])
    t_cutting.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1.5, C_SECONDARY),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_cutting)

    story.append(PageBreak())

    # ==========================================
    # PAGE 3: SEAM FINISHES, CURVES & POCKETS
    # ==========================================
    story.append(Paragraph("2. Seam Finishes, Curves & Pocket Mastery", st_section_h1))
    story.append(Paragraph("Professional tailoring techniques for smooth interiors and invisible side pockets", st_section_sub))

    p3_box = [
        [
            Paragraph("<b>The Secret of Understitching (Invisible Pockets)</b>", st_card_title),
            Paragraph("<b>Sewing & Nesting Crotch Curves</b>", st_card_title)
        ],
        [
            Paragraph(
                "<b>What it is:</b> Understitching secures the seam allowances firmly to the inner pocket bag (or facing), preventing the lining from rolling or peeking out to the front of the garment.<br/><br/>"
                "<b>How to execute:</b><br/>"
                "1. Stitch pocket bag to trouser side seam with right sides together.<br/>"
                "2. Press both seam allowances smoothly toward the pocket bag.<br/>"
                "3. From the right side of the pocket bag, edge-stitch <b>2–3 mm (1/8 in)</b> away from the seamline, catching only the pocket and seam allowances underneath.<br/>"
                "4. Press again: the pocket will now naturally roll inward, creating a razor-clean front silhouette!",
                st_body
            ),
            Paragraph(
                "<b>The 4-Way Cross Junction:</b><br/>"
                "When joining inner leg seams at the crotch, avoid bulky lumps by <b>nesting</b> the seam allowances:<br/>"
                "• Press the front inner leg seam allowance toward the left, and the back inner leg seam allowance toward the right.<br/>"
                "• Lock the two seamlines together with a pin directly through the stitching line.<br/><br/>"
                "<b>Reinforcing the Crotch Curve:</b><br/>"
                "The lower curved junction experiences maximum body stress. Stitch a <b>second parallel row of stitching</b> 1.5 mm inside the seam allowance between inner thighs, then trim or serge cleanly.",
                st_body
            )
        ]
    ]
    t_p3 = Table(p3_box, colWidths=[USABLE_W/2, USABLE_W/2])
    t_p3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_WARM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p3)
    story.append(Spacer(1, 16))

    # Seam Finishing Options Box
    seam_box = [
        [
            Paragraph("<b>Clean Seam Finishes on Standard Home Sewing Machines</b>", ParagraphStyle("SH", fontName="Poppins-Bold", fontSize=11, leading=15, textColor=C_PRIMARY))
        ],
        [
            Paragraph(
                "You do not need an expensive industrial serger to achieve clean, durable seam finishes! Use these home sewing techniques:<br/><br/>"
                "• <b>Three-Step Zigzag (Best for Linen):</b> Use a wide 3-step zigzag stitch along the raw edge. Unlike a standard zigzag which can tunnel fabric, the 3-step stitch lays completely flat and locks raw linen fibers permanently.<br/><br/>"
                "• <b>Faux Overlock Stitch:</b> Most modern domestic machines include an overcasting stitch (often paired with an overcasting presser foot with a wire guide) that wraps thread around the raw edge smoothly.<br/><br/>"
                "• <b>French Seams (Lightweight Silks & Rayons):</b> For sheer or luxury fabrics, sew wrong sides together at 6 mm (1/4 in), trim to 3 mm, press open, turn right sides together, and stitch at 6 mm (1/4 in). The raw edge is completely encased inside a pristine tube!<br/><br/>"
                "• <b>Pinking Shears:</b> For tightly woven wools and twills, trimming seam allowances with pinking shears provides a lightweight, bulk-free finish.",
                st_body
            )
        ]
    ]
    t_seam = Table(seam_box, colWidths=[USABLE_W])
    t_seam.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1.5, C_SECONDARY),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_seam)

    story.append(PageBreak())

    # ==========================================
    # PAGE 4: WAISTBANDS, ELASTIC & HEMLINES
    # ==========================================
    story.append(Paragraph("3. Elastic Waistbands & Perfect Hemlines", st_section_h1))
    story.append(Paragraph("Techniques to prevent twisted elastic and achieve weighted, elegant floor-length hems", st_section_sub))

    p4_box = [
        [
            Paragraph("<b>Continuous Elastic Casing Mastery</b>", st_card_title),
            Paragraph("<b>Tailored Wide-Leg Hemming</b>", st_card_title)
        ],
        [
            Paragraph(
                "• <b>The Bodkin Tool:</b> Never struggle with a safety pin that pops open inside your waistband casing! Use a metal bodkin (or loop turner) to thread elastic through casings smoothly in under 30 seconds.<br/><br/>"
                "• <b>The Box-and-Cross Stitch:</b> When joining elastic ends, overlap by <b>2.5 cm (1 in)</b>. Stitch a square box, then stitch an 'X' diagonally across the box. This distributes pull tension across 8 points so the elastic never snaps or creates a bulky ridge.<br/><br/>"
                "• <b>Preventing Twist (Stitch-in-the-Ditch):</b> Once elastic is distributed evenly, sew a small vertical stitch line directly into the seam groove (stitch-in-the-ditch) at both side seams and center back. This locks the elastic permanently in place so it never twists or rolls inside the casing during laundering!",
                st_body
            ),
            Paragraph(
                "• <b>Hang Before Hemming:</b> Wide-leg trousers drafted in linen or rayon can drop slightly on the bias after sewing. Try on the trousers with the shoes you plan to wear, and let them hang for a few hours before marking your finished hemline.<br/><br/>"
                "• <b>The Double-Folded Hem:</b><br/>"
                "1. Press a crisp <b>1 cm (3/8 in)</b> fold along the lower raw edge with steam.<br/>"
                "2. Fold up a second time by <b>2 cm (3/4 in)</b> to encase the raw edge completely.<br/>"
                "3. Edgestitch from the inside, exactly <b>2 mm</b> from the upper folded edge.<br/><br/>"
                "• <b>Adding Weight:</b> A deep 3 cm tailored hem adds gentle weight to the lower trousers, ensuring wide-leg pants swing gracefully around the ankles when walking.",
                st_body
            )
        ]
    ]
    t_p4 = Table(p4_box, colWidths=[USABLE_W/2, USABLE_W/2])
    t_p4.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_WARM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p4)
    story.append(Spacer(1, 16))

    # Steam & Clapper Pressing Secrets
    press_box = [
        [
            Paragraph("<b>The Pro Steam & Wooden Clapper Method</b>", ParagraphStyle("PH", fontName="Poppins-Bold", fontSize=11, leading=15, textColor=C_PRIMARY))
        ],
        [
            Paragraph(
                "• <b>Use a Pressing Cloth:</b> When pressing the right side of dark linen, wool, or cotton, place a lightweight damp white cotton handkerchief or press cloth between the iron and your garment. This prevents the fabric surface from developing an unsightly shiny glaze.<br/><br/>"
                "• <b>Wooden Tailor's Clapper:</b> After pressing a hem or waistband seam with burst steam, immediately remove the iron and press the flat wooden tailor's clapper firmly against the warm seam. Hold it with firm downward pressure until the fabric cools. The wood absorbs moisture and traps the heat, producing razor-sharp bespoke tailored edges that hold their shape through washing.<br/><br/>"
                "• <b>Pressing Hams for Curves:</b> Never press curved hip seams or crotch seams flat on an ironing board! Press over a curved tailor's ham to preserve the natural three-dimensional contour of the garment.",
                st_body
            )
        ]
    ]
    t_press = Table(press_box, colWidths=[USABLE_W])
    t_press.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1.5, C_SECONDARY),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_press)

    story.append(PageBreak())

    # ==========================================
    # PAGE 5: TROUBLESHOOTING & SUPPORT GUARANTEE
    # ==========================================
    story.append(Paragraph("4. Quick Troubleshooting & Care Guide", st_section_h1))
    story.append(Paragraph("Fast solutions to common sewing machine hiccups and our personal support guarantee", st_section_sub))

    trouble_box = [
        [
            Paragraph("Symptom", st_th),
            Paragraph("Root Cause", st_th),
            Paragraph("Instant Solution", st_th),
        ],
        [
            Paragraph("<b>Thread loops/birdnesting underneath fabric</b>", st_body_bold),
            Paragraph("Top thread is not seated inside tension discs.", st_body),
            Paragraph("Rethread top thread with <b>presser foot raised</b> so tension discs open to receive thread.", st_body),
        ],
        [
            Paragraph("<b>Skipped stitches on seamlines</b>", st_body_bold),
            Paragraph("Dull, bent, or wrong needle type.", st_body),
            Paragraph("Insert a fresh needle (Microtex for viscose/tencel, Jeans/Universal for linen/cotton).", st_body),
        ],
        [
            Paragraph("<b>Seam puckering along straight lines</b>", st_body_bold),
            Paragraph("Tension too tight or needle too thick.", st_body),
            Paragraph("Reduce top tension slightly, switch to size 75/11 needle, and lengthen stitch to 2.8 mm.", st_body),
        ],
        [
            Paragraph("<b>Wavy or stretched seam edges</b>", st_body_bold),
            Paragraph("Fabric stretched while feeding under presser foot.", st_body),
            Paragraph("Reduce presser foot pressure, use a walking foot, and guide fabric without pulling.", st_body),
        ],
    ]
    t_trouble = Table(trouble_box, colWidths=[140, 160, USABLE_W - 300])
    t_trouble.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), C_WHITE),
        ('BACKGROUND', (0,1), (-1,-1), C_BG_WARM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_trouble)
    story.append(Spacer(1, 16))

    # Long Term Care Box
    care_box = [
        [
            Paragraph("<b>Linen & Natural Fiber Longevity Care</b>", st_card_title)
        ],
        [
            Paragraph(
                "• <b>Gentle Laundering:</b> Machine wash on gentle cycle in cool water with mild, bleach-free detergent.<br/>"
                "• <b>Drying:</b> Hang to dry in shade, or tumble dry on low for 10 minutes and remove while still slightly damp to minimize stiff creases.<br/>"
                "• <b>Pressing:</b> Press on medium-high steam setting while slightly damp. Linen softens beautifully with each wash and wear, becoming more luxurious over time.",
                st_body
            )
        ]
    ]
    t_care = Table(care_box, colWidths=[USABLE_W])
    t_care.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_care)
    story.append(Spacer(1, 16))

    # Customer Support Card
    support_box = [
        [
            Paragraph("💌 WE CELEBRATE YOUR SEWING JOURNEY!", ParagraphStyle("SH", fontName="Poppins-Bold", fontSize=12, leading=16, textColor=C_WHITE))
        ],
        [
            Paragraph(
                "Sewing your own clothing is a deeply empowering and creative experience. If you ever feel stuck on any technique:<br/>"
                "• Need advice on adjusting needle sizes or tension for your specific machine?<br/>"
                "• Have a question about a particular step or finish in your pattern?<br/><br/>"
                "<b>Send us a direct message anytime on Etsy!</b> We check our shop messages daily and love helping makers create boutique-quality garments they are truly proud to wear.<br/><br/>"
                "<i>Happy Sewing & Beautiful Stitches! ❤️ · SewLuxePatterns</i>",
                ParagraphStyle("SBody", fontName="Poppins-Regular", fontSize=9.8, leading=14.5, textColor=HexColor("#F5F2EF"))
            )
        ]
    ]
    t_support = Table(support_box, colWidths=[USABLE_W])
    t_support.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('LINEBELOW', (0,0), (-1,0), 1, C_SECONDARY),
    ]))
    story.append(t_support)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[OK] Generated: {OUT_PDF}")

    # Copy to brain artifact directory
    import shutil
    shutil.copy2(OUT_PDF, BRAIN_PDF)
    print(f"[OK] Copied to Brain: {BRAIN_PDF}")

if __name__ == "__main__":
    build_pdf()
