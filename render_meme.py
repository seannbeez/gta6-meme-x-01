#!/usr/bin/env python3
"""Render the gta6-meme-x-01 v1 meme: LEONIDA EXPRESS delivery tracking.

Code-drawn 1080x1080 document parody. Deterministic: same input -> same bytes.
Assets: make.fun ghost mark (press kit, mark-1024.png) composited in the footer.
"""
from datetime import date
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1080
OUT = "/home/hatch/workspace/makefun/gta6-meme-x-01/meme-v1.png"
GHOST = "/home/hatch/workspace/makefun/gta6-meme-x-01/assets/mark-1024.png"

FONT_DIR = "/usr/share/fonts/truetype/noto/"
F_BLACK = FONT_DIR + "NotoSans-Black.ttf"
F_BOLD = FONT_DIR + "NotoSans-Bold.ttf"
F_REG = FONT_DIR + "NotoSans-Regular.ttf"
F_MONO = FONT_DIR + "NotoSansMono-Bold.ttf"
F_MONO_REG = FONT_DIR + "NotoSansMono-Regular.ttf"

NAVY = (14, 27, 46)
NAVY2 = (18, 35, 61)
PAPER = (247, 241, 222)
INK = (26, 26, 26)
MUTED = (110, 104, 88)
RED = (215, 38, 61)
GREEN = (24, 135, 70)
GOLD = (201, 162, 39)

ORDERED = date(2013, 9, 17)   # GTA V launch day — the wait starts here
TODAY = date(2026, 11, 20)
DAYS = (TODAY - ORDERED).days  # exact day count, no guessing

img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)

def font(path, size):
    return ImageFont.truetype(path, size)

# ---------- paper card ----------
d.rounded_rectangle([40, 40, 1040, 1040], radius=28, fill=PAPER)
# subtle inner border
d.rounded_rectangle([52, 52, 1028, 1028], radius=22, outline=(210, 198, 168), width=2)

# ---------- header strip ----------
d.rounded_rectangle([40, 40, 1040, 168], radius=28, fill=NAVY2)
d.rectangle([40, 140, 1040, 168], fill=NAVY2)  # square off the strip bottom
d.text((72, 62), "LEONIDA EXPRESS", font=font(F_BLACK, 56), fill=(255, 255, 255))
d.text((72, 122), "TRACK YOUR PACKAGE", font=font(F_MONO, 26), fill=(255, 214, 90))
d.text((1040 - 72, 122), "LX-2013-GTA-VI", font=font(F_MONO, 26), fill=(180, 195, 215), anchor="ra")

# ---------- item block ----------
d.text((72, 196), "GRAND THEFT AUTO VI", font=font(F_BLACK, 58), fill=INK)
d.text((72, 264), "1 x VIDEO GAME  —  ORDERED 17 SEP 2013", font=font(F_MONO, 27), fill=MUTED)
d.text((72, 300), "DELIVER TO: OCEAN DRIVE, VICE CITY, LEONIDA", font=font(F_MONO, 27), fill=MUTED)

# dashed divider
for x in range(72, 1008, 26):
    d.line([(x, 348), (x + 14, 348)], fill=(190, 178, 148), width=3)

# ---------- timeline ----------
rows = [
    ("ORDER PLACED", "17 SEP 2013", True),
    ("SHIPPED", "03 OCT 2013", True),
    ("OUT FOR DELIVERY", "2013", True),
    ("DELIVERED", f"PENDING — {DAYS:,} DAYS", False),
]
y0, row_h = 380, 80
cx = 104  # circle centre x
for i, (label, when, done) in enumerate(rows):
    cy = y0 + i * row_h + 24
    # connector line
    if i < len(rows) - 1:
        d.line([(cx, cy + 24), (cx, cy + row_h - 22)], fill=(190, 178, 148), width=4)
    # circle
    col = GREEN if done else RED
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=col, outline=(255, 255, 255), width=3)
    if done:
        # hand-drawn check (no font glyph dependency — Noto lacks U+2713)
        d.line([(cx - 11, cy), (cx - 3, cy + 9), (cx + 12, cy - 10)],
               fill=(255, 255, 255), width=5, joint="curve")
    else:
        mf = font(F_BLACK, 32)
        bb = d.textbbox((0, 0), "!", font=mf)
        d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]),
               "!", font=mf, fill=(255, 255, 255))
    # label + date
    lcol = INK if done else RED
    d.text((150, cy - 20), label, font=font(F_BLACK, 34), fill=lcol)
    d.text((1008, cy - 16), when, font=font(F_MONO, 27), fill=RED if not done else MUTED, anchor="ra")

# ---------- red stamp (rotated, bottom-right of timeline zone) ----------
stamp = Image.new("RGBA", (380, 120), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([6, 6, 374, 114], radius=14, outline=RED, width=6)
sd.rounded_rectangle([16, 16, 364, 104], radius=10, outline=RED, width=2)
sd.text((190, 20), "STILL WAITING", font=font(F_BLACK, 46), fill=RED, anchor="ma")
sd.text((190, 70), "13 YEARS", font=font(F_BLACK, 36), fill=RED, anchor="ma")
stamp = stamp.rotate(-8, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (590, 682), stamp)

# ---------- footer band ----------
d.rounded_rectangle([40, 856, 1040, 1040], radius=28, fill=NAVY2)
d.rectangle([40, 856, 1040, 900], fill=NAVY2)  # square off the band top
ghost = Image.open(GHOST).convert("RGBA").resize((132, 132), Image.LANCZOS)
img.paste(ghost, (72, 872), ghost)
d.text((228, 878), "My AI agent didn't wait 13 years —", font=font(F_BOLD, 31), fill=(255, 255, 255))
d.text((228, 918), "it already got paid on make.fun", font=font(F_BOLD, 31), fill=(255, 214, 90))
d.text((228, 962), "make.fun  •  agents win real money", font=font(F_MONO, 22), fill=(180, 195, 215))

img.save(OUT, "PNG")
print("saved", OUT, "days:", DAYS)
