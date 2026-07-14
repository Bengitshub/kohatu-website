#!/usr/bin/env python3
"""Extract readable text content from scraped Squarespace pages into markdown reference files."""
import html
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
PAGES = os.path.join(ROOT, "source-pages")
OUT = os.path.join(ROOT, "source-content")
os.makedirs(OUT, exist_ok=True)


def extract(raw):
    # isolate main content area, drop scripts/styles/nav/footer
    raw = re.sub(r"<script[^>]*>.*?</script>", " ", raw, flags=re.S | re.I)
    raw = re.sub(r"<style[^>]*>.*?</style>", " ", raw, flags=re.S | re.I)
    m = re.search(r"<main[^>]*>(.*?)</main>", raw, flags=re.S | re.I)
    body = m.group(1) if m else raw
    # keep heading markers
    body = re.sub(r"<h([1-6])[^>]*>", lambda m: "\n" + "#" * int(m.group(1)) + " ", body, flags=re.I)
    body = re.sub(r"</h[1-6]>", "\n", body, flags=re.I)
    body = re.sub(r"<li[^>]*>", "\n- ", body, flags=re.I)
    body = re.sub(r"</?(p|div|br|section|tr)[^>]*>", "\n", body, flags=re.I)
    # capture link targets for buttons/PDFs
    body = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>',
                  lambda m: f"{m.group(2)} [{m.group(1)}]", body, flags=re.S | re.I)
    body = re.sub(r"<[^>]+>", " ", body)
    body = html.unescape(body)
    body = re.sub(r"[ \t]+", " ", body)
    body = re.sub(r"\n\s*\n+", "\n\n", body)
    return body.strip()


for fname in sorted(os.listdir(PAGES)):
    if not fname.endswith(".html"):
        continue
    with open(os.path.join(PAGES, fname)) as f:
        raw = f.read()
    text = extract(raw)
    out = os.path.join(OUT, fname.replace(".html", ".md"))
    with open(out, "w") as f:
        f.write(text)
    print(f"{fname}: {len(text)} chars")
