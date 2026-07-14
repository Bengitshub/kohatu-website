#!/usr/bin/env python3
"""Deploy kohatu-demo-deploy.zip to Netlify.

Usage: NETLIFY_TOKEN=... python3 deploy.py
Creates the site if needed (tries the preferred names in order), then zip-deploys.
"""
import json
import os
import sys
import urllib.request
import urllib.error

TOKEN = os.environ.get("NETLIFY_TOKEN")
if not TOKEN:
    sys.exit("Set NETLIFY_TOKEN")

API = "https://api.netlify.com/api/v1"
HDR = {"Authorization": f"Bearer {TOKEN}"}
NAMES = ["kohatu-demo", "kohatu-mc-demo", "kohatumc-demo"]
ROOT = os.path.dirname(os.path.abspath(__file__))
ZIP = os.path.join(ROOT, "kohatu-demo-deploy.zip")


def req(method, path, data=None, ctype="application/json"):
    body = data if isinstance(data, (bytes, type(None))) else json.dumps(data).encode()
    r = urllib.request.Request(API + path, data=body, method=method,
                               headers={**HDR, "Content-Type": ctype})
    with urllib.request.urlopen(r, timeout=120) as resp:
        return json.loads(resp.read())


# find or create the site
site = None
for s in req("GET", "/sites?per_page=100"):
    if s["name"] in NAMES:
        site = s
        break
if site is None:
    for name in NAMES:
        try:
            site = req("POST", "/sites", {"name": name})
            break
        except urllib.error.HTTPError as e:
            if e.code == 422:
                print(f"name {name} taken, trying next")
                continue
            raise
if site is None:
    sys.exit("all preferred site names taken — pick another in NAMES")

print("site:", site["name"], site["id"])

with open(ZIP, "rb") as f:
    deploy = req("POST", f"/sites/{site['id']}/deploys", f.read(), "application/zip")

print("deployed:", deploy.get("state"))
print("URL: https://%s.netlify.app" % site["name"])
