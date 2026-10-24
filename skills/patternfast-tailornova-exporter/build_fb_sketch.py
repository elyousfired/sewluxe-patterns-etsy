import os
from PIL import Image, ImageOps
import xml.etree.ElementTree as ET
import pymupdf as fitz
import copy

BRAIN_DIR = r"C:\Users\red1e\.gemini\antigravity\brain\0e44cbbf-4db1-4039-afc1-6d1991b659b0"

def get_bbox(im):
    gray = im.convert("L")
    inv = ImageOps.invert(gray)
    bbox = inv.getbbox()
    return im.crop(bbox)

# Process Front Button SVG
tree = ET.parse(os.path.join(BRAIN_DIR, "PatternFast_Original_Authentic_Sketch.svg"))
root = tree.getroot()

# Front only
root_front = copy.deepcopy(root)
for g in list(root_front):
    if '{http://www.w3.org/2000/svg}g' in g.tag:
        for child in list(g):
            if child.attrib.get('class') == 'back-view':
                g.remove(child)

doc_front = fitz.open(stream=ET.tostring(root_front, encoding='utf-8'), filetype='svg')
im_front = Image.frombytes("RGB", [doc_front[0].get_pixmap(dpi=300).width, doc_front[0].get_pixmap(dpi=300).height], doc_front[0].get_pixmap(dpi=300).samples)

# Back only
root_back = copy.deepcopy(root)
for g in list(root_back):
    if '{http://www.w3.org/2000/svg}g' in g.tag:
        for child in list(g):
            if child.attrib.get('class') == 'front-view':
                g.remove(child)
            elif child.attrib.get('class') == 'back-view':
                child.attrib.pop('transform', None)

doc_back = fitz.open(stream=ET.tostring(root_back, encoding='utf-8'), filetype='svg')
im_back = Image.frombytes("RGB", [doc_back[0].get_pixmap(dpi=300).width, doc_back[0].get_pixmap(dpi=300).height], doc_back[0].get_pixmap(dpi=300).samples)

front_crop = get_bbox(im_front)
back_crop = get_bbox(im_back)

canvas_fb = Image.new("RGB", (1800, 1800), (255, 255, 255))
target_h = 1350
f_ratio = target_h / front_crop.height
f_w = int(front_crop.width * f_ratio)
front_resized = front_crop.resize((f_w, target_h), Image.Resampling.LANCZOS)

b_ratio = target_h / back_crop.height
b_w = int(back_crop.width * b_ratio)
back_resized = back_crop.resize((b_w, target_h), Image.Resampling.LANCZOS)

gap = 120
total_w = f_w + b_w + gap
start_x = (1800 - total_w) // 2
y = (1800 - target_h) // 2

canvas_fb.paste(front_resized, (start_x, y))
canvas_fb.paste(back_resized, (start_x + f_w + gap, y))

out_path_fb = os.path.join(BRAIN_DIR, "PatternFast_Original_Front_Button_1800.png")
canvas_fb.save(out_path_fb, quality=95)
print("Saved PatternFast_Original_Front_Button_1800.png")
