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
