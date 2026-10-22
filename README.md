# DateNight Agent — an agentic planner with taste

Entry for the **Qloo Agentic Hackathon** ($25,000 prizes: $15k/$6k/$4k —
deadline Oct 30, 2026, 11:45 PM ET).

## What it does
You describe a person and an evening in plain English. The agent:
1. Parses the brief into taste seeds + location + occasion (LLM, with a
   rule-based fallback).
2. Resolves each seed to Qloo taste-graph entities — the "taste fingerprint."
3. Queries Qloo's cross-domain insights seeded by that fingerprint for
   restaurants (dinner), movies (film), and places (evening stroll) — the
   taste-transfer Qloo exists for.
4. An LLM narrates a coherent date-night itinerary citing the affinity
   scores as evidence (template fallback included).

Example: *"Plan a date night for someone who loves Wes Anderson films and
Taylor Swift, in Chicago"* → dinner + film + stroll picks ranked by
taste-graph affinity to those seeds.

## Why it fits the hackathon
- **Agentic**: multi-step tool-use loop (parse → search → insights → narrate),
  not a single API call.
- **Qloo at the core**: every recommendation is seeded by the entrant's
  taste fingerprint via `/search` + `/v2/insights`; affinity scores are
  surfaced, not hidden.
- **Real-world use**: date-night planning is a concrete, relatable problem
  the taste graph genuinely solves better than generic search.

## Run it
```
python3 agent.py            # http://127.0.0.1:8001
python3 test_flow.py        # end-to-end smoke test (mock mode, all passing)
```

## Optional env (real modes)
- `QLOO_API_KEY` — free hackathon key via the Google Form linked from the
  official rules (qloo.devpost.com/rules → docs.qloo.com hackathon developer
  guide "Getting your API key"). Blocked 2026-10-16 17:40 EDT: shared
  Chromium's Google session is SIGNED OUT (verified by a separate job
  17:20 EDT) and the form needs his name/email → his tap or a browser
  retry after the Google session is restored. Without it, the app runs in
  clearly labeled mock mode. `QLOO_BASE_URL` overrides the API host if the
  key-issuance email names a different one.
- `OPENAI_API_KEY` (+ `OPENAI_BASE_URL`, `OPENAI_MODEL`) — LLM brief parsing
  and itinerary narration. Any OpenAI-compatible endpoint works.

## Submission status
**DRAFT — NOT SUBMITTED.** Before submission:
1. Get the free Qloo API key (Google Form — browser step) and run one live
   query to verify the base URL + response shape.
2. Push to a public GitHub repo under midnightmichigan with this MIT license.
3. Main-agent review, then submit on Devpost before Oct 30, 2026 11:45 PM ET
   (demo = functional app link + run instructions; no video required).
