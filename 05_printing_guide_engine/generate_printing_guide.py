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
OUT_PDF = r"C:\Users\red1e\Desktop\SewLuxe_Elastic_Wide_Leg_Pants\07_Customer_Delivery_Guide\SewLuxe_Printing_And_Assembling_Guide.pdf"
BRAIN_PDF = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0\SewLuxe_Printing_And_Assembling_Guide.pdf"

# Register Fonts
pdfmetrics.registerFont(TTFont("Lora-Regular", os.path.join(FONTS_DIR, "Lora-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Lora-Bold", os.path.join(FONTS_DIR, "Lora-Bold.ttf")))
pdfmetrics.registerFont(TTFont("Lora-Italic", os.path.join(FONTS_DIR, "Lora-Italic.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Regular", os.path.join(FONTS_DIR, "Poppins-Regular.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Medium", os.path.join(FONTS_DIR, "Poppins-Medium.ttf")))
pdfmetrics.registerFont(TTFont("Poppins-Bold", os.path.join(FONTS_DIR, "Poppins-Bold.ttf")))

# Color Palette
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
            self.drawString(MARGIN_L, PAGE_H - 30, "SewLuxePatterns · Universal Printing & Assembling Guide")
            self.setFont("Poppins-Medium", 8)
            self.drawRightString(PAGE_W - MARGIN_R, PAGE_H - 30, "PDF PATTERN SUCCESS GUIDE")
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
        "CoverBrand",
        fontName="Lora-Italic",
        fontSize=20,
        leading=24,
        textColor=C_SECONDARY,
        alignment=1
    )
    st_cover_title = ParagraphStyle(
        "CoverTitle",
        fontName="Lora-Bold",
        fontSize=30,
        leading=36,
        textColor=C_PRIMARY,
        alignment=1
    )
    st_cover_sub = ParagraphStyle(
        "CoverSub",
        fontName="Poppins-Regular",
        fontSize=12,
        leading=18,
        textColor=C_MUTED,
        alignment=1
    )
    st_section_h1 = ParagraphStyle(
        "SectionH1",
        fontName="Lora-Bold",
        fontSize=20,
        leading=25,
        textColor=C_PRIMARY,
        spaceAfter=4
    )
    st_section_sub = ParagraphStyle(
        "SectionSub",
        fontName="Lora-Italic",
        fontSize=11,
        leading=15,
        textColor=C_MUTED,
        spaceAfter=14
    )
    st_card_title = ParagraphStyle(
        "CardTitle",
        fontName="Lora-Bold",
        fontSize=13,
        leading=17,
        textColor=C_PRIMARY,
        spaceAfter=4
    )
    st_body = ParagraphStyle(
        "BodyDark",
        fontName="Poppins-Regular",
        fontSize=9.5,
        leading=14.5,
        textColor=C_TEXT
    )
    st_body_bold = ParagraphStyle(
        "BodyBold",
        fontName="Poppins-Bold",
        fontSize=9.5,
        leading=14.5,
        textColor=C_TEXT
    )
    st_bullet = ParagraphStyle(
        "BulletText",
        fontName="Poppins-Regular",
        fontSize=9.5,
        leading=14.5,
        textColor=C_TEXT,
        leftIndent=14
    )

    story = []

    # ==========================================
    # PAGE 1: COVER & QUICK START
    # ==========================================
    story.append(Spacer(1, 15))
    story.append(Paragraph("SewLuxePatterns", st_cover_brand))
    story.append(Spacer(1, 10))
    story.append(Paragraph("How to Download, Print & Assemble<br/>Your PDF Sewing Pattern", st_cover_title))
    story.append(Spacer(1, 10))
    story.append(Paragraph("A comprehensive companion guide for flawless scale, effortless assembly, and professional fit", st_cover_sub))
    story.append(Spacer(1, 24))

    # Golden Rule Box
    golden_content = [
        [
            Paragraph("⭐ THE GOLDEN RULE OF PDF PATTERNS", ParagraphStyle("GRHead", fontName="Poppins-Bold", fontSize=11, leading=14, textColor=C_WHITE)),
        ],
        [
            Paragraph(
                "Always open and print your pattern files from the <b>free Adobe Acrobat Reader</b> software on a <b>laptop or desktop computer</b>.<br/><br/>"
                "• <b>NEVER</b> print directly from a web browser window (Chrome, Safari, Edge) or a smartphone/tablet app. Web browsers and mobile viewers automatically shrink or stretch pages to fit their margins, which will distort the sizing of your finished garment.<br/>"
                "• Download free Adobe Acrobat Reader at: <b>get.adobe.com/reader</b>",
                ParagraphStyle("GRBody", fontName="Poppins-Regular", fontSize=9.5, leading=14.5, textColor=HexColor("#F5F2EF"))
            )
        ]
    ]
    t_golden = Table(golden_content, colWidths=[USABLE_W])
    t_golden.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 16),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBELOW', (0,0), (-1,0), 1, C_SECONDARY),
    ]))
    story.append(t_golden)
    story.append(Spacer(1, 20))

    # Quick Start Steps
    story.append(Paragraph("Quick-Start Checklist (From Checkout to Cutting)", st_card_title))
    story.append(Spacer(1, 8))

    steps_data = [
        [
            Paragraph("<b>1. Download Files</b>", st_body_bold),
            Paragraph("Access your purchase on Etsy via a computer browser: <i>Etsy > Purchases & Reviews > Download Files</i>. Save the ZIP archives to your computer desktop.", st_body)
        ],
        [
            Paragraph("<b>2. Unzip & Select Format</b>", st_body_bold),
            Paragraph("Right-click the downloaded ZIP folder and select <i>Extract All</i>. Choose the folder matching your printer: <b>A4</b> (International) or <b>US Letter</b> (North America).", st_body)
        ],
        [
            Paragraph("<b>3. Open in Adobe Reader</b>", st_body_bold),
            Paragraph("Open your chosen pattern size in Adobe Acrobat Reader. Check that the layers menu shows your desired size.", st_body)
        ],
        [
            Paragraph("<b>4. Print Page 1 & Measure</b>", st_body_bold),
            Paragraph("Print ONLY Page 1 first. Set print scaling to <b>100% / Actual Size</b>. Measure the 4x4 in (10x10 cm) test square with a rigid ruler before printing the rest.", st_body)
        ],
        [
            Paragraph("<b>5. Assemble & Sew</b>", st_body_bold),
            Paragraph("Trim the border margins, match the alignment markers, tape the tiled sheets into rows, and cut your fabric with pure confidence!", st_body)
        ]
    ]
    t_steps = Table(steps_data, colWidths=[140, USABLE_W - 140])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_WARM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_steps)

    story.append(PageBreak())

    # ==========================================
    # PAGE 2: SCALE VERIFICATION & PRINTER SETTINGS
    # ==========================================
    story.append(Paragraph("1. Scale Verification & Printer Settings", st_section_h1))
    story.append(Paragraph("How to configure your home printer for 100% pixel-perfect accuracy", st_section_sub))

    p2_box = [
        [
            Paragraph("<b>The Test Square: Your Precision Guarantee</b>", st_card_title),
        ],
        [
            Paragraph(
                "Every SewLuxe pattern file includes a precision <b>4 in × 4 in (101.6 mm × 101.6 mm)</b> calibration square on Page 1. This square is drafted with CAD precision to guarantee that your printer reproduces the garment exactly to scale.<br/><br/>"
                "<b>How to verify your scale:</b><br/>"
                "1. Open your pattern PDF in Adobe Acrobat Reader.<br/>"
                "2. Press <b>Ctrl+P</b> (Windows) or <b>Cmd+P</b> (Mac) to open the print dialog.<br/>"
                "3. Under <i>Pages to Print</i>, select <b>Page 1 only</b>.<br/>"
                "4. In the <i>Page Sizing & Handling</i> section, select <b>Actual Size</b> (or enter <b>Custom Scale: 100%</b>).<br/>"
                "5. Uncheck 'Choose paper source by PDF page size'.<br/>"
                "6. Click <b>Print</b>.",
                st_body
            )
        ]
    ]
    t_p2 = Table(p2_box, colWidths=[USABLE_W])
    t_p2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_WARM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p2)
    story.append(Spacer(1, 16))

    # Measuring Table
    measure_box = [
        [
            Paragraph("<b>Ruler Measurement Check</b>", st_body_bold),
            Paragraph("<b>What to Do If the Size is Off</b>", st_body_bold)
        ],
        [
            Paragraph(
                "Measure the printed test box using a <b>metal ruler or rigid measuring stick</b> (avoid soft fabric measuring tapes, as they stretch over time).<br/><br/>"
                "• <b>Imperial:</b> Exactly 4.0 inches on all 4 sides.<br/>"
                "• <b>Metric:</b> Exactly 10.2 cm (101.6 mm) on all 4 sides.<br/><br/>"
                "If both measurements match, your setup is 100% accurate! Proceed to print the full pattern.",
                st_body
            ),
            Paragraph(
                "• <b>If the box measures 3.75 in (9.5 cm):</b> Your printer is applying 'Fit to Page' or 'Scale to Fit'. Return to the print settings and ensure <i>Actual Size</i> is selected.<br/><br/>"
                "• <b>If printing from Mac Preview:</b> Open the PDF in free Adobe Acrobat Reader instead. Mac Preview often overrides scaling rules.<br/><br/>"
                "• <b>Still troubleshooting?</b> Send us a message on Etsy with your printer model and we will assist immediately!",
                st_body
            )
        ]
    ]
    t_measure = Table(measure_box, colWidths=[USABLE_W/2, USABLE_W/2])
    t_measure.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1.5, C_SECONDARY),
        ('INNERGRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_measure)
    story.append(Spacer(1, 16))

    story.append(Paragraph("<b>Paper Selection & Orientation:</b>", st_card_title))
    story.append(Paragraph("• <b>North American Sewists:</b> Choose the <i>US Letter</i> files (8.5 × 11 in paper). Set printer paper to Letter and Auto portrait/landscape.<br/>"
                           "• <b>International Sewists:</b> Choose the <i>A4</i> files (210 × 297 mm paper). Set printer paper to A4.<br/>"
                           "• <b>Quality:</b> Standard or Draft black & white printing is ideal. High-resolution glossy photo settings are unnecessary.", st_body))

    story.append(PageBreak())

    # ==========================================
    # PAGE 3: ASSEMBLING TILED SHEETS
    # ==========================================
    story.append(Paragraph("2. Assembling Tiled A4 & US Letter Sheets", st_section_h1))
    story.append(Paragraph("A fast, stress-free system to tape your pattern sheets together flawlessly", st_section_sub))

    p3_intro = [
        [
            Paragraph("<b>Understanding the Tile Coordinate System</b>", st_card_title)
        ],
        [
            Paragraph(
                "Every tiled page features clear coordinate numbers at the edge (for example: <b>1/1, 2/1, 3/1...</b>).<br/>"
                "• The <b>first number</b> indicates the column from left to right.<br/>"
                "• The <b>second number</b> indicates the horizontal row from top to bottom.<br/>"
                "• Alignment diamonds and dashed borderlines guide you to align pages with millimetric precision.",
                st_body
            )
        ]
    ]
    t_p3 = Table(p3_intro, colWidths=[USABLE_W])
    t_p3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_WARM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p3)
    story.append(Spacer(1, 16))

    # Fast Trimming Method
    trim_box = [
        [
            Paragraph("<b>The Pro 'Half-Trim' Method (Saves 50% Assembly Time!)</b>", ParagraphStyle("TH", fontName="Poppins-Bold", fontSize=11, leading=15, textColor=C_PRIMARY))
        ],
        [
            Paragraph(
                "You do <b>NOT</b> need to trim all four margins of every sheet! Trimming all four sides is exhausting and unnecessary. Follow this professional shortcut instead:<br/><br/>"
                "1. <b>Trim ONLY the Right & Bottom Margins:</b> Use paper shears or a rotary cutter on a cutting mat to slice along the dashed borderlines on the <b>right edge</b> and the <b>bottom edge</b> of each page. Leave the top and left borders untrimmed.<br/><br/>"
                "2. <b>Assemble in Rows:</b> Overlap the trimmed right edge of Page 1 onto the untrimmed left border of Page 2. Match the corner alignment diamonds and tape in place. Complete Row 1 first.<br/><br/>"
                "3. <b>Join the Rows Together:</b> Overlap the trimmed bottom edge of Row 1 onto the untrimmed top border of Row 2. Align the vertical seamlines and tape across the horizontal junction.<br/><br/>"
                "4. <b>Tape Recommendation:</b> Use matte invisible tape (Magic Tape). Matte tape can be lightly pressed with a warm iron if pattern sheets become wrinkled, and you can write notes on it with a pencil or ballpoint pen.",
                st_body
            )
        ]
    ]
    t_trim = Table(trim_box, colWidths=[USABLE_W])
    t_trim.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1.5, C_SECONDARY),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_trim)
    story.append(Spacer(1, 16))

    story.append(Paragraph("<b>Helpful Assembly Tips:</b>", st_card_title))
    story.append(Paragraph("• <b>Smooth Surface:</b> Assemble your pattern on a clean kitchen table or hard floor. Carpet allows paper to bow and skew.<br/>"
                           "• <b>Pattern Weights:</b> Place household items (mugs, smooth stones, or scissors) on pages while taping to keep them completely flat.<br/>"
                           "• <b>Cut-Out Lines:</b> Trace or cut along the exact solid outline corresponding to your size. All seam allowances are already included!", st_body))

    story.append(PageBreak())

    # ==========================================
    # PAGE 4: A0 COPYSHOP & PROJECTOR SEWING
    # ==========================================
    story.append(Paragraph("3. A0 Copyshop & Fabric Projector Guide", st_section_h1))
    story.append(Paragraph("Zero-taping commercial printing and modern paperless projector setups", st_section_sub))

    a0_box = [
        [
            Paragraph("<b>Printing Wide-Format A0 Files at a Copy Shop</b>", st_card_title)
        ],
        [
            Paragraph(
                "If you prefer zero paper trimming and zero taping, use the included <b>A0 Copyshop Large-Format PDF</b>. A0 sheets measure 33.1 × 46.8 inches (841 × 1189 mm) and print the entire garment in continuous, full-scale layouts.<br/><br/>"
                "<b>How to order A0 prints:</b><br/>"
                "• <b>Local Print Shops:</b> Upload or take your A0 PDF file to any local commercial printer (e.g., Staples, FedEx Office, Office Depot, or local blueprint/architectural shops).<br/>"
                "• <b>Online Pattern Printers:</b> Dedicated online pattern printing services (such as PDFPlotting, Patternsy, NetPrinter, or Spool & Spindle) specialize in shipping inexpensive folded pattern sheets directly to your door.<br/>"
                "• <b>What to specify:</b> Instruct the printer: <i>'Please print at 100% scale (no scaling) on standard lightweight black & white 20 lb bond / 75-80 gsm paper.'</i><br/>"
                "• Always verify the 4x4 in calibration square on the printed sheet before cutting your fabric.",
                st_body
            )
        ]
    ]
    t_a0 = Table(a0_box, colWidths=[USABLE_W])
    t_a0.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_WARM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_a0)
    story.append(Spacer(1, 16))

    proj_box = [
        [
            Paragraph("<b>Using Fabric Projectors (Paperless Sewing)</b>", st_card_title)
        ],
        [
            Paragraph(
                "Projector sewing eliminates paper completely by projecting the pattern pieces directly onto your cutting mat and fabric from a ceiling-mounted or mini ultra-short-throw projector.<br/><br/>"
                "<b>Quick Setup Walkthrough:</b><br/>"
                "1. <b>Open in Adobe Acrobat:</b> Open the A0 or wide-format PDF in Adobe Reader on your computer or tablet.<br/>"
                "2. <b>Full Screen Mode:</b> Press <b>Ctrl+L</b> (Windows) or <b>Cmd+L</b> (Mac) to enter borderless full-screen view.<br/>"
                "3. <b>Calibrate Scale:</b> Zoom in or out until the projected 4x4 in (10x10 cm) test square aligns 100% accurately with the inch/cm grid lines printed on your physical cutting mat.<br/>"
                "4. <b>Keystone Check:</b> Verify that the projected lines are completely square at all four corners of your cutting mat.<br/>"
                "5. <b>Cut Directly:</b> Place your fabric smoothly on the cutting mat and cut out pieces using a rotary cutter!",
                st_body
            )
        ]
    ]
    t_proj = Table(proj_box, colWidths=[USABLE_W])
    t_proj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1.5, C_SECONDARY),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_proj)

    story.append(PageBreak())

    # ==========================================
    # PAGE 5: SIZING & GRADING BETWEEN SIZES
    # ==========================================
    story.append(Paragraph("4. Choosing Your Size & Grading Between Sizes", st_section_h1))
    story.append(Paragraph("How to achieve a custom couture fit tailored to your unique body proportions", st_section_sub))

    p5_guide = [
        [
            Paragraph("<b>Step 1: Choose Your Governing Measurement</b>", st_card_title)
        ],
        [
            Paragraph(
                "Garments are engineered with different primary focal points. Compare your body measurements against the Body Measurement Chart in the sewing booklet:<br/>"
                "• <b>Trousers, Pants & Skirts:</b> Governed by your <b>Full Hip measurement</b> (the fullest part around your buttocks). If your waist and hip fall into different sizes, always pick the size matching your hip, because elastic waistbands easily adapt to waist circumference.<br/>"
                "• <b>Tops, Jackets & Dresses:</b> Governed by your <b>Upper Bust / Full Bust measurement</b>.<br/>"
                "• <b>Finished Garment Measurements:</b> Check the finished measurement tables in Page 4 of the booklet to see how much wearing ease is designed into the silhouette.",
                st_body
            )
        ]
    ]
    t_p5 = Table(p5_guide, colWidths=[USABLE_W])
    t_p5.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_WARM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_p5)
    story.append(Spacer(1, 16))

    grading_box = [
        [
            Paragraph("<b>How to Grade Between Two Sizes (Blending Curves)</b>", ParagraphStyle("GH", fontName="Poppins-Bold", fontSize=11, leading=15, textColor=C_PRIMARY))
        ],
        [
            Paragraph(
                "Human bodies rarely fit into a single standard size! Blending between sizes is simple and ensures garments hang cleanly without pulling or pooling:<br/><br/>"
                "<b>Example Scenario:</b> Your waist measures Size 8, but your hips measure Size 12.<br/>"
                "1. <b>Print Both Sizes:</b> Print the pattern sheets with both sizes visible.<br/>"
                "2. <b>Locate Key Balance Points:</b> Mark the waistline notch on the Size 8 line, and mark the hipline level on the Size 12 line.<br/>"
                "3. <b>Draw a Smooth Blend Line:</b> Using a curved ruler or French curve (or a steady hand), draw a smooth, gentle diagonal line connecting the Size 8 waist to the Size 12 hip along the side seam.<br/>"
                "4. <b>Maintain Pocket & Balance Notches:</b> Ensure pocket markings and balance notches transition smoothly without sharp corners or kinks.<br/>"
                "5. <b>True the Seams:</b> Measure the front side seam blend and rear side seam blend to confirm both edges are the exact same vertical length.",
                st_body
            )
        ]
    ]
    t_grade = Table(grading_box, colWidths=[USABLE_W])
    t_grade.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_WHITE),
        ('BOX', (0,0), (-1,-1), 1.5, C_SECONDARY),
        ('PADDING', (0,0), (-1,-1), 14),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_grade)

    story.append(PageBreak())

    # ==========================================
    # PAGE 6: LENGTH ADJUSTMENTS & CUSTOMER SUPPORT
    # ==========================================
    story.append(Paragraph("5. Lengthening, Shortening & 5-Star Support", st_section_h1))
    story.append(Paragraph("Simple pattern adjustments and our dedicated customer care guarantee", st_section_sub))

    adj_box = [
        [
            Paragraph("<b>Lengthening & Shortening Garment Pieces</b>", st_card_title)
        ],
        [
            Paragraph(
                "SewLuxe patterns are drafted for an average height of 5'5\" – 5'7\" (165 – 170 cm). If you are taller or petite, adjust your pattern pieces before cutting:<br/><br/>"
                "• <b>To Lengthen:</b> Cut the pattern piece horizontally across the middle of the leg (or torso). Place a scrap piece of paper underneath, spread the two pieces apart by the desired amount (e.g., 2 in / 5 cm), keeping cut edges parallel, and tape flat. Blend the side seam smooth.<br/>"
                "• <b>To Shorten:</b> Draw a horizontal fold line across the leg or torso. Fold the pattern upward by half the desired reduction (e.g., fold up 1 in / 2.5 cm to shorten total length by 2 in / 5 cm), tape flat, and smooth the side seam.<br/>"
                "• <b>Hem Adjustments:</b> For minor adjustments (under 1.5 in / 4 cm), simply trim or extend at the hemline while honoring the hem allowance.",
                st_body
            )
        ]
    ]
    t_adj = Table(adj_box, colWidths=[USABLE_W])
    t_adj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_WARM),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 12),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(t_adj)
    story.append(Spacer(1, 16))

    # Support Guarantee Card
    support_box = [
        [
            Paragraph("💌 WE ARE HERE TO HELP YOU SUCCEED!", ParagraphStyle("SH", fontName="Poppins-Bold", fontSize=12, leading=16, textColor=C_WHITE))
        ],
        [
            Paragraph(
                "Every sewist deserves a joyful, stress-free making experience. If you ever feel unsure about:<br/>"
                "• Choosing the ideal size for your body measurements<br/>"
                "• Selecting fabric weight, drape, or notions<br/>"
                "• Troubleshooting printer scale or assembly alignment<br/>"
                "• Understanding a specific sewing technique or step in the instructions<br/><br/>"
                "<b>Please send us a direct message anytime on Etsy!</b><br/>"
                "We check our shop inbox continuously and will gladly review your measurements, provide custom advice, and walk you through every step.<br/><br/>"
                "<i>Thank you for making SewLuxePatterns part of your handmade wardrobe. Happy sewing! ❤️</i>",
                ParagraphStyle("SBody", fontName="Poppins-Regular", fontSize=10, leading=15, textColor=HexColor("#F5F2EF"))
            )
        ]
    ]
    t_support = Table(support_box, colWidths=[USABLE_W])
    t_support.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_PRIMARY),
        ('PADDING', (0,0), (-1,-1), 18),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
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
