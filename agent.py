"""DateNight Agent — an agentic planner with taste.

Agentic loop:
  1. Parse the user's brief (LLM, or fallback keyword extraction) into
     taste seeds + location + occasion.
  2. For each seed: Qloo /search -> entity IDs (the "taste fingerprint").
  3. Qloo /v2/insights seeded by the fingerprint, per domain:
     restaurant -> dinner, movie -> film, place -> evening stroll/stop.
     This is the cross-domain taste transfer Qloo exists for.
  4. LLM narrates a coherent date-night plan citing the affinity scores
     as evidence; fallback composes a template plan from the top picks.
  5. Return the plan as JSON; the UI renders it as an itinerary.

Zero-dependency stdlib server. Mock mode (no QLOO_API_KEY) runs the whole
loop with deterministic fake data so judges need zero configuration.
"""
import json
import os
import re
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

import qloo_client

STOPWORDS = {"a", "an", "the", "for", "and", "with", "who", "loves", "love",
             "likes", "like", "into", "plan", "night", "date", "evening",
             "someone", "person", "my", "of", "in", "on", "to"}


def _llm(prompt, system="You are a concise planning assistant."):
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    payload = {"model": model, "temperature": 0.7, "max_tokens": 600,
               "messages": [{"role": "system", "content": system},
                            {"role": "user", "content": prompt}]}
    req = urllib.request.Request(
        base.rstrip("/") + "/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + api_key,
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode())
    return data["choices"][0]["message"]["content"].strip()


def parse_brief(brief):
    """Step 1: brief -> {seeds, location, occasion}."""
    prompt = ("Extract JSON {\"seeds\": [taste keywords], \"location\": city or null,"
              " \"occasion\": short string} from this date-night brief. "
              "Seeds are the person's tastes (artists, films, cuisines, vibes). "
              f"Brief: {brief}")
    raw = _llm(prompt)
    if raw:
        try:
            start, end = raw.index("{"), raw.rindex("}") + 1
            parsed = json.loads(raw[start:end])
            return {"seeds": parsed.get("seeds", [])[:6],
                    "location": parsed.get("location"),
                    "occasion": parsed.get("occasion", "date night")}
        except (ValueError, json.JSONDecodeError):
            pass
    # fallback: keyword extraction
    words = [w.strip(".,!?\"'").lower() for w in brief.split()]
    seeds = [w for w in words if w not in STOPWORDS and len(w) > 2][:6]
    return {"seeds": seeds, "location": None, "occasion": "date night"}


def build_fingerprint(seeds):
    """Step 2: seeds -> Qloo entity IDs (the taste fingerprint)."""
    fingerprint = []
    for seed in seeds:
        for ent in qloo_client.search_entities(seed, limit=2):
            if ent.get("id"):
                fingerprint.append(ent)
    # dedupe by id, then by name (mock mode can return same-name variants)
    seen, uniq = set(), []
    for e in fingerprint:
        if e["id"] not in seen:
            seen.add(e["id"])
            uniq.append(e)
    seen_names, deduped = set(), []
    for e in uniq:
        n = e["name"].lower()
        if n not in seen_names:
            seen_names.add(n)
            deduped.append(e)
    return deduped


def gather_recommendations(fingerprint):
    """Step 3: cross-domain insights seeded by the fingerprint."""
    ids = [e["id"] for e in fingerprint]
    if not ids:
        ids = ["urn:entity:mock:fallback"]
    domains = {
        "dinner": "urn:entity:restaurant",
        "film": "urn:entity:movie",
        "stroll": "urn:entity:place",
    }
    recs = {}
    for label, ftype in domains.items():
        try:
            recs[label] = qloo_client.insights(ids, ftype, take=3)
        except Exception as exc:  # never let one domain kill the plan
            recs[label] = [{"name": f"(unavailable: {exc})", "affinity": 0,
                            "type": ftype}]
    return recs


def narrate(parsed, fingerprint, recs):
    """Step 4: LLM narration, or a template plan from top picks."""
    evidence = []
    for label, items in recs.items():
        for it in items[:2]:
            evidence.append(f"- {label}: {it['name']} "
                            f"(taste affinity {it.get('affinity', '?')})")
    seeds_txt = ", ".join(e["name"] for e in fingerprint) or "their vibe"
    prompt = ("Write a warm, specific date-night itinerary (dinner, film, "
              "evening stroll) for someone whose tastes include: "
              f"{seeds_txt}. Use ONLY these Qloo taste-graph picks, citing "
              "why each fits:\n" + "\n".join(evidence) +
              "\nKeep it under 220 words, no purple prose.")
    text = _llm(prompt)
    if text:
        return text
    lines = [f"Date-night plan, tuned to: {seeds_txt}."]
    order = [("dinner", "Dinner"), ("film", "Film"), ("stroll", "Evening stroll")]
    for label, title in order:
        top = recs.get(label, [{}])[0]
        lines.append(f"- {title}: {top.get('name')} "
                     f"(taste affinity {top.get('affinity', '?')})")
    lines.append("Picks ranked by Qloo taste-graph affinity to your seeds.")
    return "\n".join(lines)


def plan_date_night(brief):
    parsed = parse_brief(brief)
    fingerprint = build_fingerprint(parsed["seeds"])
    recs = gather_recommendations(fingerprint)
    return {
        "brief": brief,
        "parsed": parsed,
        "fingerprint": fingerprint,
        "recommendations": recs,
        "itinerary": narrate(parsed, fingerprint, recs),
        "mock": not bool(os.environ.get("QLOO_API_KEY")),
    }


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        data = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open(os.path.join("static", "index.html"), "rb") as f:
                self._send(200, f.read(), "text/html")
        elif self.path == "/api/health":
            self._send(200, json.dumps({"ok": True,
                                       "mock": not bool(os.environ.get("QLOO_API_KEY"))}))
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def do_POST(self):
        if self.path != "/api/plan":
            return self._send(404, json.dumps({"error": "not found"}))
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length).decode() or "{}")
        except json.JSONDecodeError:
            return self._send(400, json.dumps({"error": "invalid JSON"}))
        brief = (body.get("brief") or "").strip()
        if not brief:
            return self._send(400, json.dumps({"error": "brief is required"}))
        try:
            self._send(200, json.dumps(plan_date_night(brief)))
        except Exception as exc:
            self._send(500, json.dumps({"error": str(exc)}))

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    HTTPServer(("127.0.0.1", port), Handler).serve_forever()
    print(f"DateNight Agent on http://127.0.0.1:{port}")
