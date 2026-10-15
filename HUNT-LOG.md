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
