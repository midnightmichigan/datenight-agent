# HUNT-LOG — Qloo Agentic Hackathon scaffold (2026-10-09)

## Opportunity (rules verified from https://qloo.devpost.com/rules)
- **Qloo Agentic Hackathon** — $25,000 total: 1st $15,000 / 2nd $6,000 / 3rd $4,000.
- Registration + submission: Sept 30 – **Oct 30, 2026, 11:45 PM ET**.
- Judging Nov 2–16; winners ~Nov 23.
- Solo allowed. Global eligibility (18+, not in sanctioned regions).
- Build: working app that integrates the Qloo API and (a) functions as an
  agentic tool, (b) is built with an agent framework, or (c) plugs Qloo into
  an existing agent. New or existing projects OK (existing must show
  meaningful updates during the window).
- Submit: functional demo app link + **public repo with OSI license** +
  text description. **No video required** (rules mention video only as an
  optional judging aid: "as depicted in the video and/or expressed in the
  text description").
- Judging (equally weighted): Technological Implementation, Design,
  Potential Impact, Quality of the Idea.
- API key: free via the Google Form linked on the hackathon site
  (key within ~4h per prior hackathons; hackathon-use only).

## API researched (verified via docs.qloo.com + prior hackathon builds)
- Base: `https://hackathon.api.qloo.com` (env-overridable; CONFIRM against
  the key-issuance email — the 2026 hackathon may use a new host).
- Auth: `X-Api-Key` header.
- `GET /search?query=<q>&limit=N` → entity candidates with IDs.
- `GET /v2/insights?filter.type=urn:entity:<type>&signal.interests.entities=<ids>&take=N`
  (POST variant for complex bodies) → recommendations with `affinity` 0–1.
- Verified entity types: `urn:entity:restaurant`, `urn:entity:movie`,
  `urn:entity:place`, `urn:entity:brand`, `urn:entity:destination`,
  `urn:entity:tv_show`.

## Concept: DateNight Agent
An agentic date-night planner with taste. User describes a person
("loves Wes Anderson films and Taylor Swift"); the agent builds a Qloo
taste fingerprint, pulls cross-domain recommendations (dinner / film /
stroll), and narrates an itinerary citing affinity scores. Hits all four
judging criteria: genuine agentic tool-use loop, complete product UX,
relatable real-world problem, non-obvious cross-domain taste transfer.

## What was scaffolded
`~/workspace/bounty-hunts/qloo-agentic/`:
- `agent.py` — stdlib server + the 5-step agentic loop (parse → fingerprint
  → insights → narrate → JSON plan); routes `/`, `/api/health`, `/api/plan`.
- `qloo_client.py` — `/search` + `/v2/insights` wrapper with labeled mock
  fallback (zero-config for judges).
- `static/index.html` — single-page UI with live/mock mode badge.
- `test_flow.py` — end-to-end smoke test, ALL PASSING (mock mode).
- `README.md`, `LICENSE` (MIT), `.gitignore` — push-ready.

## Build plan (remaining)
1. **API key** (browser/form step for parent): fill the hackathon Google Form,
   confirm base URL from the issuance email, run one live `/search` to
   verify shape.
2. Optional polish: location-aware restaurant filtering (Qloo supports
   geohash/radius params), LLM taste-seed expansion for richer fingerprints.
3. Push to `midnightmichigan/datenight-agent` (public, MIT).
4. Main-agent review → Devpost submit before Oct 30, 11:45 PM ET.

## Bounds honored
$0 spend. No identity committed beyond authorized free signups. Nothing
submitted; all submission steps flagged ready-for-review.

## 2026-10-17 ~04:45 EDT — API key RECOVERED + live-verify in progress
- The hackathon API key ISSUED BY QLOO on 2026-10-13 02:44 EDT (email from
  hackathon@qloo.com, "Your Qloo API Access for the Agentic Hackathon";
  Gmail msg 1a134010502846a9) — it had been sitting in the inbox for 4 days
  while the log still said "API key request in flight." Dedupe corrected:
  never trust "in flight" without re-checking the inbox.
- Verified LIVE this run: `GET /search` against hackathon.api.qloo.com with
  the key returns real entities (Wes Anderson, Accidentally Wes Anderson).
- Bug fixed in qloo_client.py: `urn:entity:restaurant` is REJECTED by the
  2026 hackathon API (400 "not supported for filter.type"). Per the official
  developer guide (docs.qloo.com, read 2026-10-17), supported filter.types:
  artist, book, brand, destination, movie, person, place, podcast, tv_show,
  video_game. Food & beverage places → urn:entity:place. Added
  FILTER_TYPE_ALIASES mapping (restaurant/dinner→place,
  evening_stroll→destination, film→movie, tv→tv_show, music→artist);
  also fixed search result `type` extraction (field is `types[]`, not `type`).
- BLOCKED: full live-pipeline verify (place/movie/destination insights)
  stalled on VM outbound-network failure starting ~04:48 EDT (all direct
  HTTPS from the VM timing out; gmail/browser.search unaffected). Retry the
  live verify on the next healthy run, then: push public repo → prepare
  Devpost submission package → flag READY FOR HIS REVIEW (never final-submit).
  Deadline: Oct 30, 2026 11:45 PM ET (~13 days).

## 2026-10-17 ~05:45 EDT — submission package DRAFTED + pipeline re-verified healthy
- Live-pipeline verify STILL blocked: VM outbound-network failure persists
  (curl to hackathon.api.qloo.com times out at 10s; same pattern as the
  04:40 run). Key NOT re-fetched from Gmail this run — no point until the
  network is healthy; nothing stored.
- Re-verified mock pipeline: `python3 test_flow.py` → ALL PASSED
  (seeds → fingerprint → dinner/film/stroll recs → itinerary). Build healthy.
- Wrote SUBMISSION-PACKAGE-DRAFT.md: complete Devpost-ready package
  (name, tagline, full Inspiration/What-it-does/How-we-built-it/
  Challenges/Accomplishments/What's-next writeup, Built With, Try-it-out,
  eligibility note). No video required per rules. DRAFT — never submitted.
- Remaining for READY-FOR-REVIEW: (1) live verify (key + healthy network),
  (2) public repo push `midnightmichigan/datenight-agent` (MIT) — his
  per-item approval, (3) his review. Deadline Oct 30, 11:45 PM ET (~13 days).

## 2026-10-17 ~06:55 EDT — live pipeline FIXED end-to-end (network recovered, then flaky again)
- Network back up early in the run; key re-fetched from Gmail msg 1a134010502846a9, used transiently via env only — nothing stored.
- plan_date_night() verified LIVE (mock:false, real entities across dinner/film/stroll domains).
- BUG FIXED in qloo_client._resolve_filter_type: full URNs short-circuited the alias map; urn:entity:restaurant hit the API's 400. Now URNs normalize through the map (restaurant/dinner→urn:entity:place). Dinner domain returns real entities.
- OPEN: (1) affinity field absent from raw v2 insight entities (all 0.0 — ranking no-op; check `query` sub-block); (2) signal fidelity unverified (UUID vs urn:entity:<uuid> prefix); (3) API went flaky again (2x timeouts) — one more healthy-network session needed.
- NOT submitted; repo push + his review still the gate. Deadline Oct 30 11:45 PM ET.

## 2026-10-17 ~07:55 EDT — live quality pass BLOCKED by VM network outage (no code changes)
- Attempted the 06:55 run's open items: (1) locate the real affinity field
  (raw v2 entities had none — all 0.0), (2) test `urn:entity:<uuid>` signal
  prefix vs raw UUID.
- Key re-fetched from Gmail msg 1a134010502846a9 (+read; raw get failed
  twice transiently); saved copy deleted immediately after in-memory
  extraction — transient use only, nothing on disk.
- hackathon.api.qloo.com timed out from the VM (15s urlopen + 2x 12s curl);
  google.com/devpost.com also down — full VM outbound outage, same transient
  pattern as 04:40/05:40 runs. Bounded probes only; no hammering. Both open
  items carry to the next healthy run.
- Deadline unchanged: Oct 30, 2026 11:45 PM ET. NOT submitted; repo push +
  his review still the gate.

## 2026-10-27 ~11:52-12:05 EDT — live verify PASSED, affinity bug FIXED, package staged (NOT pushed/submitted)
- Gmail transport HEALTHY this run: key re-fetched from msg 1a134010502846a9
  via `gmail +read` (account e0fac396..., ~1.9s, exit 0). Key used ONLY as
  env var in transient verify scripts (scripts deleted after run); never
  written to any file/log/report. Base URL confirmed from the issuance
  email: https://hackathon.api.qloo.com — matches qloo_client.py default.
- LIVE search: `search_entities("Wes Anderson")` returned real entities
  (Wes Anderson — author/person types, Accidentally Wes Anderson — book).
  Search IDs are raw UUIDs (no urn prefix).
- OPEN ITEM 1 RESOLVED — affinity: raw v2 insight entities have NO
  top-level `affinity` field (all read 0.0). The real score is
  `entity.query.affinity` (e.g. movie: The Salt of the Earth 0.926,
  The Great Beauty 0.922, Victoria 0.918; place: Strawberry Fields 0.912).
  FIXED in qloo_client.insights(): fall back to query.affinity when the
  top-level field is absent. Post-fix full pipeline (mock:false) returns
  real affinities: dinner 0.955/0.941/0.940, film 0.891/0.889/0.888.
- OPEN ITEM 2 RESOLVED — signal prefix: raw UUID signals WORK;
  `urn:entity:<uuid>`-prefixed signals are REJECTED (HTTP 400). Current
  code already passes raw UUIDs from /search — correct as-is, do NOT prefix.
- Destination note: `filter.type=urn:entity:destination` with a person
  seed returns HTTP 400 "All of the provided signal.interests.entities
  were invalid" — destination insights reject that seed type. The agent
  pipeline does not use destination (stroll = urn:entity:place, working);
  the evening_stroll→destination alias in qloo_client is unused by
  agent.py. No pipeline impact; documented here, not "fixed" by swapping
  the working place mapping.
- Known cosmetic limitation (unchanged): without an LLM key, parse_brief's
  keyword fallback splits multi-word names ("Wes Anderson" → wes/anderson),
  so the live fingerprint is noisier than the LLM path. Recommendations
  still return real, affinity-ranked entities.
- Mock tests: `python3 test_flow.py` → ALL TESTS PASSED after the fix.
- Repo prep (stage only, NO push, NO submit): repo
  midnightmichigan/datenight-agent already public with 2 commits
  (6381325 scaffold, 9e8e73e hardening); `git ls-remote origin HEAD`
  matches local HEAD 9e8e73e. The affinity fix (qloo_client.py) +
  SUBMISSION-PACKAGE-DRAFT.md status/challenges updates + this log entry
  are STAGED locally, uncommitted.
- SUBMISSION-PACKAGE-DRAFT.md updated: header now records live-verify
  PASSED; Challenges section documents the query.affinity field and the
  raw-UUID signal rule. Package is Devpost-ready as a draft.
- REMAINING for the push + submit step (parent/Dakota gate):
  (1) commit the staged changes, (2) `git push origin master` to
  midnightmichigan/datenight-agent, (3) Dakota's review, (4) Devpost
  submission on qloo.devpost.com using SUBMISSION-PACKAGE-DRAFT.md
  (browser step; no video required) before Oct 30, 2026 11:45 PM ET.
- $0 spend. NOT submitted. Deadline: Oct 30, 2026 11:45 PM ET (~3.5 days).
