#!/usr/bin/env python
"""Map the pre-made brand/logos/<row#>_<business-slug>.png emblems to the
per-domain filenames build.py actually looks for, with their flat white
background knocked out to transparent.

brand/logos/ ships 200 hand-made 200x200 emblem PNGs named by their row number
in domains.csv (e.g. "02_mesa_garage_door_co.png" == row 2 == mesagaragedoorco.com),
each with a near-white (~253-254) background baked into the pixels. build.py looks
up assets by *domain*: "<domain>-emblem.png" (header/nav + footer) and
"<domain>-favicon.png" in that same folder. Nothing previously bridged the two, so
every built site fell back to the generated SVG door mark (see ENGINE_GUIDE.md §8.1).

This copies each numbered emblem to its domain-named twin AND removes the white
background (soft alpha ramp, not a hard cutoff, to keep anti-aliased edges clean)
so the mark can sit directly on a dark background (the footer) without a visible
white box. The header still wraps it in an explicit white ".brand__chip" box via
CSS, so it looks the same there either way. Source files are never modified.

Usage:
  python logo_prep.py [--sheet ../domains.csv] [--logos ../brand/logos]
"""
import argparse
import csv
import os
import re

from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))

# alpha ramp: pixels whiter than LO start fading out; fully transparent by HI
WHITE_LO, WHITE_HI = 225, 250


def strip_white_bg(src_path, dst_path):
    im = Image.open(src_path).convert("RGBA")
    px = im.load()
    w, h = im.size
    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            whiteness = min(r, g, b)
            if whiteness <= WHITE_LO:
                continue
            if whiteness >= WHITE_HI:
                px[x, y] = (r, g, b, 0)
            else:
                t = (whiteness - WHITE_LO) / (WHITE_HI - WHITE_LO)
                px[x, y] = (r, g, b, int(a * (1 - t)))
    im.save(dst_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sheet", default=os.path.join(os.path.dirname(ROOT), "domains.csv"))
    ap.add_argument("--logos", default=os.path.join(os.path.dirname(ROOT), "brand", "logos"))
    a = ap.parse_args()

    if not os.path.exists(a.sheet):
        print(f"! sheet not found: {a.sheet}"); return
    if not os.path.isdir(a.logos):
        print(f"! logos dir not found: {a.logos}"); return

    # index existing files by their leading row number ("02_..." / "141_..._logo.png" -> 2 / 141)
    by_row = {}
    for fn in os.listdir(a.logos):
        m = re.match(r"^0*(\d+)_", fn)
        if m and fn.lower().endswith(".png"):
            by_row[int(m.group(1))] = fn

    rows = list(csv.DictReader(open(a.sheet, encoding="utf-8-sig")))
    mapped = skipped = 0
    for r in rows:
        domain = (r.get("Domain (Purchased)") or "").strip()
        num = (r.get("#") or "").strip()
        if not domain or not num.isdigit():
            continue
        src_fn = by_row.get(int(num))
        if not src_fn:
            skipped += 1
            continue
        src = os.path.join(a.logos, src_fn)
        for dst_name in (f"{domain}-emblem.png", f"{domain}-favicon.png"):
            strip_white_bg(src, os.path.join(a.logos, dst_name))
        mapped += 1

    print(f"Mapped {mapped} domains to transparent-background emblem/favicon PNGs "
          f"({skipped} rows have no logo file yet).")
    print(f"Total source emblems available: {len(by_row)} / {len(rows)} domains.")


if __name__ == "__main__":
    main()
