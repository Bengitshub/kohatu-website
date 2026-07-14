#!/usr/bin/env python3
"""Scrape kohatumc.co.nz: save page HTML and download original images from the Squarespace CDN."""
import json
import os
import re
import urllib.request

BASE = "https://www.kohatumc.co.nz"
PAGES = [
    "/",
    "/adventure-motorcycle-events",
    "/trail-rides",
    "/gallery",
    "/location",
    "/park",
    "/terms-conditions",
    "/home-2",
    "/nelson-tasman-motorcycle-events",
]
ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES_DIR = os.path.join(ROOT, "source-pages")
ASSETS_DIR = os.path.join(ROOT, "source-assets")
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}


def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def save_page(path):
    name = path.strip("/").replace("/", "_") or "index"
    html = fetch(BASE + path).decode("utf-8", "replace")
    with open(os.path.join(PAGES_DIR, name + ".html"), "w") as f:
        f.write(html)
    return html


def main():
    all_html = []
    # discover event detail pages from the listing page
    listing = save_page("/adventure-motorcycle-events")
    event_paths = sorted(set(re.findall(r'href="(/adventure-motorcycle-events/[^"/][^"#?]*)"', listing)))
    event_paths = [p for p in event_paths if "/category/" not in p]
    print("event pages:", event_paths)

    for path in PAGES + event_paths:
        if path == "/adventure-motorcycle-events":
            all_html.append(listing)
            continue
        try:
            all_html.append(save_page(path))
            print("saved", path)
        except Exception as e:
            print("FAILED", path, e)

    # collect squarespace CDN image urls (strip size params, dedupe)
    urls = set()
    for html in all_html:
        for m in re.findall(r'https://images\.squarespace-cdn\.com/[^\s"\'\\)]+', html):
            m = m.split("?")[0]
            if re.search(r"\.(jpe?g|png|webp|gif)$", m, re.I):
                urls.add(m)
    print(f"{len(urls)} unique images")

    manifest = []
    for i, u in enumerate(sorted(urls)):
        fname = re.sub(r"[^A-Za-z0-9._-]", "_", u.split("/")[-1])[-80:]
        out = os.path.join(ASSETS_DIR, f"{i:03d}_{fname}")
        try:
            data = fetch(u + "?format=2500w")
            with open(out, "wb") as f:
                f.write(data)
            manifest.append({"url": u, "file": os.path.basename(out), "bytes": len(data)})
            print("ok", os.path.basename(out), len(data) // 1024, "KB")
        except Exception as e:
            print("FAILED img", u, e)

    with open(os.path.join(ASSETS_DIR, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)


if __name__ == "__main__":
    main()
