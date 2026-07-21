# Kohatu Motorcycle Centre — pitch site

Demo rebuild of [kohatumc.co.nz](https://www.kohatumc.co.nz) (Dave McLeod, Nelson NZ) built by Webhero as a pitch.
Everything ships from `kohatu-netlify-deploy/` — static HTML/CSS, no build step.

## Layout

- `kohatu-netlify-deploy/` — the deployable site (index, the-clarence, terms, 404, `_headers` with noindex, robots.txt, img/, fonts/)
- `source-pages/` — raw HTML scraped from the current Squarespace site (Jul 2026)
- `source-content/` — text extracted from those pages (fact-check source of truth)
- `source-assets/` — original images pulled from the Squarespace CDN
- `scrape.py` / `extract_text.py` / `optimize.py` — the scrape → text → WebP pipeline

## Content decisions

- All prices, itineraries, contact details and park info come from Dave's own site (see `source-content/`).
- Future event dates (Aug 2026, Feb/Mar/May 2027) are the teaser dates published on his current homepage.
- "Kohatu grading system" (grades 1–5) is a NEW concept invented for the pitch — presented as a proposal, not something Dave runs today.
- The "Book your spot" button opens a dialog explaining where Humanitix embedded checkout would go — no fake payment flow.
- Email capture is a Netlify form (`ride-list`) — works as soon as it's deployed on Netlify.

## Deploy

Zip the contents of `kohatu-netlify-deploy/` and deploy via Netlify API (see BDBR project for the pattern), or link the repo with publish dir `kohatu-netlify-deploy` (netlify.toml already set).

At go-live (if Dave signs): remove `X-Robots-Tag: noindex` from `_headers`, open up `robots.txt`, add a sitemap + 301 map from the old Squarespace URLs.

## Confirm with Dave before go-live

- Exact dates for every 2026/27 event (site shows month-level placeholders from his homepage)
- Five Year Plan price: his site shows both $2,990 (event page) and $3,350 (old festival page)
- The Clarence inclusions (Hanmer meals, sweep-rider count) and per-event kit lists
- Grading names + each event's grade (the 1–5 system is a Webhero proposal)
- Are mountain-bike / e-MTB events still part of Kohatu (old meta + gallery photos suggest they were — e.g. "Torque and Trails")? If yes, they need a section.
- Privacy statement wording (drafted at /privacy.html) and nominated privacy contact
- Participant terms: current terms.html mirrors his site (refunds + force majeure only). For launch he should get proper participant terms reviewed: rider responsibility/skill, bike condition + rego + insurance, route changes, weather/fire/landowner restrictions, postponement + minimum numbers, medical + emergency response, risk acknowledgement, damage to bikes/belongings, photography consent, behaviour/removal, transfers, third-party accommodation, NZ law.
- Care plan: recommend a monthly plan (hosting + event updates) or Sveltia CMS self-editing as an upsell; do not promise self-management before it exists.
- Video rights: festival films are by Blake Jones, park film by RideLifeNZ — embedded (fine); for a self-hosted hero loop at go-live, get footage/permission first.

## Launch scope already staged

- `_redirects` — full 301 map from current kohatumc.co.nz URLs (live on the demo)
- Re-enable forms: add `data-netlify="true"` + honeypot (or mailing platform) and remove the `js-demo-form` interceptor in site.js
- Remove `X-Robots-Tag: noindex` from `_headers`, open robots.txt, add sitemap
- Connect Humanitix embedded checkout on event pages (replaces book-demo dialog)
- 11 ha lease figure on park.html/about (from news research, not Dave's site) — confirm with Dave
- "Deep in the Sounds" (Facebook-promoted, starts Fri 24 Jul 2026, listed via allevents.in under Kohatu's org, organiser shown as Nelson Motorcycles) — on the demo's "this week" band; confirm details/ownership with Dave. His website not listing it is a pitch talking point.
- Five Year Plan PDF removed from demo (Oct 2025 upload, describes the original Feb 2026 running — contradicts the August reschedule). Dave to issue an updated pack.
