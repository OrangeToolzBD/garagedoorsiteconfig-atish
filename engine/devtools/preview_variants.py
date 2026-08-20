#!/usr/bin/env python
"""Render every section variant on one page, and audit it for overflow.

The gate in measure_similarity.py reads HTML and CSS as text. It cannot see
layout, so it cannot catch the bug class that actually reaches the eye: a box
painting outside the box that is supposed to contain it. Both page-hero grid
bugs were of that kind -- a 249px breadcrumb tail inside a 190px rail, then a
375px grid track inside a 354px container -- and both passed the gate 17/17.

    python3 devtools/preview_variants.py out/
    python3 -m http.server 8890 --directory out/
    # open /audit.html and read the result

The audit iframes the preview at five widths and reports any element that
paints outside its parent's content box, plus any page that scrolls sideways.
"""
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import build as B

# Which site's tokens to render with. Fonts now vary per domain, and a face
# 16% wider than Urbanist wraps headings differently, so the domain chosen
# decides which typography this preview actually exercises. Pass one on the
# command line to audit a different pairing.
DOMAIN = os.environ.get("PREVIEW_DOMAIN", "dallasgaragedoor.com")

LONG_H1 = "Garage Door Repair for Dallas Homes Built 1973-2007"
SHORT_H1 = "About Dallas Garage Door"
DESC = ("Broken springs and stuck tracks are common in Dallas homes built "
        "1973-2007. See what a repair call involves, what it costs, and when "
        "to skip DIY fixes.")
LINKS = [("Home", "/"), ("Services", "/services/")]
HEADINGS = [("common-failures", "What usually breaks on an older door"),
            ("repair-costs", "What a repair actually costs"),
            ("diy-safety", "When to skip the DIY fix"),
            ("warranty", "Warranty and parts"),
            ("timing", "How long a call takes"),
            ("faq", "Questions people ask")]
# the longest real area label in the estate, which is what broke the pills
AREAS = ["buckner-terrace-everglade-park", "lakewood", "preston-hollow",
         "desoto", "balch-springs", "cedar-crest", "ferris"]

AUDIT = """<meta charset="utf-8"><title>overflow audit</title>
<body style="font:13px/1.5 monospace;padding:14px"><pre id="out">running...</pre>
<script>
const NL = String.fromCharCode(10);
const WIDTHS = [1280, 900, 768, 390, 360];
function audit(doc, win) {
  const bad = [];
  doc.querySelectorAll('.page-hero, .aside, header.site').forEach(root => {
    const tag = root.className.replace(/\\s+/g, '.');
    root.querySelectorAll('*').forEach(el => {
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      const own = getComputedStyle(el).position;
      if (own === 'absolute' || own === 'fixed') {
        // A dropdown is meant to be wider than the button it hangs off, so
        // measuring it against its parent reports the design as a fault. What
        // actually matters for something out of flow is whether it stays on
        // screen -- a 560px menu is fine until it runs off the right edge.
        if (r.right > win.innerWidth + 1 || r.left < -1)
          bad.push('    ' + tag + ' > ' + (el.className || el.tagName) +
                   ' leaves the viewport: ' + Math.round(r.left) + '..' +
                   Math.round(r.right) + ' of ' + win.innerWidth);
        return;
      }
      const p = el.parentElement, pr = p.getBoundingClientRect();
      const cs = getComputedStyle(p);
      const inL = pr.left + parseFloat(cs.paddingLeft);
      const inR = pr.right - parseFloat(cs.paddingRight);
      if (cs.overflow === 'visible' && (r.right > inR + 1 || r.left < inL - 1))
        bad.push('    ' + tag + ' > ' + (el.className || el.tagName) + ' spills ' +
                 Math.round(Math.max(r.right - inR, inL - r.left)) + 'px');
    });
  });
  if (doc.documentElement.scrollWidth > win.innerWidth + 1)
    bad.push('    PAGE scrolls sideways: ' + doc.documentElement.scrollWidth +
             ' > ' + win.innerWidth);
  return bad;
}
function frame(w, src) {
  return new Promise(res => {
    const f = document.createElement('iframe');
    f.style.cssText = 'position:absolute;left:-9999px;border:0;height:1000px;width:' + w + 'px';
    f.src = src;
    f.onload = () => setTimeout(() => res(f), 220);
    document.body.appendChild(f);
  });
}
(async () => {
  const out = [];
  for (const u of ['/heroes.html', '/sidebars.html']) {
    for (const w of WIDTHS) {
      const f = await frame(w, u);
      let bad = [];
      try { bad = audit(f.contentDocument, f.contentWindow); }
      catch (e) { bad = ['    could not read: ' + e.message]; }
      f.remove();
      if (bad.length) out.push('  ' + u + '  @' + w + NL + bad.join(NL));
    }
  }
  document.getElementById('out').textContent = out.length
    ? 'PROBLEMS:' + NL + out.join(NL)
    : 'CLEAN - nothing spills its container at any width.';
})();
</script>
"""


def shell(css, body, extra=""):
    # The font <link> lives in head_html(), not in the stylesheet, so a preview
    # built from css(t) alone renders in system-ui -- every height measured here
    # before this line was added was the fallback face, not the site's own.
    t = B.load_config()[DOMAIN]
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family='
            f'{t["fonts"]}&display=swap">'
            f"<title>variants</title><style>{css}\n"
            ".lbl{font:600 12px/1 ui-monospace,monospace;letter-spacing:.08em;"
            "text-transform:uppercase;color:#888;margin:22px 0 6px;padding:0 16px}"
            f"body{{margin:0}}{extra}</style></head><body>{body}</body></html>")


def main(dest):
    os.makedirs(dest, exist_ok=True)
    t = B.load_config()[DOMAIN]
    css = B.strip_css_comments(B.GARAGE["css"](t))

    src = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "dist", DOMAIN, "assets")
    if os.path.isdir(src):
        shutil.rmtree(os.path.join(dest, "assets"), ignore_errors=True)
        shutil.copytree(src, os.path.join(dest, "assets"))

    # ---- page heroes: every variant, with a long and a short title ----------
    orig = B.PAGE_HERO_VARIANTS
    blocks = []
    for v in orig:
        B.PAGE_HERO_VARIANTS = [v]
        blocks.append(
            f'<p class="lbl">{v} &mdash; long title, with description</p>'
            + B.page_hero(t, LINKS, LONG_H1, LONG_H1, desc=DESC, img="gd-1.jpg")
            + f'<p class="lbl">{v} &mdash; short title, no description</p>'
            + B.page_hero(t, [("Home", "/")], SHORT_H1, SHORT_H1, desc="", img="gd-2.jpg"))
    B.PAGE_HERO_VARIANTS = orig
    open(os.path.join(dest, "heroes.html"), "w", encoding="utf-8",
         newline="\n").write(shell(css, "".join(blocks)))

    # ---- sidebars: every variant, in every article layout -------------------
    # article--wide has no column at all: the aside stacks below the prose, and
    # that is where the table of contents landed -- after the article it
    # indexes, on 75 sites. Rendering only the 320px column hid that entirely.
    pages = {f"/service-areas/{s}/": {"cat": "area", "url": f"/service-areas/{s}/",
                                      "slug": s, "h1": s.replace("-", " ").title()}
             for s in AREAS}
    prose = ('<h2 id="common-failures">What usually breaks</h2><p>'
             + "Body copy. " * 40
             + '</p><h2 id="repair-costs">What a repair costs</h2><p>'
             + "More copy. " * 40 + "</p>")
    orig = B.ASIDE_VARIANTS
    out = []
    for lay in B.ARTICLE_LAYOUTS:
        for v in orig:
            B.ASIDE_VARIANTS = [v]
            out.append(f'<p class="lbl">{v} &mdash; article{lay or " (default)"}</p>'
                       f'<div class="wrap"><div class="article {lay}">'
                       f'<div class="body">{prose}</div>'
                       + B.quote_card(t, pages, HEADINGS) + "</div></div>")
    B.ASIDE_VARIANTS = orig
    open(os.path.join(dest, "sidebars.html"), "w", encoding="utf-8",
         newline="\n").write(shell(css, "".join(out), ".aside{position:static}"))

    # ---- headers: every variant, with a dropdown forced open ----------------
    # The header is 21% of every page and carries the only JavaScript in the
    # build. The dropdown has to be audited OPEN: closed it is 0x0 and cannot
    # overflow anything, which is exactly the state that hides the problem.
    hdr_pages = dict(pages)
    for i, n in enumerate(["Garage Door Repair", "New Door Installation",
                           "Spring Replacement", "Opener Repair"]):
        hdr_pages[f"/services/s{i}/"] = {"cat": "service", "url": f"/services/s{i}/",
                                         "slug": f"s{i}", "h1": n}
    orig = B.HEADER_VARIANTS
    out = []
    for pack in orig:
        B.HEADER_VARIANTS = [pack]
        # header() is a page-opener: it ends with `<main id="main">`. Keep only
        # the header itself, or <main> lands inside it and the audit reports the
        # harness rather than the header.
        mk = B.header(t, hdr_pages)
        # .open on every dropdown: the class the script toggles, so the audit
        # measures what a reader actually gets rather than a hidden state
        out.append(f'<p class="lbl">header &mdash; {pack[0]}</p>'
                   + mk[:mk.index("<main")].replace('class="nav-item"',
                                                    'class="nav-item open"')
                   + '<div style="height:420px"></div>')
    B.HEADER_VARIANTS = orig
    open(os.path.join(dest, "headers.html"), "w", encoding="utf-8",
         newline="\n").write(shell(css, "".join(out),
             # Only unhide them. Do NOT pin left/transform: the open state has
             # its own values, and overriding them measures a position no reader
             # ever sees. Every element carries .open in the markup below, so
             # this is the genuine open geometry.
             ".nav-item.open .mega{opacity:1!important;visibility:visible!important}"
             "header.site{position:static}"))

    # ---- service areas: every variant, sparse and dense ---------------------
    # 3 places is what almost every site has today; 26 is what the one site
    # with real neighbourhood data has. A design that only ever sees 3 hides
    # the case that matters, and the long name is the one that breaks columns.
    sparse = [("Kessler", 2, "/service-areas/kessler/"),
              ("Lakewood", 4, "/service-areas/lakewood/"),
              ("DeSoto", 15, None)]
    dense = [(n, m, None if n == "Ferris" else f"/service-areas/{n.lower()}/")
             for n, m in [("Old East Dallas", 1), ("South Dallas", 3), ("Kessler", 2),
                          ("Lakewood", 4), ("Lower Greenville", 3), ("Northeast Dallas", 6),
                          ("Cedar Crest", 5), ("Buckner Terrace / Everglade Park", 7),
                          ("Downtown Historic District", 1), ("Balch Springs", 14),
                          ("DeSoto", 15), ("Ferris", 20), ("Kessler Park", 2),
                          ("Oak Cliff", 5), ("Preston Hollow", 9), ("Uptown", 2),
                          ("Lake Highlands", 8), ("Deep Ellum", 2), ("Knox-Henderson", 3),
                          ("Bishop Arts", 4), ("Trinity Groves", 3), ("Casa Linda", 7),
                          ("Wilshire Heads", 6), ("Munger Place", 2),
                          ("Junius Heights", 3), ("Swiss Avenue", 2)]]
    orig = B.AREAS_VARIANTS
    out = []
    for v in orig:
        B.AREAS_VARIANTS = [v]
        for label, items in (("3 places", sparse), ("26 places", dense)):
            out.append(f'<p class="lbl">{v} &mdash; {label}</p>'
                       f'<section class="sec"><div class="wrap">'
                       + B.areas_list(t, items) + "</div></section>")
    B.AREAS_VARIANTS = orig
    open(os.path.join(dest, "areas.html"), "w", encoding="utf-8",
         newline="\n").write(shell(css, "".join(out)))

    open(os.path.join(dest, "audit.html"), "w", encoding="utf-8",
         newline="\n").write(AUDIT.replace("'/sidebars.html'",
                                           "'/sidebars.html', '/areas.html', '/headers.html'"))
    print(f"wrote heroes.html, sidebars.html and audit.html to {dest}")
    print(f"  python3 -m http.server 8890 --directory {dest}")
    print("  then open http://127.0.0.1:8890/audit.html")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "preview")
