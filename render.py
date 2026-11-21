#!/usr/bin/env python3
"""Render the ORVENNA travel poster (1024x1024) with pure PIL.

Concept (follows live #1 VALDORA's family, own differentiator):
invented coastal/mystical place + ONE iconic landmark + place name set
big into the poster. Ours: ORVENNA - The Observatory Above the Clouds -
a cliffside observatory town above a sea of clouds at dusk. Landmark:
the great observatory dome on the cliff. No real destination, no extra
copy, no quotes, no star ratings.

Deterministic: fixed seed, no time, no network, no external assets.
Run: python3 render.py  -> writes entry.png next to this file.
"""
import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
RNG = random.Random(20261121)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def vgrad(size, stops):
    """Vertical gradient. stops: list of (pos 0..1, (r,g,b))."""
    w, h = size
    ys = np.linspace(0.0, 1.0, h)
    arr = np.zeros((h, w, 3), dtype=np.uint8)
    for j in range(len(stops) - 1):
        p0, c0 = stops[j]
        p1, c1 = stops[j + 1]
        m = (ys >= p0) & (ys <= p1)
        t = np.clip((ys[m] - p0) / max(p1 - p0, 1e-9), 0.0, 1.0)
        for k in range(3):
            arr[m, :, k] = (c0[k] + (c1[k] - c0[k]) * t)[:, None]
    arr[ys < stops[0][0]] = stops[0][1]
    arr[ys > stops[-1][0]] = stops[-1][1]
    return Image.fromarray(arr, "RGB")


def glow_disc(layer, cx, cy, r, color, peak=200):
    """Soft radial glow: concentric circles, alpha falling off."""
    d = ImageDraw.Draw(layer)
    steps = 24
    for i in range(steps, 0, -1):
        rr = r * i / steps
        a = int(peak * (1.0 - i / steps) ** 1.6)
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=color + (a,))


def radial_glow(cx, cy, r, color, alpha):
    """Soft radial glow: solid disc, heavily blurred (no banding)."""
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(g)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (alpha,))
    return g.filter(ImageFilter.GaussianBlur(max(2, int(r * 0.55))))


def soft_ellipse(layer, box, color, alpha):
    d = ImageDraw.Draw(layer)
    d.ellipse(box, fill=color + (alpha,))


def tracked_text(base, cx, y, text, font, fill, tracking=0, shadow=None):
    """Draw letterspaced caps text centred on cx at top y. Returns width."""
    widths = []
    for ch in text:
        widths.append(font.getlength(ch))
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2.0
    if shadow is not None:
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
        ds = ImageDraw.Draw(sh)
        xx = x
        for ch, wd in zip(text, widths):
            ds.text((xx, y + shadow[1]), ch, font=font, fill=shadow[0])
            xx += wd + tracking
        sh = sh.filter(ImageFilter.GaussianBlur(shadow[2]))
        base.alpha_composite(sh)
    d = ImageDraw.Draw(base)
    xx = x
    for ch, wd in zip(text, widths):
        d.text((xx, y), ch, font=font, fill=fill)
        xx += wd + tracking
    return total


def pine(draw, x, y, h, color):
    """Simple pine silhouette: stacked triangles + trunk."""
    w = h * 0.42
    for i, (fy, fw) in enumerate([(0.0, 1.0), (0.28, 0.78), (0.55, 0.55)]):
        ty = y - h + h * fy
        bw = w * fw / 2.0
        draw.polygon([(x, ty), (x - bw, ty + h * 0.34), (x + bw, ty + h * 0.34)],
                     fill=color)
    draw.rectangle([x - h * 0.03, y - h * 0.06, x + h * 0.03, y], fill=color)


def main():
    img = Image.new("RGB", (W, H))

    # ---- sky -----------------------------------------------------------
    sky = vgrad((W, H), [
        (0.00, (16, 12, 44)),
        (0.28, (42, 27, 82)),
        (0.46, (91, 42, 104)),
        (0.56, (163, 74, 94)),
        (0.64, (224, 122, 69)),
        (0.70, (247, 178, 103)),
        (1.00, (247, 178, 103)),
    ])
    img.paste(sky, (0, 0))
    base = img.convert("RGBA")

    # ---- stars (upper sky only) ---------------------------------------
    stars = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ds = ImageDraw.Draw(stars)
    for _ in range(240):
        x = RNG.uniform(0, W)
        y = RNG.uniform(0, 430) * (1.0 - RNG.random() * 0.4)
        r = RNG.choice([0.8, 1.0, 1.2, 1.6])
        a = int(RNG.uniform(60, 230) * max(0.25, 1.0 - y / 520.0))
        ds.ellipse([x - r, y - r, x + r, y + r], fill=(255, 244, 214, a))
    for _ in range(14):  # a few brighter stars with cross sparkle
        x = RNG.uniform(40, W - 40)
        y = RNG.uniform(30, 300)
        ds.line([x - 7, y, x + 7, y], fill=(255, 246, 220, 200), width=1)
        ds.line([x, y - 7, x, y + 7], fill=(255, 246, 220, 200), width=1)
        ds.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 250, 230, 230))
    base.alpha_composite(stars)

    # ---- small crescent moon, top right (night is coming) -------------
    moon = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    moon.alpha_composite(radial_glow(906, 128, 70, (220, 220, 255), 50))
    dm = ImageDraw.Draw(moon)
    dm.ellipse([888, 110, 924, 146], fill=(240, 238, 255, 235))
    dm.ellipse([896, 106, 928, 142], fill=(22, 18, 52, 255))
    base.alpha_composite(moon)

    # ---- low sun + halo (left of centre, clear of the observatory) ----
    sun = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sun.alpha_composite(radial_glow(300, 548, 210, (255, 166, 88), 95))
    sun.alpha_composite(radial_glow(300, 548, 120, (255, 196, 120), 140))
    d = ImageDraw.Draw(sun)
    d.ellipse([300 - 58, 548 - 58, 300 + 58, 548 + 58],
              fill=(255, 224, 160, 255))
    d.ellipse([300 - 46, 548 - 46, 300 + 46, 548 + 46],
              fill=(255, 240, 205, 255))
    base.alpha_composite(sun)

    # ---- distant hazy ridges ------------------------------------------
    ridge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(ridge)
    dr.polygon([(0, 640), (90, 588), (210, 622), (330, 580), (470, 626),
                (600, 592), (760, 630), (900, 596), (1024, 624), (1024, 700),
                (0, 700)], fill=(107, 74, 122, 150))
    dr.polygon([(0, 668), (140, 622), (300, 660), (430, 628), (580, 664),
                (740, 630), (880, 662), (1024, 636), (1024, 720), (0, 720)],
               fill=(74, 47, 94, 190))
    base.alpha_composite(ridge)

    # ---- sea of clouds -------------------------------------------------
    clouds = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # base wash
    wash = vgrad((W, 420), [(0.0, (122, 85, 120)), (0.55, (88, 62, 106)),
                            (1.0, (44, 30, 74))]).convert("RGBA")
    clouds.paste(wash, (0, 604))
    dc = ImageDraw.Draw(clouds)
    # break the wash's straight top edge with a row of puffs
    for _ in range(26):
        x = RNG.uniform(-30, W + 30)
        y = RNG.uniform(596, 636)
        rx = RNG.uniform(50, 130)
        ry = RNG.uniform(12, 26)
        col = RNG.choice([(150, 105, 135), (178, 130, 140), (122, 88, 124)])
        dc.ellipse([x - rx, y - ry, x + rx, y + ry],
                   fill=col + (RNG.randint(110, 165),))
    # distinct puff clusters: shadowed base + warm lit crown each
    for _ in range(52):
        px = RNG.uniform(-40, W + 40)
        py = RNG.uniform(640, 980)
        pr = RNG.uniform(55, 160)
        # shadowed underside
        dc.ellipse([px - pr, py - pr * 0.28, px + pr, py + pr * 0.34],
                   fill=(52, 34, 74, 150))
        # crown of overlapping lit puffs
        for _ in range(4):
            ox = px + RNG.uniform(-pr * 0.6, pr * 0.6)
            oy = py - RNG.uniform(0, pr * 0.30)
            rx = RNG.uniform(pr * 0.28, pr * 0.55)
            ry = RNG.uniform(pr * 0.12, pr * 0.24)
            near_sun = 1.0 - min(1.0, abs(ox - 300) / 700.0)
            warm = RNG.random() < (0.35 + 0.55 * near_sun)
            if warm:
                col = (247, 196, 137) if RNG.random() < 0.7 else (240, 170, 130)
            else:
                col = (178, 138, 158) if RNG.random() < 0.5 else (140, 104, 138)
            dc.ellipse([ox - rx, oy - ry, ox + rx, oy + ry],
                       fill=col + (RNG.randint(100, 165),))
    # a few deep shadow puffs for depth
    for _ in range(16):
        x = RNG.uniform(0, W)
        y = RNG.uniform(700, 1000)
        rx = RNG.uniform(60, 170)
        ry = RNG.uniform(14, 30)
        dc.ellipse([x - rx, y - ry, x + rx, y + ry],
                   fill=(40, 26, 62, 130))
    # warm light pool on the sea below the sun
    clouds.alpha_composite(radial_glow(300, 720, 260, (255, 190, 120), 55))
    clouds = clouds.filter(ImageFilter.GaussianBlur(4))
    base.alpha_composite(clouds)
    # thin mist band where cloud sea meets the sky
    mist = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dm = ImageDraw.Draw(mist)
    dm.rectangle([0, 596, W, 640], fill=(250, 205, 150, 46))
    mist = mist.filter(ImageFilter.GaussianBlur(10))
    base.alpha_composite(mist)

    # ---- cliff promontory ---------------------------------------------
    cliff = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dc = ImageDraw.Draw(cliff)
    pts = [(0, 1024), (0, 912), (120, 862), (250, 812), (360, 752),
           (452, 692), (520, 640), (566, 602), (640, 586), (742, 586),
           (800, 606), (872, 652), (950, 716), (1024, 790), (1024, 1024)]
    dc.polygon(pts, fill=(30, 20, 55, 255))
    # rock facets
    dc.polygon([(120, 862), (250, 812), (300, 880), (180, 930)],
               fill=(24, 16, 46, 255))
    dc.polygon([(452, 692), (520, 640), (566, 602), (520, 700), (470, 740)],
               fill=(24, 16, 46, 255))
    dc.polygon([(800, 606), (872, 652), (900, 720), (820, 700)],
               fill=(38, 26, 66, 255))
    # sun-side rim light along the top edge
    rim = [(566, 602), (640, 586), (742, 586), (800, 606), (872, 652),
           (950, 716), (1024, 790)]
    dc.line(rim, fill=(247, 178, 103, 235), width=4)
    dc.line([(452, 692), (520, 640), (566, 602)],
            fill=(247, 178, 103, 120), width=3)
    # faint rock strata on the cliff face
    for pts, a in [([(200, 890), (300, 850), (380, 815)], 32),
                   ([(500, 770), (600, 725), (680, 700)], 30),
                   ([(260, 950), (380, 915), (480, 885)], 26),
                   ([(720, 820), (820, 785), (900, 760)], 28)]:
        dc.line(pts, fill=(140, 105, 165, a), width=3)
    base.alpha_composite(cliff)

    # ---- observatory (the ONE landmark) -------------------------------
    obs = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    do = ImageDraw.Draw(obs)
    # soft glow behind the dome
    obs.alpha_composite(radial_glow(660, 470, 170, (255, 190, 110), 60))
    do = ImageDraw.Draw(obs)
    # main tower
    do.polygon([(622, 586), (628, 470), (692, 470), (698, 586)],
               fill=(43, 28, 78, 255))
    do.line([(628, 470), (622, 586)], fill=(247, 178, 103, 160), width=2)
    # great dome: lighter than the tower so the form reads
    do.pieslice([592, 384, 728, 520], start=180, end=360,
                fill=(122, 90, 168, 255))
    do.rectangle([592, 452, 728, 472], fill=(122, 90, 168, 255))
    # thin bright rim on the sun side of the dome
    do.arc([592, 384, 728, 520], start=180, end=255,
           fill=(235, 200, 160, 220), width=4)
    # glowing telescope slit: narrow tapered slot from apex to base
    do.polygon([(654, 392), (666, 392), (672, 470), (648, 470)],
               fill=(255, 212, 130, 255))
    do.polygon([(657, 396), (663, 396), (666, 468), (654, 468)],
               fill=(255, 240, 200, 255))
    # finial + beacon star
    do.line([660, 384, 660, 362], fill=(247, 196, 130, 255), width=3)
    do.ellipse([655, 356, 665, 366], fill=(255, 224, 160, 255))
    # lit arched windows on the tower, one soft shared glow
    obs.alpha_composite(radial_glow(660, 514, 60, (255, 190, 100), 70))
    do = ImageDraw.Draw(obs)
    for wx in (640, 660, 680):
        do.rounded_rectangle([wx - 6, 500, wx + 6, 528], radius=6,
                             fill=(255, 205, 120, 255))
    # small dome (secondary) on its own tower
    do.polygon([(744, 586), (748, 536), (788, 536), (792, 586)],
               fill=(38, 25, 68, 255))
    do.pieslice([740, 498, 796, 554], start=180, end=360,
                fill=(96, 68, 138, 255))
    do.rectangle([740, 526, 796, 538], fill=(96, 68, 138, 255))
    do.polygon([(764, 504), (772, 504), (776, 536), (760, 536)],
               fill=(255, 212, 130, 255))
    base.alpha_composite(obs)

    # ---- cliff path lights + houses -----------------------------------
    lights = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dl = ImageDraw.Draw(lights)
    path = [(640, 600), (600, 640), (560, 680), (520, 716), (480, 748),
            (440, 780), (400, 812)]
    dl.line(path, fill=(255, 200, 120, 170), width=2)
    for (x, y) in path:
        glow_disc(lights, x, y, 16, (255, 200, 110), peak=150)
        dl.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(255, 232, 170, 255))
    # two tiny houses on the lower slope, below the path
    for hx, hy, hw, hh in [(292, 902, 52, 34), (366, 922, 44, 30)]:
        dl.polygon([(hx, hy), (hx + hw // 2, hy - 18), (hx + hw, hy)],
                   fill=(30, 20, 55, 255))
        dl.rectangle([hx, hy, hx + hw, hy + hh], fill=(52, 36, 84, 255))
        dl.rectangle([hx + 8, hy + 10, hx + 21, hy + 23],
                     fill=(255, 215, 140, 255))
        dl.rectangle([hx + hw - 21, hy + 10, hx + hw - 8, hy + 23],
                     fill=(255, 215, 140, 255))
        dl.line([(hx, hy), (hx + hw, hy)], fill=(247, 178, 103, 180),
                width=2)
        lights.alpha_composite(
            radial_glow(hx + hw // 2, hy + 16, 30, (255, 200, 110), 90))
    base.alpha_composite(lights)

    # ---- pines framing the bottom corners ------------------------------
    fr = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    df = ImageDraw.Draw(fr)
    pine(df, 70, 1024, 190, (18, 11, 38, 255))
    pine(df, 150, 1024, 140, (22, 14, 44, 255))
    pine(df, 968, 1024, 150, (18, 11, 38, 255))
    pine(df, 906, 1024, 105, (22, 14, 44, 255))
    base.alpha_composite(fr)

    # ---- birds ----------------------------------------------------------
    birds = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    db = ImageDraw.Draw(birds)
    for bx, by, s in [(300, 300, 12), (340, 282, 9), (380, 312, 10),
                      (820, 250, 11), (860, 272, 8)]:
        db.line([bx - s, by, bx, by - s * 0.55, bx + s, by],
                fill=(28, 18, 52, 220), width=2)
    base.alpha_composite(birds)

    # ---- type: name + subtitle ----------------------------------------
    name_font = ImageFont.truetype(SERIF_BLACK, 148)
    sub_font = ImageFont.truetype(SANS, 27)
    tracked_text(base, W // 2, 82, "ORVENNA", name_font,
                 fill=(255, 246, 220, 255), tracking=26,
                 shadow=((26, 16, 48, 200), 5, 6))
    # small diamond ornaments + subtitle
    sub = "THE OBSERVATORY ABOVE THE CLOUDS"
    w_sub = tracked_text(base, W // 2, 252, sub, sub_font,
                         fill=(246, 200, 126, 255), tracking=11)
    d2 = ImageDraw.Draw(base)
    cx = W // 2
    for sx in (cx - w_sub // 2 - 34, cx + w_sub // 2 + 34):
        d2.polygon([(sx, 258), (sx + 6, 266), (sx, 274), (sx - 6, 266)],
                   fill=(246, 200, 126, 255))
    # thin gold rule under the subtitle
    d2.line([cx - 150, 300, cx + 150, 300], fill=(246, 200, 126, 200),
            width=2)

    # ---- vignette + poster frame --------------------------------------
    vig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dv = ImageDraw.Draw(vig)
    for i in range(30):
        a = int(10 * (i / 30) ** 2)
        dv.rectangle([i, i, W - i, H - i], outline=(10, 6, 30, a), width=1)
    base.alpha_composite(vig)
    d3 = ImageDraw.Draw(base)
    d3.rectangle([26, 26, W - 27, H - 27], outline=(255, 246, 220, 110),
                 width=2)

    out = base.convert("RGB")
    path = os.path.join(HERE, "entry.png")
    out.save(path, format="PNG", optimize=True)
    print("wrote", path, os.path.getsize(path), "bytes")


if __name__ == "__main__":
    main()
