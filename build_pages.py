#!/usr/bin/env python3
"""Generate the inner pages of the Kohatu demo from shared templates + content dicts.
Facts come from source-content/ (Dave's own site). Run: python3 build_pages.py
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kohatu-netlify-deploy")

NAV = """<header class="nav scrolled" id="nav">
  <div class="wrap nav-inner">
    <a class="brand" href="./">
      <img src="img/emblem-96.webp" alt="" width="44" height="43">
      <b>Kohatu<small>Motorcycle Centre</small></b>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Menu">&#9776;</button>
    <ul class="nav-links" id="nav-links">
      <li><a href="rides.html">Rides &amp; Events</a></li>
      <li><a href="index.html#grades">Grades</a></li>
      <li><a href="trail-rides.html">Trail Rides</a></li>
      <li><a href="park.html">The Park</a></li>
      <li><a href="gallery.html">Gallery</a></li>
      <li><a href="#contact">Contact</a></li>
      <li><a class="btn btn-red" href="rides.html">Book a ride</a></li>
    </ul>
  </div>
</header>"""

FOOTER = """<footer id="contact">
  <div class="wrap">
    <div class="foot-grid">
      <div class="foot-logo">
        <img src="img/logo-stacked-600.webp" alt="Kohatu Motorcycle Centre" width="150" height="163" loading="lazy">
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
        <h3>Find us</h3>
        <ul>
          <li>Kohatu Park, Spooners Range</li>
          <li>Via Olivers Road, off Motueka Valley Highway</li>
          <li>1.1 km from Kohatu Flat Rock Cafe</li>
        </ul>
      </div>
      <div>
        <h3>Rides</h3>
        <ul>
          <li><a href="rides.html">Upcoming events</a></li>
          <li><a href="trail-rides.html">Trail rides</a></li>
          <li><a href="park.html">The park</a></li>
          <li><a href="index.html#ride-list">Join the ride list</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-legal">
      <span>&copy; <span id="yr">2026</span> Kohatu Motorcycle Centre Ltd</span>
      <span><a href="terms.html">Terms &amp; refunds</a> · <a href="privacy.html">Privacy</a> · Site concept by <a href="mailto:ben@webhero.au">Webhero</a></span>
    </div>
  </div>
</footer>"""

CONCEPT_BAR = """<div id="concept-bar" role="note"><span><b>Concept preview by Webhero</b> — event dates, routes, pricing and inclusions are subject to confirmation by Kohatu Motorcycle Centre.</span><button id="concept-bar-close" aria-label="Dismiss notice">&times;</button></div>"""

ENQUIRY = """<div class="enquiry-panel" id="enquire">
  <span class="kicker">Register interest</span>
  <h2 style="font-size:clamp(1.9rem,4vw,2.6rem); margin-bottom:1.2rem">Get on the list for {name}</h2>
  <form class="js-demo-form form-grid" data-dialog="enquiry-demo" method="POST" action="#enquire">
    <div><label for="q-name">Name</label><input id="q-name" name="name" type="text" autocomplete="name" required></div>
    <div><label for="q-email">Email</label><input id="q-email" name="email" type="email" autocomplete="email" required></div>
    <div><label for="q-phone">Phone</label><input id="q-phone" name="phone" type="tel" autocomplete="tel" required></div>
    <div><label for="q-ename">Emergency contact name</label><input id="q-ename" name="emergency-name" type="text" required></div>
    <div><label for="q-ephone">Emergency contact phone</label><input id="q-ephone" name="emergency-phone" type="tel" required></div>
    <div><label for="q-msg">Your bike / anything we should know</label><input id="q-msg" name="message" type="text"></div>
    <div class="full"><button class="btn btn-red" type="submit">Register interest</button>
    <p class="form-note" style="margin-top:.7rem">Same details Dave collects today — see our <a href="privacy.html" style="color:var(--red)">privacy statement</a>.</p></div>
  </form>
</div>

<dialog class="book-demo" id="enquiry-demo">
  <h3>On the live site, this goes straight onto the entry list</h3>
  <p>Rider details, emergency contact and bike info land in one tidy list — no email back-and-forth. With online payment connected (Humanitix), the entry fee is settled at the same time and capacity counts down automatically.</p>
  <p>This is a demo — nothing was stored.</p>
  <button class="btn btn-line" data-close>Close</button>
</dialog>"""

BOOK_DIALOG = """<dialog class="book-demo" id="book-demo">
  <h3>This is where riders book &amp; pay online</h3>
  <p>On the live site this button opens a secure embedded checkout (Humanitix) right here on the page: card payment, rider details, emergency contact, bike and licence info — all captured automatically.</p>
  <p>Capacity is tracked in real time, sold-out rides flip to a wait-list, and every entry lands in one tidy list. No spreadsheets, no phone tag.</p>
  <button class="btn btn-line" data-close>Close</button>
</dialog>"""


def page(fname, title, desc, body, jsonld="", ogimg="img/hero-ford-1200.webp"):
    html = f"""<!DOCTYPE html>
<html lang="en-NZ">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="theme-color" content="#0d0f0e">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="favicon-48.png" type="image/png">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="fonts/anton-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/barlowcondensed-700.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="styles.css">
<script>if ('IntersectionObserver' in window) document.documentElement.classList.add('js');</script>
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://kohatu-demo.netlify.app/{fname}">
<meta property="og:image" content="https://kohatu-demo.netlify.app/{ogimg}">
{jsonld}</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
{NAV}
<main id="main">
{body}
</main>
{FOOTER}
{CONCEPT_BAR}
<script src="site.js" defer></script>
</body>
</html>
"""
    with open(os.path.join(OUT, fname), "w") as f:
        f.write(html)
    print("wrote", fname)


def event_jsonld(name, month, place, locality, price, desc, img, url):
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "{name}",
  "startDate": "{month}",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
  "location": {{ "@type": "Place", "name": "{place}", "address": {{ "@type": "PostalAddress", "addressLocality": "{locality}", "addressCountry": "NZ" }} }},
  "image": "{img}",
  "description": "{desc}",
  "organizer": {{ "@type": "Organization", "name": "Kohatu Motorcycle Centre", "email": "dave@kohatumc.co.nz", "telephone": "+64274486688" }},
  "offers": {{ "@type": "Offer", "price": "{price}", "priceCurrency": "NZD", "availability": "https://schema.org/PreOrder", "url": "{url}" }}
}}
</script>
"""


def detail_hero(img_base, alt, crumb_label, h1, badge, grade_label, grade_var, srcs=(480, 800, 1200)):
    srcset = ", ".join(f"img/{img_base}-{w}.webp {w}w" for w in srcs)
    biggest = f"img/{img_base}-{max(srcs)}.webp"
    return f"""<section class="detail-hero" aria-label="{h1}">
  <div class="hero-bg">
    <img src="{biggest}" srcset="{srcset}" sizes="100vw" fetchpriority="high" alt="{alt}">
  </div>
  <div class="wrap">
    <p class="crumb"><a href="rides.html">Rides &amp; events</a> / {crumb_label}</p>
    <h1>{h1}</h1>
    <div class="detail-flags">
      <span class="badge badge-soon">{badge}</span>
      <a class="badge" href="index.html#grades"><span class="dot" style="background:var({grade_var})"></span>{grade_label}</a>
    </div>
  </div>
</section>"""


def stat_grid(stats):
    cells = "\n".join(f'      <div class="stat"><b>{b}</b><span>{s}</span></div>' for b, s in stats)
    return f'    <div class="stat-grid reveal">\n{cells}\n    </div>'


def book_panel(kicker, price, price_small, inc, cta):
    lis = "\n".join(f"          <li>{i}</li>" for i in inc)
    return f"""      <aside class="book-panel reveal" id="book" aria-label="Book this ride">
        <span class="kicker">{kicker}</span>
        <span class="price">{price}<small>{price_small}</small></span>
        <ul class="inc">
{lis}
        </ul>
        {cta}
        <p class="alt">Entries limited · or <a href="mailto:dave@kohatumc.co.nz">email Dave</a></p>
      </aside>"""


def yt(vid, title, credit):
    return f"""<button class="yt-lite reveal" data-id="{vid}" data-title="{title}" style="background-image:url('https://i.ytimg.com/vi/{vid}/hqdefault.jpg')" aria-label="Play video: {title}"><span class="play"></span></button>
      <p class="film-credit">{title} — <b>{credit}</b></p>"""


# ================= five-year-plan.html =================
body = detail_hero("five-year-plan", "Loaded adventure bike in a paddock pointing toward rugged Marlborough hills",
                   "Multi-day", "The Five Year Plan", "Year 1 · August 2026 · Northland", "Grade 3 — Station rider", "--g3") + f"""
<section style="padding-top:2.5rem">
  <div class="wrap">
{stat_grid([("6 days", "Riding per year"), ("5 years", "Cape Reinga to Stewart Is."), ("Grade 3", "Station rider"), ("2026–2030", "One leg each year"), ("Rest days", "Between ride weeks"), ("$2,990", "Per year")])}
    <div class="detail-layout">
      <div class="detail-main">
        <h2>The plan</h2>
        <p>Starting at Cape Reinga, we're setting out on a five-year journey to ride the length of New Zealand — off-road tracks, private land and scenic public trails, with rest days between weeks of riding to recharge.</p>
        <ul>
          <li><b>Year 1 (2026)</b> — Cape Reinga &amp; Northland</li>
          <li><b>Year 2 (2027)</b> — Central North Island</li>
          <li><b>Year 3 (2028)</b> — Lower North Island</li>
          <li><b>Year 4 (2029)</b> — Upper South Island</li>
          <li><b>Year 5 (2030)</b> — Lower South Island, <b>prize giving on Stewart Island</b></li>
        </ul>
        <p>Join for a single year's leg, or challenge yourself and ride the whole length — each year starts from Cape Reinga, so in year five you can choose one week in the deep south or five weeks top to bottom. The final-year prize giving on Stewart Island celebrates every rider who completed the adventure.</p>
        <h2>Good to know</h2>
        <p>Full details live in the <a href="https://static1.squarespace.com/static/64ed33960283396d7b9277b9/t/68f8403e988f12045adafa2d/1761099838983/event-5yearplan.pdf" style="color:var(--red)">event info pack (PDF)</a>. Grade 3 riding — see <a href="index.html#grades" style="color:var(--red)">how grading works</a>.</p>
      </div>
{book_panel("Year 1 · August 2026", "$2,990", "per year", [
    "6 nights' accommodation", "Dinner on 6 evenings", "GPS route downloads",
    "Two sweep riders", "All land access fees", "Luggage van for your gear", "Rest days built in"],
    '<a class="btn btn-red" href="#enquire" style="display:block; text-align:center">Register interest</a>')}
    </div>
{ENQUIRY.format(name="The Five Year Plan")}
  </div>
</section>"""
page("five-year-plan.html", "The Five Year Plan — Ride the Length of NZ | Kohatu Motorcycle Centre",
     "Six days a year for five years: Cape Reinga to Stewart Island over NZ's off-road tracks and private land. $2,990 per year with accommodation, dinners, GPX routes, sweeps and luggage van.",
     body, event_jsonld("The Five Year Plan — Year 1: Northland", "2026-08", "Cape Reinga, Northland", "Northland", "2990",
                        "Year one of a five-year journey riding the length of New Zealand. Six days of riding from Cape Reinga through Northland.",
                        "img/five-year-plan-1200.webp", "five-year-plan.html"), "img/five-year-plan-1200.webp")

# ================= sounds-like.html =================
body = detail_hero("gallery-jetty", "Rider's view from a jetty over the water with snow-capped ranges beyond",
                   "Two-day", "Sounds Like", "February 2027 · Dates announced soon", "Grade 3 — Station rider", "--g3", srcs=(480, 800)) + f"""
<section style="padding-top:2.5rem">
  <div class="wrap">
{stat_grid([("2 days", "Riding"), ("Grade 3", "Station rider"), ("3 farms", "Outer Sounds private land"), ("1 night", "French Pass hall"), ("Fundraiser", "For the local community"), ("$295", "All up")])}
    <div class="detail-layout">
      <div class="detail-main">
        <h2>The ride</h2>
        <p>Two full days on private farm tracks and gravel in and around Marlborough's Admiralty Bay and French Pass. The off-road runs across three large outer-Sounds farms including <b>Te Kuta</b> and <b>Port Ligar</b> — country you can't reach any other way, with the Sounds below you most of the day.</p>
        <p>We overnight at the <b>French Pass hall</b>, and the event fundraises to support the community that hosts us — dinner and breakfast are put on by the locals.</p>
        <h2>What to bring</h2>
        <ul>
          <li>A road-registered, warranted and insured adventure bike</li>
          <li>Full riding gear — helmet, boots, gloves, body protection</li>
          <li>A mattress and sleeping bag — they travel in the support vehicle</li>
          <li>Your GPS loaded with the supplied GPX route</li>
        </ul>
        <h2>Good to know</h2>
        <p>GPX files are provided before the ride, and a luggage and support vehicle carries your overnight gear. Grade 3 riding — see <a href="index.html#grades" style="color:var(--red)">how grading works</a>.</p>
      </div>
{book_panel("February 2027", "$295", "per rider", [
    "French Pass hall accommodation", "Dinner &amp; breakfast", "GPX route files", "Luggage &amp; support vehicle"],
    '<a class="btn btn-red" href="#enquire" style="display:block; text-align:center">Register interest</a>')}
    </div>
{ENQUIRY.format(name="Sounds Like")}
  </div>
</section>"""
page("sounds-like.html", "Sounds Like — French Pass &amp; the Outer Sounds 2-Day Ride | Kohatu Motorcycle Centre",
     "Two days across three big outer-Sounds farms including Te Kuta and Port Ligar, overnighting at the French Pass hall. $295 with meals and support vehicle.",
     body, event_jsonld("Sounds Like — French Pass and the Outer Sounds", "2027-02", "French Pass, Marlborough Sounds", "Marlborough", "295",
                        "Two days on private farm tracks and gravel across three large outer-Sounds farms, overnighting at the French Pass hall.",
                        "img/gallery-jetty-800.webp", "sounds-like.html"), "img/gallery-jetty-800.webp")

# ================= nelson-tasman-festival.html =================
body = detail_hero("festival", "Drone view of an event basecamp in a forested valley, riders waving beside their bikes",
                   "Festival", "Nelson Tasman Motorcycle Festival", "May 2027 · Dates announced soon", "All riders welcome", "--g1") + f"""
<section style="padding-top:2.5rem">
  <div class="wrap">
{stat_grid([("2 days", "Adventure riding"), ("1 day", "Road treasure hunt"), ("All bikes", "Every class welcome"), ("Founders", "Festival finish, Nelson"), ("Fundraiser", "NT Search &amp; Rescue"), ("$45–$350", "Road / adventure")])}
    <div class="detail-layout">
      <div class="detail-main">
        <h2>The festival</h2>
        <p>The Top of the South's motorcycle weekend. Adventure bikes ride private-land courses on both days; road bikes of every class join a Saturday <b>treasure hunt</b> around Nelson Tasman. Then everyone rolls into <b>Founders Heritage Park</b> together to celebrate all things motorcycle — static displays, vendors and food trucks, open to the public.</p>
        <p>The festival raises funds for <b>Nelson Tasman Search &amp; Rescue</b> — the crew who come and get us when a ride goes properly wrong.</p>
        <h2>Watch the last one</h2>
        {yt("r0OEHg4zxCg", "Nelson Tasman Motorcycle Festival 2025 — full film", "Blake Jones")}
        <div style="margin-top:1.5rem"></div>
        {yt("7Odz8i9qgms", "Festival 2025 — the Nelson ADV ride", "Blake Jones")}
      </div>
{book_panel("May 2027", "$350", "adventure entry · road $45", [
    "2 days of adventure courses", "Road treasure hunt entry", "Founders festival finish",
    "Supporting NT Search &amp; Rescue"],
    '<a class="btn btn-red" href="#enquire" style="display:block; text-align:center">Register interest</a>')}
    </div>
{ENQUIRY.format(name="the Nelson Tasman Motorcycle Festival")}
  </div>
</section>"""
page("nelson-tasman-festival.html", "Nelson Tasman Motorcycle Festival | Kohatu Motorcycle Centre",
     "Adventure rides, a road-bike treasure hunt and a festival finish at Founders Heritage Park — raising funds for Nelson Tasman Search & Rescue. Adventure $350, road $45.",
     body, event_jsonld("Nelson Tasman Motorcycle Festival", "2027-05", "Founders Heritage Park, Nelson", "Nelson", "45",
                        "Adventure rides and a road-bike treasure hunt finishing at Founders Heritage Park, raising funds for Nelson Tasman Search and Rescue.",
                        "img/festival-1200.webp", "nelson-tasman-festival.html"), "img/festival-1200.webp")

# ================= wellington-festival.html =================
body = detail_hero("wellington2", "Adventure and dirt bikes parked in a forest clearing during a ride stop",
                   "Festival", "Wellington Motorcycle Festival", "May 2027 · Dates announced soon", "All riders welcome", "--g1") + f"""
<section style="padding-top:2.5rem">
  <div class="wrap">
{stat_grid([("2 days", "Riding"), ("All bikes", "Every class welcome"), ("Poker run", "Trentham &amp; Masterton"), ("Brewtown", "Festival finish"), ("Private land", "Not normally rideable"), ("$45–$350", "Road / adventure")])}
    <div class="detail-layout">
      <div class="detail-main">
        <h2>The festival</h2>
        <p>An event for all classes and types of motorcycle. Adventure courses run over two days across council parks, forestry and private land not normally open to riders.</p>
        <p>Saturday's <b>poker run</b> starts in Trentham and Masterton and ends at <b>Brewtown</b> — seven locations, collect a playing card at each, discard two, and present your best poker hand for prizes. On Saturday evening all riders gather at the Brewtown greenspace for static displays from clubs and vendors while the brews and food trucks keep everyone fed and watered.</p>
      </div>
{book_panel("May 2027", "$350", "adventure entry · road $45", [
    "2 days of adventure courses", "Poker run entry", "Brewtown festival evening"],
    '<a class="btn btn-red" href="#enquire" style="display:block; text-align:center">Register interest</a>')}
    </div>
{ENQUIRY.format(name="the Wellington Motorcycle Festival")}
  </div>
</section>"""
page("wellington-festival.html", "Wellington Motorcycle Festival | Kohatu Motorcycle Centre",
     "Adventure courses over council parks, forestry and private land, plus a Saturday poker run from Trentham and Masterton to Brewtown. Adventure $350, road $45.",
     body, event_jsonld("Wellington Motorcycle Festival", "2027-05", "Brewtown, Upper Hutt", "Upper Hutt", "45",
                        "Adventure courses over council parks, forestry and private land, plus a Saturday poker run ending at Brewtown.",
                        "img/wellington2-1200.webp", "wellington-festival.html"), "img/wellington2-1200.webp")

# ================= summer-series.html =================
body = detail_hero("summer-series", "Dozens of dirt bikes and riders parked in a forest clearing above a river gorge",
                   "One-day rides", "Summer Ride Series", "October – May · New season announced soon", "Grade 3–4", "--g4") + f"""
<section style="padding-top:2.5rem">
  <div class="wrap">
{stat_grid([("~Monthly", "Through summer"), ("1 day", "Per ride"), ("Grade 3–4", "With optional loops"), ("GPX", "Issued before each ride"), ("Sweeps + medic", "On every ride"), ("$100–$130", "Per ride")])}
    <div class="detail-layout">
      <div class="detail-main">
        <h2>How the series works</h2>
        <p>Roughly once a month through the riding season, we open a route you can't normally touch — private farms, station tracks and back roads negotiated with local landowners. GPX files are issued before each ride, sweep riders and medical support run on every one, and part of many entries goes straight back to the farms for track upkeep.</p>
        <p>Dates and routes are announced through the season — <a href="index.html#ride-list" style="color:var(--red)">join the ride list</a> and you'll hear the moment entries open. Rides regularly sell out.</p>
        <h2>Recent rides from the series</h2>
        <details>
          <summary>Lake Matiri — with a tractor · $120</summary>
          <div class="a">A 237&nbsp;km day out of Murchison with a genuine party trick: bikes towed across the river by tractor to reach the Matiri Valley. Sold out.</div>
        </details>
        <details>
          <summary>Anything Mechanical · $110</summary>
          <div class="a">Registration at Nelson Motorcycles, farm tracks through Matt Dicks' and Ian Parkes' farms, a climb to the Inwoods Lookout at around 1,000&nbsp;m, then three hours exploring 55&nbsp;km of tracks at the Anything Mechanical farm. Sign-out at the Sprig &amp; Fern, Brightwater. $20 of every entry went to farm track maintenance.</div>
        </details>
        <details>
          <summary>Rainey River Road &amp; Lakes Station · $130</summary>
          <div class="a">Station country in the Nelson Lakes region, with an optional Rainbow Ski Field leg. Part of the entry supported local fundraising.</div>
        </details>
        <details>
          <summary>Tempello · $130</summary>
          <div class="a">Marlborough station riding with lunch at Mt Altimarloch — views over the Awatere on a good day.</div>
        </details>
      </div>
{book_panel("2026–27 season", "From $100", "per rider, per ride", [
    "GPX route before every ride", "Sweep riders &amp; medical support", "Private land access",
    "Entries support farm upkeep"],
    '<a class="btn btn-red" href="#enquire" style="display:block; text-align:center">Get ride alerts</a>')}
    </div>
{ENQUIRY.format(name="the Summer Ride Series")}
  </div>
</section>"""
page("summer-series.html", "Summer Ride Series — One-Day Adventure Rides | Kohatu Motorcycle Centre",
     "Roughly monthly one-day rides over private farms and station tracks across the Top of the South. GPX supplied, sweeps and medical on every ride. From $100.",
     body, "", "img/summer-series-1200.webp")

# ================= trail-rides.html =================
body = detail_hero("trail-rides", "Rider catching air on a red Honda over a grass mound",
                   "Trail rides", "Trail Rides", "Summer series · Dates announced soon", "Grade 3–4 · No rego needed", "--g4", srcs=(480, 800)) + f"""
<section style="padding-top:2.5rem">
  <div class="wrap">
{stat_grid([("1 day", "Per ride"), ("No rego", "Trail &amp; enduro bikes"), ("$80", "Per rider"), ("Marshals", "Recovery &amp; first aid"), ("Main loop", "+ optional technical"), ("Pre-entry", "Essential — limited spots")])}
    <div class="detail-layout">
      <div class="detail-main">
        <h2>Real trail terrain, no rego required</h2>
        <p>Working with Nelson Tasman landowners, we run summer trail rides for <b>non-road-registered trail and enduro bikes</b> — forest tracks, open climbs, river crossings and views across the Nelson Lakes region, on land that's open for one day only.</p>
        <ul>
          <li><b>Main loop</b> — ideal for competent off-road riders</li>
          <li><b>Optional sections</b> — more technical tracks for those who want a challenge</li>
          <li><b>Support crew</b> — marshals, recovery and first aid on site all day</li>
        </ul>
        <h2>What to bring</h2>
        <ul>
          <li>Off-road motorcycle in good condition</li>
          <li>Full riding gear — helmet, boots, gloves, body protection</li>
          <li>Extra fuel, water and basic tools</li>
          <li>A positive attitude and sense of adventure</li>
        </ul>
        <h2>The last round</h2>
        <details>
          <summary>Round 1 — Anything Mechanical · Korere Tophouse Road, St Arnaud</summary>
          <div class="a">Sign-on from 7:30am, riders' briefing 8:15, start 8:30, finish 3pm. A full day through private farmland, forest and back-country trails near the top of the South. Round up your mates and make a weekend of it — St Arnaud has plenty of places to stay.</div>
        </details>
      </div>
{book_panel("Next round", "$80", "per rider", [
    "Marshals, recovery &amp; first aid", "Main loop + optional technical sections",
    "Event info &amp; directions after entry"],
    '<a class="btn btn-red" href="#enquire" style="display:block; text-align:center">Register interest</a>')}
    </div>
{ENQUIRY.format(name="the next trail ride")}
  </div>
</section>"""
page("trail-rides.html", "Trail Rides — No Rego Needed | Kohatu Motorcycle Centre",
     "Summer trail rides for non-road-registered trail and enduro bikes near St Arnaud — forest tracks, open climbs and river crossings with marshals, recovery and first aid. $80, pre-entry essential.",
     body, "", "img/trail-rides-800.webp")

# ================= park.html =================
body = f"""<section class="page-hero">
  <div class="wrap">
    <span class="kicker">Kohatu Park · Spooners Range</span>
    <h1>The adventure training ground</h1>
    <p>5.5&nbsp;km of purpose-built adventure-bike single track loaded with training features and challenges, right beside the Nelson Car Club gravel track — plus a kids' area for young riders finding their feet. Built by riders, for riders, on 11 hectares of Kohatu Park.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="split" style="margin-bottom:3rem">
      <div>
        <div class="price-cards">
          <div class="price-card"><b>$30</b><span>Adults</span></div>
          <div class="price-card"><b>$10</b><span>Under 15</span></div>
          <div class="price-card"><b>$40</b><span>Family pass</span></div>
        </div>
        <p style="color:var(--muted)">Open days 11am–4pm — check <a href="https://www.facebook.com/kohatumotorcyclecentre" style="color:var(--red)">Facebook</a> for dates, or <a href="mailto:dave@kohatumc.co.nz" style="color:var(--red)">email Dave</a> before you come. Cash only at the gate. Groups of 6+ can book the park any day for training or private events.</p>
        <h3 style="margin:1.8rem 0 .6rem">Finding the park</h3>
        <p style="color:var(--muted)">Turn onto <b style="color:var(--text)">Olivers Road</b> from the Motueka Valley Highway — 1.1&nbsp;km from the Kohatu Flat Rock Cafe, 6.6&nbsp;km from Tapawera. Keep left to Kohatu Park, through the gate to Stanley Brook Road, then north past the Nelson Car Club. The gravel road is a strict 50&nbsp;km/h shared zone; leave gates as you find them. No cellphone coverage — download directions before you leave.</p>
      </div>
      <div class="split-media reveal">
        <img src="img/park-aerial-800.webp" srcset="img/park-aerial-480.webp 480w, img/park-aerial-800.webp 800w, img/park-aerial-1200.webp 1200w" sizes="(max-width: 860px) 92vw, 45vw" loading="lazy" width="800" height="450" alt="Aerial view of the Kohatu training ground with mowed trail loops beside pine forest">
      </div>
    </div>

    <h2 style="font-size:clamp(1.9rem,4vw,2.6rem); margin-bottom:1rem">Park FAQs</h2>
    <details>
      <summary>What is the park for?</summary>
      <div class="a">With 5.5&nbsp;km of track and numerous features, it's fun to ride — and a place to train so we're all safer, more capable riders. But mostly for fun.</div>
    </details>
    <details>
      <summary>What do I need to do before arriving?</summary>
      <div class="a">Email <a href="mailto:dave@kohatumc.co.nz">dave@kohatumc.co.nz</a> to let us know you're coming — we'll only be in touch if there's an unforeseen closure. Questions? Call Dave on <a href="tel:+64274486688">+64 27 448 6688</a>.</div>
    </details>
    <details>
      <summary>What do I need to bring?</summary>
      <div class="a">A roadworthy, warranted and insured bike (kids' bikes excepted), cash for the gate fee, and your own food and water — there are no facilities on site yet. On arrival your bike gets checked and you'll sign a liability form, then ride as many laps as you like.</div>
    </details>
    <details>
      <summary>Which bikes does the park cater for?</summary>
      <div class="a">Adventure and enduro bikes, with a children's fun area for kids' bikes and quads. Under-12s ride with an adult present.</div>
    </details>
    <details>
      <summary>Can I rent a motorbike?</summary>
      <div class="a">Not yet — it's a service we hope to offer. It is the ideal place to test ride an adventure bike you're looking to buy.</div>
    </details>
    <details>
      <summary>Can I book the park for a private event or training day?</summary>
      <div class="a">Yes — we're happy to open any day for groups of six or more. <a href="mailto:dave@kohatumc.co.nz">Email Dave</a> and we'll do our best to accommodate your crew.</div>
    </details>
  </div>
</section>"""
page("park.html", "The Park — Adventure Training Ground | Kohatu Motorcycle Centre",
     "5.5 km of purpose-built adventure-bike single track at Kohatu Park, Spooners Range. $30 adults, $10 under-15, $40 family. Open days 11am–4pm — check Facebook for dates.",
     body, "", "img/park-aerial-1200.webp")

# ================= gallery.html =================
tiles = [
    ("gallery-mud", 480, 640, "Grinning rider covered head to toe in mud beside his adventure bike"),
    ("gallery-wheelie", 480, 320, "Rider wheelying a red Honda across a daisy-covered paddock"),
    ("gallery-tractor", 480, 651, "View from a bike being towed across a river behind a muddy tractor"),
    ("gallery-gate", 480, 360, "Rider on a KTM coming through a farm gate on a forest trail"),
    ("gallery-street", 480, 270, "Dirt and adventure bikes parked along a small-town main street with mountains behind"),
    ("trail-rides", 480, 320, "Rider catching air on a red Honda over a grass mound"),
    ("gallery-lineup", 480, 270, "Five riders lined up behind a locked access gate in native bush"),
    ("gallery-jetty", 480, 270, "Rider's selfie at a lake jetty with snow-capped ranges behind"),
    ("gallery-riverbank", 480, 270, "Riders walking a rocky riverbank through native beech forest"),
    ("gallery-lake", 480, 270, "Mirror-calm bush-lined mountain lake under a clear sky"),
    ("gallery-penstock", 480, 270, "Adventure bike parked on a mossy remote trail beside a giant hydro penstock"),
    ("sounds-like", 480, 270, "Still river reach flanked by native forest hills under a blue sky"),
]
tile_html = "\n".join(
    f'      <a href="https://www.facebook.com/kohatumotorcyclecentre" aria-label="See more photos on Facebook"><img src="img/{b}-480.webp" srcset="img/{b}-480.webp 480w, img/{b}-800.webp 800w" sizes="(max-width:700px) 46vw, 320px" loading="lazy" width="{w}" height="{h}" alt="{alt}"></a>'
    for b, w, h, alt in tiles)
body = f"""<section class="page-hero">
  <div class="wrap">
    <span class="kicker">Straight from the rides</span>
    <h1>Where the action happens</h1>
    <p>No stock photos — every shot and every frame below is from our rides, our park, our riders.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <h2 style="font-size:clamp(1.9rem,4vw,2.6rem); margin-bottom:1.4rem">The films</h2>
    <div class="split" style="align-items:start">
      <div>
        {yt("r0OEHg4zxCg", "Nelson Tasman Motorcycle Festival 2025 — full film", "Blake Jones")}
      </div>
      <div>
        {yt("2huJ1oYqfSk", "Kohatu Motorcycle Centre — the park", "RideLifeNZ")}
      </div>
    </div>
  </div>
</section>
<section class="why cut-l">
  <div class="wrap">
    <h2 style="font-size:clamp(1.9rem,4vw,2.6rem); margin-bottom:1.4rem">The photos</h2>
    <div class="gal">
{tile_html}
    </div>
    <p style="margin-top:1.5rem"><a class="btn btn-ghost" href="https://www.facebook.com/kohatumotorcyclecentre">More on Facebook &rarr;</a></p>
  </div>
</section>"""
page("gallery.html", "Gallery — Films &amp; Photos | Kohatu Motorcycle Centre",
     "Films by Blake Jones and RideLifeNZ, and photos straight from Kohatu Motorcycle Centre rides — no stock, just riders.",
     body, "", "img/gallery-wheelie-800.webp")

# ================= rides.html =================
# cards: (cat, img_base, srcs, w, h, alt, flag, flagcls, grade_var, grade, meta, title, href, blurb, price, small, cta_label, red)
cards = [
    ("multi", "five-year-plan", (480, 800, 1200), 800, 600, "Loaded adventure bike in a green paddock pointing toward rugged Marlborough hills",
     "Next up · Aug 2026", "badge-open", "--g3", "Grade 3", "6 days · August 2026 · Year 1 of 5", "The Five Year Plan", "five-year-plan.html",
     "Ride the length of New Zealand over five years, starting at Cape Reinga. Six days of Northland's off-road tracks, private land and scenic trails.",
     "$2,990", "per year", "View ride", False),
    ("multi", "clarence", (480, 800, 1200), 800, 450, "Group of adventure riders gathered on a river gravel bar beneath bush-clad mountains",
     "March 2027", "badge-soon", "--g3", "Grade 3", "3 days · ~750 km · Nelson &rarr; Hanmer &rarr; Nelson", "The Clarence", "the-clarence.html",
     "Private stations the whole way — Tempello, the Clarence Valley and Muzzle, then Glenhope — with a tractor river crossing if the water's up.",
     "$925", "accommodation + most meals", "View ride &amp; book", True),
    ("multi", "gallery-jetty", (480, 800), 800, 450, "Rider's view from a jetty over the water, snow-capped ranges beyond",
     "February 2027", "badge-soon", "--g3", "Grade 3", "2 days · French Pass &amp; the outer Sounds", "Sounds Like", "sounds-like.html",
     "Private farm tracks across three big outer-Sounds stations including Te Kuta and Port Ligar. Overnight at the French Pass hall.",
     "$295", "hall stay + meals included", "View ride", False),
    ("festival", "festival", (480, 800, 1200), 800, 450, "Drone view of an event basecamp in a forested valley, riders waving beside their bikes",
     "May 2027", "badge-soon", "--g1", "All riders", "2 days · Nelson · Finishes at Founders Park", "Nelson Tasman Motorcycle Festival", "nelson-tasman-festival.html",
     "Adventure bikes ride both days, road bikes join a treasure hunt — then everyone rolls into Founders. Raising funds for NT Search &amp; Rescue.",
     "$45–$350", "road / adventure entry", "View festival", False),
    ("festival", "wellington2", (480, 800, 1200), 800, 450, "Adventure and dirt bikes parked in a forest clearing during a ride stop",
     "May 2027", "badge-soon", "--g1", "All riders", "2 days · Trentham &amp; Masterton &rarr; Brewtown", "Wellington Motorcycle Festival", "wellington-festival.html",
     "Adventure courses over parks, forestry and private land, plus a Saturday poker run ending at Brewtown.",
     "$45–$350", "road / adventure entry", "View festival", False),
    ("day", "summer-series", (480, 800, 1200), 800, 600, "Dozens of dirt bikes and riders parked in a forest clearing above a river gorge",
     "Oct–May season", "badge-soon", "--g4", "Grade 3–4", "One-day rides · Roughly monthly", "Summer Ride Series", "summer-series.html",
     "Lake Matiri with a tractor. Anything Mechanical. Tempello. Rainey River. One-day adventures over farms and back roads you can't normally touch.",
     "From $100", "per rider, per ride", "See the series", False),
    ("day", "trail-rides", (480, 800), 800, 533, "Rider catching air on a red Honda over a grass mound",
     "No rego needed", "badge-open", "--g4", "Grade 3–4", "One-day trail rides · Trail &amp; enduro bikes", "Trail Rides", "trail-rides.html",
     "Forest tracks, open climbs and river crossings for non-road-registered bikes — marshals, recovery and first aid on site all day.",
     "$80", "per rider", "View trail rides", False),
]
card_html = ""
for cat, base, srcs, w, h, alt, flag, flagcls, gvar, grade, meta, title, href, blurb, price, small, cta, red in cards:
    srcset = ", ".join(f"img/{base}-{s}.webp {s}w" for s in srcs)
    btn = "btn-red" if red else "btn-line"
    card_html += f"""
      <article class="event-card reveal" data-cat="{cat}">
        <div class="event-media">
          <img src="img/{base}-{max(srcs)}.webp" srcset="{srcset}" sizes="(max-width: 700px) 92vw, 400px" loading="lazy" width="{w}" height="{h}" alt="{alt}">
          <div class="flags">
            <span class="badge {flagcls}">{flag}</span>
            <a class="badge" href="index.html#grades"><span class="dot" style="background:var({gvar})"></span>{grade}</a>
          </div>
        </div>
        <div class="event-body">
          <span class="event-meta">{meta}</span>
          <h3><a href="{href}">{title}</a></h3>
          <p>{blurb}</p>
          <div class="event-foot">
            <span class="price">{price}<small>{small}</small></span>
            <a class="btn {btn}" href="{href}">{cta}</a>
          </div>
        </div>
      </article>"""

body = f"""<section class="page-hero">
  <div class="wrap">
    <span class="kicker">Rides &amp; events</span>
    <h1>Pick your next ride</h1>
    <p>Every ride shows its grade, price and what's included — no phone tag required. Entries are limited on every event and the good ones fill fast. Not sure what suits? Check <a href="index.html#grades" style="color:var(--red)">how grading works</a>.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filter rides">
      <button class="chip" aria-pressed="true" data-filter="all">All rides</button>
      <button class="chip" aria-pressed="false" data-filter="multi">Multi-day</button>
      <button class="chip" aria-pressed="false" data-filter="festival">Festivals</button>
      <button class="chip" aria-pressed="false" data-filter="day">One-day &amp; trail</button>
    </div>
    <div class="event-grid">
{card_html}
    </div>
  </div>
</section>"""
page("rides.html", "Rides &amp; Events | Kohatu Motorcycle Centre",
     "Every Kohatu ride with its grade, price and what's included — multi-day station rides, festivals, one-day adventures and no-rego trail rides.",
     body, "", "img/clarence-1200.webp")

# ================= privacy.html =================
body = """<section class="page-hero">
  <div class="wrap" style="max-width:46rem">
    <span class="kicker">The fine print</span>
    <h1>Privacy statement</h1>
    <p style="font-size:.95rem">Draft for review — to be confirmed by Kohatu Motorcycle Centre before launch.</p>
  </div>
</section>
<section style="padding-top:0">
  <div class="wrap" style="max-width:46rem">
    <h2 style="font-size:1.5rem; margin:0 0 .8rem">What we collect and why</h2>
    <p style="color:var(--muted)">When you join the ride list we collect your name, email address and which rides interest you — so we can email you when entries open. When you register for an event we also collect your phone number, emergency contact details and information about your bike — so we can run the event safely and reach someone who cares about you if something goes wrong.</p>

    <h2 style="font-size:1.5rem; margin:2rem 0 .8rem">Where it goes</h2>
    <p style="color:var(--muted)">Your information is held by Kohatu Motorcycle Centre Ltd and the service providers that run our website and entries: our website host, our mailing-list provider, and our ticketing/booking provider when you pay for an event online. We don't sell your information or share it with anyone else, except where the law requires.</p>

    <h2 style="font-size:1.5rem; margin:2rem 0 .8rem">Your choices</h2>
    <p style="color:var(--muted)">Every email we send has an unsubscribe link. You can ask to see, correct or delete the personal information we hold about you at any time under the Privacy Act 2020 — contact <a href="mailto:dave@kohatumc.co.nz" style="color:var(--red)">dave@kohatumc.co.nz</a> or call <a href="tel:+64274486688" style="color:var(--red)">+64 27 448 6688</a>.</p>

    <p style="margin-top:2.5rem"><a class="btn btn-ghost" href="./">&larr; Back to the rides</a></p>
  </div>
</section>"""
page("privacy.html", "Privacy Statement | Kohatu Motorcycle Centre",
     "What Kohatu Motorcycle Centre collects when you join the ride list or enter an event, where it goes, and your rights under the NZ Privacy Act 2020.",
     body)

print("all pages generated")
