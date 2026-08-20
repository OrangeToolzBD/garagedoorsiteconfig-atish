#!/usr/bin/env python
"""Serve every built site under ONE origin, for sharing a single review link.

serve.py gives each site its own port, which is right locally and useless
through a tunnel: one tunnel, one port. Putting the sites under paths instead
breaks them, because every page references `/assets/site.css` absolutely -- I
have now watched that 404 twice and spent a pass each time reading contrast
numbers off completely unstyled pages.

So this rewrites the absolute references as it serves, per site:

    /dallasgaragedoor.com/services/   ->  dist/dallasgaragedoor.com/services/
    href="/about/"                    ->  href="/dallasgaragedoor.com/about/"
    url(/assets/photos/x.webp)        ->  url(/dallasgaragedoor.com/assets/...)

    python3 devtools/review_server.py 8600
"""
import os
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")

TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
         ".js": "application/javascript", ".json": "application/json",
         ".xml": "application/xml", ".txt": "text/plain; charset=utf-8",
         ".svg": "image/svg+xml", ".webp": "image/webp", ".jpg": "image/jpeg",
         ".jpeg": "image/jpeg", ".png": "image/png", ".ico": "image/x-icon",
         ".woff2": "font/woff2"}

# ="/foo but never ="// (protocol-relative) and never a full URL
_ABS = re.compile(rb'((?:href|src|action|content)=")/(?!/)')
_URL = re.compile(rb'url\((["\']?)/(?!/)')


def sites():
    if not os.path.isdir(DIST):
        return []
    return sorted(d for d in os.listdir(DIST)
                  if os.path.isfile(os.path.join(DIST, d, "index.html")))


def portal():
    rows = []
    for d in sites():
        n = sum(len(f) for _r, _dd, f in os.walk(os.path.join(DIST, d)))
        rows.append(
            f'<li><a href="/{d}/">{d}</a><span>{n} files</span></li>')
    return f"""<!doctype html><meta charset="utf-8"><title>Review build</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
 body{{font:16px/1.6 system-ui,sans-serif;margin:0;background:#eef1f5;color:#182029}}
 .w{{max-width:760px;margin:0 auto;padding:32px 20px 60px}}
 h1{{font-size:22px;margin:0 0 4px}} p{{color:#5c6773;margin:0 0 22px}}
 ul{{list-style:none;padding:0;margin:0;background:#fff;border:1px solid #dde3ea;
    border-radius:12px;overflow:hidden}}
 li{{display:flex;justify-content:space-between;align-items:center;
    border-bottom:1px solid #eef1f4}}
 li:last-child{{border-bottom:0}}
 li a{{flex:1;padding:14px 18px;color:#182029;text-decoration:none;font-weight:600}}
 li a:hover{{background:#f5f7f9}}
 li span{{padding-right:18px;color:#8a95a1;font-size:13px}}
</style><div class="w"><h1>Garage door sites &mdash; review build</h1>
<p>{len(sites())} sites. Open any one, then browse it normally.</p>
<ul>{''.join(rows)}</ul></div>"""


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        path = self.path.split("?")[0].split("#")[0]
        if path in ("/", "/index.html"):
            return self._send(portal().encode("utf-8"), "text/html; charset=utf-8")

        parts = [p for p in path.split("/") if p]
        if not parts:
            return self.send_error(404)
        site, rest = parts[0], parts[1:]
        base = os.path.join(DIST, site)
        if not os.path.isdir(base):
            return self.send_error(404, "no such site")

        target = os.path.join(base, *rest) if rest else base
        if os.path.isdir(target):
            target = os.path.join(target, "index.html")
        # keep the served file inside its own site
        if not os.path.abspath(target).startswith(os.path.abspath(base)):
            return self.send_error(403)
        if not os.path.isfile(target):
            return self.send_error(404)

        body = open(target, "rb").read()
        ext = os.path.splitext(target)[1].lower()
        if ext in (".html", ".css", ".xml", ".txt", ".js", ".json"):
            pre = f"/{site}/".encode()
            body = _ABS.sub(lambda m: m.group(1) + pre, body)
            body = _URL.sub(lambda m: b"url(" + m.group(1) + pre, body)
        self._send(body, TYPES.get(ext, "application/octet-stream"))

    def _send(self, body, ctype):
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8600
    print(f"serving {len(sites())} sites on http://127.0.0.1:{port}/")
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
