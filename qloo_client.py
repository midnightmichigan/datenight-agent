"""Qloo Taste API client with a mock fallback.

Real mode: set QLOO_API_KEY (free hackathon key via the Google Form linked
from https://qloo.devpost.com/rules). Optional QLOO_BASE_URL override.
Endpoints (verified against the Qloo docs + prior hackathon builds):
  GET {base}/search?query=...&limit=N          -> entity candidates
  GET {base}/v2/insights?filter.type=...&signal.interests.entities=...&take=N
Mock mode: when no key is set, returns deterministic fake entities/insights
so the app and judges run the full agentic flow with zero configuration.
"""
import json
import os
import time
import urllib.parse
import urllib.request

BASE = os.environ.get("QLOO_BASE_URL", "https://hackathon.api.qloo.com")
# NOTE: confirm the base URL against the key-issuance email for the 2026
# Agentic Hackathon; prior hackathons used hackathon.api.qloo.com.


def _headers():
    return {"X-Api-Key": os.environ["QLOO_API_KEY"],
            "accept": "application/json"}


def _get(path, params):
    url = BASE + path + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=_headers())
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def search_entities(query, limit=5):
    """Resolve a taste seed (e.g. 'Wes Anderson') to Qloo entity IDs."""
    if not os.environ.get("QLOO_API_KEY"):
        return _mock_search(query, limit)
    data = _get("/search", {"query": query, "limit": limit})
    out = []
    for e in data.get("results", [])[:limit]:
        types = e.get("types") or []
        out.append({"id": e.get("entity_id") or e.get("id"),
                    "name": e.get("name", query),
                    "type": types[0] if types else ""})
    return out


def insights(entity_ids, filter_type, take=6):
    """Cross-domain recommendations seeded by entity IDs.

    filter_type: a supported Qloo filter.type (urn:entity:movie,
    urn:entity:place, urn:entity:destination, ...). Friendly aliases
    ('restaurant' -> urn:entity:place, 'film' -> urn:entity:movie, ...)
    are also accepted.
    """
    resolved = _resolve_filter_type(filter_type)
    if not os.environ.get("QLOO_API_KEY"):
        return _mock_insights(resolved, take)
    data = _get("/v2/insights", {
        "filter.type": resolved,
        "signal.interests.entities": ",".join(entity_ids),
        "take": take,
    })
    results = data.get("results", {})
    items = []
    # v2 returns results grouped; flatten defensively.
    groups = results.values() if isinstance(results, dict) else results
    for group in groups:
        for e in (group if isinstance(group, list) else []):
            items.append({
                "name": e.get("name", "Unknown"),
                "affinity": round(float(e.get("affinity", 0)), 3),
                "type": resolved,
                "entity_id": e.get("entity_id"),
            })
    return sorted(items, key=lambda x: x["affinity"], reverse=True)[:take]


# Supported filter.type values for the Qloo Agentic Hackathon
# (https://docs.qloo.com/reference/qloo-llm-hackathon-developer-guide).
# Food & beverage: use urn:entity:place, not urn:entity:restaurant.
FILTER_TYPE_ALIASES = {
    "restaurant": "urn:entity:place",
    "dinner": "urn:entity:place",
    "evening_stroll": "urn:entity:destination",
    "movie": "urn:entity:movie",
    "film": "urn:entity:movie",
    "tv": "urn:entity:tv_show",
    "music": "urn:entity:artist",
    "artist": "urn:entity:artist",
    "book": "urn:entity:book",
    "brand": "urn:entity:brand",
    "place": "urn:entity:place",
    "destination": "urn:entity:destination",
    "podcast": "urn:entity:podcast",
    "video_game": "urn:entity:video_game",
}


def _resolve_filter_type(filter_type):
    # Normalize BOTH full URNs and short names through the alias map —
    # urn:entity:restaurant is rejected by the 2026 hackathon API, so it
    # must resolve to urn:entity:place even when passed as a full URN.
    key = filter_type
    if key.startswith("urn:entity:"):
        key = key[len("urn:entity:"):]
    return FILTER_TYPE_ALIASES.get(key.lower(), filter_type)

def _mock_search(query, limit):
    seed = abs(hash(query)) % 100000
    return [{"id": f"urn:entity:mock:{seed + i}",
             "name": query.title(),
             "type": "mock"} for i in range(limit)]


def _mock_insights(filter_type, take):
    kind = filter_type.split(":")[-1]
    banks = {
        "restaurant": ["The Velvet Fork", "Ember & Oak", "Juniper Table",
                       "Copper Spoon", "Wild Thyme", "Marigold Room"],
        "movie": ["Moonrise Reverie", "The Grand Budapest of Us",
                  "Paper Moons", "Static Bloom", "Amber Reel",
                  "The Night Projectionist"],
        "place": ["Riverside Walk", "Old Mill District", "Lantern Alley",
                  "Hilltop Gardens", "The Foundry Lofts", "Cedar Pier"],
        "brand": ["Field Notes Supply", "Analog Club", "Woven & Co.",
                  "Slowline", "Paper Trail Goods", "Kindred Audio"],
    }
    names = banks.get(kind, banks["place"])
    return [{"name": n,
             "affinity": round(0.95 - i * 0.06, 3),
             "type": filter_type,
             "entity_id": f"urn:entity:mock:{kind}:{i}",
             "mock": True} for i, n in enumerate(names[:take])]
