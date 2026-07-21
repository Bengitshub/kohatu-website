# V2 rebuild — working plan (from Ben's pasted V2 brief, 21 Jul 2026)

Stack ruling (brief §10 allows it): keep existing static setup — python generator (build_v2.py) → kohatu-netlify-deploy/. No Astro/11ty (no node on this Mac).

## Verified corrections to the brief
- No /mountain-bike-events page exists on live site (all 404, absent from live sitemap). Torque & Trails DID run (gallery photos: "Torque and trails" e-MTB race). Build honest e-MTB page from verifiable facts only; handicap/rounds/prizes = owner-confirmation, not stated as fact.
- Full festival film = r0OEHg4zxCg (Blake Jones). 7Odz8i9qgms = "Nelson ADV Ride" edit. Park film = 2huJ1oYqfSk (RideLifeNZ). Brief's manifest had these wrong.
- Deep in the Sounds (starts Fri 24 Jul 2026, via Kohatu FB/allevents, org shown as Nelson Motorcycles) = interest-open event record.

## Route map (directory URLs, trailing slash)
/ /events/ /events/adventure/ /events/trail-rides/ /events/torque-and-trails/ /events/past/
/events/{five-year-plan,the-clarence,sounds-like,nelson-tasman-motorcycle-festival,wellington-motorcycle-festival,deep-in-the-sounds}/
/events/{lake-matiri,anything-mechanical,rainey-river-lakes-station,tempello,st-arnaud-trail-ride}/ (ride reports)
/kohatu-park/ /ride-grades/ /safety-support/ /stories/ /gallery/ /films/ /about/ /sponsors/ /location/ /contact/ /privacy/ /terms/ /proposal/ 404.html

## Status → CTA map (never "Book" without a real booking route)
provisional→Get event updates · interest-open→Register interest · entries-open→Book your place · limited→Book final spaces · sold-out→View event · waitlist→Join the waitlist · postponed→View event update · completed→View ride report · cancelled→View cancellation notice

## Homepage floor plan (exact order)
status strip · hero (ford, existing headline, "View upcoming events"/"Find your ride type") · 4 pathway cards (Adventure/Trail/Park/Torque&Trails) · next 3 events (from data) · FYP signature w/ 5-year timeline · what Kohatu unlocks (4 proofs) · grading preview (compact, link /ride-grades/) · proof (film r0OEHg4zxCg + no fabricated testimonials) · meet Dave · park strip · ride alerts (name/email/interest only) · footer

## Rules
- Everything event-related reads from src/data/events.json (cards, pages, JSON-LD, status strip, related).
- No developer/sales commentary on public pages → all moved to /proposal/ (noindex, not in nav). Demo forms show "demonstration only — nothing stored" confirmation.
- No invented dates/routes/prices/testimonials. requiresOwnerConfirmation flags rendered as provisional styling in preview.
- Phases: A data → B generator (shell+events) → C homepage → D aux+proposal → E css/redirects/prune → deploy → QA workflow → change log (docs/v2-changelog.md).
