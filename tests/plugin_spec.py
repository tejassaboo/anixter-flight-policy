"""The handbook-specific settings the template's acceptance tests read. Every other file in tests/ is the
template's and stays identical across plugins (see TEMPLATE_GUIDE.md)."""

from pathlib import Path

import contract

ROOT = Path(__file__).resolve().parents[1]

# Ids that are published or taken: a new plugin never reuses one (MASTER_PLAN section 4, "id check").
PUBLISHED_IDS = {
    "aiib-delegation-entitlement", "ec-mission-cabin-allowance", "ftr-city-pair-fare-selection",
    "gates-vendor-flight-ranking", "njc-cabin-meal-allowance", "sfc-travel-preapproval", "uc-g28-expense-audit",
    "un-staff-air-travel-audit", "vt-airfare-policy-booking", "wa-saam-travel-versioned-audit",
    "energy-corporate-flight-booking", "pharma-distributor-flight-booking", "shipping-company-flight-booking",
    "telecommunications-flight-booking", "preference-aware-flight-booking", "llm-context-compress",
    "weather-alert", "word-check", "arxiv-source",
}

# The frozen original's SHA256SUMS, when this checkout sits beside pilot_work/ (skipped elsewhere).
FROZEN_SHA256SUMS = ROOT.parents[1] / "pilot_work" / "originals" / "anixter" / "frozen" / "SHA256SUMS"

# Scenario mix by primary category (EDGE_CASES.md section 5.2; the 32-scenario row).
MIX = {"easy": 6, "boundary_twin": 8, "multi_rule": 5, "hidden_clause": 3, "distractor": 3, "refusal": 3, "flag": 4}

# Overlay minimums (EDGE_CASES.md section 5.3) for the rules this handbook has.
OVERLAY_MINIMUMS = {
    "multi_leg": 3, "date_arithmetic": 2, "month_end": 1, "personal_travel": 1, "multi_traveller": 1,
    "dearer_option": 2, "upgrade_not_taken": 2, "outside_air_section": 2,
}

# Words a scenario id may not contain beyond the template's universal list: this handbook's rule and role
# terms.
ID_FORBIDDEN_TERMS = {
    "coach", "economy", "business", "premium", "customer", "spouse", "wife", "husband", "companion", "guest",
    "senior", "executive", "vice", "president", "treasury", "regional", "manager", "supervisor", "domestic",
    "international", "mexico", "canada", "caribbean", "layover", "connection", "nonstop", "preferred", "miles",
    "loyalty", "status", "refundable", "hidden", "city", "beyond", "skiplag", "personal", "vacation", "holiday",
    "extended", "later", "saturday", "combined", "approval", "written", "prior", "self", "disability", "agency",
}

# The handbook-specific enums whose member words a scenario id may not contain either.
ID_CATEGORY_ENUMS = [contract.Passenger, contract.Purpose, contract.ExtraDays, contract.ApprovalSubject]

# How many scenarios a degenerate agent may pass: one that always holds the right offer for approval, and
# one that always books the cheapest seat (with the right section). Set to what each actually passes (README).
MAX_PASS_ALWAYS_FLAG = 3
MAX_PASS_ALWAYS_LOWEST = 5  # NONE is accepted on every BOOK (sync 4'): birch-lagoon, flint-marsh, garnet-rill,
# walnut-spur, zinnia-loch (zinnia-loch declines the airline on the lowest-fare rule itself, lines 107-108,
# so LOWEST_FARE stays there; no other booking that declines a request accepts it)

# Hand-built duration cases beyond the automatic both-sides tests: (rule, outbound scheduled minutes per
# flight, layovers, expected True / False / None for unclear). coach-flight is per flight, with connections
# unclear when every flight is within five hours but their sum is over; business-flying-time adds the flights'
# minutes and leaves the layovers out.
DURATION_CASES = [
    ("coach-flight", [301], [], True),
    ("coach-flight", [300], [], False),
    ("coach-flight", [140, 150], [120], False),  # 290 flying, 410 elapsed: within on every reading
    ("coach-flight", [150, 150], [240], False),  # exactly 300 flying: within
    ("coach-flight", [290, 275], [85], None),  # each flight within, total over: unclear
    ("coach-flight", [400, 90], [60], None),  # one flight over, one within: unclear
    ("coach-flight", [320, 310], [70], True),  # every flight over
    ("business-flying-time", [301], [], True),
    ("business-flying-time", [300], [], False),
    ("business-flying-time", [140, 160], [300], False),  # 300 flying, layover left out
    ("business-flying-time", [140, 161], [30], True),  # 301 flying
    ("business-flying-time", [100, 100, 101], [60, 60], True),
]
