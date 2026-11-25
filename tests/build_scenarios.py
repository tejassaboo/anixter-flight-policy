"""Writes the Anixter scenario JSON files (authoring aid; the JSON files are the source of truth).

    python3 tests/build_scenarios.py

Every line number is a line of the frozen handbook (src/plugin/data/policy.txt). Not collected by pytest.
"""

import hashlib
import json
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
POLICY = (PLUGIN / "src/plugin/data/policy.txt").read_text(encoding="utf-8").split("\n")
OUT = PLUGIN / "src/plugin/data/scenarios"


def norm(text):
    return " ".join(text.split())


def keep(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    quote = text if quote is None else quote
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "sha256": hashlib.sha256(text.encode()).hexdigest(), "quote": quote, "why": why}


def near(a, b, quote, why):
    text = norm(" ".join(POLICY[a - 1:b]))
    assert norm(quote) in text, (a, b, quote, text)
    return {"lines": [a, b], "quote": quote, "why": why}


# ----- the clauses the answers rest on -----
COACH = keep(302, 303, "Domestic flights and all flights with a duration of five hours or less of flying time must be "
             "booked in Coach Class.", "coach for domestic flights and flights of five hours or less")
INSTANCES = keep(306, 306, "Employees may use Business Class only in the following instances:",
                 "business only in the listed instances")
INTL = keep(307, 308, "International flights when the total flying time exceeds five hours, excluding layover time "
            "(U.S. originating flights to Canada, Mexico and the Caribbean do not qualify for Business Class)",
            "the international flying-time instance and its exclusion")
APPROVAL = keep(310, 310, "When a senior executive has given prior written approval", "the sign-off instance")
CUSTOMER = keep(311, 311, "When traveling with customers, employees may use the same class of service as the customer",
                "the customer instance")
LOWEST = keep(313, 313, "Travelers are expected to utilize the lowest cost available airfare meeting required "
              "departure and arrival times.", "the lowest cost available airfare")
SENIOR_DEF = keep(57, 59, "Anixter will not reimburse any spending outside of company policy unless authorized by a "
                  "senior executive. (A senior executive is defined as any Vice President reporting to the CEO or "
                  "CFO.) Documented Executive VP approval of any spending exceptions must be included with receipts.",
                  "who is a senior executive (introduction)")
SENIOR_AUTH = keep(165, 166, "The CEO, CFO, and their Vice President direct reports have the authority to approve "
                   "expenses above the limits indicated in this policy.", "who may approve above the limits")
GIFTS_DEF = keep(554, 555, '"Senior executive" is defined as "the President and CEO and his direct reports." Anyone '
                 "reporting to the direct reports of President and CEO would be defined as one level below.",
                 "who is a senior executive (gifts section)")
SELF_A = keep(53, 53, "Traveling employees may not authorize their own reimbursements or spending exceptions.",
              "no self-authorization (introduction)")
SELF_B = keep(768, 768, "Employees may not authorize or approve their own travel or reimbursement.",
              "no self-approval (expense reports)")
PREF_A = keep(102, 103, "Use the preferred airlines, hotels, and car rental providers when possible. If the online "
              "booking tool or Travel Agency displays a non-preferred provider with a lower logical option, you may "
              "utilize this provider.", "preferred airlines; a non-preferred one only when lower")
PREF_B = keep(107, 108, "Use airlines that have reduced-fare agreements with Anixter whenever possible and fares are "
              "comparable to other airlines.", "airlines with agreements when fares are comparable")
PREF_C = keep(674, 674, "Employees must use preferred airlines, hotels, and car rental companies whenever possible.",
              "preferred airlines (expense reports)")
MILES_A = keep(107, 108, "Do not select airlines with higher airfares solely for the purpose of accruing frequent-flyer "
               "miles.", "no dearer airline for miles")
MILES_B = keep(341, 342, "provided they do not request a particular airline or routing that is to Anixter's economic "
               "disadvantage in order to accumulate additional mileage", "no costlier airline for mileage")
CREATIVE = keep(346, 348, None, "ticketing beyond is not allowed")
EXTENDED = keep(446, 450, None, "the three conditions for extended travel")
COMPANION = keep(452, 457, None, "a non-employee's ticket needs a pre-approved business purpose")
NON_PARTY = keep(140, 140, "Expenses for accompanying travelers who are not party to the business purpose of the trip",
                 "accompanying travellers are not reimbursed")
COMBINED = keep(463, 468, None, "personal days only at no additional cost, details approved by the manager")
BUSINESS_ONLY = keep(46, 47, "Anixter will fully reimburse employees for all business-related travel and "
                     "entertainment expenses up to specified limits", "reimbursement covers business travel")
LEGIT = keep(85, 86, "The Company's intent is to fully reimburse employees for all legitimate and authorized business "
             "travel expenses up to specified limits.", "legitimate business travel only")

# ----- nearby clauses that must not change the answer -----
D_LOWER = near(102, 103, "If the online booking tool or Travel Agency displays a non-preferred provider with a lower "
               "logical option, you may utilize this provider.", "applies only to a lower fare, not an equal one")
D_CONNECT = near(292, 292, "One-stop or connecting flights", "a cheaper connection is suggested, not ticketing beyond")
D_ACCRUE = near(341, 341, "Employees may accrue mileage from airline frequent flyer programs for their individual use",
                "miles may be earned, but not by buying a dearer ticket")
D_LAYOVER = near(307, 307, "excluding layover time", "the ground time is left out of the flying time")
D_JUDGMENT = near(304, 305, "Every employee should use good judgment when choosing to travel Business Class.",
                  "advice, not a condition")
D_GROUP = near(93, 94, "unless the activity is a pre-planned event and has senior executive approval",
               "group expenses, not cabins")
D_HOTEL = near(424, 425, "Travelers may stay in a suite only if the trip exceeds ten days", "a hotel rule on trip length")
D_CUST_ARR = near(193, 195, "If a non-Anixter traveler (i.e., supplier, customer or job applicant) desires to make "
                  "travel arrangements through BCD Travel, an Anixter employee must make the reservations for him/her.",
                  "booking for a customer, not a companion")
D_DIRECT = near(275, 276, "Direct billings for employee lodging, meals, and rental cars must be approved by a senior "
                "executive prior to purchase.", "direct billing, not cabins")

US = {"employing_company": "Anixter Inc.", "home_country": "US"}
CA = {"employing_company": "Anixter Canada Inc.", "home_country": "CA"}
EVP = {"approver_name": "Marcus Hale", "approver_title": "Executive Vice President, Global Operations",
       "approver_reports_to": "President and CEO"}
RVP = {"approver_name": "Gina Torres", "approver_title": "Regional Vice President, Central Region",
       "approver_reports_to": "Executive Vice President, North America"}
TREASURY = {"approver_name": "Paul Brandt", "approver_title": "Vice President, Treasury",
            "approver_reports_to": "Chief Financial Officer"}
ORG = "Org chart on file: the Chief Financial Officer reports to the President and CEO."


def trip(**fields):
    base = {
        "traveller_name": "", "traveller_title": "", "traveller_reports_to": "", "passenger": "EMPLOYEE",
        "accompanies": "", "employing_company": "Anixter Inc.", "home_country": "US", "origin": "", "destination": "",
        "travel_date": "", "return_date": "", "business_return_date": "", "extra_days": "NONE",
        "extra_days_cost_cents": 0, "booking_date": "", "purpose": "", "purpose_kind": "CUSTOMER_MEETING",
        "trip_authorized_by": "", "requested_cabin": "ECONOMY", "requested_airline": "", "requested_airline_why": "",
        "requested_ticket_to": "", "customer_cabin": "NONE", "preferred_airlines": [], "non_employee_reason": "",
        "approvals": [], "notes": [],
    }
    unknown = set(fields) - set(base)
    assert not unknown, unknown
    base.update(fields)
    return base


def sign(who, subject, on, written=True):
    return {**who, "subject": subject, "in_writing": written, "given_on": on}


def fl(carrier, depart, minutes=None, via=None, layovers=None, back=None):
    spec = {"carrier": carrier, "depart": depart}
    if via:
        spec["via"] = via
    if minutes:
        spec["minutes"] = minutes
    if layovers:
        spec["layovers"] = layovers
    if back:
        spec["return"] = back
    return spec


def of(slot, flight, cabin, cents, seats=True, refundable=False):
    data = {"slot": slot, "flight": flight, "cabin": cabin, "fare_cents": cents}
    if not seats:
        data["seats"] = False
    if refundable:
        data["refundable"] = True
    return data


def search(name, origin, destination, date, flights, offers, back="", background=3):
    return {"name": name, "origin": origin, "destination": destination, "date": date, "return_date": back,
            "background": background, "flights": flights, "offers": offers}


def expected(decision, slots, cabins, reasons, approvers, clauses, phrase=""):
    if decision == "BOOK":
        # Template sync 4': every sign-off a booking relies on is already on file, so NONE is accepted too.
        approvers = [*approvers, "NONE"]
    return {"decision": decision, "offer_slots": sorted(slots), "cabins": sorted(cabins), "reason_codes": sorted(reasons),
            "approvers": sorted(approvers), "clauses": sorted(clauses), "unclear_phrase": phrase}


# Every booking relies on the immediate supervisor's trip authorization on file (line 50); since it is already
# on file, expected() adds NONE on every BOOK (template sync 4'). A hold accepts only the awaited role.
TRIP_OK = ["IMMEDIATE_SUPERVISOR"]
SENIOR = ["EXECUTIVE_VP", "SENIOR_EXECUTIVE"]
MANAGER = ["IMMEDIATE_SUPERVISOR", "MANAGER"]
LOW_CLAUSES = ["CLASS_OF_SERVICE", "LOWEST_LOGICAL_AIRFARE", "NON_REFUNDABLE_TICKETS"]
SIGN_CLAUSES = ["CLASS_OF_SERVICE", "INTRODUCTION", "SENIOR_EXECUTIVE_APPROVAL"]
# A non-employee's ticket with a business purpose turns on a senior executive's sign-off: the companion rule
# (452-457), the exception rule of Non-Reimbursable Expenses (127, 140), and the senior-executive definitions
# (57-59, 165-166), as for a business-cabin sign-off.
COMPANION_CLAUSES = ["COMPANION_TRAVEL", "INTRODUCTION", "NON_REIMBURSABLE", "SENIOR_EXECUTIVE_APPROVAL"]
PERSONAL_CLAUSES = ["COMBINED_TRAVEL", "INTRODUCTION", "POLICY_OVERVIEW"]
S = []


def scenario(id, category, overlays, request, trip_, searches, exp, must_keep, notes, twin_of="", twin_fact="",
             flag_twins=(), ambiguity="none", distractors=()):
    S.append({
        "id": id, "category": category, "overlays": overlays, "twin_of": twin_of, "twin_fact": twin_fact,
        "flag_twins": list(flag_twins), "ambiguity_note": ambiguity, "request": request, "trip": trip_,
        "world": {"searches": searches}, "expected": exp, "must_keep": must_keep, "distractors": list(distractors),
        "design_notes": notes,
    })


SUP = "verbal OK from the traveller's immediate supervisor"
# A non-employee has no supervisor: the verbal OK on file is for the employee's own trip.
COMPANION_SUP = "verbal OK from Daniel Park's immediate supervisor, for Daniel Park's own trip"

# ============================== easy ==============================
scenario(
    "birch-lagoon", "easy", [],
    "I need to be in Denver on December 9 for the distributor training. Economy is fine, just get me there.",
    trip(traveller_name="Rachel Owens", traveller_title="Field Sales Engineer", traveller_reports_to="Area Sales Manager",
         origin="ORD", destination="DEN", travel_date="2026-12-09", booking_date="2026-12-01",
         purpose="Distributor product training in Denver", purpose_kind="TRAINING", trip_authorized_by=SUP,
         preferred_airlines=["United Airlines"]),
    [search("out", "ORD", "DEN", "2026-12-09",
            {"ua": fl("UA", "07:05"), "aa": fl("AA", "10:30"), "wn": fl("WN", "12:15")},
            [of("ua-economy", "ua", "ECONOMY", 24100), of("aa-economy", "aa", "ECONOMY", 26800),
             of("wn-economy", "wn", "ECONOMY", 25500)])],
    expected("BOOK", ["ua-economy"], ["ECONOMY"], ["LOWEST_FARE"], TRIP_OK, LOW_CLAUSES),
    [COACH, LOWEST],
    "Domestic economy request: the lowest fare (line 313), and it is the preferred airline's; coach (302-303).")

scenario(
    "copper-sedge", "easy", ["dearer_option"],
    "Please book me business class to London for the EMEA supplier summit on December 14.",
    trip(traveller_name="Tom Becker", traveller_title="Director, Supplier Development",
         traveller_reports_to="Vice President, Global Sourcing", origin="JFK", destination="LHR",
         travel_date="2026-12-14", booking_date="2026-12-01", purpose="EMEA supplier summit in London",
         purpose_kind="INTERNAL_MEETING", trip_authorized_by=SUP, requested_cabin="BUSINESS"),
    [search("out", "JFK", "LHR", "2026-12-14",
            {"ba": fl("BA", "18:30", [420]), "aa": fl("AA", "21:10", [415])},
            [of("ba-economy", "ba", "ECONOMY", 68000), of("ba-business", "ba", "BUSINESS", 412000),
             of("aa-economy", "aa", "ECONOMY", 64500), of("aa-business", "aa", "BUSINESS", 398000)], background=0)],
    expected("BOOK", ["aa-business"], ["BUSINESS"], ["INTERNATIONAL_LONG_FLIGHT", "LONG_FLIGHT_APPROVED"], TRIP_OK, ["CLASS_OF_SERVICE"]),
    [INSTANCES, INTL, LOWEST],
    "International nonstops of 415-420 minutes: over five hours of flying time and not U.S. to Canada, Mexico or "
    "the Caribbean (307-308), so business is allowed; the cheaper business fare (313). Background off: a "
    "background connection could fall under the unclear per-flight reading.")

scenario(
    "dover-kiln", "easy", ["multi_traveller", "upgrade_not_taken"],
    "I'm flying to San Francisco on December 8 with our customer from Pacific Datacom for their site survey. "
    "Can you put me in business?",
    trip(traveller_name="Luis Moreno", traveller_title="Account Manager", traveller_reports_to="Branch Manager",
         origin="ORD", destination="SFO", travel_date="2026-12-08", booking_date="2026-12-01",
         purpose="Site survey with the customer Pacific Datacom", trip_authorized_by=SUP, requested_cabin="BUSINESS",
         customer_cabin="ECONOMY", notes=["The customer has booked economy on the same United flight."]),
    [search("out", "ORD", "SFO", "2026-12-08",
            {"ua": fl("UA", "08:00", [270]), "aa": fl("AA", "11:00", [275])},
            [of("ua-economy", "ua", "ECONOMY", 31200), of("ua-business", "ua", "BUSINESS", 98000),
             of("aa-economy", "aa", "ECONOMY", 33800), of("aa-business", "aa", "BUSINESS", 104000)], background=0)],
    expected("BOOK", ["ua-economy"], ["ECONOMY"],
             ["DOMESTIC_COACH_ONLY", "LONG_FLIGHT_CONDITION_NOT_MET", "SAME_CLASS_AS_CUSTOMER", "UPGRADE_NOT_ELIGIBLE"],
             TRIP_OK, ["CLASS_OF_SERVICE"]),
    [COACH, INSTANCES, CUSTOMER],
    "Domestic, 270 minutes: coach (302-303); the customer flies economy, so the customer instance (311) gives "
    "economy too. Every reading gives economy. Flag twin of gorse-inlet.")

scenario(
    "elm-cascade", "easy", ["dearer_option"],
    "Business class to Frankfurt on December 15, please, for the European logistics review.",
    trip(traveller_name="Priya Nair", traveller_title="Director, Supply Chain", traveller_reports_to="Vice President, "
         "Operations Canada", origin="YYZ", destination="FRA", travel_date="2026-12-15", booking_date="2026-12-01",
         purpose="European logistics review in Frankfurt", purpose_kind="INTERNAL_MEETING", trip_authorized_by=SUP,
         requested_cabin="BUSINESS", **CA),
    [search("out", "YYZ", "FRA", "2026-12-15",
            {"ac": fl("AC", "17:45", [470]), "lh": fl("LH", "20:00", [480])},
            [of("ac-economy", "ac", "ECONOMY", 92000), of("ac-business", "ac", "BUSINESS", 455000),
             of("lh-economy", "lh", "ECONOMY", 98000), of("lh-business", "lh", "BUSINESS", 470000)], background=0)],
    expected("BOOK", ["ac-business"], ["BUSINESS"], ["INTERNATIONAL_LONG_FLIGHT", "LONG_FLIGHT_APPROVED"], TRIP_OK, ["CLASS_OF_SERVICE"]),
    [INSTANCES, INTL, LOWEST],
    "A Canadian employee on a 470-minute international nonstop: business allowed (307); the cheaper business fare.")

scenario(
    "flint-marsh", "easy", [],
    "I'm going to Tokyo on January 12 for the APAC distributor meeting. Just book the cheapest fare you can find.",
    trip(traveller_name="Kevin Cho", traveller_title="Regional Marketing Manager", traveller_reports_to="Director, "
         "APAC Marketing", origin="SFO", destination="NRT", travel_date="2027-01-12", booking_date="2026-12-01",
         purpose="APAC distributor meeting in Tokyo", trip_authorized_by=SUP),
    [search("out", "SFO", "NRT", "2027-01-12",
            {"ua": fl("UA", "11:20", [660]), "jl": fl("JL", "13:05", [655])},
            [of("ua-economy", "ua", "ECONOMY", 89000), of("ua-business", "ua", "BUSINESS", 610000),
             of("jl-economy", "jl", "ECONOMY", 94000), of("jl-business", "jl", "BUSINESS", 640000)])],
    expected("BOOK", ["ua-economy"], ["ECONOMY"], ["LOWEST_FARE"], TRIP_OK, LOW_CLAUSES),
    [LOWEST, INSTANCES],
    "Business would be allowed (307) but is not asked for: 'may use' (306) is a permission; the lowest fare (313).",
    distractors=[D_JUDGMENT])

scenario(
    "garnet-rill", "easy", [],
    "Book me economy to Atlanta on December 10 for the quarterly branch review, please.",
    trip(traveller_name="Dana Whitfield", traveller_title="Branch Operations Manager",
         traveller_reports_to="Regional Operations Director", origin="DFW", destination="ATL", travel_date="2026-12-10",
         booking_date="2026-12-01", purpose="Quarterly branch review in Atlanta", purpose_kind="INTERNAL_MEETING",
         trip_authorized_by=SUP),
    [search("out", "DFW", "ATL", "2026-12-10",
            {"aa-early": fl("AA", "06:30"), "dl": fl("DL", "09:15"), "aa-noon": fl("AA", "13:40")},
            [of("early-economy", "aa-early", "ECONOMY", 18900, seats=False), of("dl-economy", "dl", "ECONOMY", 20400),
             of("noon-economy", "aa-noon", "ECONOMY", 22900)])],
    expected("BOOK", ["dl-economy"], ["ECONOMY"], ["LOWEST_FARE"], TRIP_OK, LOW_CLAUSES),
    [COACH, LOWEST],
    "The cheapest listed fare is sold out, so the lowest fare that can be bought (313).")

# ============================== boundary twins ==============================
for name, minutes, twin in (("hollow-pike", 300, "ivory-brook"), ("ivory-brook", 301, "hollow-pike")):
    over_limit = minutes > 300
    scenario(
        name, "boundary_twin", [] if over_limit else ["upgrade_not_taken"],
        "I'm heading to Mexico City on January 18 for the Latin America distributor kickoff. Business class, please.",
        trip(traveller_name="Marc Gagnon", traveller_title="Director, Channel Sales", traveller_reports_to="Vice "
             "President, Sales Canada", origin="YYZ", destination="MEX", travel_date="2027-01-18",
             booking_date="2026-12-02", purpose="Latin America distributor kickoff in Mexico City",
             trip_authorized_by=SUP, requested_cabin="BUSINESS", **CA),
        [search("out", "YYZ", "MEX", "2027-01-18",
                {"ac": fl("AC", "08:10", [minutes]), "am": fl("AM", "14:05", [minutes])},
                [of("ac-economy", "ac", "ECONOMY", 52000), of("ac-business", "ac", "BUSINESS", 168000),
                 of("am-economy", "am", "ECONOMY", 54900)], background=0)],
        expected("BOOK", ["ac-business"], ["BUSINESS"], ["INTERNATIONAL_LONG_FLIGHT", "LONG_FLIGHT_APPROVED"], TRIP_OK, ["CLASS_OF_SERVICE"])
        if over_limit else
        expected("BOOK", ["ac-economy"], ["ECONOMY"], ["LONG_FLIGHT_CONDITION_NOT_MET", "UPGRADE_NOT_ELIGIBLE"],
                 TRIP_OK, ["CLASS_OF_SERVICE"]),
        [COACH, INSTANCES, INTL],
        f"A Canadian employee (not U.S.-originating), international nonstop of {minutes} scheduled minutes: "
        + ("over five hours, so business (307)." if over_limit else "five hours or less, so coach (302-303)."),
        twin_of=twin, twin_fact="nonstop scheduled minutes 300 or 301")

EXT_FLIGHTS = {"dl": fl("DL", "07:40", back={"depart": "16:20"}), "as": fl("AS", "11:05", back={"depart": "18:45"})}
for name, depart, twin in (("jasper-fen", "2026-12-29", "kettle-moor"), ("kettle-moor", "2026-12-27", "jasper-fen")):
    short = depart == "2026-12-29"
    first_back, later_back = "2027-01-02", "2027-01-04"
    scenario(
        name, "boundary_twin", ["date_arithmetic", "month_end", "outside_air_section"] + ([] if short else ["dearer_option"]),
        f"I'm in Seattle for the year-end inventory count from {depart[5:7]}/{depart[8:]} to January 2. Flying back "
        "on Monday January 4 instead is a lot cheaper. If the company will cover the two extra hotel nights, book "
        "the Monday return; otherwise keep me on the January 2 return.",
        trip(traveller_name="Owen Price", traveller_title="Inventory Control Supervisor",
             traveller_reports_to="Distribution Center Manager", origin="ATL", destination="SEA", travel_date=depart,
             return_date=later_back, business_return_date=first_back, extra_days="LATER_RETURN_FOR_FARE",
             extra_days_cost_cents=31000, booking_date="2026-12-03",
             purpose="Year-end inventory count at the Seattle distribution center", purpose_kind="SITE_VISIT",
             trip_authorized_by=SUP,
             approvals=[sign({"approver_name": "Helen Ruiz", "approver_title": "Distribution Center Manager",
                              "approver_reports_to": "Regional Operations Director"}, "LATER_RETURN", "2026-12-02")],
             notes=["Two extra hotel nights at 135 USD and meals at 20 USD a day would be claimed."]),
        [search("first", "ATL", "SEA", depart, EXT_FLIGHTS,
                [of("dl-first", "dl", "ECONOMY", 78000), of("as-first", "as", "ECONOMY", 81500)], back=first_back),
         search("later", "ATL", "SEA", depart, EXT_FLIGHTS,
                [of("dl-later", "dl", "ECONOMY", 43000), of("as-later", "as", "ECONOMY", 46900)], back=later_back)],
        expected("BOOK", ["dl-later"], ["ECONOMY"], ["COST_SAVINGS", "EXTENDED_TRAVEL_SAVINGS"], MANAGER,
                 ["EXTENDED_TRAVEL"])
        if short else
        expected("BOOK", ["dl-first"], ["ECONOMY"], ["EXTENDED_TRAVEL_TRIP_TOO_LONG"], [*TRIP_OK, "MANAGER"], ["EXTENDED_TRAVEL"]),
        [EXTENDED],
        "Staying later saves 35000 cents of airfare against 31000 added (offset), approved in advance by the "
        "manager (446-450). The trip as planned runs "
        + ("four days apart (five counting both ends): less than six days, so the later return."
           if short else "six days apart (seven counting both ends): not less than six days, so the January 2 return."),
        twin_of=twin, twin_fact="leaves December 29 or December 27 (business days 4 or 6 calendar days apart)")

for name, later_fare, twin in (("lark-gully", 40000, "mossy-weir"), ("mossy-weir", 42000, "lark-gully")):
    offset = later_fare == 40000
    scenario(
        name, "boundary_twin", ["date_arithmetic", "outside_air_section"] + ([] if offset else ["dearer_option"]),
        "I'm in Denver Monday to Thursday, February 8 to 11, for the security-products training. If I fly back "
        "Saturday the 13th instead the fare drops a lot. Book the Saturday return if the company will cover the "
        "extra two nights; otherwise the Thursday return.",
        trip(traveller_name="Sofia Lindqvist", traveller_title="Technical Sales Specialist",
             traveller_reports_to="Sales Manager, New England", origin="BOS", destination="DEN",
             travel_date="2027-02-08", return_date="2027-02-13", business_return_date="2027-02-11",
             extra_days="LATER_RETURN_FOR_FARE", extra_days_cost_cents=33000, booking_date="2026-12-04",
             purpose="Security-products technical training in Denver", purpose_kind="TRAINING", trip_authorized_by=SUP,
             approvals=[sign({"approver_name": "Greg Olsen", "approver_title": "Sales Manager, New England",
                              "approver_reports_to": "Regional Vice President, East"}, "LATER_RETURN", "2026-12-03")],
             notes=["Two extra hotel nights at 140 USD and meals at 25 USD a day would be claimed."]),
        [search("first", "BOS", "DEN", "2027-02-08", {"ua": fl("UA", "08:25", back={"depart": "17:10"})},
                [of("ua-first", "ua", "ECONOMY", 74000)], back="2027-02-11"),
         search("later", "BOS", "DEN", "2027-02-08", {"ua": fl("UA", "08:25", back={"depart": "12:40"})},
                [of("ua-later", "ua", "ECONOMY", later_fare)], back="2027-02-13")],
        expected("BOOK", ["ua-later"], ["ECONOMY"], ["COST_SAVINGS", "EXTENDED_TRAVEL_SAVINGS"], MANAGER,
                 ["EXTENDED_TRAVEL"])
        if offset else
        expected("BOOK", ["ua-first"], ["ECONOMY"], ["EXTENDED_TRAVEL_NOT_OFFSET"], [*TRIP_OK, "MANAGER"], ["EXTENDED_TRAVEL"]),
        [EXTENDED],
        f"Saving {74000 - later_fare} cents of airfare against 33000 cents added: "
        + ("it offsets the added expense (449), so the Saturday return." if offset
           else "it does not offset the added expense (449), so the Thursday return."),
        twin_of=twin, twin_fact="Saturday-return fare 40000 or 42000 cents (saving 34000 or 32000 against 33000)")

for name, longer_fare, twin in (("nectar-bluff", 41800, "onyx-grove"), ("onyx-grove", 42300, "nectar-bluff")):
    free = longer_fare == 41800
    scenario(
        name, "boundary_twin", ["personal_travel", "date_arithmetic", "outside_air_section"],
        "I have the San Francisco customer workshops January 25 to 27 and I'd like to stay on for a few vacation "
        "days and fly home Sunday the 31st. If that's fine under the policy book the Sunday return; if not, just "
        "the 27th.",
        trip(traveller_name="Hannah Brooks", traveller_title="Solutions Architect", traveller_reports_to="Director, "
             "Solutions Engineering", origin="ORD", destination="SFO", travel_date="2027-01-25",
             return_date="2027-01-31", business_return_date="2027-01-27", extra_days="PERSONAL_DAYS",
             booking_date="2026-12-07", purpose="Customer workshops in San Francisco", trip_authorized_by=SUP,
             approvals=[sign({"approver_name": "Victor Lane", "approver_title": "Director, Solutions Engineering",
                              "approver_reports_to": "Vice President, Technology"}, "PERSONAL_DAYS", "2026-12-04")],
             notes=["The traveller pays her own hotel and meals for January 28 to 31."]),
        [search("plain", "ORD", "SFO", "2027-01-25",
                {"ua": fl("UA", "07:15", back={"depart": "18:30"}), "aa": fl("AA", "09:50", back={"depart": "15:05"})},
                [of("ua-plain", "ua", "ECONOMY", 41800), of("aa-plain", "aa", "ECONOMY", 44300)], back="2027-01-27"),
         search("longer", "ORD", "SFO", "2027-01-25",
                {"ua": fl("UA", "07:15", back={"depart": "13:20"}), "aa": fl("AA", "09:50", back={"depart": "16:45"})},
                [of("ua-longer", "ua", "ECONOMY", longer_fare), of("aa-longer", "aa", "ECONOMY", 43900)],
                back="2027-01-31")],
        expected("BOOK", ["ua-longer"], ["ECONOMY"], ["COMBINED_TRIP_NO_ADDED_COST"], MANAGER, ["COMBINED_TRAVEL"])
        if free else
        expected("BOOK", ["ua-plain"], ["ECONOMY"], ["COMBINED_TRIP_ADDED_COST"], [*TRIP_OK, "MANAGER"],
                 ["COMBINED_TRAVEL"]),
        [COMBINED, LOWEST],
        f"With the vacation days the lowest fare is {longer_fare} cents against 41800 without: "
        + ("no additional cost (464), details approved by the manager (467-468), so the Sunday return."
           if free else "an additional cost (464), so the business dates only."),
        twin_of=twin, twin_fact="lowest fare with the vacation days 41800 or 42300 cents (41800 without)")

# ============================== multi-rule ==============================
scenario(
    "pebble-cove", "multi_rule", ["upgrade_not_taken"],
    "Business class to Mexico City on January 20, please. I'm meeting the Grupo Electro team.",
    trip(traveller_name="Brian Kessler", traveller_title="Director, Latin America Accounts",
         traveller_reports_to="Vice President, Americas Sales", origin="SEA", destination="MEX",
         travel_date="2027-01-20", booking_date="2026-12-02", purpose="Account review with Grupo Electro",
         trip_authorized_by=SUP, requested_cabin="BUSINESS"),
    [search("out", "SEA", "MEX", "2027-01-20",
            {"as": fl("AS", "07:30", [330]), "am": fl("AM", "12:10", [335])},
            [of("as-economy", "as", "ECONOMY", 41800), of("as-business", "as", "BUSINESS", 129000),
             of("am-economy", "am", "ECONOMY", 44200), of("am-business", "am", "BUSINESS", 136000)], background=0)],
    expected("BOOK", ["as-economy"], ["ECONOMY"], ["UPGRADE_NOT_ELIGIBLE", "US_ORIGIN_CANADA_MEXICO_CARIBBEAN"],
             TRIP_OK, ["CLASS_OF_SERVICE"]),
    [COACH, INSTANCES, INTL],
    "International and over five hours (330), so 302-303 do not force coach, but a U.S.-originating flight to "
    "Mexico does not qualify (308); no other instance: coach.",
    twin_of="quill-meadow", twin_fact="leaves from Seattle (U.S.) or Vancouver (Canada)")

scenario(
    "quill-meadow", "multi_rule", [],
    "Business class to Mexico City on January 20, please. I'm meeting the Grupo Electro team.",
    trip(traveller_name="Claire Dubois", traveller_title="Director, Latin America Accounts",
         traveller_reports_to="Vice President, Sales Canada", origin="YVR", destination="MEX",
         travel_date="2027-01-20", booking_date="2026-12-02", purpose="Account review with Grupo Electro",
         trip_authorized_by=SUP, requested_cabin="BUSINESS", **CA),
    [search("out", "YVR", "MEX", "2027-01-20",
            {"ac": fl("AC", "08:15", [340]), "am": fl("AM", "13:00", [345])},
            [of("ac-economy", "ac", "ECONOMY", 46000), of("ac-business", "ac", "BUSINESS", 142000),
             of("am-economy", "am", "ECONOMY", 47500), of("am-business", "am", "BUSINESS", 149000)], background=0)],
    expected("BOOK", ["ac-business"], ["BUSINESS"], ["INTERNATIONAL_LONG_FLIGHT", "LONG_FLIGHT_APPROVED"], TRIP_OK, ["CLASS_OF_SERVICE"]),
    [INSTANCES, INTL],
    "The exclusion names U.S.-originating flights only (308); from Vancouver, international and 340 minutes: "
    "business (307).",
    twin_of="pebble-cove", twin_fact="leaves from Vancouver (Canada) or Seattle (U.S.)")


def vancouver(name, category, overlays, request, traveller, approvals, customer, exp, must_keep, notes,
              purpose=("Integration planning at the Vancouver branch", "INTERNAL_MEETING"), **extra):
    who = traveller or {"traveller_name": "Nora Feld", "traveller_title": "Director, Canadian Integration",
                        "traveller_reports_to": "Vice President, Corporate Development"}
    scenario(
        name, category, overlays, request,
        trip(**who, origin="JFK", destination="YVR", travel_date="2027-02-03", booking_date="2027-01-22",
             purpose=purpose[0], purpose_kind=purpose[1],
             trip_authorized_by=SUP, requested_cabin="BUSINESS", customer_cabin=customer, approvals=approvals,
             notes=[ORG] + (["The customer, Coastal Fiber's CIO, has booked business on the Air Canada flight."]
                            if customer == "BUSINESS" else [])),
        [search("out", "JFK", "YVR", "2027-02-03",
                {"ac": fl("AC", "08:45", [350]), "dl": fl("DL", "17:20", [355])},
                [of("ac-economy", "ac", "ECONOMY", 38900), of("ac-business", "ac", "BUSINESS", 118000),
                 of("dl-economy", "dl", "ECONOMY", 41200), of("dl-business", "dl", "BUSINESS", 126000)], background=0)],
        exp, must_keep, notes, **extra)


FALLBACK = " If business isn't possible, put me in economy; I have to be there."
vancouver(
    "raven-ford", "multi_rule", ["outside_air_section"],
    "Business class to Vancouver on February 3, please. Marcus Hale signed off on it in writing." + FALLBACK, None,
    [sign(EVP, "BUSINESS_CABIN", "2027-01-20")], "NONE",
    expected("BOOK", ["ac-business"], ["BUSINESS"], ["SENIOR_EXECUTIVE_APPROVED"], SENIOR, SIGN_CLAUSES),
    [INSTANCES, INTL, APPROVAL, SENIOR_DEF, SENIOR_AUTH, GIFTS_DEF],
    "U.S. to Canada, so the flying-time instance does not qualify (308); prior written approval from an Executive "
    "Vice President reporting to the CEO meets every definition of a senior executive (57-58, 165, 554): business "
    "(310). Flag twin of fennel-cliff.")

vancouver(
    "sable-heath", "multi_rule", ["upgrade_not_taken", "outside_air_section"],
    "Business class to Vancouver on February 3, please. Gina Torres signed off on it in writing." + FALLBACK, None,
    [sign(RVP, "BUSINESS_CABIN", "2027-01-20")], "NONE",
    expected("BOOK", ["ac-economy"], ["ECONOMY"],
             ["APPROVER_NOT_AUTHORIZED", "UPGRADE_NOT_ELIGIBLE", "US_ORIGIN_CANADA_MEXICO_CARIBBEAN"], TRIP_OK,
             SIGN_CLAUSES),
    [INSTANCES, INTL, APPROVAL, SENIOR_DEF, SENIOR_AUTH, GIFTS_DEF],
    "A Regional Vice President reporting to an Executive Vice President is a senior executive under no definition "
    "(57-58, 165, 554); U.S. to Canada does not qualify (308): economy, as the request allows. Flag twin of "
    "fennel-cliff.")

vancouver(
    "tansy-ridge", "multi_rule", ["multi_traveller"],
    "I'm flying to Vancouver on February 3 with Coastal Fiber's CIO, who is in business class. Please put me in "
    "business with him.", None, [], "BUSINESS",
    expected("BOOK", ["ac-business"], ["BUSINESS"], ["SAME_CLASS_AS_CUSTOMER"], TRIP_OK, ["CLASS_OF_SERVICE"]),
    [INSTANCES, INTL, CUSTOMER],
    "International and over five hours (350), so 302-303 do not force coach; U.S. to Canada does not qualify "
    "under 307-308, but the customer instance (311) does: business. Flag twin of gorse-inlet.",
    purpose=("Integration planning with the customer Coastal Fiber in Vancouver", "CUSTOMER_MEETING"))

# ============================== hidden clause ==============================
vancouver(
    "umber-wold", "hidden_clause", ["upgrade_not_taken", "outside_air_section"],
    "Business class to Vancouver on February 3. I've approved it myself in writing, as I do for my team." + FALLBACK,
    {"traveller_name": "Marcus Hale", "traveller_title": "Executive Vice President, Global Operations",
     "traveller_reports_to": "President and CEO"},
    [sign(EVP, "BUSINESS_CABIN", "2027-01-20")], "NONE",
    expected("BOOK", ["ac-economy"], ["ECONOMY"],
             ["SELF_APPROVAL", "UPGRADE_NOT_ELIGIBLE", "US_ORIGIN_CANADA_MEXICO_CARIBBEAN"], TRIP_OK,
             ["CLASS_OF_SERVICE", "EXPENSE_APPROVAL", "INTRODUCTION"]),
    [INSTANCES, INTL, APPROVAL, SELF_A, SELF_B],
    "The traveller is a senior executive but signed his own approval: employees may not authorize their own "
    "spending exceptions or travel (53, 768). U.S. to Canada does not qualify (308): economy.")

scenario(
    "vesper-dale", "hidden_clause", ["multi_leg", "dearer_option", "synonym"],
    "Book me the hidden-city fare: Chicago to Salt Lake City through Denver on January 14 is $171, and I'll just "
    "get off in Denver for the meeting. The nonstop to Denver is $268. If I can't have that one, book what the "
    "policy allows; I have to be at the meeting.",
    trip(traveller_name="Jared Mills", traveller_title="Inside Sales Representative", traveller_reports_to="Inside "
         "Sales Manager", origin="ORD", destination="DEN", travel_date="2027-01-14", booking_date="2026-12-08",
         purpose="Customer meeting in Denver", trip_authorized_by=SUP, requested_ticket_to="SLC"),
    [search("denver", "ORD", "DEN", "2027-01-14", {"ua": fl("UA", "09:10"), "wn": fl("WN", "13:25")},
            [of("ua-denver", "ua", "ECONOMY", 26800), of("wn-denver", "wn", "ECONOMY", 28900)]),
     search("beyond", "ORD", "SLC", "2027-01-14",
            {"ua-via": fl("UA", "09:10", [130, 95], ["DEN"], [70])},
            [of("ua-beyond", "ua-via", "ECONOMY", 17100)])],
    expected("BOOK", ["ua-denver"], ["ECONOMY"], ["CREATIVE_TICKETING"], TRIP_OK,
             ["CREATIVE_TICKETING"]),
    [CREATIVE],
    "'Hidden-city' is the handbook's 'ticketing beyond' (347-348): not allowed; the lowest fare to Denver, where "
    "the meeting is.", distractors=[D_CONNECT])

COMPANION_TRIP = {
    "traveller_name": "Elena Park", "traveller_title": "Spouse of the employee Daniel Park", "passenger": "ACCOMPANYING_NON_EMPLOYEE",
    "accompanies": "Daniel Park, Vice President, Channel Sales", "origin": "ORD", "destination": "LAS",
    "travel_date": "2027-02-22", "booking_date": "2027-01-25", "purpose": "Anixter partner conference in Las Vegas",
    "purpose_kind": "TRADE_SHOW", "trip_authorized_by": COMPANION_SUP}
REASON = ("Hosts the partners' spouses' program at the partner conference, as the conference plan requires (plan "
          "on file).")


def companion_searches():
    return [search("out", "ORD", "LAS", "2027-02-22",
                   {"ua": fl("UA", "08:00"), "wn": fl("WN", "10:20"), "aa": fl("AA", "14:35")},
                   [of("ua-economy", "ua", "ECONOMY", 29700), of("wn-economy", "wn", "ECONOMY", 27600),
                    of("aa-economy", "aa", "ECONOMY", 31400)])]


scenario(
    "walnut-spur", "hidden_clause", ["multi_traveller", "outside_air_section"],
    "Please book my wife Elena to Las Vegas on February 22 for the partner conference. She's "
    "running the partners' spouses' program; Marcus Hale approved it in writing.",
    trip(**COMPANION_TRIP, non_employee_reason=REASON, approvals=[sign(EVP, "NON_EMPLOYEE_TICKET", "2027-01-18")],
         notes=["Marcus Hale's signed approval names Elena Park and gives the reason above for her to come."]),
    companion_searches(),
    expected("BOOK", ["wn-economy"], ["ECONOMY"], ["LOWEST_FARE", "SENIOR_EXECUTIVE_APPROVED"], SENIOR,
             COMPANION_CLAUSES),
    [COMPANION, LOWEST, SENIOR_DEF],
    "A documented business purpose pre-approved by an Executive Vice President reporting to the CEO (452-457): "
    "the ticket can be issued, at the lowest fare. Flag twin of heron-scree.", distractors=[D_CUST_ARR])

# ============================== distractors ==============================
scenario(
    "yarrow-tarn", "distractor", ["multi_leg", "upgrade_not_taken"],
    "I need to get to Denver on January 26 for the cabling contractor meeting, business class please. It's a "
    "long day with the Chicago connection.",
    trip(traveller_name="Luc Tremblay", traveller_title="Business Development Manager", traveller_reports_to="Director, "
         "Business Development Canada", origin="YUL", destination="DEN", travel_date="2027-01-26",
         booking_date="2026-12-09", purpose="Cabling contractor meeting in Denver", trip_authorized_by=SUP,
         requested_cabin="BUSINESS", **CA),
    [search("out", "YUL", "DEN", "2027-01-26",
            {"ua": fl("UA", "07:00", [135, 155], ["ORD"], [120]), "ac": fl("AC", "12:30", [235])},
            [of("ua-economy", "ua", "ECONOMY", 39800), of("ua-business", "ua", "BUSINESS", 121000),
             of("ac-economy", "ac", "ECONOMY", 42500)], background=0)],
    expected("BOOK", ["ua-economy"], ["ECONOMY"], ["LONG_FLIGHT_CONDITION_NOT_MET", "UPGRADE_NOT_ELIGIBLE"], TRIP_OK,
             ["CLASS_OF_SERVICE"]),
    [COACH, INSTANCES, INTL],
    "Flights of 135 and 155 minutes: 290 minutes of flying time, excluding the 120-minute layover (307); each "
    "flight and the total are five hours or less: coach on every reading (302-303). The 410 elapsed minutes do "
    "not count. Flag twin of ember-shoal.", distractors=[D_LAYOVER])

scenario(
    "zinnia-loch", "distractor", [],
    "Book me on United to Chicago on December 16, please. I'm close to the next status level and need the miles. "
    "If United isn't possible, book what the policy allows; I have to be at the meeting.",
    trip(traveller_name="Amy Castillo", traveller_title="Product Manager", traveller_reports_to="Director, Product "
         "Management", origin="BOS", destination="ORD", travel_date="2026-12-16", booking_date="2026-12-01",
         purpose="Product planning meeting at headquarters", purpose_kind="INTERNAL_MEETING", trip_authorized_by=SUP,
         requested_airline="United Airlines", requested_airline_why="to reach the next frequent-flyer status level"),
    [search("out", "BOS", "ORD", "2026-12-16",
            {"aa": fl("AA", "07:50"), "b6": fl("B6", "10:15"), "ua": fl("UA", "12:40")},
            [of("aa-economy", "aa", "ECONOMY", 32200), of("b6-economy", "b6", "ECONOMY", 35800),
             of("ua-economy", "ua", "ECONOMY", 41200)])],
    expected("BOOK", ["aa-economy"], ["ECONOMY"], ["LOWEST_FARE", "LOYALTY_PROGRAM_PREFERENCE"], TRIP_OK,
             ["FREQUENT_FLYER", "LOWEST_LOGICAL_AIRFARE", "NON_REFUNDABLE_TICKETS", "TRAVELER_REQUIREMENTS"]),
    [MILES_A, MILES_B, LOWEST],
    "United is 9000 cents dearer and asked for only for miles (108, 341-342): the lowest fare (313).",
    distractors=[D_ACCRUE])

scenario(
    "aspen-knoll", "distractor", [],
    "Economy to Los Angeles on December 11, please, for the West region sales meeting.",
    trip(traveller_name="Derek Hughes", traveller_title="Territory Sales Manager", traveller_reports_to="Regional Sales "
         "Director", origin="ATL", destination="LAX", travel_date="2026-12-11", booking_date="2026-12-01",
         purpose="West region sales meeting", purpose_kind="INTERNAL_MEETING", trip_authorized_by=SUP,
         preferred_airlines=["Delta Air Lines"]),
    [search("out", "ATL", "LAX", "2026-12-11",
            {"aa": fl("AA", "06:15"), "dl": fl("DL", "09:30"), "ua": fl("UA", "11:45", via=["DEN"])},
            [of("aa-economy", "aa", "ECONOMY", 38900), of("dl-economy", "dl", "ECONOMY", 38900),
             of("ua-economy", "ua", "ECONOMY", 41500)])],
    expected("BOOK", ["dl-economy"], ["ECONOMY"], ["LOWEST_FARE", "PREFERRED_CARRIER_REQUIRED"], TRIP_OK,
             ["COMMERCIAL_AIRLINES", "EXPENSE_GUIDELINES", "LOWEST_LOGICAL_AIRFARE", "NON_REFUNDABLE_TICKETS",
              "TRAVELER_REQUIREMENTS"]),
    [PREF_A, PREF_B, PREF_C, LOWEST],
    "American and Delta sell the same lowest fare; Delta is the preferred airline (102, 107, 674); a non-preferred "
    "airline is allowed only with a lower fare (103).", distractors=[D_LOWER])

# ============================== refusals ==============================
scenario(
    "basil-crag", "refusal", ["multi_traveller", "personal_travel", "outside_air_section"],
    "Could you book my wife Elena on the same Miami trip on March 3? She'd love to see Miami while I'm at the "
    "trade show.",
    trip(traveller_name="Elena Park", traveller_title="Spouse of the employee Daniel Park",
         passenger="ACCOMPANYING_NON_EMPLOYEE", accompanies="Daniel Park, Vice President, Channel Sales",
         origin="ORD", destination="MIA", travel_date="2027-03-03", booking_date="2027-01-25",
         purpose="Accompanying her husband to the security trade show in Miami", purpose_kind="TRADE_SHOW",
         trip_authorized_by=COMPANION_SUP),
    [search("out", "ORD", "MIA", "2027-03-03", {"aa": fl("AA", "07:30"), "ua": fl("UA", "10:45")},
            [of("aa-economy", "aa", "ECONOMY", 24600), of("ua-economy", "ua", "ECONOMY", 26100)])],
    expected("REFUSE", [], ["NONE"], ["COMPANION_NOT_AUTHORIZED", "COMPANION_NOT_COVERED"], ["IMMEDIATE_SUPERVISOR", "NONE"],
             ["COMPANION_TRAVEL", "NON_REIMBURSABLE"]),
    [COMPANION, NON_PARTY],
    "No business purpose for the spouse and no authorization (452-457); accompanying travellers who are not "
    "party to the business purpose are not reimbursed (140): no ticket. Flag twin of heron-scree.")

scenario(
    "cobble-mere", "refusal", ["personal_travel"],
    "The Denver customer meeting on January 21 got cancelled, but I'd still like to go and spend the days "
    "skiing. Can you book the flight as planned?",
    trip(traveller_name="Kyle Benson", traveller_title="Account Executive", traveller_reports_to="Sales Manager, "
         "Midwest", origin="ORD", destination="DEN", travel_date="2027-01-21", booking_date="2026-12-10",
         purpose="The customer meeting was cancelled; the traveller wants to go skiing", purpose_kind="PERSONAL"),
    [search("out", "ORD", "DEN", "2027-01-21", {"ua": fl("UA", "08:40"), "wn": fl("WN", "11:10")},
            [of("ua-economy", "ua", "ECONOMY", 23300), of("wn-economy", "wn", "ECONOMY", 21900)])],
    expected("REFUSE", [], ["NONE"], ["OUTSIDE_POLICY_SCOPE", "PERSONAL_TRAVEL_NOT_COVERED"], ["NONE"],
             PERSONAL_CLAUSES),
    [BUSINESS_ONLY, LEGIT, COMBINED],
    "No business left: reimbursement covers business-related travel (46-47, 85-86); personal travel only combined "
    "with necessary business travel (463): no ticket.")

scenario(
    "dahlia-glen", "refusal", ["personal_travel"],
    "My mother has been taken into hospital in Phoenix. Please book me on the first flight on December 5; I'll "
    "work remotely from there.",
    trip(traveller_name="Maya Ortiz", traveller_title="Credit Analyst", traveller_reports_to="Credit Manager",
         origin="ORD", destination="PHX", travel_date="2026-12-05", booking_date="2026-12-04",
         purpose="Visiting the traveller's mother in hospital", purpose_kind="PERSONAL"),
    [search("out", "ORD", "PHX", "2026-12-05", {"aa": fl("AA", "06:20"), "wn": fl("WN", "09:05")},
            [of("aa-economy", "aa", "ECONOMY", 35400), of("wn-economy", "wn", "ECONOMY", 33900)])],
    expected("REFUSE", [], ["NONE"], ["OUTSIDE_POLICY_SCOPE", "PERSONAL_TRAVEL_NOT_COVERED"], ["NONE"],
             PERSONAL_CLAUSES),
    [BUSINESS_ONLY, LEGIT],
    "A family visit is not business travel (46-47, 85-86); the handbook has no family-emergency travel rule: no "
    "ticket.")

# ============================== flags ==============================
scenario(
    "ember-shoal", "flag", ["multi_leg", "unclear_phrase"],
    "Business class to Bogota on January 19, please, for the Andean distributor launch. It's the Mexico City "
    "connection.",
    trip(traveller_name="Marc Gagnon", traveller_title="Director, Channel Sales", traveller_reports_to="Vice President, "
         "Sales Canada", origin="YYZ", destination="BOG", travel_date="2027-01-19", booking_date="2026-12-02",
         purpose="Andean distributor launch in Bogota", trip_authorized_by=SUP, requested_cabin="BUSINESS", **CA),
    [search("out", "YYZ", "BOG", "2027-01-19",
            {"am": fl("AM", "07:20", [290, 275], ["MEX"], [85])},
            [of("am-economy", "am", "ECONOMY", 61000), of("am-business", "am", "BUSINESS", 189000)], background=0)],
    expected("FLAG_FOR_APPROVAL", ["am-business", "am-economy"], ["BUSINESS", "ECONOMY"], ["UNCLEAR_POLICY_TEXT"],
             ["NOT_NAMED", "SENIOR_EXECUTIVE"], ["CLASS_OF_SERVICE"],
             "all flights with a duration of five hours or less of flying time"),
    [COACH, INSTANCES, INTL],
    "Two international flights of 290 and 275 minutes: 565 minutes of flying time without the layover. Each "
    "flight is five hours or less (302-303: coach); the itinerary's total flying time exceeds five hours (307: "
    "business). No order is given.",
    flag_twins=["ivory-brook", "yarrow-tarn"],
    ambiguity={"phrase": "all flights with a duration of five hours or less of flying time",
               "readings": [("Each flight of the connection is a flight of five hours or less, so lines 302-303 "
                            "require coach for it: economy."),
                            ("Line 307 measures 'the total flying time ... excluding layover time' of an "
                            "international itinerary, 565 minutes here, so business qualifies: business.")]})

vancouver(
    "fennel-cliff", "flag", ["unclear_phrase", "outside_air_section"],
    "Business class to Vancouver on February 3, please. Paul Brandt, our VP of Treasury, signed off on it in "
    "writing.", None, [sign(TREASURY, "BUSINESS_CABIN", "2027-01-20")], "NONE",
    expected("FLAG_FOR_APPROVAL", ["ac-business", "ac-economy"], ["BUSINESS", "ECONOMY"], ["UNCLEAR_POLICY_TEXT"],
             ["EXECUTIVE_VP", "NOT_NAMED", "SENIOR_EXECUTIVE"], SIGN_CLAUSES + ["GIFTS"], "senior executive"),
    [INSTANCES, INTL, APPROVAL, SENIOR_DEF, SENIOR_AUTH, GIFTS_DEF],
    "Line 310 needs a senior executive's prior written approval. A Vice President reporting to the CFO is one "
    "under lines 57-58 and 165, but not an 'Executive VP' (58) nor 'the President and CEO and his direct "
    "reports' (554), which puts him one level below.",
    flag_twins=["raven-ford", "sable-heath"],
    ambiguity={"phrase": "senior executive",
               "readings": [("Lines 57-58 ('any Vice President reporting to the CEO or CFO') and 165 ('their Vice "
                            "President direct reports'): the Vice President, Treasury qualifies, so business."),
                            ("Line 58 ('Documented Executive VP approval') and line 554 ('the President and CEO and "
                            "his direct reports'; anyone below is 'one level below'): he does not, so economy.")]})

scenario(
    "gorse-inlet", "flag", ["multi_traveller", "unclear_phrase"],
    "I'm flying to San Francisco on December 8 with our customer from Pacific Datacom for their site survey. "
    "Can you put me in business?",
    trip(traveller_name="Luis Moreno", traveller_title="Account Manager", traveller_reports_to="Branch Manager",
         origin="ORD", destination="SFO", travel_date="2026-12-08", booking_date="2026-12-01",
         purpose="Site survey with the customer Pacific Datacom", trip_authorized_by=SUP, requested_cabin="BUSINESS",
         customer_cabin="BUSINESS", notes=["The customer has booked business on the same United flight."]),
    [search("out", "ORD", "SFO", "2026-12-08",
            {"ua": fl("UA", "08:00", [270]), "aa": fl("AA", "11:00", [275])},
            [of("ua-economy", "ua", "ECONOMY", 31200), of("ua-business", "ua", "BUSINESS", 98000),
             of("aa-economy", "aa", "ECONOMY", 33800), of("aa-business", "aa", "BUSINESS", 104000)], background=0)],
    expected("FLAG_FOR_APPROVAL", ["ua-business", "ua-economy"], ["BUSINESS", "ECONOMY"], ["UNCLEAR_POLICY_TEXT"],
             ["NOT_NAMED", "SENIOR_EXECUTIVE"], ["CLASS_OF_SERVICE"],
             "When traveling with customers, employees may use the same class of service as the customer"),
    [COACH, INSTANCES, CUSTOMER],
    "A domestic 270-minute flight 'must be booked in Coach Class' (302-303), while 'When traveling with customers, "
    "employees may use the same class of service as the customer' (311) allows business. No order is given.",
    flag_twins=["dover-kiln", "tansy-ridge"],
    ambiguity={"phrase": "When traveling with customers, employees may use the same class of service as the customer",
               "readings": [("Lines 302-303 are a 'must' for domestic flights and flights of five hours or less, so "
                            "the employee flies coach: economy."),
                            ("Line 311 is one of the instances in which business may be used, and it names no "
                            "flight length, so the employee may join the customer: business.")]})

scenario(
    "heron-scree", "flag", ["multi_traveller", "approval_required", "outside_air_section"],
    "Please book my wife Elena to Las Vegas on February 22 for the partner conference. She's "
    "running the partners' spouses' program.",
    trip(**COMPANION_TRIP, non_employee_reason=REASON),
    companion_searches(),
    expected("FLAG_FOR_APPROVAL", ["wn-economy"], ["ECONOMY"], ["APPROVAL_REQUIRED", "COMPANION_NOT_AUTHORIZED"], SENIOR,
             COMPANION_CLAUSES),
    [COMPANION, LOWEST],
    "A business purpose is documented, but no senior executive has pre-approved it, and the travel agency will "
    "not issue a ticket without that authorization (452-457): hold the lowest fare for the sign-off.",
    flag_twins=["walnut-spur", "basil-crag"],
    ambiguity="none: a sign-off is missing; the text is clear")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for path in OUT.glob("*.json"):
        path.unlink()
    for data in S:
        (OUT / f"{data['id']}.json").write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {len(S)} scenarios")


if __name__ == "__main__":
    main()
