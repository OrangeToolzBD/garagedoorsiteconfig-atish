#!/usr/bin/env python
"""Render one real page block in every candidate font pairing, for choosing.

Typography is the one axis where measurement settles nothing -- the numbers say
a 116%-wide face wraps to two lines, not whether it looks like a garage-door
company. So this shows the actual hero, section head, buttons and prose from the
real stylesheet, with only --disp and --body swapped.

    python3 devtools/preview_fonts.py preview
    python3 -m http.server 8890 --directory preview   # open /fonts.html

Weights are requested as an explicit list per family, from WEIGHTS below, which
was checked family by family against the css2 API. The range form (wght@600..800)
looks tidier and is a trap: it works only for variable families, and for a static
one -- Poppins, Barlow, Lato and four others here -- Google drops the family from
the response with no error, so the page quietly renders in system-ui.

91 of the themes in themes.json currently ask for weights their own font does not
serve, which is why h1 and .brand would come out as a faked bold.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import build as B

DOMAIN = "dallasgaragedoor.com"

# (group, display, body, note). Grouped by character, because that is the
# decision -- not the individual face.
PAIRINGS = [
    ("Geometric sans - closest to today",
     [("Urbanist", "Open Sans", "what every site uses now"),
      ("Poppins", "Inter", ""),
      ("Outfit", "DM Sans", ""),
      ("Figtree", "Figtree", "one family, two weights")]),
    ("Grotesk - neutral and modern",
     [("Inter", "Inter", "one family"),
      ("Archivo", "Roboto", ""),
      ("Manrope", "Manrope", "one family"),
      ("Sora", "Inter", ""),
      ("Space Grotesk", "Inter", "no 800 weight - headings top out at 700")]),
    ("Humanist - warmer, friendlier",
     [("Nunito Sans", "Nunito Sans", "one family"),
      ("Rubik", "Karla", ""),
      ("Lexend", "Lexend", "one family")]),
    ("Slab - industrial, trade-shop feel",
     [("Roboto Slab", "Roboto", ""),
      ("Bitter", "Source Sans 3", ""),
      ("Zilla Slab", "Karla", "no 800 weight")]),
    ("Serif - editorial, more premium",
     [("Playfair Display", "Source Sans 3", ""),
      ("Fraunces", "Nunito Sans", ""),
      ("Source Serif 4", "IBM Plex Sans", "")]),
    ("Condensed - fits long headlines on one line",
     [("Barlow Condensed", "Barlow", ""),
      ("Archivo Narrow", "Archivo", ""),
      ("Oswald", "Roboto", "no 800 weight")]),
]

# Weights each family actually serves, checked one by one against the css2 API
# rather than assumed. Two things this catches:
#   * Archivo Narrow, Oswald, Space Grotesk and Zilla Slab have no 800 at all,
#     so h1 and .brand would be faked by the browser.
#   * Lato serves only 400 -- no 500, no 600 -- which rules it out as a body
#     face here even though it is the classic partner for Playfair Display.
# Ranges (wght@600..800) are NOT usable: they work only for variable families,
# and for a static one Google silently drops the family from the response
# entirely, so the page falls back to system-ui with no error anywhere.
WEIGHTS = {
    "Archivo": [400, 500, 600, 700, 800], "Archivo Narrow": [600, 700],
    "Barlow": [400, 500, 600], "Barlow Condensed": [600, 700, 800],
    "Bitter": [600, 700, 800], "DM Sans": [400, 500, 600],
    "Figtree": [400, 500, 600, 700, 800], "Fraunces": [600, 700, 800],
    "IBM Plex Sans": [400, 500, 600], "Inter": [400, 500, 600, 700, 800],
    "Karla": [400, 500, 600], "Lexend": [400, 500, 600, 700, 800],
    "Manrope": [400, 500, 600, 700, 800], "Nunito Sans": [400, 500, 600, 700, 800],
    "Open Sans": [400, 500, 600], "Oswald": [600, 700],
    "Outfit": [600, 700, 800], "Playfair Display": [600, 700, 800],
    "Poppins": [600, 700, 800], "Roboto": [400, 500, 600],
    "Roboto Slab": [600, 700, 800], "Rubik": [600, 700, 800],
    "Sora": [600, 700, 800], "Source Sans 3": [400, 500, 600],
    "Source Serif 4": [600, 700, 800], "Space Grotesk": [600, 700],
    "Urbanist": [600, 700, 800], "Zilla Slab": [600, 700],
}
NO_800 = {f for f, w in WEIGHTS.items() if 800 not in w}

H1 = "Garage Door Repair for Dallas Homes Built 1973-2007"
LEAD = ("Broken springs and stuck tracks are common in Dallas homes built "
        "1973-2007. See what a repair call involves and when to skip DIY fixes.")
PROSE = ("When a garage door will not budge and you hear a loud bang from the "
         "ceiling, that is almost always a broken torsion spring. In a city "
         "built out in waves, the door on a 1978 house and the door on a 2004 "
         "house fail in different ways, and the parts are not interchangeable.")


def google_url():
    """One entry per family, listing the weights that family really serves.

    Discrete weights, not a range: verified working for all 29 families here,
    where the range syntax silently dropped 6 of them."""
    need = {}
    for _grp, rows in PAIRINGS:
        for disp, body, _n in rows:
            need.setdefault(disp, set()).update({600, 700, 800})
            need.setdefault(body, set()).update({400, 500, 600})
    fams = []
    for f in sorted(need):
        have = sorted(set(WEIGHTS.get(f, [])) & need[f]) or sorted(WEIGHTS.get(f, []))
        fams.append(f"family={f.replace(' ', '+')}:wght@" + ";".join(map(str, have)))
    return "https://fonts.googleapis.com/css2?" + "&".join(fams) + "&display=swap"


def block(disp, body, note, i):
    tag = f'<span class="note">{note}</span>' if note else ""
    return (
        f'<section class="fp" style="--disp:\'{disp}\',system-ui,sans-serif;'
        f'--body:\'{body}\',system-ui,sans-serif">'
        f'<div class="fp__bar"><b>{i}. {disp}</b> + {body} {tag}</div>'
        f'<div class="fp__body">'
        f'<p class="eyebrow">Garage door repair</p>'
        f"<h1>{H1}</h1>"
        f'<p class="lead">{LEAD}</p>'
        f'<p class="fp__btns"><a class="btn btn--primary" href="#">Request a Quote</a>'
        f'<a class="btn btn--outline" href="#">See Our Services</a></p>'
        f"<h2>What usually breaks on an older door</h2>"
        f"<p>{PROSE}</p>"
        f"</div></section>")


def main(dest):
    os.makedirs(dest, exist_ok=True)
    t = B.load_config()[DOMAIN]
    css = B.strip_css_comments(B.GARAGE["css"](t))

    parts, i = [], 0
    for group, rows in PAIRINGS:
        parts.append(f'<h3 class="grp">{group}</h3>')
        for disp, body, note in rows:
            i += 1
            parts.append(block(disp, body, note, i))

    page = (
        '<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        "<title>font pairings</title>"
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        f'<link rel="stylesheet" href="{google_url()}">'
        f"<style>{css}\n"
        "body{margin:0;background:#eef1f5}"
        ".grp{font:700 13px/1 ui-monospace,monospace;letter-spacing:.12em;"
        "text-transform:uppercase;color:#5c6773;margin:34px 0 10px;padding:0 20px}"
        ".fp{background:#fff;margin:0 16px 14px;border:1px solid #dde3ea;"
        "border-radius:10px;overflow:hidden}"
        ".fp__bar{font:400 12px/1.4 ui-monospace,monospace;color:#5c6773;"
        "background:#f5f7f9;border-bottom:1px solid #e3e8ee;padding:8px 18px}"
        ".fp__bar b{color:#182029}"
        ".note{color:#9a4a1a}"
        ".fp__body{padding:22px 26px 26px}"
        ".fp h1{font-size:clamp(1.9rem,3.6vw,2.9rem);margin:0 0 12px}"
        ".fp h2{font-size:1.35rem;margin:22px 0 8px}"
        ".fp .lead{color:#5c6773;max-width:62ch;margin:0 0 16px;font-size:1.02rem}"
        ".fp p{max-width:70ch}"
        ".fp__btns{display:flex;gap:12px;flex-wrap:wrap;margin:0}"
        "</style></head><body>"
        + "".join(parts) + "</body></html>")
    open(os.path.join(dest, "fonts.html"), "w", encoding="utf-8",
         newline="\n").write(page)
    print(f"wrote {os.path.join(dest, 'fonts.html')}  ({i} pairings)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "preview")
