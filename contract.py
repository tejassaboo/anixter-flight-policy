"""Each tool's and task's typed input and output (see nanoagent.plugin.v0001.contract): declarations only.

The first part is the original-handbook template's shared contract and is the same in every plugin made from
it. The HANDBOOK-SPECIFIC part in the middle is filled per handbook: the scenario ids, the closed lists of
approvers and sections, and the trip record; the shared inputs and outputs after it refer to those names.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output

# ---------------------------------------------------------------------------------------------------------
# SHARED (template): keep identical across plugins, except the agent task's id in Task.BOOK_FLIGHT.
# ---------------------------------------------------------------------------------------------------------


class Tool(Enum):
    BOOKING_REQUIREMENTS = "booking_requirements"
    GET_TRIP = "get_trip"
    SEARCH_FLIGHTS = "search_flights"
    SOLVE_BOOKING = "solve_booking"


class Task(Enum):
    BOOKING_REQUIREMENTS = "booking-requirements"
    SEARCH_FLIGHTS = "search-flights"
    BOOK_FLIGHT = "book-anixter-flight"


class Decision(Enum):
    BOOK = "BOOK"
    REFUSE = "REFUSE"
    FLAG_FOR_APPROVAL = "FLAG_FOR_APPROVAL"


class Cabin(Enum):
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"
    NONE = "NONE"


class ReasonCode(Enum):
    """Why the decision was made. The list is shared by every handbook plugin, so it also holds reasons
    that a given handbook never uses."""

    LOWEST_FARE = "LOWEST_FARE"
    UPGRADE_NOT_ELIGIBLE = "UPGRADE_NOT_ELIGIBLE"
    CLIENT_REIMBURSABLE = "CLIENT_REIMBURSABLE"
    UPGRADE_WITHIN_FARE_MARGIN = "UPGRADE_WITHIN_FARE_MARGIN"
    MEDICAL_NEED = "MEDICAL_NEED"
    COST_SAVINGS = "COST_SAVINGS"
    NO_ECONOMY_SEATS_URGENT = "NO_ECONOMY_SEATS_URGENT"
    TRAVELER_PAYS_UPGRADE = "TRAVELER_PAYS_UPGRADE"
    LONG_FLIGHT_APPROVED = "LONG_FLIGHT_APPROVED"
    LONG_FLIGHT_CONDITION_NOT_MET = "LONG_FLIGHT_CONDITION_NOT_MET"
    PREMIUM_ECONOMY_ALLOWED = "PREMIUM_ECONOMY_ALLOWED"
    UPGRADE_COST_NOT_NOMINAL = "UPGRADE_COST_NOT_NOMINAL"
    ALTERNATE_ROUTE_WITHIN_MARGIN = "ALTERNATE_ROUTE_WITHIN_MARGIN"
    ALTERNATE_ROUTE_TOO_EXPENSIVE = "ALTERNATE_ROUTE_TOO_EXPENSIVE"
    LOYALTY_PROGRAM_PREFERENCE = "LOYALTY_PROGRAM_PREFERENCE"
    COMPANION_NOT_COVERED = "COMPANION_NOT_COVERED"
    PERSONAL_TRAVEL_NOT_COVERED = "PERSONAL_TRAVEL_NOT_COVERED"
    OUTSIDE_POLICY_SCOPE = "OUTSIDE_POLICY_SCOPE"
    NO_COMPLIANT_OFFER = "NO_COMPLIANT_OFFER"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    UNCLEAR_POLICY_TEXT = "UNCLEAR_POLICY_TEXT"
    ADVANCE_PURCHASE_TOO_LATE = "ADVANCE_PURCHASE_TOO_LATE"
    DISTANCE_BELOW_MINIMUM = "DISTANCE_BELOW_MINIMUM"
    DRIVING_EXPECTED = "DRIVING_EXPECTED"
    RAIL_PREFERRED = "RAIL_PREFERRED"
    REFUNDABLE_FARE_NOT_ALLOWED = "REFUNDABLE_FARE_NOT_ALLOWED"
    PREFERRED_CARRIER_REQUIRED = "PREFERRED_CARRIER_REQUIRED"
    CONNECTION_TOO_LONG = "CONNECTION_TOO_LONG"
    OVERNIGHT_STOP_REQUIRED = "OVERNIGHT_STOP_REQUIRED"
    NATIONAL_CARRIER_REQUIRED = "NATIONAL_CARRIER_REQUIRED"
    SENIOR_ROLE_ENTITLEMENT = "SENIOR_ROLE_ENTITLEMENT"
    INTERNATIONAL_LONG_FLIGHT = "INTERNATIONAL_LONG_FLIGHT"
    TRAVELLER_LIMIT_PER_FLIGHT = "TRAVELLER_LIMIT_PER_FLIGHT"
    # HANDBOOK-SPECIFIC reason codes go below this line; keep every shared one above.
    DOMESTIC_COACH_ONLY = "DOMESTIC_COACH_ONLY"
    US_ORIGIN_CANADA_MEXICO_CARIBBEAN = "US_ORIGIN_CANADA_MEXICO_CARIBBEAN"
    SAME_CLASS_AS_CUSTOMER = "SAME_CLASS_AS_CUSTOMER"
    SENIOR_EXECUTIVE_APPROVED = "SENIOR_EXECUTIVE_APPROVED"
    APPROVER_NOT_AUTHORIZED = "APPROVER_NOT_AUTHORIZED"
    SELF_APPROVAL = "SELF_APPROVAL"
    APPROVAL_NOT_PRIOR_WRITTEN = "APPROVAL_NOT_PRIOR_WRITTEN"
    CREATIVE_TICKETING = "CREATIVE_TICKETING"
    EXTENDED_TRAVEL_SAVINGS = "EXTENDED_TRAVEL_SAVINGS"
    EXTENDED_TRAVEL_NOT_OFFSET = "EXTENDED_TRAVEL_NOT_OFFSET"
    EXTENDED_TRAVEL_TRIP_TOO_LONG = "EXTENDED_TRAVEL_TRIP_TOO_LONG"
    COMBINED_TRIP_NO_ADDED_COST = "COMBINED_TRIP_NO_ADDED_COST"
    COMBINED_TRIP_ADDED_COST = "COMBINED_TRIP_ADDED_COST"
    COMPANION_NOT_AUTHORIZED = "COMPANION_NOT_AUTHORIZED"
    DENIED_BOARDING_NOT_ALLOWED = "DENIED_BOARDING_NOT_ALLOWED"
    # Decoys: codes for rules of other handbooks that this one lacks, so the list hints at none of its own rules.
    WEEKEND_TRAVEL_HOME = "WEEKEND_TRAVEL_HOME"
    WEEKEND_TRIP_NOT_EARNED = "WEEKEND_TRIP_NOT_EARNED"
    NEXT_OF_KIN_TRAVEL = "NEXT_OF_KIN_TRAVEL"
    FLY_AMERICA_US_CARRIER_REQUIRED = "FLY_AMERICA_US_CARRIER_REQUIRED"
    OPEN_SKIES_AGREEMENT = "OPEN_SKIES_AGREEMENT"
    CHANCELLOR_WRITTEN_AUTHORIZATION = "CHANCELLOR_WRITTEN_AUTHORIZATION"
    DOUBLE_BOOKING_PROHIBITED = "DOUBLE_BOOKING_PROHIBITED"
    PRIVATE_AIRCRAFT_NOT_APPROVED = "PRIVATE_AIRCRAFT_NOT_APPROVED"
    TRAVEL_PACKAGE_NOT_ITEMIZED = "TRAVEL_PACKAGE_NOT_ITEMIZED"


class TripType(Enum):
    ONE_WAY = "ONE_WAY"
    ROUND_TRIP = "ROUND_TRIP"


class Topic(Enum):
    ALL = "ALL"
    FIELDS = "FIELDS"
    AIRPORTS = "AIRPORTS"


CODE = "An IATA airport code, e.g. JFK"


@dataclass
class Airport(Output):
    code: Annotated[str, CODE]
    name: Annotated[str, "The airport's name"]
    city: Annotated[str, "The city it serves"]
    country: Annotated[str, "Its country, as an ISO code"]


@dataclass
class Segment(Output):
    flight_number: Annotated[str, "The airline's flight number, e.g. BA 117"]
    origin: Annotated[str, CODE]
    destination: Annotated[str, CODE]
    depart_local: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, local time at that airport"]
    arrive_local: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, local time at that airport"]
    depart_utc: Annotated[str, "When it leaves: YYYY-MM-DD HH:MM, UTC"]
    arrive_utc: Annotated[str, "When it lands: YYYY-MM-DD HH:MM, UTC"]
    scheduled_minutes: Annotated[int, "Its scheduled time from departure to arrival, in minutes"]


@dataclass
class Offer(Output):
    offer_id: Annotated[str, "The offer's id, to submit when booking or holding it"]
    carrier: Annotated[str, "The airline"]
    trip_type: Annotated[TripType, "ONE_WAY, or ROUND_TRIP when the fare covers the flights out and back"]
    cabin: Annotated[Cabin, "The cabin sold on every flight of the offer"]
    fare_cents: Annotated[int, "The whole fare for one passenger, in cents of the search's currency"]
    seats_available: Annotated[bool, "False when this cabin is sold out on these flights: it is listed but cannot be bought"]
    refundable: Annotated[bool, "Whether the fare can be refunded or changed without a fee"]
    stops: Annotated[int, "Connections on the way out; zero for a nonstop"]
    segments: Annotated[list[Segment], "The flights out, in order"]
    layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights out"]
    stopover_nights: Annotated[list[bool], "Per connection out: true when it is a ticketed stopover with a hotel night booked"]
    flying_minutes: Annotated[int, "The flights' scheduled minutes out added together, ground time left out"]
    elapsed_minutes: Annotated[int, "Minutes from the first departure out to the last arrival, ground time included"]
    return_segments: Annotated[list[Segment], "For a round trip, the flights back, in order; empty otherwise"]
    return_layover_minutes: Annotated[list[int], "Minutes on the ground between consecutive flights back"]
    return_stopover_nights: Annotated[list[bool], "Per connection back: true for a ticketed stopover with a hotel night"]
    return_flying_minutes: Annotated[int, "The flights' scheduled minutes back added together; zero one way"]
    return_elapsed_minutes: Annotated[int, "Minutes from the first departure back to the last arrival; zero one way"]


# ---------------------------------------------------------------------------------------------------------
# HANDBOOK-SPECIFIC: Anixter, Global Travel, Entertainment & Expense Policy (revised March 24, 2014).
# ---------------------------------------------------------------------------------------------------------


class Scenario(Enum):
    ASPEN_KNOLL = "aspen-knoll"
    BASIL_CRAG = "basil-crag"
    BIRCH_LAGOON = "birch-lagoon"
    COBBLE_MERE = "cobble-mere"
    COPPER_SEDGE = "copper-sedge"
    DAHLIA_GLEN = "dahlia-glen"
    DOVER_KILN = "dover-kiln"
    ELM_CASCADE = "elm-cascade"
    EMBER_SHOAL = "ember-shoal"
    FENNEL_CLIFF = "fennel-cliff"
    FLINT_MARSH = "flint-marsh"
    GARNET_RILL = "garnet-rill"
    GORSE_INLET = "gorse-inlet"
    HERON_SCREE = "heron-scree"
    HOLLOW_PIKE = "hollow-pike"
    IVORY_BROOK = "ivory-brook"
    JASPER_FEN = "jasper-fen"
    KETTLE_MOOR = "kettle-moor"
    LARK_GULLY = "lark-gully"
    MOSSY_WEIR = "mossy-weir"
    NECTAR_BLUFF = "nectar-bluff"
    ONYX_GROVE = "onyx-grove"
    PEBBLE_COVE = "pebble-cove"
    QUILL_MEADOW = "quill-meadow"
    RAVEN_FORD = "raven-ford"
    SABLE_HEATH = "sable-heath"
    TANSY_RIDGE = "tansy-ridge"
    UMBER_WOLD = "umber-wold"
    VESPER_DALE = "vesper-dale"
    WALNUT_SPUR = "walnut-spur"
    YARROW_TARN = "yarrow-tarn"
    ZINNIA_LOCH = "zinnia-loch"


class Approver(Enum):
    """Roles that may sign off. NONE: the decision relies on no one's sign-off, given or awaited (one for
    something else may be on file). NOT_NAMED: one is needed, but the handbook names no role."""

    NONE = "NONE"
    NOT_NAMED = "NOT_NAMED"
    IMMEDIATE_SUPERVISOR = "IMMEDIATE_SUPERVISOR"
    MANAGER = "MANAGER"
    SENIOR_EXECUTIVE = "SENIOR_EXECUTIVE"
    EXECUTIVE_VP = "EXECUTIVE_VP"
    RVP = "RVP"
    FINANCE_VP = "FINANCE_VP"
    CEO = "CEO"
    CFO = "CFO"
    LEGAL_DEPARTMENT = "LEGAL_DEPARTMENT"
    HUMAN_RESOURCES = "HUMAN_RESOURCES"
    TRAVEL_AGENCY = "TRAVEL_AGENCY"


class Clause(Enum):
    """The handbook's sections, by heading."""

    INTRODUCTION = "INTRODUCTION"
    POLICY_OVERVIEW = "POLICY_OVERVIEW"
    TRAVELER_REQUIREMENTS = "TRAVELER_REQUIREMENTS"
    NON_REIMBURSABLE = "NON_REIMBURSABLE"
    SENIOR_EXECUTIVE_APPROVAL = "SENIOR_EXECUTIVE_APPROVAL"
    RESERVATIONS = "RESERVATIONS"
    PASSPORTS_VISAS = "PASSPORTS_VISAS"
    CORPORATE_CREDIT_CARDS = "CORPORATE_CREDIT_CARDS"
    COMMERCIAL_AIRLINES = "COMMERCIAL_AIRLINES"
    LOWEST_LOGICAL_AIRFARE = "LOWEST_LOGICAL_AIRFARE"
    ADVANCE_PURCHASE = "ADVANCE_PURCHASE"
    CLASS_OF_SERVICE = "CLASS_OF_SERVICE"
    NON_REFUNDABLE_TICKETS = "NON_REFUNDABLE_TICKETS"
    UNUSED_TICKETS = "UNUSED_TICKETS"
    DENIED_BOARDING = "DENIED_BOARDING"
    FREQUENT_FLYER = "FREQUENT_FLYER"
    CREATIVE_TICKETING = "CREATIVE_TICKETING"
    RENTAL_CARS = "RENTAL_CARS"
    HOTELS = "HOTELS"
    EXTENDED_TRAVEL = "EXTENDED_TRAVEL"
    COMPANION_TRAVEL = "COMPANION_TRAVEL"
    COMBINED_TRAVEL = "COMBINED_TRAVEL"
    GIFTS = "GIFTS"
    EXPENSE_GUIDELINES = "EXPENSE_GUIDELINES"
    EXPENSE_APPROVAL = "EXPENSE_APPROVAL"


class Passenger(Enum):
    EMPLOYEE = "EMPLOYEE"
    ACCOMPANYING_NON_EMPLOYEE = "ACCOMPANYING_NON_EMPLOYEE"


class Purpose(Enum):
    CUSTOMER_MEETING = "CUSTOMER_MEETING"
    INTERNAL_MEETING = "INTERNAL_MEETING"
    TRAINING = "TRAINING"
    TRADE_SHOW = "TRADE_SHOW"
    SITE_VISIT = "SITE_VISIT"
    PERSONAL = "PERSONAL"


class ExtraDays(Enum):
    """What the days between business_return_date and return_date are for."""

    NONE = "NONE"
    LATER_RETURN_FOR_FARE = "LATER_RETURN_FOR_FARE"
    PERSONAL_DAYS = "PERSONAL_DAYS"


class ApprovalSubject(Enum):
    BUSINESS_CABIN = "BUSINESS_CABIN"
    NON_EMPLOYEE_TICKET = "NON_EMPLOYEE_TICKET"
    LATER_RETURN = "LATER_RETURN"
    PERSONAL_DAYS = "PERSONAL_DAYS"


@dataclass
class Approval(Output):
    approver_name: Annotated[str, "Who gave it"]
    approver_title: Annotated[str, "Their job title"]
    approver_reports_to: Annotated[str, "The job title of the person they report to"]
    subject: Annotated[ApprovalSubject, "What it covers"]
    in_writing: Annotated[bool, "True when it is on file as a signed document or email; false when it was only said"]
    given_on: Annotated[str, "The day it was given, YYYY-MM-DD"]


@dataclass
class Trip(Output):
    traveller_name: Annotated[str, "Who flies"]
    traveller_title: Annotated[str, "Their job title, or their relation to the employee they accompany"]
    traveller_reports_to: Annotated[str, "For an employee, the job title of the person they report to; empty otherwise"]
    passenger: Annotated[Passenger, "What the person flying is to the company"]
    accompanies: Annotated[str, "For a non-employee, the employee they go with, by name and title; empty otherwise"]
    employing_company: Annotated[str, "The company unit that employs the traveller, or the employee they go with"]
    home_country: Annotated[str, "That unit's country, as an ISO code"]
    origin: Annotated[Airport, "Where the flight leaves from"]
    destination: Annotated[Airport, "Where the traveller has to be"]
    travel_date: Annotated[str, "The day to leave, YYYY-MM-DD: the local date at the origin airport"]
    return_date: Annotated[str, "For a round trip, the day the traveller asks to fly back, YYYY-MM-DD; empty for one way"]
    business_return_date: Annotated[
        str, "For a round trip, the day the traveller would fly back if the trip held only its working days; empty for one way"
    ]
    extra_days: Annotated[ExtraDays, "Why return_date is later than business_return_date; NONE when they are the same day"]
    extra_days_cost_cents: Annotated[
        int, "Hotel and meal cost in cents of the days between those two dates that would be claimed from the company; zero when none"
    ]
    booking_date: Annotated[str, "Today in this world, the day the ticket is bought, YYYY-MM-DD"]
    purpose: Annotated[str, "Why the trip is made, in plain words"]
    purpose_kind: Annotated[Purpose, "The kind of trip"]
    trip_authorized_by: Annotated[str, "Who agreed that the trip should happen, and how; empty when nobody has"]
    requested_cabin: Annotated[Cabin, "The cabin the traveller asks for"]
    requested_airline: Annotated[str, "An airline the traveller asks for by name; empty when none"]
    requested_airline_why: Annotated[str, "The traveller's reason for asking for that airline; empty when none"]
    requested_ticket_to: Annotated[
        str, "An airport code the traveller asks to be ticketed to when it is not where they have to be; empty otherwise"
    ]
    customer_cabin: Annotated[
        Cabin, "The cabin a customer flying with the traveller on the same flights has booked; NONE when no customer flies with them"
    ]
    preferred_airlines: Annotated[list[str], "Airlines with a negotiated company agreement, by name; empty when none are on file"]
    non_employee_reason: Annotated[
        str, "For a non-employee, the documented reason the company has for them to come; empty when none is documented"
    ]
    approvals: Annotated[list[Approval], "Sign-offs on file for this trip"]
    notes: Annotated[list[str], "Other facts on file for this trip"]


# ---------------------------------------------------------------------------------------------------------
# SHARED (template), continued: the tools' and tasks' inputs and outputs.
# ---------------------------------------------------------------------------------------------------------


@dataclass
class TaskInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    request: Annotated[str, "The traveller's request, in their own words"]


@dataclass
class TripInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id, as the task input gives it"]


@dataclass
class TripOutput(Output):
    scenario: Annotated[Scenario, "The case id"]
    request: Annotated[str, "The traveller's request, in their own words"]
    trip: Annotated[Trip, "The trip record behind the request"]


@dataclass
class SearchInput(Output):
    scenario: Annotated[Scenario, "The booking request's case id"]
    origin: Annotated[str, "The airport to leave from: An IATA airport code, e.g. JFK"]
    destination: Annotated[str, "The airport to fly to: An IATA airport code, e.g. JFK"]
    date: Annotated[str, "The day to leave, YYYY-MM-DD: the local date at the origin airport, on or after the booking date"]
    return_date: Annotated[str, "For round-trip fares, the day to fly back, YYYY-MM-DD, local at the destination; empty for one way"]


@dataclass
class SearchOutput(Output):
    note: Annotated[str, "Where the offers come from, and a word when this case lists none for the search"]
    currency: Annotated[str, "The currency of every fare, as an ISO code"]
    offers: Annotated[list[Offer], "Every offer leaving on that local date, in departure order"]


@dataclass
class BookingOutput(Output):
    decision: Annotated[
        Decision,
        "BOOK: buy offer_id now. REFUSE: buy nothing, because the organisation buys no ticket at all for this request. "
        "FLAG_FOR_APPROVAL: hold offer_id and buy nothing yet, because someone must approve it first or "
        "the handbook's words leave the answer open",
    ]
    offer_id: Annotated[str, "The offer bought or held, exactly as search_flights listed it; empty when refusing"]
    cabin: Annotated[Cabin, "That offer's cabin; NONE when refusing"]
    reason_code: Annotated[ReasonCode, "Why, from the closed list"]
    approver: Annotated[
        Approver,
        "The role whose sign-off this decision relies on, whether already on file or still awaited; NONE when "
        "this decision relies on no one's sign-off, even if a sign-off for something else is on file; NOT_NAMED "
        "when a sign-off is needed but the handbook names no role",
    ]
    clause: Annotated[Clause, "The handbook section the decision rests on"]


@dataclass
class SolveOutput(Output):
    trip: Annotated[Trip, "The trip record"]
    offers: Annotated[list[Offer], "Every offer on the trip's route and date"]
    decision: Annotated[Decision, "The correct decision"]
    offer_ids: Annotated[list[str], "Every offer id that is a correct choice; empty when refusing"]
    cabins: Annotated[list[Cabin], "Every correct cabin"]
    reason_codes: Annotated[list[ReasonCode], "Every accepted reason"]
    approvers: Annotated[list[Approver], "Every accepted approver"]
    clauses: Annotated[list[Clause], "Every accepted section"]
    unclear_phrase: Annotated[str, "For a hold over unclear words, those words; empty otherwise"]
    explanation: Annotated[str, "How the answer key reached the answer"]


@dataclass
class FieldHelp(Output):
    name: Annotated[str, "The trip record field's name"]
    kind: Annotated[str, "Its type"]
    description: Annotated[str, "What it means"]


@dataclass
class RequirementsInput(Output):
    topic: Annotated[Topic, "ALL for everything, FIELDS for the trip record's fields, AIRPORTS for the airport list"]


@dataclass
class RequirementsOutput(Output):
    fields: Annotated[list[FieldHelp], "The trip record's fields; empty for AIRPORTS"]
    conventions: Annotated[list[str], "How times, dates, fares and seats work in this world; empty for AIRPORTS"]
    airports: Annotated[list[Airport], "The airports the simulated world knows; empty for FIELDS"]


TOOLS = {
    Tool.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Tool.GET_TRIP: (TripInput, TripOutput),
    Tool.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Tool.SOLVE_BOOKING: (TaskInput, SolveOutput),
}
TASKS = {
    Task.BOOKING_REQUIREMENTS: (RequirementsInput, RequirementsOutput),
    Task.SEARCH_FLIGHTS: (SearchInput, SearchOutput),
    Task.BOOK_FLIGHT: (TaskInput, BookingOutput),
}
