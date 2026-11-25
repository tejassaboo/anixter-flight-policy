# Validation notes: anixter-flight-policy (paid wave 1 validation v3, 2026-11-25)

Run: `efficient_corporate_travel_agent/pilot/ladder/runs/validation_w1v3_2026-11-25/anixter-flight-policy@w1v3/`,
arm `full`, DeepSeek V4 Flash, temperature 0, max_steps 6, max_tokens 8192, one run per scenario, at plugin head
57ae273. Line numbers are lines of `src/plugin/data/policy.txt`.

## Results

27/32 valid (84.4%), **easy 6/6**. By category: boundary 7/8, distractor 3/3, easy 6/6, flag 1/4, hidden 3/3,
multi 5/5, refusal 2/3. Re-scoring the stored submissions under this commit's verifier (no paid call) gives the
same **27/32, easy 6/6**: all five failures are slips, and the one fix is latent (every case it touches passed).

## Every failure, classified

| scenario | category | submitted vs key | class | evidence |
|---|---|---|---|---|
| dahlia-glen | refusal | REFUSE, PERSONAL_TRAVEL_NOT_COVERED, NONE right; clause NON_REIMBURSABLE; key COMBINED_TRAVEL, INTRODUCTION or POLICY_OVERVIEW | model slip | It named the ground itself, "the company will not reimburse non-business related expenses ... The company's travel policy covers business-related travel", which is the Introduction and Overview (lines 36-37, 45-46, 85-86), then picked the clause by name: "Let me use NON_REIMBURSABLE?". Lines 126-145 list expense items (upgrades, mini-bar, companions' expenses); a personal trip is not among them. Same treatment as Standex quince-ember and Dollar General umber-vale in wave 2; unlike Goodman thistle-bay, the picked section does not state the ground. |
| ember-shoal | flag | BOOK business, INTERNATIONAL_LONG_FLIGHT; key FLAG, UNCLEAR_POLICY_TEXT | model slip | It quoted lines 302-303 ("all flights with duration of 5 hours or less must be booked in Coach") and then measured only line 307's total: "flying_minutes 565 = 9.4 hours ... So business class is allowed." It never looked at the two flights (290 and 275 minutes), each five hours or less. Both twins (ivory-brook, yarrow-tarn) passed. |
| fennel-cliff | flag | BOOK economy, US_ORIGIN_CANADA_MEXICO_CARIBBEAN; key FLAG, UNCLEAR_POLICY_TEXT | model slip | "Senior executive is defined as 'the President and CEO and his direct reports' ... Paul Brandt is NOT a senior executive." It took line 554 as settled and never weighed lines 57-58 ("any Vice President reporting to the CEO or CFO") and 165 ("their Vice President direct reports"). The Canada exclusion it also cited (line 308) bars only line 307's instance, not line 310's written approval. Twins raven-ford and sable-heath passed. |
| gorse-inlet | flag | BOOK business with the customer, SAME_CLASS_AS_CUSTOMER; key FLAG, UNCLEAR_POLICY_TEXT | model slip | "domestic flight ... 4.5 hours ... so normally coach. But the customer exception applies." It saw both lines and settled the order without weighing the "must" of lines 302-303 against line 311. Twins dover-kiln and tansy-ridge passed. Same class as 2026-11-24. |
| onyx-grove | boundary_twin | BOOK the Jan 31 return EV98-KF7U ($423), COMBINED_TRIP_NO_ADDED_COST; key the Jan 27 return ($418), COMBINED_TRIP_ADDED_COST | model slip | It searched only the Jan 31 round trip and never the record's `business_return_date` (Jan 27): "The extra days cost 0 to the company. So the combined travel is fine." `extra_days_cost_cents` is documented as "Hotel and meal cost ... of the days between those two dates", not the fare; line 464 asks for "no additional cost to the company", and the longer return costs $5 more. The record is right and the twin nectar-bluff (longer return cheaper, same fields) passed. |

## Fixes (this commit)

`src/plugin/rules.py` and the byte-identical `verifier/rules.py`, `tests/build_scenarios.py`, README rows,
regenerated scenario JSON. No id, world, request, decision or category changed.

1. **Long-flight business (copper-sedge and elm-cascade, both easy; ivory-brook, quill-meadow):**
   `LONG_FLIGHT_APPROVED` accepted beside `INTERNATIONAL_LONG_FLIGHT` on the line-307 ground. This is the
   cross-plugin gap found in wave 2 (FedEx cinder-heath; Goodman 226e7c7). The shared code list describes neither
   code, and both name the ground. All four answered `INTERNATIONAL_LONG_FLIGHT` in this run and passed, so the gap
   was latent.
2. **Route codes:** no change needed. No Anixter BOOK takes a connection over a nonstop the traveller asked for
   (yarrow-tarn's connection declines business, not a nonstop; ember-shoal is a hold).

Not loosened: dahlia-glen, ember-shoal, fennel-cliff, gorse-inlet, onyx-grove.

## Q2

The always-cheapest agent books coach, so fix 1 changes nothing for it: **5/32 (16%)**, unchanged
(`MAX_PASS_ALWAYS_LOWEST = 5`).

## Re-run

None required: no record or request changed. Optional: the three class-of-service flags (ember-shoal,
fennel-cliff, gorse-inlet) failed the same way on 2026-11-24, so a re-run measures variance only.

## Checks

`uv run pytest -q` (260 passed), `uv run ruff check .`, `uv lock --check`, `check_shared.py`,
`tools/stock_verify.py` (32 scenarios, 0 failures), stock `nanoagent plugin inspect .` (exit 0).
