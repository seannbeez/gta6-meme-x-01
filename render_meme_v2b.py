#!/usr/bin/env python3
"""Render the gta6-meme-x-01 v2b meme: LEONIDA EXPRESS missing-parcel
investigation report — a photo of a physical paper form, NOT a flat
graphic card. Vintage yellowed paper, fibre texture, fold creases,
typewriter (Liberation Mono) typography, a drawn CCTV evidence photo of
the dusty GTA VI box, and a giant wet-ink stamp as the focal point.

Deterministic: same input -> same bytes (seeded RNGs).
Assets: make.fun ghost mark (press kit, mark-1024.png) as letterhead logo.
"""
import random
from datetime import date
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageEnhance

W, H = 1080, 1080
OUT = "/home/hatch/workspace/makefun/gta6-meme-x-01/meme-v2b.png"
GHOST = "/home/hatch/workspace/makefun/gta6-meme-x-01/assets/mark-1024.png"

NOTO = "/usr/share/fonts/truetype/noto/"
LIB = "/usr/share/fonts/truetype/liberation/"
F_BLACK = NOTO + "NotoSans-Black.ttf"
F_BOLD = NOTO + "NotoSans-Bold.ttf"
F_MONO = LIB + "LiberationMono-Bold.ttf"
F_MONO_REG = LIB + "LiberationMono-Regular.ttf"

PAPER = (231, 217, 180)
INK = (42, 36, 25)
MUTED = (107, 95, 69)
FAINT = (190, 175, 140)
RED = (165, 42, 29)
RED_DARK = (143, 31, 20)

ORDERED = date(2013, 9, 17)
TODAY = date(2026, 11, 20)
DAYS = (TODAY - ORDERED).days  # 4,812 exact

rng = random.Random(2013)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def tracked(draw, xy, text, fnt, fill, tracking=3):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def wrap(draw, text, fnt, max_w):
    words = text.split(" ")
    lines, cur = [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


# ---------- paper fibre + grain ----------
fibre = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(fibre)
fr = random.Random(2013)
for _ in range(900):
    x, y = fr.randint(0, W - 1), fr.randint(0, H - 1)
    ln = fr.randint(8, 60)
    col = (217, 201, 160, 46) if fr.random() < 0.5 else (242, 232, 204, 46)
    fd.line([(x, y), (x + ln, y + fr.randint(-2, 2))], fill=col, width=1)
img = Image.alpha_composite(img.convert("RGBA"), fibre).convert("RGB")
d = ImageDraw.Draw(img)
grain = Image.effect_noise((W, H), 14).convert("L")
img = Image.composite(
    img, Image.new("RGB", (W, H), (226, 211, 172)),
    grain.point(lambda p: 255 - int(p * 0.08)),
)
d = ImageDraw.Draw(img)

# ---------- fold creases (subtle: light line + shadow line) ----------
d.line([(360, 24), (360, 1056)], fill=(244, 234, 206), width=2)
d.line([(362, 24), (362, 1056)], fill=(198, 182, 140), width=1)
d.line([(24, 560), (1056, 560)], fill=(244, 234, 206), width=2)
d.line([(24, 562), (1056, 562)], fill=(198, 182, 140), width=1)

# ---------- vignette (photo-of-paper edges) ----------
vig = Image.radial_gradient("L").resize((W, H))
mask = vig.point(lambda p: int((255 - p) * 0.30))
img = Image.composite(Image.new("RGB", (W, H), (74, 58, 32)), img, mask)
d = ImageDraw.Draw(img)

# ---------- header ----------
ghost = Image.open(GHOST).convert("RGBA").resize((58, 58), Image.LANCZOS)
img.paste(ghost, (56, 50), ghost)
d.text((126, 46), "LEONIDA EXPRESS", font=font(F_MONO, 44), fill=INK)
tracked(d, (128, 100), "MISSING PARCEL INVESTIGATION REPORT",
        font(F_MONO, 23), MUTED, tracking=2)
d.text((1024, 52), "FORM LX-01", font=font(F_MONO, 20), fill=MUTED, anchor="ra")
d.text((1024, 80), "EST. 2013", font=font(F_MONO, 20), fill=MUTED, anchor="ra")
d.line([(56, 138), (1024, 138)], fill=INK, width=3)
d.line([(56, 146), (1024, 146)], fill=INK, width=1)
d.text((56, 158), "CASE ID:  LX-GTA6-2013-2026", font=font(F_MONO, 22), fill=INK)
d.text((56, 188), "RECIPIENT:  LUCIA & JASON — OCEAN DRIVE, VICE CITY, LEONIDA",
       font=font(F_MONO, 22), fill=INK)

# ---------- incident log (left + centre) ----------
d.text((56, 226), "INCIDENT LOG", font=font(F_MONO, 26), fill=INK)
d.line([(56, 260), (640, 260)], fill=INK, width=2)
rows = [
    ("17 SEP 2013", "Dispatched from Los Santos (PS3 / 30 FPS Edition)", False),
    ("14 NOV 2014", "Rerouted — Next-Gen Remaster Cash-Grab", False),
    ("15 MAR 2022", "Held at Customs — Unpaid Shark Card Tax", False),
    ("05 DEC 2023", "Trailer 1 Spotted in Leonida Airspace", False),
    ("2025 – 2026", "DELAY EXCEPTION — Rockstar Still Polishing Puddles "
     "(3x Rescheduled)", True),
]
f_date = font(F_MONO, 21)
f_ev = font(F_MONO_REG, 20)
f_ev_b = font(F_MONO, 20)
row_y, row_h = 274, 92
for i, (when, event, hot) in enumerate(rows):
    y = row_y + i * row_h
    if i:
        d.line([(56, y - 8), (640, y - 8)], fill=(210, 196, 160), width=1)
    d.text((56, y), when, font=f_date, fill=RED_DARK if hot else INK)
    ef = f_ev_b if hot else f_ev
    ecol = RED_DARK if hot else INK
    lines = wrap(d, event, ef, 434)[:2]
    for j, ln in enumerate(lines):
        d.text((206, y + j * 26), ln, font=ef, fill=ecol)

# status box
d.rectangle([56, 738, 640, 800], outline=INK, width=2)
d.rectangle([62, 744, 634, 794], outline=FAINT, width=1)
d.text((84, 758), f"STATUS:  LOST IN TRANSIT  ({DAYS:,}+ DAYS)",
       font=font(F_MONO, 23), fill=RED_DARK)

# ---------- evidence photo (top right) ----------
d.text((668, 226), "EVIDENCE PHOTO", font=font(F_MONO, 22), fill=INK)
PW, PH = 356, 258
photo = Image.new("RGB", (PW, PH), (30, 27, 23))
pd = ImageDraw.Draw(photo)
# back wall gradient (brightened so the box + webs read clearly)
for yy in range(PH):
    t = yy / PH
    pd.line([(0, yy), (PW, yy)],
            fill=(int(80 - 28 * t), int(74 - 26 * t), int(65 - 22 * t)))
# shelves (right side, faint)
pd.rectangle([258, 40, 356, 52], fill=(36, 32, 28))
pd.rectangle([258, 110, 356, 122], fill=(36, 32, 28))
pd.rectangle([272, 14, 300, 40], fill=(54, 49, 42))
pd.rectangle([312, 88, 344, 110], fill=(54, 49, 42))
# floor
pd.rectangle([0, 196, PW, PH], fill=(76, 67, 56))
pd.line([(0, 196), (PW, 196)], fill=(20, 17, 14), width=2)
# light beam from top-left
beam = Image.new("RGBA", (PW, PH), (0, 0, 0, 0))
bd = ImageDraw.Draw(beam)
bd.polygon([(20, 0), (150, 0), (260, 196), (90, 196)], fill=(255, 220, 150, 72))
photo = Image.alpha_composite(photo.convert("RGBA"), beam).convert("RGB")
pd = ImageDraw.Draw(photo)
# the box (3/4 view, centre-left) — brighter cardboard so it pops
bx0, by0, bx1, by1 = 62, 96, 252, 212
pd.polygon([(bx0, by0 + 26), (bx0 + 34, by0), (bx1 + 34, by0),
            (bx1, by0 + 26)], fill=(216, 172, 118))          # top face
pd.polygon([(bx1, by0 + 26), (bx1 + 34, by0), (bx1 + 34, by1 - 18),
            (bx1, by1)], fill=(155, 122, 74))               # side face
pd.rectangle([bx0, by0 + 26, bx1, by1], fill=(205, 158, 100))  # front face
pd.line([(bx0, by0 + 26), (bx1, by0 + 26)], fill=(140, 108, 66), width=2)
pd.line([(bx0, by0 + 26), (bx0, by1)], fill=(140, 108, 66), width=2)
pd.line([(bx1, by0 + 26), (bx1, by1)], fill=(140, 108, 66), width=2)
# tape strip down the front
pd.rectangle([bx0 + 86, by0 + 26, bx0 + 104, by1], fill=(228, 206, 152))
pd.line([(bx0 + 86, by0 + 26), (bx0 + 86, by1)], fill=(186, 162, 110), width=1)
pd.line([(bx0 + 104, by0 + 26), (bx0 + 104, by1)], fill=(186, 162, 110), width=1)
# stencil on the front face
pd.text((bx0 + 95, by0 + 44), "GRAND THEFT", font=font(F_MONO, 22),
        fill=(58, 40, 20), anchor="ma")
pd.text((bx0 + 95, by0 + 70), "AUTO VI", font=font(F_MONO, 22),
        fill=(58, 40, 20), anchor="ma")
pd.text((bx0 + 95, by0 + 100), "FRAGILE", font=font(F_MONO, 13),
        fill=(80, 58, 30), anchor="ma")
# thick dust on the top face + speckles on the front
dr = random.Random(2013)
for _ in range(46):
    dx = dr.randint(bx0 + 4, bx1 + 30)
    dy = dr.randint(by0 + 2, by0 + 24)
    r = dr.randint(2, 6)
    pd.ellipse([dx, dy, dx + r, dy + r // 2], fill=(217, 201, 163))
for _ in range(60):
    dx = dr.randint(bx0 + 4, bx1)
    dy = dr.randint(by0 + 30, by1 - 4)
    r = dr.randint(1, 3)
    pd.ellipse([dx, dy, dx + r, dy + r], fill=(217, 201, 163))
# dust motes in the beam
for _ in range(26):
    dx = dr.randint(10, 300)
    dy = dr.randint(6, 190)
    r = dr.randint(1, 2)
    pd.ellipse([dx, dy, dx + r, dy + r], fill=(255, 232, 180))
# cobweb: top-right corner of the photo
web_col = (207, 201, 189)
for k in range(1, 4):
    r_ = 26 * k
    pd.arc([356 - r_, -r_, 356 + r_, r_], start=0, end=90,
           fill=web_col, width=2)
for a in [12, 32, 52, 72]:
    import math
    x2 = 356 - int(84 * math.cos(math.radians(a)))
    y2 = int(84 * math.sin(math.radians(a)))
    pd.line([(356, 0), (x2, y2)], fill=web_col, width=1)
# cobweb draped over the box top-right corner
for k in range(1, 3):
    r_ = 14 * k
    pd.arc([bx1 + 30 - r_, by0 - r_, bx1 + 30 + r_, by0 + r_],
           start=200, end=340, fill=web_col, width=1)
# CCTV overlay + grain + scanlines
pd.text((10, 8), "CAM 04", font=font(F_MONO, 14), fill=(235, 235, 225))
pd.ellipse([300, 12, 308, 20], fill=(200, 40, 30))
pd.text((312, 8), "REC", font=font(F_MONO, 14), fill=(235, 235, 225))
pd.text((346, 238), "02:13:47", font=font(F_MONO, 13),
        fill=(235, 235, 225), anchor="ra")
for yy in range(0, PH, 4):
    pd.line([(0, yy), (PW, yy)], fill=(0, 0, 0), width=1)
pgrain = Image.effect_noise((PW, PH), 22).convert("L")
photo = Image.composite(
    photo, Image.new("RGB", (PW, PH), (40, 38, 34)),
    pgrain.point(lambda p: 255 - int(p * 0.10)),
)
# final lift so the box + webs read clearly (scanlines already drawn above)
photo = ImageEnhance.Brightness(photo).enhance(1.12)
# white photo border + tape corners
frame = Image.new("RGB", (PW + 16, PH + 16), (245, 240, 228))
frame.paste(photo, (8, 8))
fd2 = ImageDraw.Draw(frame)
tape = Image.new("RGBA", (64, 22), (232, 217, 160, 170))
tape = tape.rotate(-8, expand=True, resample=Image.BICUBIC)
frame.paste(tape, (14, -6), tape)
tape2 = tape.rotate(16, expand=True, resample=Image.BICUBIC)
frame.paste(tape2, (PW - 58, -6), tape2)
img.paste(frame, (668, 252))
d.text((668, 528), "WAREHOUSE CCTV — 13 YEARS LATER",
       font=font(F_MONO, 17), fill=MUTED)

# ---------- case notes (right column, below photo) ----------
d.rectangle([668, 566, 1024, 792], outline=INK, width=2)
d.text((688, 580), "CASE NOTES", font=font(F_MONO, 22), fill=INK)
d.line([(688, 610), (1004, 610)], fill=FAINT, width=1)
notes = [
    ("LOCATED — SHELF B", True),
    ("DELIVERED", False),
    ("REFUND ISSUED", False),
]
ny = 626
for label, done in notes:
    d.rectangle([688, ny, 706, ny + 18], outline=INK, width=2)
    if done:
        d.line([(690, ny + 9), (696, ny + 15), (705, ny + 3)],
               fill=INK, width=3, joint="curve")
    d.text((716, ny - 2), label, font=font(F_MONO_REG, 19), fill=INK)
    ny += 34
d.text((688, 734), "LAST SEEN: SHELF B, UNDER 13",
       font=font(F_MONO_REG, 18), fill=MUTED)
d.text((688, 758), "YEARS OF DUST.", font=font(F_MONO_REG, 18), fill=MUTED)

# ---------- giant wet-ink stamp (focal point, bottom centre) ----------
stamp = Image.new("RGBA", (400, 150), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
# bleed halo: lighter red, slightly offset copies
sd.text((200, 18), "DELAYED 13 YEARS", font=font(F_BLACK, 38),
        fill=(196, 90, 70, 255), anchor="ma")
sd.text((200, 66), "MY AI AGENT GOT PAID FIRST", font=font(F_BOLD, 20),
        fill=(196, 90, 70, 255), anchor="ma")
sd.rounded_rectangle([5, 5, 395, 145], radius=10, outline=(196, 90, 70), width=5)
sd.rounded_rectangle([13, 13, 387, 137], radius=7, outline=(196, 90, 70), width=2)
# crisp main ink on top
sd.text((200, 16), "DELAYED 13 YEARS", font=font(F_BLACK, 38),
        fill=RED, anchor="ma")
sd.text((200, 64), "MY AI AGENT GOT PAID FIRST", font=font(F_BOLD, 20),
        fill=RED_DARK, anchor="ma")
sd.rounded_rectangle([5, 5, 395, 145], radius=10, outline=RED, width=5)
sd.rounded_rectangle([13, 13, 387, 137], radius=7, outline=RED, width=2)
# light grunge (wet ink bleeds, it does not flake)
gr = random.Random(2013)
smask = Image.new("L", stamp.size, 0)
md = ImageDraw.Draw(smask)
for _ in range(220):
    gx, gy = gr.randint(0, 399), gr.randint(0, 149)
    r = gr.randint(1, 3)
    md.ellipse([gx, gy, gx + r, gy + r], fill=255)
alpha = stamp.split()[3]
stamp.putalpha(ImageChops.subtract(alpha, smask))
# wet-ink softness
stamp = stamp.filter(ImageFilter.GaussianBlur(1.0))
stamp = stamp.rotate(-12, expand=True, resample=Image.BICUBIC)
img.paste(stamp, (340, 800), stamp)

# ---------- footer: barcode left, signature right ----------
# barcode (seeded bars for LX-GTA6-2013-2026)
d.text((56, 848), "SHIPMENT BARCODE", font=font(F_MONO, 17), fill=MUTED)
brng = random.Random(20130617)
x = 56
while x < 300:
    wdt = brng.choice([2, 3, 3, 4, 5, 6])
    if brng.random() < 0.55:
        d.rectangle([x, 872, x + wdt, 934], fill=INK)
    x += wdt + brng.choice([2, 3, 4])
d.text((56, 940), "LX-GTA6-2013-2026", font=font(F_MONO, 19), fill=INK)
# signature (right, clear of the stamp)
d.text((820, 848), "RECIPIENT SIGNATURE", font=font(F_MONO, 17), fill=MUTED)
d.line([(820, 906), (1024, 906)], fill=INK, width=2)
d.text((820, 914), "X  Not Home —", font=font(F_MONO_REG, 20), fill=INK)
d.text((820, 940), "Still Waiting", font=font(F_MONO_REG, 20), fill=INK)
# verification line + micro-print (bottom strip, below the stamp)
d.text((56, 1004), "REF:  MAKE.FUN-AGENT-PAYOUT-VERIFIED",
       font=font(F_MONO, 20), fill=RED_DARK)
d.text((56, 1032), "TERMS: DELIVERY EVENTUALLY GUARANTEED. NO REFUNDS AFTER 13 YEARS.",
       font=font(F_MONO_REG, 13), fill=MUTED)
d.text((56, 1050), "CARRIER NOT LIABLE FOR DELAYS, REMASTERS, TRAILERS, OR DAY-1 PATCHES.",
       font=font(F_MONO_REG, 13), fill=MUTED)

img.save(OUT, "PNG")
print("saved", OUT, "days:", DAYS)
