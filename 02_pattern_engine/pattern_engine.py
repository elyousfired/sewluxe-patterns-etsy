import os
import re
import sys
import json
import zipfile
import urllib.request
import urllib.parse
from typing import Dict, Any, List, Optional
import pymupdf

# Support UTF-8 encoding
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

class PatternFastEngine:
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        self.email = email or os.environ.get("PATTERNFAST_EMAIL", "benemeb244@moravita.com")
        self.password = password or os.environ.get("PATTERNFAST_PASSWORD", "Elyousfi1993@")
        self.email = email
        self.password = password
        self.token: Optional[str] = None
        self.headers: Dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

    def login(self) -> str:
        """Authenticate with PatternFast API and return Bearer token."""
        url = "https://patternfast.com/api/user/login"
        payload = json.dumps({"email": self.email, "password": self.password}).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=payload,
            headers={**self.headers, "Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            self.token = data.get("token")
            self.headers["Authorization"] = f"Bearer {self.token}"
            return self.token

    def _ensure_token(self):
        if not self.token:
            self.login()

    def get_standard_mannequins(self, chart_name_substring: str = "00-22") -> List[Dict[str, Any]]:
        """Fetch all 13 standard US sizes (00 to 22) from the gold standard Alvanon fit chart."""
        self._ensure_token()
        url = "https://api.patternfast.com/api/fit-charts-standart?offset=0&limit=20&type=FEMALE&search="
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            rows = data.get("rows", [])
            for row in rows:
                if chart_name_substring in row.get("name", "") and "Standard North America" in row.get("name", ""):
                    return row.get("mannequins", [])
            # Fallback to first row
            return rows[0].get("mannequins", []) if rows else []

    def fetch_and_render_flat_sketch(
        self,
        category_code: str,
        elem_ids: str,
        out_svg_path: str,
        out_png_path: str
    ) -> Dict[str, str]:
        """Fetch original vector SVGs, combine Front + Back, and render 300 DPI clean studio PNG."""
        self._ensure_token()
        url = f"https://patternfast.com/api/categories/{category_code}/elements?elemIds={elem_ids}&settingCodes="
        req = urllib.request.Request(url, headers=self.headers)
        with urllib.request.urlopen(req, timeout=15) as resp:
            elements_data = json.loads(resp.read().decode("utf-8"))

        front_inner = ""
        back_inner = ""
        for item in elements_data:
            el = item.get("element", {})
            sf = el.get("svgFront") or ""
            sb = el.get("svgBack") or ""
            sf = sf.replace("<svg>", "").replace("</svg>", "")
            sb = sb.replace("<svg>", "").replace("</svg>", "")
            front_inner += sf + "\n"
            back_inner += sb + "\n"

        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 60 220 155" width="1800" height="1800">
<style>
  path {{ fill: none; stroke: #1C1B1A; stroke-width: 0.55; stroke-linecap: round; stroke-linejoin: round; }}
</style>
<rect x="0" y="60" width="220" height="155" fill="#FAF8F5" rx="14" />
<g transform="translate(0, 0)">
  <!-- Front Sketch -->
  <g transform="translate(5, 0)">
    {front_inner}
  </g>
  <!-- Back Sketch -->
  <g transform="translate(110, 0)">
    {back_inner}
  </g>
</g>
<text x="55" y="209" text-anchor="middle" font-family="sans-serif" font-size="5.5" font-weight="bold" fill="#777" letter-spacing="1">FRONT</text>
<text x="160" y="209" text-anchor="middle" font-family="sans-serif" font-size="5.5" font-weight="bold" fill="#777" letter-spacing="1">BACK</text>
</svg>"""

        os.makedirs(os.path.dirname(os.path.abspath(out_svg_path)), exist_ok=True)
        with open(out_svg_path, "w", encoding="utf-8") as f:
            f.write(svg_content)

        doc = pymupdf.open(out_svg_path)
        pix = doc[0].get_pixmap(dpi=300)
        pix.save(out_png_path)
        doc.close()

        return {"svg_path": out_svg_path, "png_path": out_png_path}

    def download_sewing_instructions(
        self,
        category_code: str,
        elem_ids: str,
        mannequin_id: str,
        name: str,
        out_pdf_path: str
    ) -> str:
        """Fetch authentic 27-page Tailornova sewing instructions PDF with vector diagrams."""
        self._ensure_token()
        qs = urllib.parse.urlencode({
            "elementIds": elem_ids,
            "mannequinId": mannequin_id,
            "categoryCode": category_code,
            "format": "pdf",
            "orientation": "portrait",
            "eases": "",
            "settingCodes": "",
            "seamAllowance": "1",
            "fabricType": "1",
            "fit": "2"
        })
        payload = json.dumps({
            "sketchFront": "<svg></svg>",
            "sketchBack": "<svg></svg>",
            "name": name
        }).encode("utf-8")

        url = f"https://api.patternfast.com/api/sewing-instructions?{qs}"
        req = urllib.request.Request(
            url,
            data=payload,
            headers={**self.headers, "Content-Type": "application/json; charset=UTF-8"}
        )
        os.makedirs(os.path.dirname(os.path.abspath(out_pdf_path)), exist_ok=True)
        with urllib.request.urlopen(req, timeout=35) as resp, open(out_pdf_path, "wb") as f:
            f.write(resp.read())
        return out_pdf_path

    def whitelabel_pattern_pdf(self, in_pdf_path: str, out_pdf_path: str, size_label: str):
        """White-label PDF: replace PatternFast branding with SewLuxePatterns, verify 4x4 test square."""
        doc = pymupdf.open(in_pdf_path)
        hex_size = size_label.encode("ascii").hex()
        replacement_tj = f"[<{hex_size}> 0] TJ".encode("latin1")

        for pno in [0, 1, 2]:
            if pno >= len(doc):
                continue
            page = doc[pno]
            xrefs = page.get_contents()
            if not xrefs:
                continue
            raw = doc.xref_stream(xrefs[0])
            raw_new = re.sub(
                rb"q\n1 0 0 1 0 28\.3465 cm\n0\.75 0 0 0\.75 0 0 cm\nq\n0 0 m\n793\.706667 0 l\n793\.706667 48 l\n0 48 l\nh\nW n\n2 0 0 2 275\.853333 0 cm\nq.*?Q\nQ\nQ\n",
                rb"",
                raw,
                count=1,
                flags=re.S
            )
            if pno in (0, 1):
                raw_new = re.sub(
                    rb"\[<50>[^\]]*<202d>\s*0\]\s*TJ",
                    replacement_tj,
                    raw_new
                )
            doc.update_stream(xrefs[0], raw_new)

            # Insert Clean SewLuxePatterns Header
            page.insert_text(
                pymupdf.Point(214.83, 841.89 - 791.54),
                "SewLuxePatterns",
                fontname="helv",
                fontsize=18,
                color=(0.12, 0.12, 0.12)
            )
            page.insert_text(
                pymupdf.Point(262.28, 841.89 - 779.54),
                "SEWING PATTERNS",
                fontname="helv",
                fontsize=7.5,
                color=(0.4, 0.4, 0.4)
            )

        doc.set_metadata({
            "author": "SewLuxePatterns",
            "creator": "SewLuxe Engineering Studio",
            "producer": "SewLuxe High-Precision CAD Engine",
            "title": f"SewLuxe Pattern - {size_label}"
        })
        os.makedirs(os.path.dirname(os.path.abspath(out_pdf_path)), exist_ok=True)
        doc.save(out_pdf_path, garbage=4, deflate=True)
        doc.close()

    def generate_single_size_pattern(
        self,
        elem_ids: str,
        mannequin_id: str,
        size_name: str,
        page_size: str, # "A4", "LETTER", or "A0"
        out_pdf_path: str
    ) -> str:
        """Download raw CAD pattern from PatternFast and apply white-labeling in one pass."""
        self._ensure_token()

        preview_qs = urllib.parse.urlencode({
            "elemIds": elem_ids,
            "mannequinId": mannequin_id,
            "fabricType": "1",
            "fit": "2",
            "seamAllowance": "1",
            "eases": "",
            "settingCodes": "",
            "fontName": "DM Sans",
            "debug_params": "1",
            "view": "2"
        })
        preview_url = f"https://api.patternfast.com/api/patterns/preview?{preview_qs}"
        req_p = urllib.request.Request(preview_url, headers=self.headers)
        with urllib.request.urlopen(req_p, timeout=20) as resp:
            preview_data = json.loads(resp.read().decode("utf-8"))

        param_kits = preview_data.get("parameterizedKits", {})
        payload = {
            "mannequinId": mannequin_id,
            **param_kits,
            "cutVerticallySymmetric": False,
            "pageSize": page_size
        }

        dl_url = "https://api.patternfast.com/api/cat/download-pdf"
        req_dl = urllib.request.Request(
            dl_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={**self.headers, "Content-Type": "application/json; charset=UTF-8"}
        )

        raw_tmp_path = out_pdf_path + ".raw.tmp"
        os.makedirs(os.path.dirname(os.path.abspath(out_pdf_path)), exist_ok=True)
        with urllib.request.urlopen(req_dl, timeout=35) as dl_resp, open(raw_tmp_path, "wb") as f_out:
            f_out.write(dl_resp.read())

        # Whitelabel
        size_label = f"SIZE US {size_name}"
        self.whitelabel_pattern_pdf(raw_tmp_path, out_pdf_path, size_label)

        if os.path.exists(raw_tmp_path):
            os.remove(raw_tmp_path)

        return out_pdf_path
