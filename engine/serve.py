#!/usr/bin/env python
"""Serve the built sites locally: portal on 8000, each city on its config port.

Binds to 0.0.0.0 so each site is reachable both at http://localhost:<port>/ and
at http://<this-machine-LAN-IP>:<port>/ (e.g. from a phone on the same Wi-Fi)."""
import functools
import json
import os
import socket
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
CONFIG = os.path.join(ROOT, "config", "sites.json")


def lan_ip():
    """Best-effort primary LAN IPv4 for this machine (no traffic actually sent)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def load_sites():
    import sys
    data = json.load(open(CONFIG, encoding="utf-8"))
    domains = {s["domain"] for s in data["sites"]}
    # optional CLI filter: only argv items that are actual domains (ignores the
    # "serve" subcommand added by engine.py) restrict which sites are served.
    only = set(sys.argv[1:]) & domains
    out = []
    for i, s in enumerate(data["sites"]):
        if only and s["domain"] not in only:
            continue
        out.append((s["domain"], s.get("port") or 8001 + i))
    return out


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


def serve(directory, port):
    httpd = ThreadingHTTPServer(("0.0.0.0", port), functools.partial(Handler, directory=directory))
    httpd.serve_forever()


def main():
    ip = lan_ip()
    servers = [(DIST, 8000, "PORTAL")]
    for domain, port in load_sites():
        d = os.path.join(DIST, domain)
        if os.path.isdir(d):
            servers.append((d, port, domain))
    for directory, port, label in servers:
        threading.Thread(target=serve, args=(directory, port), daemon=True).start()
        print(f"  {label}")
        print(f"    local:   http://localhost:{port}/")
        print(f"    network: http://{ip}:{port}/")
    print(f"\nPortal: http://localhost:8000/  |  http://{ip}:8000/   (Ctrl+C to stop)")
    threading.Event().wait()


if __name__ == "__main__":
    main()
