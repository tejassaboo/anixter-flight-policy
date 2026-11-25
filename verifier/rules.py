"""The answer key's rules for Anixter's Global Travel, Entertainment & Expense Policy (revised March 24, 2014),
as exact integer code. Byte-identical in src/plugin/rules.py and verifier/rules.py; it imports only modules a
verifier may use.

Every rule cites the frozen handbook text (src/plugin/data/policy.txt) by line. Where the text leaves an
answer open, the rule returns FLAG_FOR_APPROVAL with the unclear words, and a scenario may depend on each
unclear phrase at most once (tests/test_scenarios.py). Combinations no scenario needs raise ValueError, so a
new scenario cannot fall silently into untested logic.

The duration hook. The handbook has two duration clauses that measure differently, and no other duration
definition:

- coach-flight (lines 302-303): "Domestic flights and all flights with a duration of five hours or less of
  flying time must be booked in Coach Class." Measured per flight ("all flights with a duration"), inclusive
  ("or less"): a flight is over the limit at 301 scheduled minutes. On a connection, "a flight" may be each
  flight or the whole itinerary: when every flight is over the limit every reading agrees (over); when the
  flights' minutes added together are within it every reading agrees (not over); otherwise it is unclear.
- business-flying-time (line 307): "International flights when the total flying time exceeds five hours,
  excluding layover time". Measured on the itinerary: the scheduled minutes of its flights added together,
  ground time left out, strict ("exceeds").

Only the outbound flights are measured: the handbook never says how a return is graded, and every business
request in the scenarios is one way.
"""

from contract import (
    ApprovalSubject,
    Approver,
    Cabin,
    Clause,
    Decision,
    ExtraDays,
    Passenger,
    Purpose,
    ReasonCode,
)

from .world import days_between

HANDBOOK = "Anixter, Global Travel, Entertainment & Expense Policy, revised March 24, 2014"

# Each closed-list section and the heading it names in the frozen text (tests check every heading is there).
CLAUSE_HEADINGS = {
    Clause.INTRODUCTION: "Global Travel, Entertainment, and Expense Policy Introduction",
    Clause.POLICY_OVERVIEW: "Global Travel, Entertainment, and Expense Policy Overview",
    Clause.TRAVELER_REQUIREMENTS: "General Traveler Requirements",
    Clause.NON_REIMBURSABLE: "Non-Reimbursable Expenses",
    Clause.SENIOR_EXECUTIVE_APPROVAL: "Senior Executive Approval",
    Clause.RESERVATIONS: "Reservations",
    Clause.PASSPORTS_VISAS: "Passports, Visas, and Other Travel Documentation",
    Clause.CORPORATE_CREDIT_CARDS: "Corporate Credit Cards",
    Clause.COMMERCIAL_AIRLINES: "Commercial Airlines",
    Clause.LOWEST_LOGICAL_AIRFARE: "Lowest Logical Airfare",
    Clause.ADVANCE_PURCHASE: "Advance Purchase",
    Clause.CLASS_OF_SERVICE: "Class of Service",
    Clause.NON_REFUNDABLE_TICKETS: "Non-Refundable Tickets",
    Clause.UNUSED_TICKETS: "Unused Tickets (Refundable and Non-Refundable)",
    Clause.DENIED_BOARDING: "Airline Vouchers/Denied Boarding",
    Clause.FREQUENT_FLYER: "Frequent Flyer and Related Programs",
    Clause.CREATIVE_TICKETING: '"Creative Ticketing"',
    Clause.RENTAL_CARS: "Rental Cars",
    Clause.HOTELS: "Hotels",
    Clause.EXTENDED_TRAVEL: "Extended Travel",
    Clause.COMPANION_TRAVEL: "Spouse or Companion Travel",
    Clause.COMBINED_TRAVEL: "Combined Business and Personal Travel",
    Clause.GIFTS: "Gifts To / From Non-Employees",
    Clause.EXPENSE_GUIDELINES: "General Guidelines",
    Clause.EXPENSE_APPROVAL: "Expense Report Submission / Approval",
}

# The handbook's duration thresholds (the per-handbook duration hook; tests/test_duration.py tests both
# sides of each). operator ">" is strict: "five hours or less" is within, "exceeds five hours" is over.
DURATION_RULES = (
    {"name": "coach-flight", "minutes": 300, "operator": ">", "lines": [302, 303],
     "quote": "all flights with a duration of five hours or less of flying time must be booked in Coach Class"},
    {"name": "business-flying-time", "minutes": 300, "operator": ">", "lines": [307, 307],
     "quote": "International flights when the total flying time exceeds five hours, excluding layover time"},
)
LIMITS = {rule["name"]: rule["minutes"] for rule in DURATION_RULES}

# Handbook-specific conventions shown by booking_requirements, beyond the template's (none here).
CONVENTIONS = ()

# Line 308: "U.S. originating flights to Canada, Mexico and the Caribbean do not qualify for Business Class".
# The world has no Caribbean airport, so only Canada and Mexico can arise.
EXCLUDED_FROM_US = {"CA", "MX"}

# The titles the org chart in the scenarios uses for the CEO and the CFO (lines 57-58, 165, 554).
CEO_TITLE = "President and CEO"
CFO_TITLE = "Chief Financial Officer"

# A preferred airline's fare at or above this percentage of a cheaper non-preferred fare is clearly not
# "comparable" (line 107); anything closer is not modelled.
NOT_COMPARABLE_PERCENT = 125

LOWEST_CLAUSES = [Clause.CLASS_OF_SERVICE, Clause.LOWEST_LOGICAL_AIRFARE, Clause.NON_REFUNDABLE_TICKETS]
TRIP_OK = [Approver.NONE, Approver.IMMEDIATE_SUPERVISOR]  # line 50: verbal trip authorization, not a sign-off
SENIOR = [Approver.SENIOR_EXECUTIVE, Approver.EXECUTIVE_VP]
MANAGER = [Approver.MANAGER, Approver.IMMEDIATE_SUPERVISOR]


def over(rule, offer):
    """True, False or None (unclear): whether ``offer``'s outbound flights are over the handbook's ``rule``
    duration, measured the way that clause measures it (module docstring)."""
    limit = LIMITS[rule]
    minutes = [segment.scheduled_minutes for segment in offer.segments]
    if rule == "business-flying-time":
        return sum(minutes) > limit
    if rule == "coach-flight":
        if all(value > limit for value in minutes):
            return True
        if sum(minutes) <= limit:
            return False
        return None
    raise ValueError(f"unknown duration rule {rule!r}")


def by_value(items):
    return sorted(set(items), key=lambda item: item.value)


def answer(decision, offers, reasons, approvers, clauses, why, phrase=""):
    return {
        "decision": decision,
        "offer_ids": sorted(offer.offer_id for offer in offers),
        "cabins": by_value(offer.cabin for offer in offers) or [Cabin.NONE],
        "reason_codes": by_value(reasons),
        "approvers": by_value(approvers),
        "clauses": by_value(clauses),
        "unclear_phrase": phrase,
        "explanation": why,
    }


def refuse(reasons, clauses, why):
    return answer(Decision.REFUSE, [], reasons, [Approver.NONE], clauses, why)


def cheapest(offers):
    if not offers:
        return []
    low = min(offer.fare_cents for offer in offers)
    return [offer for offer in offers if offer.fare_cents == low]


def return_day(offer):
    return offer.return_segments[0].depart_local[:10] if offer.return_segments else ""


def on_route(offers, origin, destination, back=""):
    """Offers from ``origin`` to ``destination`` (codes), flying back on local date ``back`` ("" one way)."""
    return [offer for offer in offers
            if offer.segments[0].origin == origin and offer.segments[-1].destination == destination
            and return_day(offer) == back]


def economy(offers):
    return [offer for offer in offers if offer.cabin == Cabin.ECONOMY and offer.seats_available]


def lowest_economy(trip, offers):
    """Lines 313 and 102-108: the lowest economy fare that can be bought; on a tie, the preferred airlines.
    Returns (offers, reasons, clauses, note)."""
    low = cheapest(economy(offers))
    if not low:
        raise ValueError("no economy offer on the route can be bought")
    preferred = [offer for offer in low if offer.carrier in trip.preferred_airlines]
    if preferred and len(preferred) < len(low):
        return (preferred, [ReasonCode.PREFERRED_CARRIER_REQUIRED, ReasonCode.LOWEST_FARE],
                [Clause.TRAVELER_REQUIREMENTS, Clause.EXPENSE_GUIDELINES, Clause.COMMERCIAL_AIRLINES],
                ("Lines 102, 107 and 674: equal lowest fares, so the preferred airline; line 103 allows a "
                "non-preferred airline only with a lower fare."))
    if trip.preferred_airlines and not preferred:
        best = cheapest([offer for offer in economy(offers) if offer.carrier in trip.preferred_airlines])
        if best and best[0].fare_cents * 100 < NOT_COMPARABLE_PERCENT * low[0].fare_cents:
            raise ValueError("a preferred fare close to a cheaper non-preferred one ('comparable') is not modelled")
    return low, [ReasonCode.LOWEST_FARE], list(LOWEST_CLAUSES), "Line 313: the lowest cost available airfare."


def lowest(trip, offers):
    return lowest_economy(trip, offers)[0]


def senior_approval(trip, subject):
    """Whether a sign-off on file for ``subject`` comes from a senior executive (lines 57-58, 165, 554):
    "valid" (an Executive Vice President reporting to the CEO meets every definition), "unclear" (a Vice
    President reporting to the CFO meets lines 57 and 165 but not "Executive VP" in line 58 nor "the President
    and CEO and his direct reports" in line 554), "self" (lines 53, 768), "not_authorized" (reports to
    neither), or "none"."""
    records = [record for record in trip.approvals if record.subject == subject]
    if not records:
        return "none"
    if len(records) > 1:
        raise ValueError("two sign-offs for one subject are not modelled")
    record = records[0]
    if not record.in_writing or days_between(record.given_on, trip.booking_date) < 0:
        raise ValueError("a spoken or later sign-off is not modelled")
    if record.approver_name == trip.traveller_name:
        return "self"
    if record.approver_reports_to == CEO_TITLE and record.approver_title.startswith("Executive Vice President"):
        return "valid"
    if record.approver_reports_to == CFO_TITLE and record.approver_title.startswith("Vice President"):
        return "unclear"
    if record.approver_reports_to not in (CEO_TITLE, CFO_TITLE):
        return "not_authorized"
    raise ValueError("this approver's place in the org chart is not modelled")


def manager_approved(trip, subject):
    """Whether the traveller's own manager (the title they report to) signed off ``subject`` before today."""
    for record in trip.approvals:
        if (record.subject == subject and record.approver_title == trip.traveller_reports_to
                and days_between(record.given_on, trip.booking_date) >= 0):
            return True
    return False


def solve(trip, offers, hidden):
    """The answer key for one trip and the offers of every search its scenario pins: the decision, and every
    accepted offer id, cabin, reason, approver and section. ``hidden`` (answer_key_inputs) is unused by this
    handbook."""
    if hidden:
        raise ValueError("this handbook's scenarios carry no answer_key_inputs")
    origin, destination = trip.origin.code, trip.destination.code
    if trip.purpose_kind == Purpose.PERSONAL:
        return refuse([ReasonCode.PERSONAL_TRAVEL_NOT_COVERED, ReasonCode.OUTSIDE_POLICY_SCOPE],
                      [Clause.INTRODUCTION, Clause.POLICY_OVERVIEW, Clause.COMBINED_TRAVEL],
                      "Lines 36, 46 and 85-86 cover business-related travel only; lines 463-464 allow personal "
                      "travel only combined with necessary business travel.")
    if trip.passenger == Passenger.ACCOMPANYING_NON_EMPLOYEE:
        return companion(trip, on_route(offers, origin, destination))
    if trip.requested_ticket_to:
        return creative(trip, offers)
    if trip.extra_days == ExtraDays.LATER_RETURN_FOR_FARE:
        return extended(trip, offers)
    if trip.extra_days == ExtraDays.PERSONAL_DAYS:
        return combined(trip, offers)
    if trip.return_date:
        raise ValueError("a plain round trip is not modelled")
    route = on_route(offers, origin, destination)
    if trip.requested_cabin == Cabin.BUSINESS:
        return business(trip, route)
    if trip.requested_cabin != Cabin.ECONOMY:
        raise ValueError(f"a {trip.requested_cabin.value} request is not modelled")
    if trip.requested_airline:
        return loyalty(trip, route)
    low, reasons, clauses, why = lowest_economy(trip, route)
    return answer(Decision.BOOK, low, reasons, TRIP_OK, clauses, why)


def loyalty(trip, route):
    """Lines 107-108 and 341-342: no dearer airline chosen for frequent-flyer miles."""
    low = lowest(trip, route)
    asked = cheapest([offer for offer in economy(route) if offer.carrier == trip.requested_airline])
    if not asked or asked[0].fare_cents <= low[0].fare_cents:
        raise ValueError("a requested airline that is not dearer is not modelled")
    return answer(Decision.BOOK, low, [ReasonCode.LOYALTY_PROGRAM_PREFERENCE, ReasonCode.LOWEST_FARE], TRIP_OK,
                  [Clause.FREQUENT_FLYER, Clause.TRAVELER_REQUIREMENTS, Clause.NON_REFUNDABLE_TICKETS],
                  f"Line 108: no higher airfare for miles ({asked[0].fare_cents} against {low[0].fare_cents} "
                  "cents); lines 341-342 likewise; line 313: the lowest cost.")


def business(trip, route):
    """Lines 302-311: coach unless the flight is outside line 302-303 and one of the four instances holds."""
    wanted = cheapest([offer for offer in route if offer.cabin == Cabin.BUSINESS and offer.seats_available])
    if not wanted:
        raise ValueError("a business request with no business offer is not modelled")
    verdicts = {(over("coach-flight", offer), over("business-flying-time", offer))
                for offer in route if offer.cabin == Cabin.BUSINESS}
    if len(verdicts) != 1:
        raise ValueError("business offers whose durations fall on different sides are not modelled")
    coach_over, total_over = verdicts.pop()
    coach = lowest(trip, route)
    countries = (trip.origin.country, trip.destination.country)
    domestic = countries[0] == countries[1]
    if domestic and countries[0] != trip.home_country:
        raise ValueError("a flight inside another country than the traveller's ('domestic') is not modelled")
    excluded = countries[0] == "US" and countries[1] in EXCLUDED_FROM_US
    customer = trip.customer_cabin == Cabin.BUSINESS
    if trip.customer_cabin not in (Cabin.NONE, Cabin.ECONOMY, Cabin.BUSINESS):
        raise ValueError("a customer in another cabin is not modelled")
    approval = senior_approval(trip, ApprovalSubject.BUSINESS_CABIN)
    minutes = f"{wanted[0].flying_minutes} flying minutes over {len(wanted[0].segments)} flight(s)"
    if domestic or coach_over is False:
        # Lines 302-303 apply: coach. A customer in business (line 311) collides with them; no order is given.
        if approval != "none":
            raise ValueError("a senior-executive sign-off on a flight lines 302-303 cover is not modelled")
        if customer:
            return answer(Decision.FLAG_FOR_APPROVAL, wanted + coach, [ReasonCode.UNCLEAR_POLICY_TEXT],
                          [Approver.NOT_NAMED, Approver.SENIOR_EXECUTIVE], [Clause.CLASS_OF_SERVICE],
                          f"Lines 302-303 put this flight in coach ({minutes}, domestic={domestic}); line 311 lets "
                          "the employee use the customer's business class; no order is given.",
                          phrase="When traveling with customers, employees may use the same class of service as "
                                 "the customer")
        reasons = [ReasonCode.UPGRADE_NOT_ELIGIBLE]
        if domestic:
            reasons.append(ReasonCode.DOMESTIC_COACH_ONLY)
        if coach_over is False:
            reasons.append(ReasonCode.LONG_FLIGHT_CONDITION_NOT_MET)
        if trip.customer_cabin == Cabin.ECONOMY:
            reasons.append(ReasonCode.SAME_CLASS_AS_CUSTOMER)
        return answer(Decision.BOOK, coach, reasons, TRIP_OK, [Clause.CLASS_OF_SERVICE],
                      f"Lines 302-303: coach ({minutes}, domestic={domestic}).")
    if coach_over is None:
        if customer or approval != "none" or excluded or not total_over:
            raise ValueError("a connection that is unclear under lines 302-303 is modelled only alone")
        return answer(Decision.FLAG_FOR_APPROVAL, wanted + coach, [ReasonCode.UNCLEAR_POLICY_TEXT],
                      [Approver.NOT_NAMED, Approver.SENIOR_EXECUTIVE], [Clause.CLASS_OF_SERVICE],
                      f"Each flight is five hours or less (lines 302-303: coach), but the total flying time "
                      f"exceeds five hours on an international itinerary (line 307: business) ({minutes}).",
                      phrase="all flights with a duration of five hours or less of flying time")
    granted, approvers = [], []
    if total_over and not excluded:  # line 307
        granted.append(ReasonCode.INTERNATIONAL_LONG_FLIGHT)
        approvers += TRIP_OK
    if customer:  # line 311
        granted.append(ReasonCode.SAME_CLASS_AS_CUSTOMER)
        approvers += TRIP_OK
    if approval == "valid":  # line 310
        granted.append(ReasonCode.SENIOR_EXECUTIVE_APPROVED)
        approvers += SENIOR
    sign_off_clauses = [Clause.CLASS_OF_SERVICE, Clause.INTRODUCTION, Clause.SENIOR_EXECUTIVE_APPROVAL]
    if granted:
        clauses = sign_off_clauses if approval == "valid" else [Clause.CLASS_OF_SERVICE]
        return answer(Decision.BOOK, wanted, granted, approvers, clauses,
                      f"Lines 306-311: business allowed ({', '.join(code.value for code in granted)}; {minutes}).")
    if approval == "unclear":
        return answer(Decision.FLAG_FOR_APPROVAL, wanted + coach, [ReasonCode.UNCLEAR_POLICY_TEXT],
                      [Approver.NOT_NAMED, *SENIOR], [*sign_off_clauses, Clause.GIFTS],
                      "Line 310 needs a senior executive: lines 57-58 ('any Vice President reporting to the CEO or "
                      "CFO') and 165 include this Vice President reporting to the CFO; line 58 ('Executive VP') "
                      "and line 554 ('the President and CEO and his direct reports') do not.",
                      phrase="senior executive")
    reasons, clauses = [ReasonCode.UPGRADE_NOT_ELIGIBLE], [Clause.CLASS_OF_SERVICE]
    if excluded and total_over:
        reasons.append(ReasonCode.US_ORIGIN_CANADA_MEXICO_CARIBBEAN)
    if not total_over:
        reasons.append(ReasonCode.LONG_FLIGHT_CONDITION_NOT_MET)
    if approval == "self":
        reasons.append(ReasonCode.SELF_APPROVAL)
        clauses += [Clause.INTRODUCTION, Clause.EXPENSE_APPROVAL]
    elif approval == "not_authorized":
        reasons.append(ReasonCode.APPROVER_NOT_AUTHORIZED)
        clauses += [Clause.INTRODUCTION, Clause.SENIOR_EXECUTIVE_APPROVAL]
    return answer(Decision.BOOK, coach, reasons, TRIP_OK, clauses,
                  f"Lines 306-311: no instance for business holds (excluded={excluded}, approval={approval}; "
                  f"{minutes}), so coach.")


def companion(trip, route):
    """Lines 452-457: a non-employee's ticket needs a bona fide business purpose pre-approved by a senior
    executive; "The travel agency will not issue a ticket for the individual without such authorization."
    Line 140: accompanying travellers not party to the business purpose are not reimbursed."""
    if trip.requested_cabin != Cabin.ECONOMY:
        raise ValueError("a non-employee asking for a cabin above economy is not modelled")
    if not trip.non_employee_reason:
        return refuse([ReasonCode.COMPANION_NOT_COVERED, ReasonCode.COMPANION_NOT_AUTHORIZED],
                      [Clause.COMPANION_TRAVEL, Clause.NON_REIMBURSABLE],
                      "Lines 452-454 and 140: no business purpose for the non-employee, so no ticket.")
    low = lowest(trip, route)
    state = senior_approval(trip, ApprovalSubject.NON_EMPLOYEE_TICKET)
    if state == "valid":
        return answer(Decision.BOOK, low, [ReasonCode.SENIOR_EXECUTIVE_APPROVED, ReasonCode.LOWEST_FARE], SENIOR,
                      [Clause.COMPANION_TRAVEL],
                      "Lines 452-457: documented business purpose, pre-approved by an Executive Vice President "
                      "reporting to the CEO; line 313: the lowest fare.")
    if state == "none":
        return answer(Decision.FLAG_FOR_APPROVAL, low, [ReasonCode.APPROVAL_REQUIRED], SENIOR,
                      [Clause.COMPANION_TRAVEL],
                      "Lines 452-457: a business purpose is documented, but no senior executive has pre-approved "
                      "it, and no ticket is issued without that authorization.")
    raise ValueError(f"a non-employee ticket with a {state} sign-off is not modelled")


def creative(trip, offers):
    """Lines 346-348: "ticketing beyond" (a cheaper ticket to a city beyond, getting off at the connection)
    is not allowed; the company buys the ticket to where the traveller has to be."""
    origin, destination = trip.origin.code, trip.destination.code
    beyond = [offer for offer in on_route(offers, origin, trip.requested_ticket_to)
              if any(segment.destination == destination for segment in offer.segments[:-1])]
    route = on_route(offers, origin, destination)
    low = lowest(trip, route)
    if not beyond or min(offer.fare_cents for offer in beyond) >= low[0].fare_cents:
        raise ValueError("ticketing beyond is modelled only when it is cheaper and connects at the destination")
    return answer(Decision.BOOK, low, [ReasonCode.CREATIVE_TICKETING, ReasonCode.LOWEST_FARE], TRIP_OK,
                  [Clause.CREATIVE_TICKETING],
                  f"Lines 346-348: no ticket to {trip.requested_ticket_to} to get off at {destination}; book the "
                  f"lowest fare to {destination} ({low[0].fare_cents} cents).")


def trip_days(trip):
    """Whether the trip as first planned (travel_date to business_return_date) is "scheduled for less than six
    days" (line 450). Counting calendar days as the later date minus the earlier, or counting both ends, gives
    the same side except at a difference of five days, which no scenario uses."""
    difference = days_between(trip.travel_date, trip.business_return_date)
    if difference == 5:
        raise ValueError("five days apart (six counting both ends) is not modelled")
    return difference + 1 < 6


def extended(trip, offers):
    """Lines 446-450: the extra hotel and meals of staying later are reimbursed only if the stay is approved in
    advance by the manager, saves airfare that offsets the added expense, and the trip was originally scheduled
    for less than six days. Otherwise the traveller keeps the original return (the request says so)."""
    origin, destination = trip.origin.code, trip.destination.code
    first = lowest(trip, on_route(offers, origin, destination, trip.business_return_date))
    later = lowest(trip, on_route(offers, origin, destination, trip.return_date))
    saving, added = first[0].fare_cents - later[0].fare_cents, trip.extra_days_cost_cents
    if saving == added:
        raise ValueError("a saving equal to the added expense is not modelled")
    numbers = f"saving {saving} cents against {added} cents added"
    failing = []
    if not trip_days(trip):
        failing.append(ReasonCode.EXTENDED_TRAVEL_TRIP_TOO_LONG)
    if saving < added:
        failing.append(ReasonCode.EXTENDED_TRAVEL_NOT_OFFSET)
    if failing:
        return answer(Decision.BOOK, first, failing, [*TRIP_OK, Approver.MANAGER], [Clause.EXTENDED_TRAVEL],
                      f"Lines 446-450 fail ({', '.join(code.value for code in failing)}; {numbers}): the original "
                      "return.")
    if not manager_approved(trip, ApprovalSubject.LATER_RETURN):
        raise ValueError("a later return without the manager's advance approval is not modelled")
    return answer(Decision.BOOK, later, [ReasonCode.EXTENDED_TRAVEL_SAVINGS, ReasonCode.COST_SAVINGS], MANAGER,
                  [Clause.EXTENDED_TRAVEL],
                  f"Lines 446-450 hold (approved in advance by the manager; {numbers}; originally under six days).")


def combined(trip, offers):
    """Lines 463-468: personal days may be added "if ... 3) there is no additional cost to the company", with
    the reimbursement details approved by the manager before travel. Otherwise the business dates only (the
    request says so)."""
    origin, destination = trip.origin.code, trip.destination.code
    if not manager_approved(trip, ApprovalSubject.PERSONAL_DAYS):
        raise ValueError("personal days without the manager's approval on file are not modelled")
    if trip.extra_days_cost_cents:
        raise ValueError("personal days claimed from the company are not modelled")
    plain = lowest(trip, on_route(offers, origin, destination, trip.business_return_date))
    longer = lowest(trip, on_route(offers, origin, destination, trip.return_date))
    numbers = f"{longer[0].fare_cents} cents with the personal days against {plain[0].fare_cents} without"
    if longer[0].fare_cents <= plain[0].fare_cents:
        return answer(Decision.BOOK, longer, [ReasonCode.COMBINED_TRIP_NO_ADDED_COST], MANAGER,
                      [Clause.COMBINED_TRAVEL], f"Lines 463-468: no additional cost ({numbers}).")
    return answer(Decision.BOOK, plain, [ReasonCode.COMBINED_TRIP_ADDED_COST], [*TRIP_OK, Approver.MANAGER],
                  [Clause.COMBINED_TRAVEL], f"Lines 463-464: the personal days add cost ({numbers}).")
