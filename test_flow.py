"""Smoke test: full agentic loop in mock mode (no API keys needed)."""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agent import plan_date_night

brief = ("Plan a date night for someone who loves Wes Anderson films "
         "and Taylor Swift, in Chicago")
plan = plan_date_night(brief)

assert plan["parsed"]["seeds"], "no seeds parsed"
assert plan["fingerprint"], "empty taste fingerprint"
for domain in ("dinner", "film", "stroll"):
    assert plan["recommendations"].get(domain), f"no {domain} recs"
assert plan["itinerary"], "empty itinerary"

print("seeds:", plan["parsed"]["seeds"])
print("fingerprint:", [e["name"] for e in plan["fingerprint"]])
for domain, items in plan["recommendations"].items():
    print(f"{domain}: {[i['name'] for i in items]}")
print("\n--- itinerary ---")
print(plan["itinerary"])
print("\nALL TESTS PASSED (mock mode)")
