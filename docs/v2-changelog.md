# Kohatu V2 — change log (branch `kohatu-v2-architecture`, 21 Jul 2026)

## What changed

**Architecture** — the flat 14-page demo became a 31-page site generated from a single data source:
- `src/data/events.json` — every event (12 records: 6 upcoming, 5 completed, 1 e-MTB series). Cards, pages, JSON-LD, status strip and related-event blocks all render from it.
- `src/data/media.json` — asset registry (base/widths/dimensions/alt/focal point) referenced by ID.
- `build_v2.py` — generates the entire site into `kohatu-netlify-deploy/`. One command: `python3 build_v2.py`.

**Routes** (directory URLs): `/` · `/events/` (+filters) · `/events/adventure/` · `/events/trail-rides/` · `/events/torque-and-trails/` · `/events/past/` · one page per event under `/events/<id>/` · `/kohatu-park/` · `/ride-grades/` · `/safety-support/` · `/stories/` · `/gallery/` · `/films/` · `/about/` · `/sponsors/` · `/location/` · `/contact/` · `/privacy/` · `/terms/` · `/proposal/` (noindex, unlinked) · `404.html`.

**Per the V2 brief:**
- Status strip above the nav reads the next event from data (currently Deep in the Sounds, 24–26 July).
- Homepage restructured to the floor plan: hero → 4 pathway cards (Adventure / Trail / Park / Torque and Trails) → next 3 events only → Five Year Plan signature section with 5-year timeline → proof blocks → compact grade scale → festival film → Dave (moved up) → park strip → minimal ride-alert form.
- Event-status system with honest CTA mapping — "Book" appears nowhere (no booking route exists yet).
- Torque and Trails restored as a first-class offering, using only verifiable facts (series exists, ran at the park, photographed); format/dates flagged for Dave.
- Past rides kept as ride-report pages (Lake Matiri, Anything Mechanical, Rainey River, Tempello, St Arnaud trail ride).
- All developer/sales commentary moved to `/proposal/`; public forms show a customer-appropriate "preview — nothing stored" confirmation.
- Interest forms: first name + email only. Sticky mobile CTA on upcoming-event pages.
- `_redirects`: one-to-one 301s from every current kohatumc.co.nz URL AND from the V1 flat demo URLs.
- Canonicals, unique titles/descriptions, Event JSON-LD per upcoming event, Organization data, `noindex` on proposal only.

## Unresolved — owner confirmation required (also in README)
- Deep in the Sounds: dates/details/ownership (evidence: Kohatu FB via allevents.in; organiser shown as Nelson Motorcycles).
- Five Year Plan: August dates, price ($2,990 vs $3,350 conflict), sweep count, pack reissue (old Feb PDF unlinked).
- Torque and Trails: format, rounds, handicap system, next dates, sponsors/prizes.
- Grading names and per-event grades (Webhero proposal).
- Clarence inclusions; per-event kit lists; capacities; 11 ha lease figure.
- Privacy wording + privacy contact; participant terms (legal review before online entries).
- Photo/rider permissions; film usage beyond embeds (Blake Jones, RideLifeNZ).
- Booking provider decision (Humanitix recommended) and mailing provider.

## QA
- Programmatic: 31 pages, 0 broken internal references, all JSON-LD parses, one h1 per page, noindex on proposal only. Live checks: all routes 200, old-URL 301s verified, status strip live.
- Agent QA (acceptance audit + content pass): results appended below when complete.
