#!/usr/bin/env python
"""Measure every text element against the colour actually painted behind it.

The gate reads HTML and CSS as text. It checks the colour pairs it was told
about, which is why the three alternate templates shipped for months with a
star row at 1.83:1 and body text at 3.41:1 -- nobody had told it those pairs
existed. This asks the browser instead, so a pair nobody thought of still gets
caught.

    cd engine && python3 devtools/contrast_audit.py
    # then open the printed URL for each site

Serve each site at its OWN origin. The pages reference /assets/site.css
absolutely, so hosting several under one root 404s the stylesheet and every
element is then measured unstyled -- which reads as CLEAN and means nothing.
review_server.py rewrites those paths; serve.py gives each site its own port.
Either is fine. Sharing one plain root is not.

Two things it deliberately skips, both of which cost a full pass before they
were understood:

  * text sitting on a photograph -- an <img> stretched behind a section is a
    background to the eye and invisible to getComputedStyle, so a cream
    headline on a darkened hero reads as cream-on-white
  * lazy images, which never load in a headless pane, making a section that
    has a photo look like one that does not
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")

PAGE = r"""<meta charset="utf-8"><title>rendered contrast audit</title>
<body style="font:13px/1.5 ui-monospace,monospace;padding:14px"><pre id="out">running...</pre>
<script>
const NL = String.fromCharCode(10);
// Every text-bearing element on the page, measured as it actually paints:
// its own computed colour against the first ancestor that paints a background.
// The gate checks specific token pairs it was told about. This checks what a
// reader sees, which is the only way to find a pair nobody thought to add.
function rgb(s){
  const m = s.match(/rgba?\(([^)]+)\)/);
  if (!m) return null;
  const p = m[1].split(',').map(Number);
  return {r:p[0], g:p[1], b:p[2], a:p.length > 3 ? p[3] : 1};
}
function over(fg, bg){            // flatten a translucent colour onto its ground
  const a = fg.a;
  return {r:a*fg.r+(1-a)*bg.r, g:a*fg.g+(1-a)*bg.g, b:a*fg.b+(1-a)*bg.b, a:1};
}
function lum(c){
  const f = v => { v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055, 2.4); };
  return 0.2126*f(c.r) + 0.7152*f(c.g) + 0.0722*f(c.b);
}
function ratio(a, b){
  const l1 = lum(a), l2 = lum(b);
  return (Math.max(l1,l2)+0.05) / (Math.min(l1,l2)+0.05);
}
// An <img> stretched across a section is a background to the eye and invisible
// to getComputedStyle. Reporting text on a darkened photo as "cream on white"
// wasted a whole pass here -- the hero and the pull quote were both fine.
function onPhoto(el, win){
  let n = el;
  while (n && n !== n.ownerDocument.documentElement) {
    if (win.getComputedStyle(n).backgroundImage !== 'none') return true;
    for (const img of n.children || []) {
      if (img.tagName !== 'IMG') continue;
      const ps = win.getComputedStyle(img).position;
      if (ps === 'absolute' || ps === 'fixed') {
        const a = img.getBoundingClientRect(), b = el.getBoundingClientRect();
        if (a.left <= b.left && a.right >= b.right &&
            a.top <= b.top && a.bottom >= b.bottom) return true;
      }
    }
    n = n.parentElement;
  }
  return false;
}
function ground(el, win){
  let n = el;
  while (n && n !== n.ownerDocument.documentElement) {
    const c = rgb(win.getComputedStyle(n).backgroundColor);
    if (c && c.a > 0.95) return c;
    n = n.parentElement;
  }
  return {r:255,g:255,b:255,a:1};
}
function audit(doc, win, label){
  const bad = [];
  doc.querySelectorAll('body *').forEach(el => {
    // only elements with their own visible text
    const own = [...el.childNodes].some(n => n.nodeType===3 && n.textContent.trim());
    if (!own) return;
    const cs = win.getComputedStyle(el);
    if (cs.visibility==='hidden' || cs.display==='none' || +cs.opacity===0) return;
    const r = el.getBoundingClientRect();
    if (!r.width || !r.height) return;
    const fg0 = rgb(cs.color); if (!fg0) return;
    const bg = ground(el, win);
    const fg = over(fg0, bg);
    const px = parseFloat(cs.fontSize);
    const bold = (parseInt(cs.fontWeight,10) || 400) >= 700;
    const large = px >= 24 || (px >= 18.66 && bold);
    const need = large ? 3 : 4.5;
    const got = ratio(fg, bg);
    if (got < need && !onPhoto(el, win)) {
      bad.push('    ' + el.tagName.toLowerCase() + (el.className && typeof el.className==='string'
        ? '.' + el.className.trim().split(/\s+/).join('.') : '') +
        '  ' + got.toFixed(2) + ':1 (needs ' + need + ')  colour ' + cs.color +
        ' on rgb(' + Math.round(bg.r) + ',' + Math.round(bg.g) + ',' + Math.round(bg.b) + ')' +
        '  "' + el.textContent.trim().slice(0,32) + '"');
    }
  });
  return bad;
}
function frame(w, src){
  return new Promise(res => {
    const f = document.createElement('iframe');
    f.style.cssText = 'position:absolute;left:-9999px;border:0;height:1400px;width:'+w+'px';
    f.src = src;
    f.onload = () => setTimeout(() => res(f), 500);
    document.body.appendChild(f);
  });
}
(async () => {
  const out = [];
  let n = 0;
  for (const u of PAGES) {
    for (const w of [1280, 390]) {
      const f = await frame(w, u);
      let bad = [];
      try { bad = audit(f.contentDocument, f.contentWindow, u); }
      catch (e) { bad = ['    unreadable: ' + e.message]; }
      f.remove();
      n++;
      if (bad.length) out.push('  ' + u + ' @' + w + NL + [...new Set(bad)].join(NL));
      document.getElementById('out').textContent = 'checked ' + n + ' renders, ' + out.length + ' with problems...';
    }
  }
  document.getElementById('out').textContent = out.length
    ? 'PROBLEMS:' + NL + out.join(NL)
    : 'CLEAN - every text element clears AA against the background it paints on.';
})();
</script>
"""


def pages_for(site):
    out = ["/index.html"]
    for rel in ("about", "contact", "services", "service-areas", "guides"):
        if os.path.isfile(os.path.join(DIST, site, rel, "index.html")):
            out.append(f"/{rel}/index.html")
        sub = os.path.join(DIST, site, rel)
        if os.path.isdir(sub):
            kids = sorted(k for k in os.listdir(sub)
                          if os.path.isdir(os.path.join(sub, k)))
            if kids:
                out.append(f"/{rel}/{kids[0]}/index.html")
    return out


def main():
    sites = sorted(d for d in os.listdir(DIST)
                   if os.path.isfile(os.path.join(DIST, d, "index.html")))
    for s in sites:
        dest = os.path.join(DIST, s, "contrast.html")
        open(dest, "w", encoding="utf-8", newline="\n").write(
            PAGE.replace("PAGES", json.dumps(pages_for(s))))
    print(f"wrote contrast.html into {len(sites)} sites.")
    print("start the per-site servers (python3 serve.py) and open, for each:")
    for s in sites:
        print(f"  http://localhost:<its port>/contrast.html   # {s}")
    print("")
    print("remove them again with:  rm dist/*/contrast.html")


if __name__ == "__main__":
    main()
