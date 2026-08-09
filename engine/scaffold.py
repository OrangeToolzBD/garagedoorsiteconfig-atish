#!/usr/bin/env python
"""Register new city sites into the engine config.

  python scaffold.py <master.csv> <domain1> <domain2> ...

For each domain it pulls phone + address from the master sheet CSV (matched on
the github_repo column) and logo/colour/fonts from the brand ledger, derives a
contrast-safe theme, assigns a rotating layout + next port, and writes the entry
into config/sites.json (+ a theme into config/themes.json). Idempotent per domain.
"""
import csv
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(ROOT, "config")
LEDGER = r"C:\Users\Masud\Desktop\setu\otofc\portapotty\sites-porta-potty\ledger\brand_ledger.jsonl"
LAYOUTS = ["aurora", "meridian", "cobalt", "harbor", "summit", "monarch"]
SINGLE_WEIGHT = {"Anton"}

# ---- colour helpers ----
def rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def hx(t): return "#%02x%02x%02x" % tuple(max(0, min(255, int(round(c)))) for c in t)
def lum(h):
    r, g, b = [c / 255 for c in rgb(h)]
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def contrast(a, b):
    L = sorted([lum(a), lum(b)], reverse=True); return (L[0] + 0.05) / (L[1] + 0.05)
def mix(h, t, a): x, y = rgb(h), rgb(t); return hx(tuple(x[i] + (y[i] - x[i]) * a for i in range(3)))
def darken(h, a): return mix(h, "#000000", a)
def lighten(h, a): return mix(h, "#ffffff", a)

def make_primary(p):
    for _ in range(14):
        if contrast(p, "#ffffff") >= 5.0:
            break
        p = darken(p, 0.10)
    return p

def make_accent(a):
    dark = "#241400"
    if contrast(a, dark) >= contrast(a, "#ffffff"):
        on = dark
        for _ in range(14):
            if contrast(a, on) >= 4.6:
                break
            a = lighten(a, 0.09)
    else:
        on = "#ffffff"
        for _ in range(14):
            if contrast(a, on) >= 4.6:
                break
            a = darken(a, 0.09)
    return a, on

def fonts_str(display, body):
    def fam(name, weights):
        n = name.replace(" ", "+")
        return n if name in SINGLE_WEIGHT else f"{n}:wght@{weights}"
    return f"{fam(display, '600;700')}&family={fam(body, '400;500;600')}"

def fmt_phone(num):
    d = re.sub(r"\D", "", num or "")
    if len(d) == 11 and d[0] == "1":
        d = d[1:]
    if len(d) != 10:
        return "", ""
    return f"({d[0:3]}) {d[3:6]}-{d[6:]}", d[0:3]

def parse_addr(addr):
    addr = (addr or "").strip()
    m = re.search(r"\b(\d{5})(?:-\d{4})?\s*$", addr)
    zipc = m.group(1) if m else ""
    street = addr.split(",")[0].strip()
    return street, zipc


def load_master(path):
    rows = {}
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            repo = (r.get("github_repo") or "").strip()
            if repo:
                rows[repo.rstrip("/").split("/")[-1]] = r
    return rows

def load_ledger():
    led = {}
    for line in open(LEDGER, encoding="utf-8"):
        line = line.strip()
        if line:
            j = json.loads(line); led[j.get("domain")] = j
    return led


def main():
    master = load_master(sys.argv[1])
    domains = sys.argv[2:]
    led = load_ledger()
    themes = json.load(open(os.path.join(CONFIG, "themes.json"), encoding="utf-8"))
    sdata = json.load(open(os.path.join(CONFIG, "sites.json"), encoding="utf-8"))
    existing = {s["domain"] for s in sdata["sites"]}
    next_port = max([s.get("port", 8000) for s in sdata["sites"]] + [8000]) + 1

    for domain in domains:
        if domain in existing:
            print(f"  skip (already registered): {domain}"); continue
        m = master.get(domain, {})
        l = led.get(domain, {})
        b = l.get("brand", {}); pal = b.get("palette", {}); typ = b.get("type", {})
        city = (m.get("City") or l.get("city") or domain.replace("portapros.com", "")).strip()
        st = (m.get("State") or "").strip()
        phone, area = fmt_phone(m.get("Number"))
        street, zipc = parse_addr(m.get("Verified Address") or m.get("Adress"))
        prim = pal.get("primary") or "#2c3e50"
        acc = pal.get("accent") or "#e0821a"
        p = make_primary(prim)
        a, on = make_accent(acc)
        theme_key = domain.split(".")[0]
        themes[theme_key] = {
            "p": p, "pd": darken(p, 0.30), "accent": a, "on_accent": on,
            "display": typ.get("display", "Poppins"), "body": typ.get("body", "Inter"),
            "fonts": fonts_str(typ.get("display", "Poppins"), typ.get("body", "Inter")),
        }
        entry = {
            "domain": domain, "city": city, "st": st, "area": area,
            "street": street, "zip": zipc, "theme": theme_key,
            "tagline": f"{city} Rentals", "port": next_port,
            "layout": LAYOUTS[len(sdata["sites"]) % len(LAYOUTS)],
            "phone": phone,
        }
        if l.get("site_id"):
            entry["site_id"] = int(l["site_id"])
        sdata["sites"].append(entry)
        existing.add(domain)
        next_port += 1
        print(f"  + {domain}: {city}, {st} | {phone or 'NO PHONE'} | {street} {zipc} | theme p={p} a={a} | layout={entry['layout']} | port={entry['port']}")

    json.dump(themes, open(os.path.join(CONFIG, "themes.json"), "w", encoding="utf-8"), indent=2)
    json.dump(sdata, open(os.path.join(CONFIG, "sites.json"), "w", encoding="utf-8"), indent=2)
    print("Wrote config/themes.json and config/sites.json")


if __name__ == "__main__":
    main()
