#!/usr/bin/env python3
"""Render the gta6-meme-x-01 v3 meme (revision 2, 2026-11-20): STATE OF
LEONIDA — OFFICIAL RELEASE DELAY NOTICE + OFFICIAL AGENT PAYOUT VOUCHER.

Fura's 4 precision fixes over the first v3 preview:
1. ZERO OVERLAP: the red DELAYED AGAIN stamp sits in clear space BELOW the
   STATUS line (right side, above the divider) — POLISHING PUDDLES is 100%
   untouched. Geometry verified: stamp's top-left corner clears row 3.
2. CERTIFICATE DETAILS: embossed Official Seal of Leonida beside the header
   (circular text + star, offset-highlight emboss) + two official columns
   below the stamp: RELEASE ESTIMATE / AUTHORIZED BY with a scribble
   signature. Fills the top that was too empty vs Top-10 documents.
3. BOTTOM BLOCK = OFFICIAL AGENT PAYOUT VOUCHER (~28%): dark navy, big
   ghost, big white + yellow-neon text, green PAID badge, voucher number,
   coupon notches on the edges — reads as a cut-off voucher, not a banner.
4. Criterion #1 dominance (Hard Gate): make.fun is the biggest branding on
   the page — ghost + MAKE.FUN in neon + badge + voucher number.

Deterministic: same input -> same bytes (seeded RNG, fixed dates).
Assets: make.fun ghost mark (press kit, mark-1024.png).
"""
import math
import random
from datetime import date
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1080
OUT = "/home/hatch/workspace/makefun/gta6-meme-x-01/meme-v3.png"
GHOST = "/home/hatch/workspace/makefun/gta6-meme-x-01/assets/mark-1024.png"

LIB = "/usr/share/fonts/truetype/liberation/"
F_SANS_B = LIB + "LiberationSans-Bold.ttf"
F_SERIF_B = LIB + "LiberationSerif-Bold.ttf"

# Palette (few, high contrast)
PAPER = (248, 245, 236)
PAPER_EDGE = (238, 232, 216)
NAVY = (16, 33, 61)
NAVY_DARK = (10, 20, 36)
INK = (20, 20, 20)
RED = (178, 34, 24)
YELLOW = (255, 210, 31)
GREEN = (0, 230, 118)
WHITE = (255, 255, 255)
MUTED = (90, 90, 95)

ORDERED = date(2013, 9, 17)
TODAY = date(2026, 11, 20)
DAYS = (TODAY - ORDERED).days  # 4,812 exact

TOP_H = 778  # paper section; payout block = 302px (~28%)
rng = random.Random(2013)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(text, path, start, max_w):
    size = start
    while size > 10:
        f = font(path, size)
        if d.textlength(text, font=f) <= max_w:
            return f, size
        size -= 2
    return font(path, 10), 10


def tracked(draw, xy, text, fnt, fill, tracking=3):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


# ---- subtle paper grain (very light: the doc must stay clean) ----
grain = Image.effect_noise((W, TOP_H), 14).convert("L")
grain_img = Image.new("RGB", (W, TOP_H), PAPER)
img.paste(Image.composite(grain_img, Image.new("RGB", (W, TOP_H), PAPER_EDGE),
                          grain.point(lambda p: int(p * 0.05))), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# ---- certificate frame: thick outer + thin inner, navy ----
d.rectangle([26, 26, W - 26, TOP_H - 26], outline=NAVY, width=8)
d.rectangle([44, 44, W - 44, TOP_H - 44], outline=NAVY, width=3)

# ---- Official Seal of Leonida (embossed), top-right beside the header ----
SEAL_C = (945, 118)
SEAL_R = 70


def star_points(cx, cy, r_outer, r_inner, n=5, rot=-90):
    pts = []
    for i in range(2 * n):
        r = r_outer if i % 2 == 0 else r_inner
        a = math.radians(rot + i * 180 / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def draw_seal(layer_draw, ox, oy, color):
    cx, cy = SEAL_C[0] + ox, SEAL_C[1] + oy
    layer_draw.ellipse([cx - 68, cy - 68, cx + 68, cy + 68],
                       outline=color, width=5)
    layer_draw.ellipse([cx - 52, cy - 52, cx + 52, cy + 52],
                       outline=color, width=2)
    layer_draw.polygon(star_points(cx, cy - 6, 26, 11), fill=color)
    f_yr = font(F_SANS_B, 15)
    tw = layer_draw.textlength("2013", font=f_yr)
    layer_draw.text((cx - tw / 2, cy + 26), "2013", font=f_yr, fill=color)


seal = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(seal)
# emboss highlight: white copy offset (+2,+2), low alpha
draw_seal(sd, 2, 2, (255, 255, 255, 80))
draw_seal(sd, 0, 0, NAVY + (255,))
# circular text around the seal, between the rings
circ_text = "OFFICIAL SEAL  •  STATE OF LEONIDA  •  "
f_circ = font(F_SANS_B, 15)
# white highlight pass then navy pass
for ox, oy, col in [(2, 2, (255, 255, 255, 80)), (0, 0, NAVY + (255,))]:
    total = sum(sd.textlength(ch, font=f_circ) for ch in circ_text)
    # distribute chars along the full circle starting at the top
    ang = -90.0
    for ch in circ_text:
        wch = sd.textlength(ch, font=f_circ)
        a = math.radians(ang + (wch / 2) / 60 * 180 / math.pi)
        # radius 60
        px = SEAL_C[0] + ox + 60 * math.cos(a)
        py = SEAL_C[1] + oy + 60 * math.sin(a)
        ch_img = Image.new("RGBA", (30, 30), (0, 0, 0, 0))
        cd = ImageDraw.Draw(ch_img)
        cd.text((15 - wch / 2, 15 - 8), ch, font=f_circ, fill=col)
        ch_img = ch_img.rotate(-(math.degrees(a) + 90), resample=Image.BICUBIC,
                               center=(15, 15))
        seal.paste(ch_img, (int(px - 15), int(py - 15)), ch_img)
        ang += (wch / 60) * 180 / math.pi
img.paste(seal, (0, 0), seal)
d = ImageDraw.Draw(img, "RGBA")

# ---- header (left-aligned, seal occupies the right) ----
f_head, _ = fit("STATE OF LEONIDA", F_SERIF_B, 62, 760)
tracked(d, (90, 62), "STATE OF LEONIDA", f_head, NAVY, tracking=5)
f_sub, _ = fit("OFFICIAL RELEASE DELAY NOTICE", F_SANS_B, 35, 760)
tracked(d, (90, 138), "OFFICIAL RELEASE DELAY NOTICE", f_sub, NAVY, tracking=2)
d.rectangle([90, 196, W - 90, 200], fill=NAVY)
d.rectangle([90, 206, W - 90, 208], fill=NAVY)
f_case, _ = fit("Case #GTA6-2013", F_SANS_B, 28, 600)
tracked(d, (90, 222), "Case #GTA6-2013", f_case, NAVY, tracking=2)

# ---- 3 big info lines ----
rows = [
    ("SUBJECT:", "GRAND THEFT AUTO VI", INK),
    ("DELAY:", f"13 YEARS ({DAYS:,} DAYS)", RED),
    ("STATUS:", "STILL POLISHING PUDDLES", INK),
]
y = 268
for label, value, vcolor in rows:
    fnt, _ = fit(f"{label} {value}", F_SANS_B, 46, 900)
    x = 90
    d.text((x, y), label, font=fnt, fill=NAVY)
    x += d.textlength(label, font=fnt) + 18
    d.text((x, y), value, font=fnt, fill=vcolor)
    y += 80

# ---- giant red stamp DELAYED AGAIN — clear space BELOW row 3, zero overlap ----
# Row 3 text ends y=474. Stamp top-left corner (font 54, tilt -8, centre
# (810,568)) lands at y~482 -> clears row 3 by 8px; bottom ends y~653,
# above the columns (y=668). Verified by construction, re-checked visually.
stamp_text = "DELAYED AGAIN"
f_stamp = font(F_SANS_B, 54)
tw = d.textlength(stamp_text, font=f_stamp)
pad_x, pad_y = 28, 16
sw, sh = int(tw + pad_x * 2), 54 + pad_y * 2 + 14
stamp = Image.new("RGBA", (sw, sh), (0, 0, 0, 0))
sd = ImageDraw.Draw(stamp)
sd.rounded_rectangle([4, 4, sw - 4, sh - 4], radius=13,
                     outline=RED + (235,), width=6)
sd.text((pad_x, pad_y + 3), stamp_text, font=f_stamp, fill=RED + (235,))
bleed = stamp.filter(ImageFilter.GaussianBlur(3))
bleed.putalpha(bleed.split()[3].point(lambda p: int(p * 0.45)))
stamp_rot = stamp.rotate(-8, expand=True, resample=Image.BICUBIC)
bleed_rot = bleed.rotate(-8, expand=True, resample=Image.BICUBIC)
cx, cy = 810, 568
img.paste(bleed_rot, (cx - bleed_rot.width // 2, cy - bleed_rot.height // 2),
          bleed_rot)
img.paste(stamp_rot, (cx - stamp_rot.width // 2, cy - stamp_rot.height // 2),
          stamp_rot)
d = ImageDraw.Draw(img, "RGBA")

# ---- official columns below the stamp ----
d.rectangle([90, 656, W - 90, 658], fill=(150, 140, 115))  # section rule
cols = [
    ("RELEASE ESTIMATE:", "WHEN ROCKSTAR FEELS LIKE IT (2026+)"),
    ("AUTHORIZED BY:", "LEONIDA DEPARTMENT OF ETERNAL DELAYS"),
]
cy2 = 672
for label, value in cols:
    fnt, _ = fit(f"{label} {value}", F_SANS_B, 26, 900)
    x = 90
    d.text((x, cy2), label, font=fnt, fill=NAVY)
    x += d.textlength(label, font=fnt) + 14
    d.text((x, cy2), value, font=fnt, fill=INK)
    cy2 += 34
# scribble signature at the end of the AUTHORIZED BY line
sig_x0 = 90 + d.textlength("AUTHORIZED BY: LEONIDA DEPARTMENT OF ETERNAL DELAYS",
                           font=font(F_SANS_B, 26)) + 14 + 18
sig_y = 672 + 34
sig = Image.new("RGBA", (130, 30), (0, 0, 0, 0))
sg = ImageDraw.Draw(sig)
# a signature squiggle: loop + flourish + underline
pts = []
for t in range(0, 101):
    px = t * 0.95
    py = 14 + 7 * math.sin(t / 9.0) * (1 - t / 130.0)
    pts.append((px, py))
sg.line(pts, fill=NAVY + (235,), width=3, joint="curve")
sg.line([(8, 22), (30, 6), (52, 20), (74, 8)], fill=NAVY + (235,), width=3,
        joint="curve")
sg.line([(6, 27), (118, 27)], fill=NAVY + (200,), width=2)
img.paste(sig, (int(sig_x0), sig_y), sig)
d = ImageDraw.Draw(img, "RGBA")

# ---- payout block: OFFICIAL AGENT PAYOUT VOUCHER (~28%) ----
d.rectangle([0, TOP_H, W, H], fill=NAVY_DARK)
grain2 = Image.effect_noise((W, H - TOP_H), 12).convert("L")
dark = Image.new("RGB", (W, H - TOP_H), NAVY_DARK)
img.paste(Image.composite(dark, Image.new("RGB", (W, H - TOP_H), (16, 30, 54)),
                          grain2.point(lambda p: int(p * 0.06))),
          (0, TOP_H))
d = ImageDraw.Draw(img, "RGBA")
d.rectangle([0, TOP_H, W, TOP_H + 6], fill=YELLOW)  # neon divider
# coupon notches on both edges (tear-off voucher cue)
for nx in (0, W):
    d.ellipse([nx - 14, 929 - 14, nx + 14, 929 + 14], fill=PAPER)

# voucher title row
f_vt, _ = fit("OFFICIAL AGENT PAYOUT VOUCHER", F_SANS_B, 24, 700)
tracked(d, (52, 800), "OFFICIAL AGENT PAYOUT VOUCHER", f_vt, YELLOW, tracking=2)
f_vn, _ = fit("NO. LX-2013-4812", F_SANS_B, 24, 300)
vn_w = d.textlength("NO. LX-2013-4812", font=f_vn)
d.text((W - 52 - vn_w, 800), "NO. LX-2013-4812", font=f_vn, fill=WHITE)

# big ghost, left
ghost = Image.open(GHOST).convert("RGBA").resize((200, 200), Image.LANCZOS)
img.paste(ghost, (52, 838), ghost)
d = ImageDraw.Draw(img, "RGBA")

# payout text: 3 big lines, white + yellow MAKE.FUN
tx, max_w = 280, 750
lines = [
    ("MY AI AGENT DIDN'T WAIT", None),
    ("13 YEARS — IT ALREADY", None),
    ("GOT PAID ON ", "MAKE.FUN"),
]
ly = 838
for white_part, yellow_part in lines:
    full = white_part + (yellow_part or "")
    fnt, size = fit(full, F_SANS_B, 48, max_w)
    d.text((tx, ly), white_part, font=fnt, fill=WHITE)
    if yellow_part:
        x2 = tx + d.textlength(white_part, font=fnt)
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glow)
        gd.text((x2, ly), yellow_part, font=fnt, fill=YELLOW + (255,))
        glow_b = glow.filter(ImageFilter.GaussianBlur(7))
        img.paste(glow_b, (0, 0), glow_b)
        d = ImageDraw.Draw(img, "RGBA")
        d.text((x2, ly), yellow_part, font=fnt, fill=YELLOW)
    ly += 56

# bright green PAID badge, bottom-right
badge_text = "PAID ON MAKE.FUN (REAL MONEY)"
f_badge = font(F_SANS_B, 24)
btw = d.textlength(badge_text, font=f_badge)
bx1, by1 = W - 52 - int(btw) - 44, 1012
bx2, by2 = W - 52, by1 + 48
d.rounded_rectangle([bx1, by1, bx2, by2], radius=24, fill=GREEN)
d.text((bx1 + 22, by1 + 11), badge_text, font=f_badge, fill=NAVY_DARK)

img.save(OUT, optimize=True)
print(f"saved {OUT} {img.size}")
import hashlib
print("sha256", hashlib.sha256(open(OUT, "rb").read()).hexdigest()[:16])
