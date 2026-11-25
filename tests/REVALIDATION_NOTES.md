# Re-validation of 2026-11-24 (evening): Anixter failures, classified

Run: `efficient_corporate_travel_agent/pilot/ladder/runs/revalidation_2026-11-24/` (`anixter-flight-policy@v2`,
`val_full`, one run per scenario, 28 runs, 6 valid, 22 failures). Line numbers are lines of the frozen handbook
(`src/plugin/data/policy.txt`).

## The approver rule (template sync 4')

15 of the 22 failures were wrong only on the approver: the model answered `NONE` on a BOOK where the trip
authorization (line 50), and in some cases the manager's sign-off, was already on file. These were birch-lagoon,
copper-sedge, dover-kiln, elm-cascade, flint-marsh, garnet-rill, hollow-pike, ivory-brook, kettle-moor,
mossy-weir, nectar-bluff, onyx-grove, sable-heath, umber-wold and yarrow-tarn. Under 4', every BOOK now accepts
`NONE` as well as the roles it accepted before. Holds that await a sign-off still accept only the awaited
role(s). The givers of the invalid sign-offs in sable-heath and umber-wold are still not accepted.
`MAX_PASS_ALWAYS_LOWEST` goes from 0 to 5: birch-lagoon, flint-marsh, garnet-rill, walnut-spur and
zinnia-loch.

The other 7 failures are classified below. Where they also answered `NONE` on a BOOK, rule 4' covers that part.

## Every other failure, classified

| scenario | category | submitted vs key | class | evidence | fix |
|---|---|---|---|---|---|
| aspen-knoll | distractor | clause LOWEST_LOGICAL_AIRFARE (and approver NONE); key COMMERCIAL_AIRLINES / EXPENSE_GUIDELINES / TRAVELER_REQUIREMENTS. Offer, cabin and reason right | **grader defect** | It booked Delta at the tied lowest fare because Delta is preferred (102-103, 107, 674), with reason LOWEST_FARE, which the key accepts. That reason rests on line 313, under "Non-Refundable Tickets", and on the "Lowest Logical Airfare" section (287). Every other lowest-fare booking accepts those sections, but this key did not. | The preferred-tie branch of `rules.lowest_economy` also accepts LOWEST_LOGICAL_AIRFARE and NON_REFUNDABLE_TICKETS. zinnia-loch's key had the same gap (it accepted NON_REFUNDABLE_TICKETS but not LOWEST_LOGICAL_AIRFARE), so `rules.loyalty` now accepts LOWEST_LOGICAL_AIRFARE. |
| ember-shoal | flag | BOOK am-business, INTERNATIONAL_LONG_FLIGHT, NONE; key FLAG / UNCLEAR_POLICY_TEXT | model slip | "Flying time = 290 + 275 = 565 min > 5 hours. So business class is allowed." It read only line 307 ("total flying time ... excluding layover"). It never weighed lines 302-303 ("all flights with a duration of five hours or less ... must be booked in Coach"), which cover each of the two flights. This is the per-flight vs. total ambiguity the case tests, and its twins (ivory-brook, yarrow-tarn) pin both sides. | none |
| fennel-cliff | flag | BOOK ac-business, SENIOR_EXECUTIVE_APPROVED; key FLAG / UNCLEAR_POLICY_TEXT. Approver and clause right | model slip | "The policy defines a senior executive as any VP reporting to the CEO or CFO" (57-58, 165). It never weighed "Documented Executive VP approval" (58) or line 554 ("the President and CEO and his direct reports", which makes anyone below them "one level below"). Line 554 is not limited to the gifts section, so both readings stand. | none |
| gorse-inlet | flag | BOOK ua-business, SAME_CLASS_AS_CUSTOMER, NONE; key FLAG / UNCLEAR_POLICY_TEXT | model slip | "Domestic ... 270 minutes ... normally coach is required. However, the exception applies." It treated line 311 as overriding the "must" of lines 302-303 without seeing that the handbook gives no order between them. Same pattern as Thornton velvet-prairie. Twins dover-kiln and tansy-ridge pin each side. | none |
| heron-scree | flag | reason COMPANION_NOT_AUTHORIZED; key APPROVAL_REQUIRED. Decision, offer, cabin, approver SENIOR_EXECUTIVE and clause COMPANION_TRAVEL right | **grader defect** | "The companion's travel needs senior executive authorization that isn't on file ... reason_code COMPANION_NOT_AUTHORIZED." Lines 455-457 say "The travel agency will not issue a ticket for the individual without such authorization", so the plugin's own companion code describes this hold exactly. Same as Thornton kestrel-loom (a second defensible code). The decision still separates it from basil-crag (REFUSE) and walnut-spur (BOOK). | `rules.companion` (no sign-off on file) accepts APPROVAL_REQUIRED or COMPANION_NOT_AUTHORIZED. |
| vesper-dale | hidden_clause | REFUSE, CREATIVE_TICKETING, NONE (no search); key BOOK ua-denver | **scenario defect (request wording)** | The request asks only for the hidden-city ticket ("Book me the hidden-city fare ..."). It gave no fallback, and the instructions say "REFUSE when the organisation buys no ticket at all for this request". The model: "the traveller specifically asked for the hidden-city fare ... we refuse." It identified the ban correctly (346-348). The key's BOOK assumes a fallback that the plugin's other single-option requests state explicitly (raven-ford, sable-heath and umber-wold: "If business isn't possible, put me in economy; I have to be there"). | The request adds "If I can't have that one, book what the policy allows; I have to be at the meeting." The id, answer and category are unchanged. |
| zinnia-loch | distractor | REFUSE, LOYALTY_PROGRAM_PREFERENCE, NONE; key BOOK aa-economy | **scenario defect (request wording)** | Same as vesper-dale. "Book me on United ..." names only the airline that lines 107-108 and 341-342 forbid. The model quoted line 108 correctly, then weighed both options: "the trip is legitimate ... but the request is specifically to book United", and refused. | The request adds "If United isn't possible, book what the policy allows; I have to be at the meeting." The id, answer and category are unchanged. The LOWEST_LOGICAL_AIRFARE clause is added (see aspen-knoll). |

No failure was caused by the budget or the cap. Every failed run stopped with `answer`. 6 runs (4 of them
failures: kettle-moor, mossy-weir, nectar-bluff, onyx-grove, all approver-only) would cross the 65,536-token
hosted cap at step 4, the four-call round-trip cases the README predicts. The run itself was not capped, and
the answers were wrong only on the approver.

## Scenario files changed

- Approver accept set only (4'): birch-lagoon, copper-sedge, dover-kiln, elm-cascade, flint-marsh, garnet-rill,
  hollow-pike, ivory-brook, jasper-fen, kettle-moor, lark-gully, mossy-weir, nectar-bluff, onyx-grove,
  pebble-cove, quill-meadow, raven-ford, sable-heath, tansy-ridge, umber-wold, walnut-spur, yarrow-tarn.
- Approver and clause accept sets: aspen-knoll.
- Reason accept set: heron-scree. Its approver set is unchanged, since it awaits the senior roles.
- Request wording and approver accept set: vesper-dale.
- Request wording, approver and clause accept sets: zinnia-loch.
- Unchanged: basil-crag, cobble-mere, dahlia-glen (refusals), ember-shoal, fennel-cliff, gorse-inlet (unclear
  holds).

`world.py` is unchanged. The `tools/world_diff.py --plugins` run against HEAD shows that pinned searches are
identical. `get_trip` differs only in the request of vesper-dale and zinnia-loch, and the answer keys differ as
listed above.

## Declined requests (lead's decision after the review, template APPROVER_REVIEW.md)

The booking task's instructions now end: "When you book something other than what the traveller asked for, the
reason code gives why their request is declined." Accept sets follow it:

- vesper-dale (hidden-city fare) no longer accepts `LOWEST_FARE`: the ticket asked for is the cheaper one, and
  what declines it is the ban of lines 346-348, so `CREATIVE_TICKETING` only. The paid run gave that code.
- zinnia-loch (United for the miles) keeps `LOWEST_FARE` beside `LOYALTY_PROGRAM_PREFERENCE`: lines 107-108
  decline it because United's fare is higher.
- The other bookings that decline a request (dover-kiln, hollow-pike, yarrow-tarn, pebble-cove, sable-heath,
  umber-wold, kettle-moor, mossy-weir, onyx-grove) never accepted `LOWEST_FARE`.
- Untouched, nothing asked for is declined: aspen-knoll, birch-lagoon, flint-marsh, garnet-rill, walnut-spur.

`MAX_PASS_ALWAYS_LOWEST` stays 5 of 32 (measured).
