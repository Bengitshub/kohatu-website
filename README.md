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

## Dave's current hosting (recon, 21 Jul 2026)

- **Domain**: kohatumc.co.nz — registered + DNS hosted at **iwantmyname** (NZ registrar; nameservers dns1-3.iwantmyname.com). Ask Dave who holds this login — possibly HotHouse (the previous designer).
- **Website**: Squarespace, connected externally (apex A 198.49.23.145; www CNAME ext-cust.squarespace.com). Squarespace subscription can be cancelled after cutover (~NZ$30+/mo saved).
- **Email**: dave@kohatumc.co.nz runs on **Microsoft 365** (MX mail.protection.outlook.com; SPF + MS= TXT records). DO NOT touch MX/TXT during cutover.
- Existing google-site-verification TXT (Search Console verified by someone — likely HotHouse; re-verify under Dave/Webhero at launch).

## Go-live cutover runbook (after Dave signs)

1. In build_v2.py: set PREVIEW = False and BASE_URL = "https://www.kohatumc.co.nz" (pick www or apex as canonical); rebuild.
2. Remove `X-Robots-Tag: noindex` from _headers; robots.txt → allow + Sitemap line; generate sitemap.xml.
3. Connect forms (mailing provider) + ticketing per proposal; remove js-demo-form interceptor.
4. Netlify: rename/create production site, add custom domain kohatumc.co.nz + www (Netlify auto-provisions Let's Encrypt SSL).
5. At iwantmyname DNS, change ONLY two records (email untouched):
   - apex A: 198.49.23.145 → 75.2.60.5 (Netlify load balancer)
   - www CNAME: ext-cust.squarespace.com → <site>.netlify.app
6. Verify SSL + all pages + path redirects (old Squarespace URLs already 301 via _redirects), verify email still flows (send/receive test).
7. Search Console: verify property, submit sitemap.
8. After a week of stability: cancel the Squarespace subscription (export nothing needed — all content migrated).

Ownership options: (a) site stays on Webhero's Netlify under the NZ$129/mo care plan — recommended; (b) transfer the Netlify site + GitHub repo to Dave's own accounts if he wants self-management.

## Editing & longevity (call-prep answers)

**Can Dave edit it?** Three tiers:
1. **Now (care plan)**: Dave texts/emails a change → edit src/data/events.json → rebuild → deploy. Minutes. His "CMS" is his phone.
2. **Self-edit add-on (sell later, ~1 day's work)**: link the GitHub repo to Netlify push-to-deploy (build cmd: `python3 build_v2.py`, publish `kohatu-netlify-deploy`), then add a git-based editor (Sveltia CMS / Pages CMS) exposing the SAFE fields per event — status, dateLabel, priceLabel, summary. Dave logs in, edits a form, saves; site rebuilds itself. Keep structural/body edits with Webhero. Note: Netlify Identity is deprecated — use GitHub-app auth (Sveltia) or Pages CMS.
3. Full CMS platform migration: don't — loses the speed/simplicity that is the product.

Recommended at go-live regardless of tier: link repo → Netlify auto-build (kills zip deploys + per-session tokens for us too).

**1 year+ outlook:**
- Static HTML doesn't rot: no plugins, no security patching, no PHP/DB. Only moving parts are content and third-party services (ticketing/mailing — managed, self-updating; SSL auto-renews).
- Costs: Netlify free tier at this traffic; domain renewal stays at iwantmyname (~NZ$40/yr, Dave's). If Netlify ever changes terms, the folder deploys to Cloudflare Pages in minutes (_redirects/_headers compatible) — no lock-in.
- Annual rhythm (care-plan content): season flip each spring (new events in events.json, completed ones auto-archive), FYP year rollover (timeline "tl-now" moves to next year), fresh season photos, Search Console review.
- Continuity answer for Dave: he holds the repo, the handover zip and the runbook — any developer can take over in an afternoon.
- Pricing objection to expect: care plan NZ$1,548/yr vs Squarespace ~NZ$400/yr. Answer: Squarespace was a tool he had to drive (and the stale site shows the real cost); the care plan is a webmaster. Optional lighter tier is Ben's call.

## SEO (call-prep answers)

**What Dave has to lose: almost nothing.** Current site: brand-only homepage title, stale future-tense meta description, Article (not Event) schema with the old designer's Gmail as the org contact, duplicate indexed pages (/home, /home-2, old festival page), event excerpts that are just dates, and no Google Business Profile found. His discovery is Facebook, not Google — the rebuild risks nothing meaningful and preserves the rest.

**What survives the cutover:** the domain (all backlink authority attaches to kohatumc.co.nz, not Squarespace), every existing URL via one-to-one 301s (link equity follows), brand-query rankings.

**What improves:** proper Event+Offer schema per event (rich-result eligibility his site has never had) · unique keyword+location titles/descriptions per page · clean per-event URLs · static+CDN Core Web Vitals · corrected Organization schema · duplicate stale pages killed via 301 · past-rides archive = content that compounds every season.

**Biggest single win is off-site:** create the missing Google Business Profile (events as Products, photo cadence, review requests after each ride) — local pack ≈ GBP + reviews. Recommend adding as a launch/care-plan line item.

**Launch mechanics (automated/runbooked):** sitemap.xml auto-generates when PREVIEW=False (excludes proposal); submit in Search Console; flip noindex; expect weeks (not days) for re-crawl. Set expectations honestly: brand queries safe immediately, non-brand growth ("adventure rides Nelson/NZ") builds over months.
