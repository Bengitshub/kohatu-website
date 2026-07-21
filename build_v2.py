#!/usr/bin/env python3
"""Kohatu V2 site generator. Single source of truth: src/data/events.json + media.json.
Generates every route into kohatu-netlify-deploy/ (directory URLs). Run: python3 build_v2.py
"""
import json
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "kohatu-netlify-deploy")
DATA = json.load(open(os.path.join(ROOT, "src/data/events.json")))["events"]
MEDIA = json.load(open(os.path.join(ROOT, "src/data/media.json")))
IMG = MEDIA["images"]
EV = {e["id"]: e for e in DATA}

BASE_URL = "https://kohatu-demo.netlify.app"

STATUS = {
    "provisional":   ("Dates to be confirmed", "badge-soon",  "Get event updates"),
    "interest-open": ("Registering interest",  "badge-open",  "Register interest"),
    "entries-open":  ("Entries open",          "badge-open",  "Book your place"),
    "limited":       ("Final spaces",          "badge-open",  "Book final spaces"),
    "sold-out":      ("Sold out",              "badge-soon",  "View event"),
    "waitlist":      ("Waitlist",              "badge-soon",  "Join the waitlist"),
    "postponed":     ("Postponed",             "badge-soon",  "View event update"),
    "completed":     ("Completed",             "badge-done",  "View ride report"),
    "cancelled":     ("Cancelled",             "badge-soon",  "View cancellation notice"),
}
GRADE_VAR = {1: "--g1", 2: "--g2", 3: "--g3", 4: "--g4", 5: "--g5"}
CAT_LABEL = {"adventure": "Adventure ride", "festival": "Festival", "trail": "Trail ride", "emtb": "e-MTB"}


def img_tag(media_id, sizes, cls="", loading="lazy", fetchpriority=None):
    m = IMG[media_id]
    srcset = ", ".join(f"img/{m['base']}-{w}.webp {w}w" for w in m["widths"])
    biggest = f"img/{m['base']}-{max(m['widths'])}.webp"
    attrs = f'src="/{biggest}" srcset="{srcset}" sizes="{sizes}" width="{m["w"]}" height="{m["h"]}" alt="{m["alt"]}"'
    attrs = attrs.replace("img/", "/img/").replace("//img", "/img")
    if cls: attrs += f' class="{cls}"'
    if fetchpriority: attrs += f' fetchpriority="{fetchpriority}"'
    else: attrs += f' loading="{loading}"'
    if m.get("focal") and m["focal"] != "center": attrs += f' style="object-position:{m["focal"]}"'
    return f"<img {attrs}>"


def yt(vid, title, credit):
    return (f'<button class="yt-lite reveal" data-id="{vid}" data-title="{title}" '
            f'style="background-image:url(\'https://i.ytimg.com/vi/{vid}/hqdefault.jpg\')" '
            f'aria-label="Play video: {title}"><span class="play"></span></button>\n'
            f'<p class="film-credit">{title} — <b>{credit}</b></p>')


def next_event():
    ups = [e for e in DATA if e["status"] not in ("completed", "cancelled") and e.get("startDate")]
    return sorted(ups, key=lambda e: e["startDate"])[0]


def status_strip():
    e = next_event()
    label, _, _ = STATUS[e["status"]]
    return (f'<div class="status-strip"><div class="wrap"><span><b>Next event:</b> '
            f'<a href="/events/{e["id"]}/">{e["name"]}</a> — {e["dateLabel"]} · {label}</span>'
            f'<span class="ss-park">Kohatu Park: open days on the <a href="/kohatu-park/">park page</a></span></div></div>')


NAV = """<header class="nav" id="nav">
  <div class="wrap nav-inner">
    <a class="brand" href="/">
      <img src="/img/emblem-96.webp" alt="" width="44" height="43">
      <b>Kohatu<small>Motorcycle Centre</small></b>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Menu">&#9776;</button>
    <ul class="nav-links" id="nav-links">
      <li><a href="/events/">Rides</a></li>
      <li><a href="/kohatu-park/">Kohatu Park</a></li>
      <li><a href="/ride-grades/">Ride Grades</a></li>
      <li><a href="/stories/">Stories</a></li>
      <li><a href="/about/">About</a></li>
      <li><a href="/contact/">Contact</a></li>
      <li><a class="btn btn-red" href="/events/">Upcoming events</a></li>
    </ul>
  </div>
</header>"""

FOOTER = """<footer id="contact">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-logo">
        <img src="/img/logo-stacked-600.webp" alt="Kohatu Motorcycle Centre" width="150" height="163" loading="lazy">
      </div>
      <div>
        <h3>Talk to Dave</h3>
        <ul>
          <li><a href="tel:+64274486688">+64 27 448 6688</a></li>
          <li><a href="mailto:dave@kohatumc.co.nz">dave@kohatumc.co.nz</a></li>
          <li><a href="https://www.facebook.com/kohatumotorcyclecentre">Facebook</a></li>
          <li><a href="https://www.instagram.com/kohatumotorcyclecentre">Instagram</a></li>
        </ul>
      </div>
      <div>
        <h3>Rides</h3>
        <ul>
          <li><a href="/events/">All upcoming events</a></li>
          <li><a href="/events/adventure/">Adventure rides</a></li>
          <li><a href="/events/trail-rides/">Trail rides</a></li>
          <li><a href="/events/torque-and-trails/">Torque and Trails e-MTB</a></li>
          <li><a href="/events/past/">Past rides</a></li>
        </ul>
      </div>
      <div>
        <h3>Kohatu</h3>
        <ul>
          <li><a href="/kohatu-park/">The park</a></li>
          <li><a href="/location/">Location &amp; directions</a></li>
          <li><a href="/safety-support/">Safety &amp; support</a></li>
          <li><a href="/sponsors/">Sponsors</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-legal">
      <span>&copy; <span id="yr">2026</span> Kohatu Motorcycle Centre Ltd</span>
      <span><a href="/terms/">Terms</a> · <a href="/privacy/">Privacy</a> · Site concept by <a href="mailto:ben@webhero.au">Webhero</a></span>
    </div>
  </div>
</footer>"""

CONCEPT_BAR = ('<div id="concept-bar" role="note"><span><b>Concept preview</b> — event dates, routes, pricing and '
               'inclusions are subject to confirmation by Kohatu Motorcycle Centre.</span>'
               '<button id="concept-bar-close" aria-label="Dismiss notice">&times;</button></div>')

INTEREST_DIALOG = """<dialog class="book-demo" id="demo-form-ok">
  <h3>Thanks — you're on the preview list</h3>
  <p>This is a preview website, so nothing was stored. When the site goes live, this form joins the ride list and you'll hear the moment entries open.</p>
  <p>Want in right now? Email <a href="mailto:dave@kohatumc.co.nz" style="color:var(--red)">dave@kohatumc.co.nz</a> or call <a href="tel:+64274486688" style="color:var(--red)">+64 27 448 6688</a>.</p>
  <button class="btn btn-line" data-close>Close</button>
</dialog>"""


def page(path, title, desc, body, jsonld="", ogimg="img/hero-ford-1200.webp", noindex=False, strip=True):
    canonical = BASE_URL + path
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    strip_html = status_strip() if strip else ""
    html = f"""<!DOCTYPE html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0d0f0e">
<title>{title}</title>
<meta name="description" content="{desc}">
{robots}<link rel="canonical" href="{canonical}">
<link rel="icon" href="/favicon-48.png" type="image/png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/fonts/anton-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/barlowcondensed-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/styles.css">
<script>if ('IntersectionObserver' in window) document.documentElement.classList.add('js');</script>
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE_URL}/{ogimg}">
{jsonld}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{strip_html}
{NAV}
<main id="main">
{body}
</main>
{FOOTER}
{CONCEPT_BAR}
<script src="/site.js" defer></script>
</body>
</html>
"""
    full = os.path.join(OUT, path.lstrip("/"))
    if path.endswith("/"):
        os.makedirs(full, exist_ok=True)
        full = os.path.join(full, "index.html")
    with open(full, "w") as f:
        f.write(html)
    print("wrote", path)


def interest_form(ev_name):
    return f"""<div class="enquiry-panel" id="enquire">
  <span class="kicker">Register interest</span>
  <h2 style="font-size:clamp(1.9rem,4vw,2.6rem); margin-bottom:1.2rem">Hear first about {ev_name}</h2>
  <form class="js-demo-form form-grid" data-dialog="demo-form-ok" method="POST" action="#enquire">
    <div><label for="q-name">First name</label><input id="q-name" name="name" type="text" autocomplete="given-name" required></div>
    <div><label for="q-email">Email</label><input id="q-email" name="email" type="email" autocomplete="email" required></div>
    <div class="full"><button class="btn btn-red" type="submit">Register interest</button>
    <p class="form-note" style="margin-top:.7rem">Just enough to keep you posted — full rider details are collected when you enter. <a href="/privacy/" style="color:var(--red)">Privacy statement</a>.</p></div>
  </form>
</div>
{INTEREST_DIALOG}"""


def event_card(e, sizes="(max-width: 700px) 92vw, 400px"):
    label, badge_cls, cta = STATUS[e["status"]]
    grade_label = e.get("gradeLabel") or (f"Grade {e['grade']}" if e.get("grade") else "")
    gvar = GRADE_VAR.get(e.get("grade"), "--g1")
    price = e.get("priceLabel") or ""
    m = IMG[e["cardMedia"]]
    srcset = ", ".join(f"/img/{m['base']}-{w}.webp {w}w" for w in m["widths"])
    grade_badge = (f'<a class="badge" href="/ride-grades/"><span class="dot" style="background:var({gvar})"></span>{grade_label}</a>'
                   if grade_label else "")
    return f"""      <article class="event-card reveal" data-cat="{e['category']}" data-status="{'past' if e['status'] == 'completed' else 'upcoming'}">
        <div class="event-media">
          <img src="/img/{m['base']}-{max(m['widths'])}.webp" srcset="{srcset}" sizes="{sizes}" loading="lazy" width="{m['w']}" height="{m['h']}" alt="{m['alt']}">
          <div class="flags">
            <span class="badge {badge_cls}">{e['dateLabel'] if e['status'] != 'completed' else 'Completed · ' + e['dateLabel']}</span>
            {grade_badge}
          </div>
        </div>
        <div class="event-body">
          <span class="event-meta">{CAT_LABEL[e['category']]} · {e['duration']} · {e['region']}</span>
          <h3><a href="/events/{e['id']}/">{e['name']}</a></h3>
          <p>{e['summary']}</p>
          <div class="event-foot">
            <span class="price" style="font-size:1.15rem">{price}</span>
            <a class="btn btn-line" href="/events/{e['id']}/">{cta}</a>
          </div>
        </div>
      </article>"""


def event_jsonld(e):
    if e["status"] == "completed" or not e.get("startDate"):
        return ""
    offers = ""
    if e.get("price"):
        offers = (f',\n  "offers": {{ "@type": "Offer", "price": "{e["price"]}", "priceCurrency": "NZD", '
                  f'"availability": "https://schema.org/PreOrder", "url": "{BASE_URL}/events/{e["id"]}/" }}')
    m = IMG[e["heroMedia"]]
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "{e['name']}",
  "startDate": "{e['startDate']}",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {{ "@type": "Place", "name": "{e['region']}", "address": {{ "@type": "PostalAddress", "addressCountry": "NZ" }} }},
  "image": "{BASE_URL}/img/{m['base']}-{max(m['widths'])}.webp",
  "description": "{e['summary'].replace('"', "'")}",
  "organizer": {{ "@type": "Organization", "name": "Kohatu Motorcycle Centre", "email": "dave@kohatumc.co.nz", "telephone": "+64274486688" }}{offers}
}}
</script>
"""


def build_event_pages():
    for e in DATA:
        label, badge_cls, cta = STATUS[e["status"]]
        grade_label = e.get("gradeLabel") or (f"Grade {e['grade']}" if e.get("grade") else "")
        gvar = GRADE_VAR.get(e.get("grade"), "--g1")
        m = IMG[e["heroMedia"]]
        srcset = ", ".join(f"/img/{m['base']}-{w}.webp {w}w" for w in m["widths"])
        is_past = e["status"] == "completed"
        crumb_cat = {"adventure": ("Adventure rides", "/events/adventure/"),
                     "festival": ("Festivals", "/events/adventure/"),
                     "trail": ("Trail rides", "/events/trail-rides/"),
                     "emtb": ("All events", "/events/")}[e["category"]]
        grade_badge = (f'<a class="badge" href="/ride-grades/"><span class="dot" style="background:var({gvar})"></span>{grade_label}</a>'
                       if grade_label else "")

        # quick facts
        facts = []
        if e.get("duration"): facts.append((e["duration"], "Duration"))
        if e.get("distance"): facts.append((e["distance"], "Distance"))
        if grade_label: facts.append((grade_label, "Grade"))
        facts.append((e["region"], "Region"))
        facts.append((e["dateLabel"].split(" · ")[0], "Date" if not is_past else "Ran"))
        if e.get("priceLabel"): facts.append((e["priceLabel"].replace("NZ$", "NZ$"), "Entry"))
        facts_html = "\n".join(f'      <div class="stat"><b>{b}</b><span>{s}</span></div>' for b, s in facts[:6])

        body_html = ""
        for h, p in e.get("body", []):
            body_html += f"<h2>{h}</h2>\n<p>{p}</p>\n"

        itin = ""
        if e.get("itinerary"):
            itin = "<h2>Day by day</h2>\n"
            for i, (day, km, txt) in enumerate(e["itinerary"]):
                op = " open" if i == 0 else ""
                itin += f"<details{op}>\n  <summary>{day} · {km}</summary>\n  <div class=\"a\">{txt}</div>\n</details>\n"

        timeline = ""
        if e.get("timeline"):
            rows = "\n".join(f'  <div class="tl-row{" tl-now" if i == 0 else ""}"><b>{y}</b><span>{r}</span></div>'
                             for i, (y, r) in enumerate(e["timeline"]))
            timeline = f'<h2>The five-year route</h2>\n<div class="timeline reveal">\n{rows}\n</div>\n'

        films = ""
        if e.get("films"):
            films = "<h2>Watch the last one</h2>\n" + "\n<div style='margin-top:1.5rem'></div>\n".join(
                yt(v, t, c) for v, t, c in e["films"])

        faqs = ""
        if e.get("faqs"):
            faqs = "<h2>Good to know</h2>\n" + "\n".join(
                f"<details>\n  <summary>{q}</summary>\n  <div class=\"a\">{a}</div>\n</details>" for q, a in e["faqs"])

        inc = ""
        if e.get("included"):
            lis = "\n".join(f"          <li>{i}</li>" for i in e["included"])
            inc = f'<ul class="inc">\n{lis}\n        </ul>'
        bring = ""
        if e.get("bring"):
            lis = "\n".join(f"<li>{i}</li>" for i in e["bring"])
            bring = f"<h2>What to bring</h2>\n<ul>{lis}</ul>\n"

        # side panel + CTA behaviour by status
        if is_past:
            panel_cta = '<a class="btn btn-line" href="/events/" style="display:block; text-align:center">See upcoming rides</a>'
            panel_kicker = "Ride report"
        else:
            panel_cta = '<a class="btn btn-red" href="#enquire" style="display:block; text-align:center">' + cta + '</a>'
            panel_kicker = e["dateLabel"]
        price_big = e.get("priceLabel") or "Details to come"
        panel = f"""      <aside class="book-panel reveal" aria-label="{e['name']} summary">
        <span class="kicker">{panel_kicker}</span>
        <span class="price" style="font-size:1.6rem">{price_big}</span>
        {inc}
        <div style="margin-top:1.2rem">{panel_cta}</div>
        <p class="alt">Questions? <a href="mailto:dave@kohatumc.co.nz">Email Dave</a></p>
      </aside>"""

        # related: two others, same category first, upcoming preferred
        others = [x for x in DATA if x["id"] != e["id"] and x["status"] != "completed"]
        others.sort(key=lambda x: (x["category"] != e["category"],))
        related = "\n".join(event_card(x) for x in others[:2])

        form = "" if is_past else interest_form(e["name"])
        sticky = "" if is_past else (f'<div class="sticky-cta"><span>{e["name"]} · {e["dateLabel"].split(" · ")[0]}</span>'
                                     f'<a class="btn btn-red" href="#enquire">{cta}</a></div>')
        provisional = ('<p class="prov-note">Event details shown are drawn from Kohatu\'s current published material and are subject to confirmation.</p>'
                       if e.get("requiresOwnerConfirmation") else "")

        body = f"""<section class="detail-hero" aria-label="{e['name']}">
  <div class="hero-bg">
    <img src="/img/{m['base']}-{max(m['widths'])}.webp" srcset="{srcset}" sizes="100vw" fetchpriority="high" width="{m['w']}" height="{m['h']}" alt="{m['alt']}">
  </div>
  <div class="wrap">
    <p class="crumb"><a href="/events/">Rides</a> / <a href="{crumb_cat[1]}">{crumb_cat[0]}</a></p>
    <h1>{e['name']}</h1>
    <div class="detail-flags">
      <span class="badge {badge_cls}">{label} · {e['dateLabel']}</span>
      {grade_badge}
    </div>
  </div>
</section>
<section style="padding-top:2.5rem">
  <div class="wrap">
    <div class="stat-grid reveal">
{facts_html}
    </div>
    <div class="detail-layout">
      <div class="detail-main">
        {body_html}
        {timeline}
        {itin}
        {bring}
        {films}
        {faqs}
        {provisional}
      </div>
{panel}
    </div>
{form}
    <h2 style="font-size:clamp(1.9rem,4vw,2.6rem); margin:3.5rem 0 1.4rem">More rides</h2>
    <div class="event-grid">
{related}
    </div>
  </div>
</section>
{sticky}"""
        title = f"{e['name']} | Kohatu Motorcycle Centre"
        page(f"/events/{e['id']}/", title, e["summary"][:155], body,
             jsonld=event_jsonld(e), ogimg=f"img/{m['base']}-{max(m['widths'])}.webp")


def listing_page(path, title_h1, kicker, intro, events, desc, filters=False):
    cards = "\n".join(event_card(x) for x in events)
    filter_html = ""
    if filters:
        filter_html = """    <div class="filters" role="group" aria-label="Filter rides">
      <button class="chip" aria-pressed="true" data-filter="all">All</button>
      <button class="chip" aria-pressed="false" data-filter="adventure">Adventure</button>
      <button class="chip" aria-pressed="false" data-filter="festival">Festivals</button>
      <button class="chip" aria-pressed="false" data-filter="trail">Trail rides</button>
      <button class="chip" aria-pressed="false" data-filter="emtb">e-MTB</button>
    </div>"""
    body = f"""<section class="page-hero">
  <div class="wrap">
    <span class="kicker">{kicker}</span>
    <h1>{title_h1}</h1>
    <p>{intro}</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
{filter_html}
    <div class="event-grid">
{cards}
    </div>
  </div>
</section>"""
    page(path, f"{kicker} | Kohatu Motorcycle Centre" if kicker != "Rides & events" else "Rides & Events | Kohatu Motorcycle Centre",
         desc, body)


def build_listings():
    upcoming = [e for e in DATA if e["status"] not in ("completed", "cancelled")]
    upcoming.sort(key=lambda e: e.get("startDate") or "9999")
    past = [e for e in DATA if e["status"] == "completed"]
    past.sort(key=lambda e: e["startDate"], reverse=True)

    listing_page("/events/", "Every ride on the calendar", "Rides & events",
                 'Adventure rides, festivals, trail rides and e-MTB racing — every event shows its status, grade and price. Not sure what suits? <a href="/ride-grades/" style="color:var(--red)">Check how grading works</a> or <a href="/events/past/" style="color:var(--red)">browse past rides</a>.',
                 upcoming, "Every upcoming Kohatu event — adventure rides, festivals, trail rides and Torque and Trails e-MTB racing, with status, grade and price.", filters=True)

    listing_page("/events/adventure/", "Adventure motorcycle rides", "Road-legal ADV bikes",
                 "One-day blasts, multi-day station rides and festivals for road-registered adventure bikes — private land access, GPX routes, sweeps and support on every ride.",
                 [e for e in upcoming if e["category"] in ("adventure", "festival")],
                 "Adventure motorcycle events for road-registered ADV bikes — multi-day station rides, festivals and one-day rides across the Top of the South.")

    trail_upcoming = [e for e in upcoming if e["category"] == "trail"]
    trail_cards = trail_upcoming + [e for e in past if e["category"] == "trail"]
    listing_page("/events/trail-rides/", "Trail rides — no rego needed", "Trail & enduro bikes",
                 "Summer trail rides for non-road-registered trail and enduro bikes: a main loop for competent off-road riders, optional technical sections for the hungry, and marshals, recovery and first aid on site all day. Pre-entry is essential — numbers are limited. New rounds are announced through the <a href=\"/contact/\" style=\"color:var(--red)\">ride list</a>.",
                 trail_cards,
                 "Kohatu trail rides for non-road-registered trail and enduro bikes — main loops, optional technical sections, marshals, recovery and first aid. $80, pre-entry essential.")

    listing_page("/events/past/", "Past rides", "The archive",
                 "Completed rides stay on the record — routes, prices and stories from the seasons gone. Want the next one? <a href=\"/events/\" style=\"color:var(--red)\">See what's coming up</a>.",
                 past, "Completed Kohatu rides — the archive of past adventure rides, trail rides and events.")


def build_homepage():
    upcoming = [e for e in DATA if e["status"] not in ("completed", "cancelled")]
    upcoming.sort(key=lambda e: e.get("startDate") or "9999")
    top3 = "\n".join(event_card(e) for e in upcoming[:3])
    fyp = EV["five-year-plan"]
    tl_rows = "\n".join(f'      <div class="tl-row{" tl-now" if i == 0 else ""}"><b>{y}</b><span>{r}</span></div>'
                        for i, (y, r) in enumerate(fyp["timeline"]))

    grades = [("1", "--g1", "Gravel cruiser", "Any road-legal bike · formed gravel"),
              ("2", "--g2", "Backroad explorer", "ADV bikes · farm two-track"),
              ("3", "--g3", "Station rider", "Hill-country stations · river crossings"),
              ("4", "--g4", "Single-track hunter", "Trail & enduro · technical terrain"),
              ("5", "--g5", "The hard yards", "Expert only · challenge sections")]
    grade_scale = "\n".join(
        f'      <a class="gs-item reveal" href="/ride-grades/"><span class="grade-num" style="background:var({v})">{n}</span><b>{t}</b><span>{d}</span></a>'
        for n, v, t, d in grades)

    body = f"""<!-- HERO -->
<section class="hero" aria-label="Kohatu Motorcycle Centre">
  <div class="hero-bg">
    <img src="/img/hero-ford-1920.webp" srcset="/img/hero-ford-480.webp 480w, /img/hero-ford-800.webp 800w, /img/hero-ford-1200.webp 1200w, /img/hero-ford-1920.webp 1920w" sizes="100vw" fetchpriority="high" width="1920" height="1081" alt="Adventure riders splashing through a ford on a remote backcountry gravel road" style="object-position:62% 60%">
  </div>
  <div class="wrap">
    <span class="kicker">Nelson Tasman · Top of the South · New Zealand</span>
    <h1>Ride the backcountry<br> <em>most riders never see</em></h1>
    <p class="hero-sub">Supported motorcycle, trail-bike and e-MTB events across private farms, high-country stations, forestry and remote New Zealand back roads.</p>
    <div class="hero-ctas">
      <a class="btn btn-red" href="/events/">View upcoming events</a>
      <a class="btn btn-ghost" href="#pathways">Find your ride type</a>
    </div>
  </div>
</section>

<div class="trust" role="presentation">
  <div class="wrap">
    <ul>
      <li>Private land access</li>
      <li>GPX navigation</li>
      <li>Sweep &amp; support crews</li>
      <li>Multi-day luggage support</li>
      <li>Community fundraising</li>
    </ul>
  </div>
</div>

<!-- PATHWAYS -->
<section id="pathways">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Choose your way in</span>
      <h2>Which rider are you?</h2>
    </div>
    <div class="pathway-grid">
      <a class="pathway reveal" href="/events/adventure/">
        {img_tag("clarence-river-group", "(max-width:700px) 92vw, 45vw")}
        <div class="pw-body"><h3>Adventure motorcycle rides</h3><p>Road-legal ADV bikes — one-day, multi-day and festival events</p></div>
      </a>
      <a class="pathway reveal" href="/events/trail-rides/">
        {img_tag("trail-rider-park", "(max-width:700px) 92vw, 45vw")}
        <div class="pw-body"><h3>Trail rides</h3><p>Trail &amp; enduro bikes without rego — main loops and optional technical sections</p></div>
      </a>
      <a class="pathway reveal" href="/kohatu-park/">
        {img_tag("park-aerial", "(max-width:700px) 92vw, 45vw")}
        <div class="pw-body"><h3>Kohatu Park</h3><p>Open days, practice and private group sessions — adventure, enduro and kids' riding</p></div>
      </a>
      <a class="pathway reveal" href="/events/torque-and-trails/">
        {img_tag("young-rider", "(max-width:700px) 92vw, 45vw")}
        <div class="pw-body"><h3>Torque and Trails</h3><p>Kohatu's e-MTB event series at the park — next round to be confirmed</p></div>
      </a>
    </div>
  </div>
</section>

<!-- NEXT EVENTS -->
<section class="why cut-l" id="rides">
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">What's next</span>
      <h2>The next three on the calendar</h2>
    </div>
    <div class="event-grid">
{top3}
    </div>
    <p style="margin-top:2rem"><a class="btn btn-ghost" href="/events/">View the full event calendar &rarr;</a></p>
  </div>
</section>

<!-- SIGNATURE -->
<section>
  <div class="pattern-bg" aria-hidden="true"><img src="/img/pattern.webp" alt=""></div>
  <div class="wrap split">
    <div>
      <span class="kicker">The flagship</span>
      <h2>The Five Year Plan</h2>
      <p style="color:var(--muted); margin-top:.9rem">{fyp['summary']}</p>
      <div class="timeline" style="margin:1.6rem 0">
{tl_rows}
      </div>
      <p><a class="btn btn-red" href="/events/five-year-plan/">The full plan &rarr;</a></p>
    </div>
    <div class="split-media reveal">
      {img_tag("five-year-plan", "(max-width: 860px) 92vw, 45vw")}
    </div>
  </div>
</section>

<!-- WHY -->
<section class="why cut-r">
  <div class="wrap">
    <div class="why-grid">
      <div class="why-item reveal"><h3>Access riders can't get alone</h3><p>Stations, farms and forestry blocks closed to the public — negotiated ride by ride with local landowners.</p></div>
      <div class="why-item reveal"><h3>Scouted GPX routes</h3><p>Every route scouted and supplied as a GPX download before the ride. Load it, follow it, focus on riding.</p></div>
      <div class="why-item reveal"><h3>Sweeps, marshals &amp; first aid</h3><p>Sweep riders on multi-days, marshals and first aid on trail rides. Nobody gets left in a creek bed.</p></div>
      <div class="why-item reveal"><h3>Money back into the districts</h3><p>Festival entries have funded Nelson Tasman Search &amp; Rescue; ride entries support community halls, local groups and farm-track upkeep.</p></div>
    </div>
  </div>
</section>

<!-- GRADES PREVIEW -->
<section>
  <div class="wrap">
    <div class="section-head">
      <span class="kicker">Know before you go</span>
      <h2>The Kohatu grading system</h2>
      <p>Every ride carries a grade so you can pick terrain that matches your skills and your bike.</p>
    </div>
    <div class="grade-scale">
{grade_scale}
    </div>
    <p style="margin-top:1.6rem"><a class="btn btn-ghost" href="/ride-grades/">Check your ride grade &rarr;</a></p>
  </div>
</section>

<!-- PROOF -->
<section class="why cut-l">
  <div class="wrap split" style="align-items:center">
    <div>
      {yt("r0OEHg4zxCg", "Nelson Tasman Motorcycle Festival 2025 — full film", "Blake Jones")}
    </div>
    <div>
      <span class="kicker">Proof from the trail</span>
      <h2>A real event, on film</h2>
      <p style="color:var(--muted); margin-top:.9rem">Shot at the 2025 Nelson Tasman Motorcycle Festival — what a delivered Kohatu weekend actually looks like, from the start line to Founders Heritage Park.</p>
      <p style="margin-top:1.2rem"><a class="btn btn-ghost" href="/films/">All films &rarr;</a></p>
    </div>
  </div>
</section>

<!-- DAVE -->
<section>
  <div class="wrap split">
    <div class="split-media reveal">
      {img_tag("training-conversation", "(max-width: 860px) 92vw, 45vw")}
    </div>
    <div>
      <span class="kicker">Who's behind it</span>
      <h2>Built by riders, run by riders</h2>
      <p style="color:var(--muted); margin-top:.9rem">Kohatu Motorcycle Centre is Dave's project: a leased block at Kohatu Park, built up with volunteer help into a training ground — in his own words, a place to train for our sport and become safer, more capable riders (but mostly for fun). The events grew from there: local landowners opened their gates, the rides got longer, and now the calendar runs from one-day blasts to a five-year ride down the length of the country.</p>
      <p style="margin-top:1.4rem"><a class="btn btn-ghost" href="/about/">More about Kohatu &rarr;</a></p>
    </div>
  </div>
</section>

<!-- PARK STRIP -->
<section class="why cut-r">
  <div class="wrap split">
    <div>
      <span class="kicker">Kohatu Park · Spooners Range</span>
      <h2>The adventure training ground</h2>
      <p style="color:var(--muted); margin-top:.9rem">5.5&nbsp;km of purpose-built adventure-bike single track, a kids' riding area, and private sessions for groups of six or more. Open days 11am–4pm — cash only at the gate.</p>
      <div style="display:flex; gap:.8rem; flex-wrap:wrap; margin-top:1.4rem">
        <a class="btn btn-red" href="/kohatu-park/">Park info &amp; open days</a>
        <a class="btn btn-ghost" href="/location/">Directions</a>
      </div>
    </div>
    <div class="split-media reveal">
      {img_tag("park-aerial", "(max-width: 860px) 92vw, 45vw")}
    </div>
  </div>
</section>

<!-- RIDE ALERTS -->
<section class="capture" id="ride-list">
  <div class="wrap capture-inner">
    <div>
      <span class="kicker">Don't miss a ride</span>
      <h2>Entries open. Spots go. Be first.</h2>
      <p style="color:var(--muted); margin-top:.9rem">Join the ride list and get an email the moment entries open. No spam, ever. Just rides.</p>
    </div>
    <form class="js-demo-form" data-dialog="demo-form-ok" method="POST" action="#ride-list">
      <div>
        <label for="f-name">First name</label>
        <input id="f-name" name="name" type="text" autocomplete="given-name" required>
      </div>
      <div>
        <label for="f-email">Email</label>
        <input id="f-email" name="email" type="email" autocomplete="email" required>
      </div>
      <div>
        <label for="f-ride">Which rides are you keen on?</label>
        <select id="f-ride" name="ride">
          <option>All rides</option>
          <option>Adventure rides</option>
          <option>Festivals</option>
          <option>Trail rides (no rego)</option>
          <option>Torque and Trails e-MTB</option>
          <option>Kohatu Park open days</option>
        </select>
      </div>
      <button class="btn btn-red" type="submit">Join the ride list</button>
      <p class="form-note">We only email about rides and entries. Unsubscribe anytime · <a href="/privacy/" style="color:var(--red)">privacy statement</a>.</p>
    </form>
  </div>
</section>
{INTEREST_DIALOG}"""
    page("/", "Kohatu Motorcycle Centre — Adventure, Trail & e-MTB Events, Nelson Tasman NZ",
         "Supported motorcycle, trail-bike and e-MTB events across private farms, high-country stations and remote NZ back roads — plus the Kohatu Park training ground.",
         body)


def simple(path, kicker, h1, intro, inner, desc, noindex=False, ogimg="img/hero-ford-1200.webp"):
    body = f"""<section class="page-hero">
  <div class="wrap">
    <span class="kicker">{kicker}</span>
    <h1>{h1}</h1>
    <p>{intro}</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
{inner}
  </div>
</section>"""
    page(path, f"{h1} | Kohatu Motorcycle Centre", desc, body, noindex=noindex, ogimg=ogimg)


def build_aux():
    # ---- ride grades ----
    rows = [("1", "--g1", "Gravel cruiser", "Any road-legal bike · new to off-road", "Formed gravel roads and easy station driveways. If you can ride confidently on loose metal, you're in."),
            ("2", "--g2", "Backroad explorer", "Adventure bikes · some off-road experience", "Farm two-track, paddock riding and shallow water splashes. Standing on the pegs should feel natural."),
            ("3", "--g3", "Station rider", "Most Kohatu adventure rides live here", "Full days over hill-country stations: rutted climbs, river crossings, mud when it rains and the odd tricky descent. Adventure-oriented off-road tyres and a good attitude required."),
            ("4", "--g4", "Single-track hunter", "Trail & enduro bikes · fit and experienced", "Technical single track, steep forest climbs and rock gardens. Optional loops on many rides let you earn your bragging rights."),
            ("5", "--g5", "The hard yards", "Expert only · by invitation on selected rides", "Challenge sections that will test bike, body and sense of humour. Walk it first. Then decide.")]
    inner = '<div class="grade-list">\n' + "\n".join(
        f'''      <div class="grade-row reveal">
        <span class="grade-num" style="background:var({v})">{n}</span>
        <div><h3>{t} <span>{sub}</span></h3><p>{d}</p></div>
      </div>''' for n, v, t, sub, d in rows) + "\n    </div>"
    simple("/ride-grades/", "Know before you go", "The Kohatu grading system",
           "Every ride carries a grade so you can pick terrain that matches your skills and your bike. Be honest with yourself — overestimating is how good days go bad.",
           inner, "Kohatu's five-grade system for adventure and trail rides — pick terrain that matches your skills and your bike.")

    # ---- safety & support ----
    inner = """<div class="detail-main" style="max-width:52rem">
      <h2>What runs behind every ride</h2>
      <ul>
        <li><b>Scouted routes</b> — every route is ridden and checked before the event, and supplied as a GPX download.</li>
        <li><b>Sweep riders</b> — multi-day rides run with sweep riders so nobody is left behind.</li>
        <li><b>Marshals, recovery and first aid</b> — trail rides run with marshals, recovery and first-aid support on site.</li>
        <li><b>Sign-on and briefing</b> — every event starts with registration and a riders' briefing; trail rides sign riders out at the finish.</li>
        <li><b>Luggage support</b> — a support vehicle carries overnight gear on multi-day rides.</li>
        <li><b>Route changes</b> — rides cross live rivers and working farms; sections can change on the day when conditions demand it.</li>
      </ul>
      <h2>The honest limits</h2>
      <p>These are remote-country events. Cellphone coverage is patchy to non-existent on parts of every route, help can be hours away, and river crossings depend on weather. Support crews manage risk — they can't remove it. Riders are responsible for a roadworthy bike, honest self-grading, and riding to the conditions.</p>
      <h2>Get ready properly</h2>
      <p>Start with the <a href="/ride-grades/" style="color:var(--red)">grading system</a>, check each event's what-to-bring list, and make sure your bike has the fuel range the event page states. If you're unsure whether a ride suits you, <a href="mailto:dave@kohatumc.co.nz" style="color:var(--red)">ask Dave</a> — an honest answer beats a hard day.</p>
    </div>"""
    simple("/safety-support/", "How rides are run", "Safety &amp; support",
           "What stands behind a Kohatu event — and the honest limits of support in remote country.",
           inner, "How Kohatu events are supported: scouted GPX routes, sweep riders, marshals and first aid — and the honest limits of remote-country riding.")

    # ---- films ----
    films = "\n<div style='margin-top:2rem'></div>\n".join(yt(v["id"], v["title"], v["credit"]) for v in MEDIA["videos"])
    simple("/films/", "Stories", "The films",
           "Real Kohatu events on film — credited to the riders who shot them.",
           f'<div style="max-width:56rem">{films}</div>',
           "Films from Kohatu Motorcycle Centre events, by Blake Jones and RideLifeNZ.")

    # ---- gallery ----
    tiles = ["mud-rider", "young-rider", "tractor-river-crossing", "farm-gate-rider", "gallery-street",
             "trail-rider-park", "gallery-lineup", "sounds-jetty", "gallery-riverbank", "gallery-lake",
             "gallery-penstock", "sounds-landscape"]
    gal = "\n".join(f'      <a href="https://www.facebook.com/kohatumotorcyclecentre" aria-label="See more photos on Facebook">{img_tag(t, "(max-width:700px) 46vw, 320px")}</a>' for t in tiles)
    simple("/gallery/", "Straight from the rides", "Where the action happens",
           "No stock photos — every shot is from our rides, our park, our riders.",
           f'<div class="gal">\n{gal}\n    </div>\n    <p style="margin-top:1.5rem"><a class="btn btn-ghost" href="https://www.facebook.com/kohatumotorcyclecentre">More on Facebook &rarr;</a></p>',
           "Photos from Kohatu rides and the park — real riders, no stock.")

    # ---- stories hub ----
    past = [e for e in DATA if e["status"] == "completed"]
    past.sort(key=lambda e: e["startDate"], reverse=True)
    cards = "\n".join(event_card(e) for e in past[:3])
    inner = f"""<div class="split" style="margin-bottom:3rem">
      <a class="pathway reveal" href="/films/">{img_tag("festival-aerial", "(max-width:700px) 92vw, 45vw")}<div class="pw-body"><h3>The films</h3><p>Festival and park films by Blake Jones and RideLifeNZ</p></div></a>
      <a class="pathway reveal" href="/gallery/">{img_tag("mud-rider", "(max-width:700px) 92vw, 45vw")}<div class="pw-body"><h3>The photos</h3><p>Straight from the rides — no stock</p></div></a>
    </div>
    <h2 style="font-size:clamp(1.9rem,4vw,2.6rem); margin-bottom:1.4rem">Recent ride reports</h2>
    <div class="event-grid">
{cards}
    </div>
    <p style="margin-top:1.6rem"><a class="btn btn-ghost" href="/events/past/">The full archive &rarr;</a></p>"""
    simple("/stories/", "Proof from the trail", "Stories",
           "Films, photos and ride reports from delivered Kohatu events.",
           inner, "Kohatu ride stories — films, photos and reports from delivered events.")

    # ---- kohatu park ----
    inner = f"""<div class="split" style="margin-bottom:3rem">
      <div>
        <div class="price-cards">
          <div class="price-card"><b>$30</b><span>Adults</span></div>
          <div class="price-card"><b>$10</b><span>Under 15</span></div>
          <div class="price-card"><b>$40</b><span>Family pass</span></div>
        </div>
        <p style="color:var(--muted)">Open days 11am–4pm — check <a href="https://www.facebook.com/kohatumotorcyclecentre" style="color:var(--red)">Facebook</a> for dates, or <a href="mailto:dave@kohatumc.co.nz" style="color:var(--red)">email Dave</a> before you come. Cash only at the gate. Groups of 6+ can book the park any day for training or private events.</p>
        <p style="color:var(--muted); margin-top:.8rem">On arrival your bike gets checked and you'll sign a liability form — then ride as many laps as you like. Adventure and enduro bikes, plus a children's fun area for kids' bikes and quads (under-12s with an adult).</p>
        <p style="margin-top:1.4rem"><a class="btn btn-red" href="/location/">Directions to the park</a></p>
      </div>
      <div class="split-media reveal">{img_tag("park-aerial", "(max-width: 860px) 92vw, 45vw")}</div>
    </div>
    <h2 style="font-size:clamp(1.9rem,4vw,2.6rem); margin-bottom:1rem">Before you turn up</h2>
    <details><summary>What do I need to do before arriving?</summary><div class="a">Email <a href="mailto:dave@kohatumc.co.nz">dave@kohatumc.co.nz</a> to let us know you're coming — we'll only be in touch if there's an unforeseen closure. Questions? Call Dave on <a href="tel:+64274486688">+64 27 448 6688</a>.</div></details>
    <details><summary>What do I need to bring?</summary><div class="a">A road-legal bike with current registration, WoF and insurance (kids' bikes excepted), cash for the gate fee, and your own food and water — there are no facilities on site yet. There's no cellphone coverage, so download the directions before you leave.</div></details>
    <details><summary>Can I rent a motorbike?</summary><div class="a">Not yet — it's a service we hope to offer. It is the ideal place to test ride an adventure bike you're looking to buy.</div></details>
    <details><summary>Can I book the park for a private event or training day?</summary><div class="a">Yes — we're happy to open any day for groups of six or more. <a href="mailto:dave@kohatumc.co.nz">Email Dave</a> and we'll do our best to accommodate your crew.</div></details>"""
    simple("/kohatu-park/", "Kohatu Park · Spooners Range", "The adventure training ground",
           "5.5 km of purpose-built adventure-bike single track loaded with training features and challenges, right beside the Nelson Car Club gravel track — plus a kids' area for young riders finding their feet.",
           inner, "Kohatu Park training ground: 5.5 km of adventure-bike single track, kids' area, open days 11am–4pm, $30/$10/$40, private group bookings.",
           ogimg="img/park-aerial-1200.webp")

    # ---- location ----
    inner = f"""<div class="split">
      <div class="detail-main">
        <h2>Finding the park</h2>
        <p>The only entrance to Kohatu Motorcycle Centre is via <b>Olivers Road</b>, off the Motueka Valley Highway — approximately 1.1&nbsp;km from the Kohatu Flat Rock Cafe and 6.6&nbsp;km from Tapawera.</p>
        <ul>
          <li>Turn onto Olivers Road from the Motueka Valley Highway</li>
          <li>Keep left and follow the road to Kohatu Park</li>
          <li>Through the Kohatu Park gate to Stanley Brook Road</li>
          <li>Continue north past the Nelson Car Club to Kohatu Motorcycle Centre</li>
        </ul>
        <p>The gravel road is a strict <b>50&nbsp;km/h shared zone</b> — respect all forestry signage and leave gates as you find them. There is <b>no cellphone coverage</b> at the park: save or print these directions before you leave.</p>
        <p style="margin-top:1.2rem"><a class="btn btn-red" href="https://www.google.com/maps/search/?api=1&query=Kohatu+Park+Spooners+Range+Tasman">Open in Google Maps</a></p>
      </div>
      <div class="split-media reveal">{img_tag("park-aerial", "(max-width: 860px) 92vw, 45vw")}</div>
    </div>"""
    simple("/location/", "Getting here", "Location &amp; directions",
           "Kohatu Park, Spooners Range — via Olivers Road off the Motueka Valley Highway.",
           inner, "Directions to Kohatu Motorcycle Centre at Kohatu Park, Spooners Range — via Olivers Road, 1.1 km from the Kohatu Flat Rock Cafe.")

    # ---- about ----
    inner = f"""<div class="split">
      <div class="split-media reveal">{img_tag("training-conversation", "(max-width: 860px) 92vw, 45vw")}</div>
      <div class="detail-main">
        <h2>Built by riders, run by riders</h2>
        <p>Kohatu Motorcycle Centre is Dave's project: a leased block at Kohatu Park, built up with volunteer help into a training ground — in his own words, a place to train for our sport and become safer, more capable riders. But mostly for fun.</p>
        <p>The events grew from there: local landowners opened their gates, the rides got longer, and now the calendar runs from one-day blasts and no-rego trail rides to festivals, e-MTB racing and a five-year ride down the length of the country. Every ride is scouted, supported, and finished with a story worth telling — and entries put money back into Search &amp; Rescue, community halls and the farms we cross.</p>
        <p>Want to talk rides, the park, or an idea for an event? <a href="mailto:dave@kohatumc.co.nz" style="color:var(--red)">Email Dave</a> or call <a href="tel:+64274486688" style="color:var(--red)">+64 27 448 6688</a>.</p>
      </div>
    </div>"""
    simple("/about/", "Who's behind it", "About Kohatu",
           "The rider, the park, and how the events grew.",
           inner, "About Kohatu Motorcycle Centre — the rider behind it, the Kohatu Park training ground, and how the events grew.")

    # ---- sponsors ----
    inner = """<div class="detail-main" style="max-width:52rem">
      <h2>Our sponsors</h2>
      <p>Kohatu Park's development is backed by local business. <b>Stuart Drummond Transport</b> is a Bronze sponsor of the park — and local businesses like <b>Tasman Honda</b> have been part of past Kohatu events, alongside the stations and farms that open their gates.</p>
      <h2>Sponsor the park</h2>
      <p>Park sponsorship runs in Bronze, Silver and Gold tiers — including naming rights opportunities as the park grows. Event sponsorship (festivals, trail rides and the e-MTB series) puts your name in front of the Top of the South's riding community. <a href="mailto:dave@kohatumc.co.nz?subject=Sponsorship" style="color:var(--red)">Talk to Dave about sponsoring</a>.</p>
    </div>"""
    simple("/sponsors/", "Partners", "Sponsors",
           "The businesses, stations and farms that make Kohatu events possible.",
           inner, "Sponsor a Kohatu event — festivals, trail rides and e-MTB racing across the Top of the South.")

    # ---- contact ----
    inner = """<div class="split">
      <div class="detail-main">
        <h2>Talk to Dave</h2>
        <ul>
          <li>Phone: <a href="tel:+64274486688" style="color:var(--red)">+64 27 448 6688</a></li>
          <li>Email: <a href="mailto:dave@kohatumc.co.nz" style="color:var(--red)">dave@kohatumc.co.nz</a></li>
          <li><a href="https://www.facebook.com/kohatumotorcyclecentre" style="color:var(--red)">Facebook</a> · <a href="https://www.instagram.com/kohatumotorcyclecentre" style="color:var(--red)">Instagram</a></li>
          <li><a href="/location/" style="color:var(--red)">Location &amp; directions</a></li>
        </ul>
        <p>For event entries, use the register-interest form on each event page — or go straight to the source and email Dave.</p>
      </div>
      <div class="enquiry-panel" style="margin-top:0">
        <span class="kicker">Ride alerts</span>
        <h2 style="font-size:1.6rem; margin-bottom:1rem">Join the ride list</h2>
        <form class="js-demo-form form-grid" data-dialog="demo-form-ok" method="POST" action="/contact/">
          <div><label for="c-name">First name</label><input id="c-name" name="name" type="text" autocomplete="given-name" required></div>
          <div><label for="c-email">Email</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
          <div class="full"><button class="btn btn-red" type="submit">Join the ride list</button>
          <p class="form-note" style="margin-top:.7rem">We only email about rides and entries · <a href="/privacy/" style="color:var(--red)">privacy statement</a>.</p></div>
        </form>
      </div>
    </div>
""" + INTEREST_DIALOG
    simple("/contact/", "Get in touch", "Contact",
           "Dave answers the phone, the email and the gate.",
           inner, "Contact Kohatu Motorcycle Centre — Dave, +64 27 448 6688, dave@kohatumc.co.nz.")

    # ---- privacy ----
    inner = """<div class="detail-main" style="max-width:46rem">
      <p class="prov-note">Draft for review — to be confirmed by Kohatu Motorcycle Centre before launch.</p>
      <h2>What we collect and why</h2>
      <p>When you join the ride list we collect your name, email address and which rides interest you — so we can email you when entries open. When you enter an event we also collect your phone number, emergency contact details and information about your bike — so we can run the event safely and reach someone who cares about you if something goes wrong.</p>
      <h2>Where it goes</h2>
      <p>Your information is held by Kohatu Motorcycle Centre Ltd and the service providers that run our website and entries: our website host, our mailing-list provider, and our ticketing/booking provider when you pay for an event online. We don't sell your information or share it with anyone else, except where the law requires.</p>
      <h2>Your choices</h2>
      <p>Every email we send has an unsubscribe link. You can ask to see, correct or delete the personal information we hold about you at any time under the Privacy Act 2020 — contact <a href="mailto:dave@kohatumc.co.nz" style="color:var(--red)">dave@kohatumc.co.nz</a> or call <a href="tel:+64274486688" style="color:var(--red)">+64 27 448 6688</a>.</p>
    </div>"""
    simple("/privacy/", "The fine print", "Privacy statement",
           "What we collect when you join the ride list or enter an event, where it goes, and your rights.",
           inner, "Kohatu Motorcycle Centre privacy statement — what's collected, where it goes, and your rights under the NZ Privacy Act 2020.")

    # ---- terms ----
    inner = """<div class="detail-main" style="max-width:46rem">
      <p class="prov-note">Draft carried over from the current site. Full participant terms — including cancellation and refund rights — will be prepared and legally reviewed before online entries open.</p>
      <h2>Refund policy</h2>
      <p>Every effort is made to run each event as planned, but circumstances beyond our control — a storm, natural disaster or pandemic — may force us to alter or postpone all or part of an event. In the very unlikely case an event is cancelled outright by the organisers, any refund made will be at the discretion of the organisers.</p>
      <p>A participant may be given a refund, less a <b>$40 administration fee</b>, if they cannot attend the event for medical or similar reasons, up to <b>14 days prior</b> to the event. There are no refunds within 14 days of any event unless a replacement participant is confirmed.</p>
      <h2>Force majeure</h2>
      <p>Under no circumstances shall Kohatu Motorcycle Centre Limited be held liable for any delay or failure in performance resulting directly or indirectly from acts of nature, forces or causes beyond its reasonable control, including without limitation: fires, floods, storms, explosions, acts of God, war, governmental actions, pandemics, or non-performance by third parties.</p>
    </div>"""
    simple("/terms/", "The fine print", "Terms &amp; refunds",
           "Refund policy and terms for Kohatu Motorcycle Centre events.",
           inner, "Refund policy and terms for Kohatu Motorcycle Centre events.")


def build_proposal():
    inner = """<div class="detail-main" style="max-width:52rem">
      <h2>What you're looking at</h2>
      <p>Everything on this preview — every page, photo, film and event — was rebuilt from your existing website and public material. Dates, prices and inclusions are your own published figures, marked provisional until you confirm them; anything proposed new (the grading system, the e-MTB page framing, event statuses) is flagged for your sign-off.</p>
      <h2>What's already built</h2>
      <ul>
        <li>Mobile-first design in your brand, with your photography and Blake's films</li>
        <li>Every offering on its own page: adventure rides, festivals, trail rides, Torque and Trails e-MTB, the park</li>
        <li>One event system — every card, page and Google listing reads from a single event record, so a date changes once and updates everywhere</li>
        <li>Honest event statuses (provisional / entries open / sold out / completed) with matching buttons</li>
        <li>A past-rides archive so delivered events keep selling the next ones</li>
        <li>Ride grading (1–5) so riders self-qualify instead of phoning</li>
        <li>Redirects mapped from every current kohatumc.co.nz URL — old Facebook links keep working</li>
        <li>Fast static hosting, Google event listings, privacy statement, accessibility basics</li>
      </ul>
      <h2>What it fixes</h2>
      <ul>
        <li>Every event on your current site shows a past date — this one can't drift, because events live in one place</li>
        <li>Deep in the Sounds is on Facebook but not your website — here, the next ride is the first thing visitors see</li>
        <li>Riders currently must ring or email to enter — this is built to plug straight into online entries (Humanitix: NZ-based, no monthly fee, card fees passable to the rider, capacity and waitlists automatic)</li>
        <li>e-MTB and park information were buried or missing — both are now first-class pages</li>
      </ul>
      <h2>What you'd confirm before launch</h2>
      <p>Dates, prices, inclusions, capacities, the grading names, the Five Year Plan pack, mountain-bike series details, photo permissions, and the legal pages (terms need a proper participant agreement — worth a legal review before taking money online).</p>
      <h2>The offer</h2>
      <p>The build you're looking at, finished and launched on kohatumc.co.nz: <b>project price on the call</b>. Ongoing updates (dates, statuses, new events) as a simple monthly care plan, or set up so you can edit events yourself.</p>
      <p style="margin-top:1.6rem">
        <a class="btn btn-red" href="mailto:ben@webhero.au?subject=Kohatu%20website">Email Ben</a>
        <a class="btn btn-ghost" href="/" style="margin-left:.6rem">Back to the site</a>
      </p>
      <p class="form-note" style="margin-top:1.2rem">Webhero · ben@webhero.au · This page is private — it isn't linked from the site or visible to search engines.</p>
    </div>"""
    simple("/proposal/", "For Dave", "A working replacement for kohatumc.co.nz",
           "The site around this page is a live preview built on spec by Webhero — this page is the commercial side.",
           inner, "Private proposal page.", noindex=True)


def write_redirects():
    r = """# 301 map: current kohatumc.co.nz URLs -> V2 routes (live on this preview, carries to launch)
/adventure-motorcycle-events                                    /events/adventure/               301
/adventure-motorcycle-events/the-clarence                       /events/the-clarence/            301
/adventure-motorcycle-events/the-five-year-plan-jMPFu           /events/five-year-plan/          301
/adventure-motorcycle-events/sounds-like                        /events/sounds-like/             301
/adventure-motorcycle-events/nelson-tasman-motorcycle-festival  /events/nelson-tasman-motorcycle-festival/ 301
/adventure-motorcycle-events/wellingtonmotorcyclefestival       /events/wellington-motorcycle-festival/    301
/adventure-motorcycle-events/anything-mechanical                /events/anything-mechanical/     301
/adventure-motorcycle-events/lake-matiri-with-a-tractor         /events/lake-matiri/             301
/adventure-motorcycle-events/raineyriverroad                    /events/rainey-river-lakes-station/ 301
/adventure-motorcycle-events/tempello                           /events/tempello/                301
/adventure-motorcycle-events/tba                                /events/                         301
/adventure-motorcycle-events/category/*                         /events/                         301
/mountain-bike-events                                           /events/torque-and-trails/       301
/trail-rides                                                    /events/trail-rides/             301
/park                                                           /kohatu-park/                    301
/location                                                       /location/                       200
/gallery                                                        /gallery/                        200
/terms-conditions                                               /terms/                          301
/home                                                           /                                301
/home-2                                                         /                                301
/nelson-tasman-motorcycle-events                                /events/nelson-tasman-motorcycle-festival/ 301

# V1 flat demo URLs -> V2 routes
/rides.html                     /events/                                   301
/five-year-plan.html            /events/five-year-plan/                    301
/the-clarence.html              /events/the-clarence/                      301
/sounds-like.html               /events/sounds-like/                       301
/nelson-tasman-festival.html    /events/nelson-tasman-motorcycle-festival/ 301
/wellington-festival.html       /events/wellington-motorcycle-festival/    301
/summer-series.html             /events/past/                              301
/trail-rides.html               /events/trail-rides/                       301
/park.html                      /kohatu-park/                              301
/gallery.html                   /gallery/                                  301
/privacy.html                   /privacy/                                  301
/terms.html                     /terms/                                    301
"""
    with open(os.path.join(OUT, "_redirects"), "w") as f:
        f.write(r)
    print("wrote _redirects")


def build_404():
    body = """<main style="min-height:100vh; display:grid; place-items:center; text-align:center; padding:2rem">
  <div>
    <img src="/img/emblem-320.webp" alt="" width="140" height="137" style="margin:0 auto 1.5rem; opacity:.9">
    <span class="kicker" style="justify-content:center">404 — wrong turn</span>
    <h1 style="font-size:clamp(2.1rem,5vw,3.1rem); max-width:16ch; margin:0 auto">Even with a GPX file, everyone misses a waypoint sometimes</h1>
    <p style="color:var(--muted); margin:1rem 0 1.8rem">The page you're after isn't here. Backtrack to the start and pick up the route.</p>
    <a class="btn btn-red" href="/">Back to the rides</a>
  </div>
</main>"""
    html = f"""<!DOCTYPE html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0d0f0e">
<title>Wrong turn | Kohatu Motorcycle Centre</title>
<link rel="icon" href="/favicon-48.png" type="image/png">
<link rel="stylesheet" href="/styles.css">
</head>
<body>
{body}
</body>
</html>
"""
    with open(os.path.join(OUT, "404.html"), "w") as f:
        f.write(html)
    print("wrote /404.html")


def prune_v1():
    for f in ["rides.html", "five-year-plan.html", "the-clarence.html", "sounds-like.html",
              "nelson-tasman-festival.html", "wellington-festival.html", "summer-series.html",
              "trail-rides.html", "park.html", "gallery.html", "privacy.html", "terms.html"]:
        p = os.path.join(OUT, f)
        if os.path.exists(p):
            os.remove(p)
            print("pruned", f)


if __name__ == "__main__":
    build_event_pages()
    build_listings()
    build_homepage()
    build_aux()
    build_proposal()
    write_redirects()
    build_404()
    prune_v1()
    print("V2 build complete")
