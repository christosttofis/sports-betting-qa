# Strategy & Recommendations

## Why these two tests

**API test: stake validation (TC-02)**
- Most of the serious bugs were in backend validation. The UI blocks invalid stake values, but anyone can skip the UI and call the API directly. That is how BUG-06 (negative stake) was found.
- It is data driven: one parametrized test checks every stake limit and format rule. It runs in seconds, needs no browser and is stable.

**UI test: place a single bet (TC-01)**
- It is the main money flow of the feature and goes through the whole journey, from the match list to the balance.
- The receipt bugs (BUG-01 teams reversed, BUG-03 wrong payout) only show up in the UI. An API test can't catch them.

The API test checks the rules, the UI test checks what the user sees, so they don't overlap.

The other strong candidate was TC-03 (bets on past matches, BUG-07). It would also make a good API test. I picked TC-02 because one test covers more rules. TC-03 is next in line.

Known bugs are marked `xfail` with the bug ID and `strict=True`, so the suite stays green while they are open and turns red once one is fixed.

## What I left manual

| Area | Why |
|---|---|
| Exploratory testing | Its value is in trying things nobody planned. Most bugs outside the top 3 scenarios came from here |
| Look and wording of the receipt and modals | Visual checks. A human spots layout and text problems faster than an assertion |
| Error modal, Rebet and Close (UI part of TC-05) | The modal only appears when `place-bet` fails, and the live app can't be made to fail on demand. Faking the failure in Selenium is fragile, so a manual check is cheaper for now |
| Filters (§2.6) | Lower risk: they affect finding matches, not money |
| Spec questions (e.g. minimum stake €1.00 vs €1.01) | Nothing to automate until the Product Owner decides |

## Recommendations

**1. API tests for every business rule, not just the stake limits.**
The critical bugs were all in backend validation, so this is where automation pays off most. Add fast API tests for stake vs balance (BUG-09), past matches (BUG-07) and duplicate bets (BUG-10, BUG-17). A contract check against the OpenAPI file, for example with Schemathesis, would also catch wrong responses and error codes (BUG-05, BUG-12, BUG-13).

**2. A proper test environment and test data.**
All tests share one user on the live app, so CI runs can't run in parallel. A staging environment with a test user per run would fix that. Tests also need a reliable reset (BUG-08), a bet history endpoint to check the bet itself, and a way to force a `place-bet` failure so the error modal can be automated.

**3. Clarify the spec with the Product Owner.**
These decide what the tests should expect:
- Minimum stake: €1.00 or €1.01
- When betting on a match closes, since the API has no kickoff time
- Odds filter range: 1 to 10 in the UI, 1.01 to 1000 in the spec
- Reset balance: Swagger says the response may differ from the stored balance, §5.3 says they must match
- Whether the same bet placed again right after the first one is allowed or should be blocked as a duplicate

Smaller things for later: trigger the suite from the app's deploy pipeline, Allure for test history and flaky tests, and a real auth token instead of the `x-user-id` header.
