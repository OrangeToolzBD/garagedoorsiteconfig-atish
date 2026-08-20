#!/usr/bin/env python
"""Validate content packs before a build, and say what is wrong with them.

991 of 1001 sites have no content, and the build reports each one as a single
`skip` line among a thousand. That is fine for a missing pack and useless for a
broken one: a file named `dallas-svcs-repair.json` instead of `dallas-svc-...`
is dropped by load_content() without a word, and the page it held simply never
appears.

    python3 devtools/check_content.py              # every pack
    python3 devtools/check_content.py dallas-tx    # one pack
    python3 devtools/check_content.py --sites      # what each registered site wants

Exits non-zero if any pack has a fault, so it can gate a content pipeline.


THE CONTRACT
------------
A pack is a directory `engine/content/<name>/`. `sites.json` points at it with
the site's `content` field. Inside it, every `*.json` file except `_run.json`
is a page, and the FILENAME decides which:

    <anything>-home.json              ->  /                    the homepage
    <anything>-svc-<slug>.json        ->  /services/<slug>/
    <anything>-nb-<slug>.json         ->  /service-areas/<slug>/
    <anything>-sub-<slug>.json        ->  /service-areas/<slug>/
    <anything>-top-<slug>.json        ->  /guides/<slug>/

The second dash-separated token is the type. Anything else -- a typo, a plural,
a new type nobody taught the loader -- is dropped in silence. That is the fault
this script exists to catch.

Service filenames may carry a `-<city>-<st>` tail; it is stripped from the slug.

Each file must be a JSON **object** with a `sections` key. Without it the whole
page is dropped, taking its title, meta and FAQ with it. Everything else is
optional:

    h1, title, meta        strings
    sections               [{h2, body}]     the page body -- required
    faq                    [{q, a}]         entries with no `q` are ignored
    schema_facts.areaServed                 defaults to the site's city

A pack with no `-home.json` builds a site with no homepage.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
CONFIG = os.path.join(ROOT, "config")

TYPES = {"home": "/", "svc": "/services/", "nb": "/service-areas/",
         "sub": "/service-areas/", "top": "/guides/"}


def check_pack(name):
    """(counts, faults) for one pack."""
    d = os.path.join(CONTENT, name)
    if not os.path.isdir(d):
        return {}, [f"no such directory: content/{name}/"]
    counts, faults = {k: 0 for k in TYPES}, []
    for fn in sorted(os.listdir(d)):
        if fn == "_run.json" or not fn.endswith(".json"):
            continue
        parts = fn[:-5].split("-")
        ptype = parts[1] if len(parts) > 1 else "home"
        if ptype not in TYPES:
            faults.append(f"{fn}: filename type '{ptype}' is not one of "
                          f"{sorted(TYPES)} -- this file is dropped silently")
            continue
        path = os.path.join(d, fn)
        try:
            data = json.load(open(path, encoding="utf-8"))
        except Exception as e:
            faults.append(f"{fn}: unreadable JSON ({e})")
            continue
        if not isinstance(data, dict):
            faults.append(f"{fn}: top level is {type(data).__name__}, not an object")
            continue
        if "sections" not in data:
            faults.append(f"{fn}: no 'sections' key -- the page is dropped, and "
                          f"its title, meta and faq go with it")
            continue
        if not isinstance(data["sections"], list) or not data["sections"]:
            faults.append(f"{fn}: 'sections' is empty, so the page renders blank")
        for i, s in enumerate(data.get("sections", []) or []):
            if not isinstance(s, dict) or not (s.get("body") or "").strip():
                faults.append(f"{fn}: section {i} has no body")
        for i, f in enumerate(data.get("faq", []) or []):
            if isinstance(f, dict) and f.get("a") and not f.get("q"):
                faults.append(f"{fn}: faq {i} has an answer but no question, "
                              f"so it is dropped")
        counts[ptype] += 1
    if not counts["home"]:
        faults.append("no *-home.json -- this site would build without a homepage")
    return counts, faults


def main(argv):
    if "--sites" in argv:
        sites = json.load(open(os.path.join(CONFIG, "sites.json"),
                               encoding="utf-8"))["sites"]
        want = {}
        for s in sites:
            want.setdefault(s.get("content", ""), []).append(s["domain"])
        have = set(os.listdir(CONTENT)) if os.path.isdir(CONTENT) else set()
        missing = {k: v for k, v in want.items() if k not in have}
        print(f"  registered sites   : {len(sites)}")
        print(f"  content packs on disk: {len(have)}")
        print(f"  sites that can build : {sum(len(v) for k, v in want.items() if k in have)}")
        print(f"  sites with no pack   : {sum(len(v) for v in missing.values())}"
              f"  ({len(missing)} distinct packs missing)")
        return 0

    names = [a for a in argv[1:] if not a.startswith("-")]
    if not names:
        names = sorted(d for d in os.listdir(CONTENT)
                       if os.path.isdir(os.path.join(CONTENT, d)))
    bad = 0
    for n in names:
        counts, faults = check_pack(n)
        line = (f"  {n:18} home={counts.get('home', 0)} "
                f"svc={counts.get('svc', 0)} "
                f"area={counts.get('nb', 0) + counts.get('sub', 0)} "
                f"guide={counts.get('top', 0)}")
        print(line + ("" if faults else "   ok"))
        for f in faults:
            print(f"      ! {f}")
        bad += bool(faults)
    print(f"\n  {len(names)} pack(s), {bad} with faults")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
