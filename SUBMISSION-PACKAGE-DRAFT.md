# SUBMISSION-PACKAGE-DRAFT — Qloo Agentic Hackathon
**DRAFT — NOT SUBMITTED.** Deadline: Oct 30, 2026, 11:45 PM ET.
Status 2026-10-27: (1) live-pipeline verify PASSED (see HUNT-LOG
2026-10-27 entry — real entities, real affinity scores after the
query.affinity fix), (2) public repo `midnightmichigan/datenight-agent`
already exists (2 commits, remote HEAD matches local); the 2026-10-27
affinity fix is staged locally, NOT yet pushed — push needs his
per-item approval, (3) his review of this package. Video: NOT required
by rules (video is optional judging aid only).

## Project name
**DateNight Agent** — an agentic planner with taste

## Tagline
Plan a date night from taste: Qloo's taste graph turns "loves Wes Anderson
films and Taylor Swift" into dinner, film, and stroll picks ranked by
affinity.

## What it does (Devpost description)
**Inspiration** — Recommendation engines know *what* people clicked, but
date-night planning is about *taste*: the texture of a Wes Anderson film,
the mood of a Taylor Swift record. Qloo's taste graph is the first API
that answers "what feels like this" across domains. DateNight Agent makes
that answer a plan.

**What it does** — You describe a person and an evening in plain English
(e.g., "Plan a date night for someone who loves Wes Anderson films and
Taylor Swift, in Chicago"). The agent runs a 5-step agentic loop:
1. **Parse** — LLM extracts taste seeds, location, occasion (rule-based
   fallback when no LLM key is set).
2. **Fingerprint** — each seed resolves to Qloo taste-graph entity IDs
   via `/search`; the set is the user's taste fingerprint.
3. **Investigate** — cross-domain `/v2/insights` queries seeded by the
   fingerprint pull dinner (food & beverage places), film, and evening
   stroll picks (restaurants map to `urn:entity:place` per the hackathon
   API's supported filter types; aliases handled in code).
4. **Rank** — picks are ordered by Qloo affinity score, surfaced as
   evidence, not hidden.
5. **Narrate** — an LLM narrates a coherent itinerary citing the affinity
   scores (template fallback included).

The web UI shows a live/mock mode badge: without the hackathon API key it
runs a clearly labeled deterministic mock, so judges (and the entrant)
see the full agentic flow with zero configuration.

**How we built it** — Zero-dependency Python (stdlib only): a lightweight
HTTP server (`agent.py`), a taste-API client (`qloo_client.py`) with a
labeled mock fallback, and a single-page UI (`static/index.html`).
Mock mode is deterministic so the demo is reproducible. Test flow
(`test_flow.py`) runs the full loop end-to-end.

**Challenges** — The hackathon API rejects `urn:entity:restaurant` as a
filter type (verified live, Oct 17); food & beverage must use
`urn:entity:place`, and search results carry `types[]` rather than `type`.
Affinity scores live in each insight entity's `query.affinity`, not a
top-level `affinity` field (verified live, Oct 27 — reading the wrong
field silently ranked everything 0.0). Signal entity IDs must be raw
UUIDs; `urn:entity:<uuid>`-prefixed signals are rejected with HTTP 400
(verified live, Oct 27). All three are normalized in the client with a
documented alias/field map. The demo runs identically against mock or
live backends.

**Accomplishments** — A working agentic planner that exercises Qloo as a
true tool in a multi-step loop (not a single API call), with affinity
scores cited as evidence in the final itinerary.

**What's next** — Location-aware filtering (geohash/radius) for dinner
picks, and LLM taste-seed expansion for richer fingerprints.

## Built With
Python (stdlib only), Qloo Taste API, REST/JSON

## Try it out
- Repo (to be pushed public, MIT): `midnightmichigan/datenight-agent`
- Demo: `python3 agent.py` → http://127.0.0.1:8001 ; `python3 test_flow.py`
  runs the full loop in mock mode.

## Eligibility note
Scaffold began 2026-10-09 (inside the Sept 30–Oct 30 window); meaningful
updates during the window: filter-type alias map + live-key recovery +
submission package. Submission is new work for this hackathon.
