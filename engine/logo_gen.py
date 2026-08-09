#!/usr/bin/env python
"""Garage-door brand logo generator.

Reads the domain sheet (CSV: Domain / Business Name / City / State / Primary Color)
and renders a per-domain logo set mirroring the porta-potty brand/logos-web layout:

  <domain>-favicon.png       64x64    emblem only
  <domain>-mark.png          813x219  emblem + wordmark  (dark, for light backgrounds)
  <domain>-mark-light.png    813x219  emblem + wordmark  (white, for dark backgrounds)
  <domain>-lockup.png        813x354  emblem + 2-line wordmark (dark)
  <domain>-lockup-light.png  813x354  emblem + 2-line wordmark (white)

Every domain gets a DISTINCT emblem: a container shape (circle / rounded-square /
hexagon / shield / diamond / octagon) x a garage-themed symbol (house-with-door /
arched door / lift chevron / rolling door / twin garage / monogram), chosen
deterministically from the domain name so the mark is stable and unique per site.

Usage:
  python logo_gen.py <sheet.csv> [--out DIR] [--start N] [--count M] [--only domain ...]
"""
import argparse, csv, hashlib, math, os, re
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_BLACK = r"C:\Windows\Fonts\ariblk.ttf"        # Arial Black — heavy wordmark + monogram
FONT_FALLBACK = r"C:\Windows\Fonts\arialbd.ttf"
W = 813
SS = 4                                              # supersample factor

CONTAINERS = ["circle", "rsquare", "hexagon", "shield", "diamond", "octagon"]
SYMBOLS = ["house", "archdoor", "chevron", "rolldoor", "twin", "monogram"]
SYM_SCALE = {"circle": .54, "rsquare": .62, "hexagon": .52, "shield": .50,
             "diamond": .44, "octagon": .58}


# ---------------------------------------------------------------- colour helpers
def rgb(h):
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

def lum(c):
    f = lambda x: (x / 255) / 12.92 if x / 255 <= 0.03928 else (((x / 255) + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])

def mix(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))

def darken(c, t=0.18):
    return mix(c, (0, 0, 0), t)

def ink_for(primary):
    return primary if lum(primary) < 0.55 else darken(primary, 0.45)


# ---------------------------------------------------------------- design selection
def design_for(domain):
    h = int(hashlib.md5(domain.encode()).hexdigest(), 16)
    return CONTAINERS[h % len(CONTAINERS)], SYMBOLS[(h // 7) % len(SYMBOLS)]

def initials(business):
    stop = {"door", "doors", "pros", "pro", "co", "company", "llc", "inc",
            "the", "of", "and", "services", "service", "repair", "&"}
    words = [w for w in re.sub(r"[^A-Za-z ]", " ", business).split() if w.lower() not in stop]
    words = words or business.split()
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return words[0][:2].upper()


# ---------------------------------------------------------------- container shapes
def _regular(cx, cy, r, n, rot):
    return [(cx + r * math.cos(math.radians(a + rot)), cy + r * math.sin(math.radians(a + rot)))
            for a in range(0, 360, 360 // n)]

def container(d, S, kind, color):
    m = S * 0.02
    x0, y0, x1, y1 = m, m, S - m, S - m
    cx, cy, r = S / 2, S / 2, (S - 2 * m) / 2
    if kind == "circle":
        d.ellipse([x0, y0, x1, y1], fill=color)
    elif kind == "rsquare":
        d.rounded_rectangle([x0, y0, x1, y1], radius=S * 0.24, fill=color)
    elif kind == "hexagon":
        d.polygon(_regular(cx, cy, r, 6, 90), fill=color)          # flat-top
    elif kind == "octagon":
        d.polygon(_regular(cx, cy, r, 8, 22.5), fill=color)
    elif kind == "diamond":
        d.polygon([(cx, y0), (x1, cy), (cx, y1), (x0, cy)], fill=color)
    elif kind == "shield":
        d.polygon([(x0, y0 + S * 0.04), (cx, y0), (x1, y0 + S * 0.04),
                   (x1, cy + S * 0.03), (cx, y1), (x0, cy + S * 0.03)], fill=color)


def sym_box(S, kind):
    sc = SYM_SCALE[kind]
    side = S * sc
    x = (S - side) / 2
    y = (S - side) / 2
    if kind == "shield":
        y -= S * 0.03                                              # nudge up in a shield
    return (x, y, x + side, y + side)


# ---------------------------------------------------------------- garage symbols
# each draws structure in `fg`, recesses/detail in `bg`, within box=(x0,y0,x1,y1)
def sym_house(d, box, fg, bg, S):
    x0, y0, x1, y1 = box
    w, hgt = x1 - x0, y1 - y0
    cx = (x0 + x1) / 2
    top, bot = y0 + hgt * 0.28, y1
    left, right = x0 + w * 0.08, x1 - w * 0.08
    eave = w * 0.06
    d.polygon([(left - eave, top), (cx, y0), (right + eave, top)], fill=fg)   # roof
    d.rectangle([left, top, right, bot], fill=fg)
    din = w * 0.11
    dl, dr, dtp = left + din, right - din, top + (bot - top) * 0.12
    rad = (dr - dl) * 0.16
    d.rounded_rectangle([dl, dtp, dr, bot], radius=rad, fill=bg)
    d.rectangle([dl, bot - rad, dr, bot], fill=bg)
    _door_detail(d, dl, dtp, dr, bot, fg)

def sym_archdoor(d, box, fg, bg, S):
    x0, y0, x1, y1 = box
    w, hgt = x1 - x0, y1 - y0
    d.rectangle([x0, y0 + hgt * 0.10, x1, y1], fill=fg)             # building block
    dl, dr = x0 + w * 0.14, x1 - w * 0.14
    dtp = y0 + hgt * 0.20
    d.rounded_rectangle([dl, dtp, dr, y1], radius=(dr - dl) * 0.5, fill=bg)  # tall arched door
    d.rectangle([dl, y1 - (dr - dl) * 0.5, dr, y1], fill=bg)
    _door_detail(d, dl, dtp + (dr - dl) * 0.22, dr, y1, fg, windows=False)

def sym_rolldoor(d, box, fg, bg, S):
    x0, y0, x1, y1 = box
    w = x1 - x0
    d.rounded_rectangle([x0, y0, x1, y1], radius=w * 0.14, fill=fg)  # the door panel
    d.rectangle([x0, y1 - w * 0.14, x1, y1], fill=fg)
    _door_detail(d, x0, y0, x1, y1, bg)                             # windows + slats in bg

def sym_twin(d, box, fg, bg, S):
    x0, y0, x1, y1 = box
    w, hgt = x1 - x0, y1 - y0
    top = y0 + hgt * 0.24
    d.polygon([(x0, top), ((x0 + x1) / 2, y0), (x1, top)], fill=fg)  # roof
    d.rectangle([x0, top, x1, y1], fill=fg)
    gap = w * 0.06
    dw = (w - gap * 3) / 2
    for k in range(2):
        dl = x0 + gap + k * (dw + gap)
        dr = dl + dw
        dtp = top + (y1 - top) * 0.16
        d.rounded_rectangle([dl, dtp, dr, y1], radius=dw * 0.14, fill=bg)
        d.rectangle([dl, y1 - dw * 0.14, dr, y1], fill=bg)
        for f in (0.42, 0.66, 0.9):
            yy = dtp + (y1 - dtp) * f
            d.line([dl + dw * 0.14, yy, dr - dw * 0.14, yy], fill=fg, width=max(2, int(S * 0.008)))

def sym_chevron(d, box, fg, bg, S):
    x0, y0, x1, y1 = box
    w, hgt = x1 - x0, y1 - y0
    t = hgt * 0.16                                                   # chevron thickness
    for k in (0, 1):                                                 # two stacked lift chevrons
        oy = y0 + hgt * (0.06 + k * 0.34)
        d.polygon([(x0, oy + hgt * 0.24), ((x0 + x1) / 2, oy),
                   (x1, oy + hgt * 0.24), (x1, oy + hgt * 0.24 + t),
                   ((x0 + x1) / 2, oy + t), (x0, oy + hgt * 0.24 + t)], fill=fg)
    d.rounded_rectangle([x0, y1 - hgt * 0.12, x1, y1], radius=t * 0.4, fill=fg)  # threshold

def sym_monogram(d, box, fg, bg, S, text="G"):
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    sz = int(bh * (0.95 if len(text) == 1 else 0.72))
    f = _font(FONT_BLACK, sz)
    while f.getbbox(text)[2] > bw and sz > 12:
        sz -= 4
        f = _font(FONT_BLACK, sz)
    bb = f.getbbox(text)
    tx = (x0 + x1) / 2 - (bb[2] - bb[0]) / 2 - bb[0]
    ty = (y0 + y1) / 2 - (bb[3] - bb[1]) / 2 - bb[1]
    d.text((tx, ty), text, font=f, fill=fg)

def _door_detail(d, dl, dtp, dr, dbt, color, windows=True):
    ww = dr - dl
    if windows:
        n, g = 4, ww * 0.055
        sw = (ww - (n + 1) * g) / n
        wy, wh = dtp + (dbt - dtp) * 0.12, (dbt - dtp) * 0.15
        for i in range(n):
            wx = dl + g + i * (sw + g)
            d.rounded_rectangle([wx, wy, wx + sw, wy + wh], radius=sw * 0.22, fill=color)
    lw = max(2, int((dbt - dtp) * 0.045))
    seams = (0.45, 0.63, 0.81) if windows else (0.36, 0.54, 0.72, 0.9)
    for f in seams:
        y = dtp + (dbt - dtp) * f
        d.line([dl + ww * 0.06, y, dr - ww * 0.06, y], fill=color, width=lw)

SYM_FN = {"house": sym_house, "archdoor": sym_archdoor, "rolldoor": sym_rolldoor,
          "twin": sym_twin, "chevron": sym_chevron}


# ---------------------------------------------------------------- emblem
def emblem(size, domain, primary, mode, mono="G"):
    """mode in {dark, light, favicon}. Filled container + knockout symbol."""
    kind, sym = design_for(domain)
    S = size * SS
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    white = (255, 255, 255)
    if mode == "light":
        disc, fg = white, primary
    else:                                                           # dark + favicon
        disc, fg = primary, white
    container(d, S, kind, disc)
    box = sym_box(S, kind)
    if sym == "monogram":
        sym_monogram(d, box, fg, disc, S, text=mono)
    else:
        SYM_FN[sym](d, box, fg, disc, S)
    return im.resize((size, size), Image.LANCZOS)


# ---------------------------------------------------------------- wordmark
def _font(path, sz):
    try:
        return ImageFont.truetype(path, sz)
    except Exception:
        return ImageFont.truetype(FONT_FALLBACK, sz)

def two_lines(business):
    up = business.upper().strip()
    m = re.search(r"\bGARAGE\b", up)
    if m and m.start() > 0:
        return [up[:m.start()].strip(), up[m.start():].strip()]
    words = up.split()
    if len(words) <= 2:
        return [up]
    mid = (len(words) + 1) // 2
    return [" ".join(words[:mid]), " ".join(words[mid:])]

def fit_font(lines, max_w, start, path):
    sz = start
    while sz > 14:
        f = _font(path, sz)
        if max(f.getbbox(ln)[2] for ln in lines) <= max_w:
            return f
        sz -= 2
    return _font(path, 14)

def draw_wordmark(im, lines, box, color, path):
    x, y, w, h = box
    f = fit_font(lines, w, int(h / (len(lines) * 0.92)), path)
    asc = f.getbbox("HG")[3]
    gap = int(asc * 0.06)
    total = len(lines) * asc + (len(lines) - 1) * gap
    cy = y + (h - total) // 2
    d = ImageDraw.Draw(im)
    for ln in lines:
        d.text((x, cy - f.getbbox(ln)[1]), ln, font=f, fill=color)
        cy += asc + gap


# ---------------------------------------------------------------- compose
def compose(kind, lines, primary, light, domain, mono):
    h = 219 if kind == "mark" else 354
    im = Image.new("RGBA", (W, h), (0, 0, 0, 0))
    ink = (255, 255, 255) if light else ink_for(primary)
    pad = int(h * 0.12)
    em_sz = h - pad * 2
    im.alpha_composite(emblem(em_sz, domain, primary, "light" if light else "dark", mono), (pad, pad))
    tx = pad + em_sz + int(h * 0.13)
    draw_wordmark(im, lines, (tx, pad, W - tx - pad, h - pad * 2), ink, FONT_BLACK)
    return im

def favicon(domain, primary, mono):
    return emblem(256, domain, primary, "favicon", mono).resize((64, 64), Image.LANCZOS)


# ---------------------------------------------------------------- driver
def gen_for(row, out):
    domain = row["Domain (Purchased)"].strip()
    business = row["Business Name"].strip()
    primary = rgb((row.get("Primary Color") or "#1D4ED8").strip() or "#1D4ED8")
    lines = two_lines(business)
    mono = initials(business)
    favicon(domain, primary, mono).save(os.path.join(out, f"{domain}-favicon.png"))
    emblem(256, domain, primary, "dark", mono).save(os.path.join(out, f"{domain}-emblem.png"))
    emblem(256, domain, primary, "light", mono).save(os.path.join(out, f"{domain}-emblem-light.png"))
    for kind in ("mark", "lockup"):
        compose(kind, lines, primary, False, domain, mono).save(os.path.join(out, f"{domain}-{kind}.png"))
        compose(kind, lines, primary, True, domain, mono).save(os.path.join(out, f"{domain}-{kind}-light.png"))
    return domain


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("sheet")
    ap.add_argument("--out", default=os.path.join(ROOT, "brand", "logos"))
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--count", type=int, default=0)
    ap.add_argument("--only", nargs="*", default=[])
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    rows = [r for r in csv.DictReader(open(a.sheet, encoding="utf-8-sig"))
            if (r.get("Domain (Purchased)") or "").strip()]
    if a.only:
        rows = [r for r in rows if r["Domain (Purchased)"].strip() in set(a.only)]
    else:
        rows = rows[a.start:(a.start + a.count) if a.count else None]
    n = 0
    for r in rows:
        gen_for(r, a.out)
        n += 1
        if n % 50 == 0:
            print(f"  ...{n}/{len(rows)}")
    print(f"Wrote {n} domains x 5 files -> {a.out}")


if __name__ == "__main__":
    main()
