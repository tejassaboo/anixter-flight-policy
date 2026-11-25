# Anixter Global Travel Flight Policy

**Source of the handbook:** https://corpapps.anixter.com/DocLib1/R7699UNJ/$file/Anixter_Global_Travel_Policy.pdf?openelement=. The agent reads it verbatim (bundled at `src/plugin/data/policy.txt`); flights, fares and trips are synthetic.

**No affiliation with Anixter.** The handbook is Anixter's public *Global Travel, Entertainment & Expense Policy*
(revised March 24, 2014), bundled verbatim for research. It is a corporate handbook: do not publish this plugin
before the course staff confirm that a verbatim corporate handbook may be redistributed (MASTER_PLAN section 4).

A `nanoagent.plugin/v0001` plugin. An agent handles one traveller's flight request under the company's real
travel policy: it reads the trip record, searches a simulated flight world and submits **BOOK**, **REFUSE** or
**FLAG_FOR_APPROVAL** with the offer, cabin, reason, approver and handbook section. A deterministic Python
verifier, with no LLM, rebuilds the offers and the handbook's answer itself and checks every field. Built from
the original-handbook template (`handbook_plugins/_template`); `tests/build_scenarios.py` writes the scenario
files (the JSON files are the truth).

## The handbook and the harness flag

The frozen text (`src/plugin/data/policy.txt`, 11,717 words, 994 lines, sha256 `21b7c1d0...aaf10c56`, equal to
`pilot_work/originals/anixter/frozen/SHA256SUMS`) is never paraphrased, and the task text restates no rule. Under
stock NanoAgent the agent does not see it: the plugin then runs as the `off` baseline. The `harness.policy`
switch of the NanoAgent fork (github.com/tejassaboo/nanoagent, branch `policy-switch`) adds it to the system
prompt: `harness.policy: full` adds all of it, and the selection methods add parts of it. These plugins are meant
to run with `query: instructions+input`, so a selector sees the traveller's request.

**Flight duration, as this handbook defines it.** Two clauses measure differently (`rules.DURATION_RULES`,
`rules.over`). Lines 302-303, "all flights with a duration of five hours or less of flying time must be booked
in Coach Class", are per flight and inclusive: 300 scheduled minutes is coach, 301 is not. Line 307,
"International flights when the total flying time exceeds five hours, excluding layover time", adds the
itinerary's scheduled flight minutes, leaves ground time out, and is strict. They agree on a nonstop; on a
connection whose flights are each five hours or less but add up to more, they disagree, which is one flag
(`ember-shoal`). Only outbound flights are measured; every business request is one way.

**Size.** At 1.33 tokens a word (the long-handbook bench's calibration) the handbook alone is about 15,600
tokens (about 19,000 at 4 characters a token: the text is dense with phone numbers and URLs). Under `full` the
first call carries about 17,200 input tokens (handbook, task instructions about 210, tool and submit schemas
about 1,400 at 4 characters a token, the request), and later calls up to about 18,300-19,600 as tool results
accumulate. A run makes 3 calls (`get_trip`, `search_flights`, `submit`): about 53,000 input tokens per run
(52,900 to 54,300; output tokens not counted). The six extended-travel and combined-trip cases need two
round-trip searches, so 4 calls and about 76,000-78,000 input tokens: they cross the hosted cap of 65,536 total
tokens during the fourth call. The other 26 fit, with about 11,000 tokens of margin for output and any extra
search; but an agent that checks the city beyond in `vesper-dale` (a second, one-way search, which the case
allows) makes 4 calls there too, about 72,000 input tokens, and crosses the cap as well. At 4 characters a token for the handbook too, 3-call runs are about 63,200-64,700, so the margin
nearly vanishes; run `full` locally with a raised cap.

## Task

- **Input:** `TaskInput`: `scenario` (one of 32 case ids) and `request`, the traveller's own words.
- **Steps:** `get_trip`, then `search_flights` on each route and date the decision needs (one search for most
  cases: the one-way fare out, unless the trip record gives a return date for a round-trip ticket; a later return or added personal days needs both round trips, and a ticketing-beyond request may
  look at the city beyond), then `submit`.
- **Output:** `BookingOutput`: `decision`, `offer_id` (empty when refusing), `cabin` (`NONE` when
  refusing; otherwise the chosen offer's own cabin), `reason_code`, `approver` and `clause`, each from a closed
  list. The reason list is the template's shared list (codes for rules this handbook lacks) plus 15 Anixter
  codes (`DOMESTIC_COACH_ONLY`, `US_ORIGIN_CANADA_MEXICO_CARIBBEAN`, `SAME_CLASS_AS_CUSTOMER`,
  `SENIOR_EXECUTIVE_APPROVED`, `APPROVER_NOT_AUTHORIZED`, `SELF_APPROVAL`, `APPROVAL_NOT_PRIOR_WRITTEN`,
  `CREATIVE_TICKETING`, `EXTENDED_TRAVEL_SAVINGS`, `EXTENDED_TRAVEL_NOT_OFFSET`, `EXTENDED_TRAVEL_TRIP_TOO_LONG`,
  `COMBINED_TRIP_NO_ADDED_COST`, `COMBINED_TRIP_ADDED_COST`, `COMPANION_NOT_AUTHORIZED`,
  `DENIED_BOARDING_NOT_ALLOWED`; no scenario expects `APPROVAL_NOT_PRIOR_WRITTEN` or
  `DENIED_BOARDING_NOT_ALLOWED`, which stand for rules the cases do not test), plus decoy codes from other
  handbooks' rules (weekend trips home, Fly America and others) so the list hints at none of this one's. Fares are in cents of US dollars (`currency: USD`).
- **Success:** every field is one the answer key accepts. Score = fields right / 6.
- **Hidden facts:** none (`answer_key_inputs` is unused). The org chart the senior-executive cases need (who
  reports to whom) is in the trip record.

| Scenario | Category | Expected decision (offer, cabin) | Reason | Approver | Clause (frozen lines) |
|---|---|---|---|---|---|
| `birch-lagoon` | easy | BOOK (ua-economy; ECONOMY) | LOWEST_FARE | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE or LOWEST_LOGICAL_AIRFARE or NON_REFUNDABLE_TICKETS (302-303, 313) |
| `copper-sedge` | easy | BOOK (aa-business; BUSINESS) | INTERNATIONAL_LONG_FLIGHT or LONG_FLIGHT_APPROVED | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE (306, 307-308, 313) |
| `dover-kiln` | easy | BOOK (ua-economy; ECONOMY) | DOMESTIC_COACH_ONLY or LONG_FLIGHT_CONDITION_NOT_MET or SAME_CLASS_AS_CUSTOMER or UPGRADE_NOT_ELIGIBLE | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE (302-303, 306, 311) |
| `elm-cascade` | easy | BOOK (ac-business; BUSINESS) | INTERNATIONAL_LONG_FLIGHT or LONG_FLIGHT_APPROVED | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE (306, 307-308, 313) |
| `flint-marsh` | easy | BOOK (ua-economy; ECONOMY) | LOWEST_FARE | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE or LOWEST_LOGICAL_AIRFARE or NON_REFUNDABLE_TICKETS (306, 313) |
| `garnet-rill` | easy | BOOK (dl-economy; ECONOMY) | LOWEST_FARE | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE or LOWEST_LOGICAL_AIRFARE or NON_REFUNDABLE_TICKETS (302-303, 313) |
| `hollow-pike` | boundary_twin | BOOK (ac-economy; ECONOMY) | LONG_FLIGHT_CONDITION_NOT_MET or UPGRADE_NOT_ELIGIBLE | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE (302-303, 306, 307-308) |
| `ivory-brook` | boundary_twin | BOOK (ac-business; BUSINESS) | INTERNATIONAL_LONG_FLIGHT or LONG_FLIGHT_APPROVED | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE (302-303, 306, 307-308) |
| `jasper-fen` | boundary_twin | BOOK (dl-later; ECONOMY) | COST_SAVINGS or EXTENDED_TRAVEL_SAVINGS | IMMEDIATE_SUPERVISOR or MANAGER or NONE | EXTENDED_TRAVEL (446-450) |
| `kettle-moor` | boundary_twin | BOOK (dl-first; ECONOMY) | EXTENDED_TRAVEL_TRIP_TOO_LONG | IMMEDIATE_SUPERVISOR or MANAGER or NONE | EXTENDED_TRAVEL (446-450) |
| `lark-gully` | boundary_twin | BOOK (ua-later; ECONOMY) | COST_SAVINGS or EXTENDED_TRAVEL_SAVINGS | IMMEDIATE_SUPERVISOR or MANAGER or NONE | EXTENDED_TRAVEL (446-450) |
| `mossy-weir` | boundary_twin | BOOK (ua-first; ECONOMY) | EXTENDED_TRAVEL_NOT_OFFSET | IMMEDIATE_SUPERVISOR or MANAGER or NONE | EXTENDED_TRAVEL (446-450) |
| `nectar-bluff` | boundary_twin | BOOK (ua-longer; ECONOMY) | COMBINED_TRIP_NO_ADDED_COST | IMMEDIATE_SUPERVISOR or MANAGER or NONE | COMBINED_TRAVEL (313, 463-468) |
| `onyx-grove` | boundary_twin | BOOK (ua-plain; ECONOMY) | COMBINED_TRIP_ADDED_COST | IMMEDIATE_SUPERVISOR or MANAGER or NONE | COMBINED_TRAVEL (313, 463-468) |
| `pebble-cove` | multi_rule | BOOK (as-economy; ECONOMY) | UPGRADE_NOT_ELIGIBLE or US_ORIGIN_CANADA_MEXICO_CARIBBEAN | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE (302-303, 306, 307-308) |
| `quill-meadow` | multi_rule | BOOK (ac-business; BUSINESS) | INTERNATIONAL_LONG_FLIGHT or LONG_FLIGHT_APPROVED | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE (306, 307-308) |
| `raven-ford` | multi_rule | BOOK (ac-business; BUSINESS) | SENIOR_EXECUTIVE_APPROVED | EXECUTIVE_VP or NONE or SENIOR_EXECUTIVE | CLASS_OF_SERVICE or INTRODUCTION or SENIOR_EXECUTIVE_APPROVAL (57-59, 165-166, 306, 307-308, 310, 554-555) |
| `sable-heath` | multi_rule | BOOK (ac-economy; ECONOMY) | APPROVER_NOT_AUTHORIZED or UPGRADE_NOT_ELIGIBLE or US_ORIGIN_CANADA_MEXICO_CARIBBEAN | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE or INTRODUCTION or SENIOR_EXECUTIVE_APPROVAL (57-59, 165-166, 306, 307-308, 310, 554-555) |
| `tansy-ridge` | multi_rule | BOOK (ac-business; BUSINESS) | SAME_CLASS_AS_CUSTOMER | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE (306, 307-308, 311) |
| `umber-wold` | hidden_clause | BOOK (ac-economy; ECONOMY) | SELF_APPROVAL or UPGRADE_NOT_ELIGIBLE or US_ORIGIN_CANADA_MEXICO_CARIBBEAN | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE or EXPENSE_APPROVAL or INTRODUCTION (53, 306, 307-308, 310, 768) |
| `vesper-dale` | hidden_clause | BOOK (ua-denver; ECONOMY) | CREATIVE_TICKETING | IMMEDIATE_SUPERVISOR or NONE | CREATIVE_TICKETING (346-348) |
| `walnut-spur` | hidden_clause | BOOK (wn-economy; ECONOMY) | LOWEST_FARE or SENIOR_EXECUTIVE_APPROVED | EXECUTIVE_VP or NONE or SENIOR_EXECUTIVE | COMPANION_TRAVEL or INTRODUCTION or NON_REIMBURSABLE or SENIOR_EXECUTIVE_APPROVAL (57-59, 313, 452-457) |
| `aspen-knoll` | distractor | BOOK (dl-economy; ECONOMY) | LOWEST_FARE or PREFERRED_CARRIER_REQUIRED | IMMEDIATE_SUPERVISOR or NONE | COMMERCIAL_AIRLINES or EXPENSE_GUIDELINES or LOWEST_LOGICAL_AIRFARE or NON_REFUNDABLE_TICKETS or TRAVELER_REQUIREMENTS (102-103, 107-108, 313, 674) |
| `yarrow-tarn` | distractor | BOOK (ua-economy; ECONOMY) | LONG_FLIGHT_CONDITION_NOT_MET or UPGRADE_NOT_ELIGIBLE | IMMEDIATE_SUPERVISOR or NONE | CLASS_OF_SERVICE (302-303, 306, 307-308) |
| `zinnia-loch` | distractor | BOOK (aa-economy; ECONOMY) | LOWEST_FARE or LOYALTY_PROGRAM_PREFERENCE | IMMEDIATE_SUPERVISOR or NONE | FREQUENT_FLYER or LOWEST_LOGICAL_AIRFARE or NON_REFUNDABLE_TICKETS or TRAVELER_REQUIREMENTS (107-108, 313, 341-342) |
| `basil-crag` | refusal | REFUSE (none; NONE) | COMPANION_NOT_AUTHORIZED or COMPANION_NOT_COVERED | IMMEDIATE_SUPERVISOR or NONE | COMPANION_TRAVEL or NON_REIMBURSABLE (140, 452-457) |
| `cobble-mere` | refusal | REFUSE (none; NONE) | OUTSIDE_POLICY_SCOPE or PERSONAL_TRAVEL_NOT_COVERED | NONE | COMBINED_TRAVEL or INTRODUCTION or POLICY_OVERVIEW (46-47, 85-86, 463-468) |
| `dahlia-glen` | refusal | REFUSE (none; NONE) | OUTSIDE_POLICY_SCOPE or PERSONAL_TRAVEL_NOT_COVERED | NONE | COMBINED_TRAVEL or INTRODUCTION or POLICY_OVERVIEW (46-47, 85-86) |
| `ember-shoal` | flag | FLAG_FOR_APPROVAL (am-business, am-economy; BUSINESS or ECONOMY) | UNCLEAR_POLICY_TEXT | NOT_NAMED or SENIOR_EXECUTIVE | CLASS_OF_SERVICE (302-303, 306, 307-308) |
| `fennel-cliff` | flag | FLAG_FOR_APPROVAL (ac-business, ac-economy; BUSINESS or ECONOMY) | UNCLEAR_POLICY_TEXT | EXECUTIVE_VP or NOT_NAMED or SENIOR_EXECUTIVE | CLASS_OF_SERVICE or GIFTS or INTRODUCTION or SENIOR_EXECUTIVE_APPROVAL (57-59, 165-166, 306, 307-308, 310, 554-555) |
| `gorse-inlet` | flag | FLAG_FOR_APPROVAL (ua-business, ua-economy; BUSINESS or ECONOMY) | UNCLEAR_POLICY_TEXT | NOT_NAMED or SENIOR_EXECUTIVE | CLASS_OF_SERVICE (302-303, 306, 311) |
| `heron-scree` | flag | FLAG_FOR_APPROVAL (wn-economy; ECONOMY) | APPROVAL_REQUIRED or COMPANION_NOT_AUTHORIZED | EXECUTIVE_VP or SENIOR_EXECUTIVE | COMPANION_TRAVEL or INTRODUCTION or NON_REIMBURSABLE or SENIOR_EXECUTIVE_APPROVAL (313, 452-457) |

Mix (EDGE_CASES.md 5.2, 32-scenario row): 6 easy, 8 boundary twins, 5 multi-rule, 3 hidden clause or synonym, 3
distractor, 3 refusal, 4 flags (12.5%; the 15% cap is 4). Boundary twins: 300 against 301 nonstop minutes
(`hollow-pike`, `ivory-brook`); a trip first planned 4 or 6 days apart, avoiding 5, where "less than six days"
depends on whether both ends count (`jasper-fen`, `kettle-moor`); airfare saved against the added hotel and
meals, 34,000 or 32,000 cents against 33,000 (`lark-gully`, `mossy-weir`); "no additional cost" at an equal fare
or 500 cents more (`nectar-bluff`, `onyx-grove`). Each unclear phrase is one flag with clear twins on both
sides: per flight against total flying time (`ember-shoal`; twins `ivory-brook`, `yarrow-tarn`), "senior
executive" for a Vice President reporting to the CFO (`fennel-cliff`; twins `raven-ford`, `sable-heath`), and
coach on a domestic flight with a customer in business (`gorse-inlet`; twins `dover-kiln`, `tansy-ridge`).
`heron-scree` is an approval-required hold (a non-employee's ticket with a documented purpose but no senior
executive's pre-approval), which is never the same as "no compliant offer"; its twins are `walnut-spur`
(approved: BOOK) and `basil-crag` (no business purpose: REFUSE).

Accepted approvers: the approver is the role whose sign-off the decision relies on, on file or awaited. Every
BOOK relies on the immediate supervisor's authorization of the trip (line 50; the trip record says so), so it
accepts `IMMEDIATE_SUPERVISOR` (with `MANAGER` or the senior roles where their sign-off is on file); since every
sign-off a booking relies on is already on file, it accepts `NONE` too (template sync 4', after the 2026-11-24
re-validation). A hold that awaits a sign-off accepts only the awaited role (`heron-scree`: the senior roles;
the unclear holds: `NOT_NAMED` or the senior roles), never `NONE`. A refusal relies on no sign-off and accepts
`NONE` (and `IMMEDIATE_SUPERVISOR` too when a trip authorization it does not use is on file, `basil-crag`). The
invalid sign-offs of `sable-heath` and `umber-wold` are what those cases test, so their givers are not accepted.
Degenerate agents: one that always holds the right offer as unclear passes the 3 unclear holds; one that always
books the cheapest seat with `LOWEST_FARE` and approver `NONE` passes 5 (`birch-lagoon`, `flint-marsh`,
`garnet-rill`, `walnut-spur` and `zinnia-loch`).

## Tools

| Tool | Does | Code |
|---|---|---|
| `booking_requirements` | The trip record's fields, the world's conventions (local times, dates, fares, sold-out seats) and its airports | `src/plugin/guide.py` |
| `get_trip` | A case's request and trip record: traveller and company unit, route, dates, purpose, requested cabin or airline, a customer or non-employee flying along, sign-offs with the approver's place in the org chart, notes | `src/plugin/tools.py` |
| `search_flights` | Every offer on a route and local date (one way, or round trip with `return_date`): the pinned scenario offers plus seeded background offers on those searches only; a search the case does not pin lists nothing and says so | `src/plugin/world.py` |
| `solve_booking` | The answer key (`rules.solve`), the agent task's `reference`, never shown to the agent | `src/plugin/rules.py` |

| Task | Does | Runner |
|---|---|---|
| `book-anixter-flight` | Handles one booking request | `agent`, with `get_trip` and `search_flights`; reference `solve_booking` |
| `booking-requirements` | Shows `booking_requirements` | `tool` |
| `search-flights` | Shows `search_flights` | `tool` |

## Layout

- `contract.py`: the template's shared contract plus this handbook's scenario ids, approvers, sections and trip record.
- `src/plugin/`: `world.py` (the simulated world: real airports and airline hubs, distance-based times
  and fares, hash-seeded background offers and opaque offer ids), `scenarios.py`, `guide.py`,
  `answer.py`, `tools.py`, `rules.py` (this handbook's rules, citing frozen lines), `__main__.py`.
- `src/plugin/data/`: `policy.txt` (frozen), `handbook.json`, `scenarios/*.json`.
- `verifier/`: byte-identical copies of `world.py`, `scenarios.py`, `guide.py`, `answer.py` and
  `rules.py`, plus `booking.py` (`verify_task`) and `tools.py` (`verify_input`, `verify_output`).
- `tests/`: the template's acceptance suite; `tests/plugin_spec.py` holds this handbook's settings;
  `tests/build_scenarios.py` writes the scenario files.

## Develop and run

```bash
uv sync --extra dev
uv run pytest
uv run ruff check .
uv lock --check
python3 tests/build_scenarios.py   # rewrites src/plugin/data/scenarios/*.json
# from a NanoAgent checkout (stock NanoAgent runs this plugin as the `off` baseline;
# the fork's `harness.policy: full` flag adds the handbook):
nanoagent plugin inspect <this folder>
nanoagent plugin pack <this folder> /tmp/anixter-flight-policy.tar.gz
<nanoagent>/.venv/bin/python ../_template/tools/stock_verify.py
```

Offline: `hosts: []`, an empty `.env`, `write: []`, no clock (each case fixes its `booking_date`).
