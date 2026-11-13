# Test Plan: Single Bet Placement

| | |
|---|---|
| Application | https://qae-assignment-tau.vercel.app/ |
| Reference | Single Bet Placement Feature Specification |
| Scope | Desktop web (Chrome) and the backend API for the single bet flow |

## How I prioritised

I ranked the scenarios by business impact if they fail:

1. Money. A wrong deduction or payout is a direct loss or a customer dispute.
2. Bets that should never be accepted, like past events or invalid stakes. This is a fraud and compliance risk.
3. User trust. A confusing receipt or a broken error flow means support tickets.
4. Backend validation. The API can be called without the UI, so the backend must enforce rules 1–2 itself and not rely on the UI checks.

Precondition for every scenario: reset the balance with `POST /api/reset-balance` and note the starting value from `GET /api/balance`.

## Test Scenarios

| ID | Title | Priority | Risk Rationale | Steps | Expected Result |
|---|---|---|---|---|---|
| TC&#8209;01 | Place a valid single bet: receipt and balance are correct | Critical | This is the main revenue flow. If the recorded bet (teams, selection, odds, stake, payout) doesn't match what the user picked, we either pay out the wrong amount or settle a bet the user never made. Both end in disputes. | 1. Open the app with `?user-id=<id>`<br>2. On an upcoming match click 2 (away), note teams and odds<br>3. Check the bet slip shows the match, selection and odds<br>4. Enter stake `10`<br>5. Check bet slip payout = 10 × odds<br>6. Click Place Bet<br>7. Check the receipt, then close it | • Button shows `Placing...` while in progress<br>• Receipt shows Bet ID, match, selection, stake €10.00, odds, payout and timestamp, all matching the bet slip<br>• Balance drops by exactly €10.00 in the header, the bet slip and `GET /api/balance`<br>• Bet slip is empty after closing the receipt |
| TC&#8209;02 | Stake limits and format | Critical | The stake limits cap how much we can lose per bet. Off-by-one bugs live right at the limits, and the spec disagrees on the minimum (see ambiguity #1). | 1. Select any upcoming outcome<br>2. Try each stake: `0.99`, `1.00`, `1.01`, `100.00`, `100.01`, `1.234`, `abc`, empty, `-5`, `0`<br>3. Send the invalid ones with `POST /api/place-bet` too | • `1.00`*, `1.01`, `100.00` accepted<br>• `0.99`: "Minimum stake is €1.00"<br>• `100.01`: "Maximum stake is €100.00"<br>• `1.234`, `abc`, empty, `-5`, `0` blocked<br>• API returns 422 for invalid values<br>• Balance unchanged after each rejection<br>*see ambiguity #1 |
| TC&#8209;03 | Only upcoming matches can be bet on | Critical | Betting on a match that is already played means betting on a known result. That is a guaranteed loss and a compliance problem. | 1. Compare kickoff dates in the list with today<br>2. Try to bet on a past match in the UI<br>3. Send `POST /api/place-bet` with that `matchId` | • Past matches are not listed (the section says "Upcoming")<br>• If one is listed, it can't be bet on<br>• API returns 422<br>• Balance unchanged |
| TC&#8209;04 | Stake higher than the balance | High | Users must not bet money they don't have. Separate from TC-02 because once the balance is under €100, the balance is the real limit, not the €100 max. | 1. Place bets until the balance is under €100 (e.g. €40)<br>2. Enter a stake above the balance but ≤ €100 (e.g. €50)<br>3. Click Place Bet<br>4. Repeat with the API | • UI shows "Insufficient balance", no bet placed<br>• API returns 422<br>• Balance unchanged |
| TC&#8209;05 | Errors and double submit | High | Double clicks and retries are where duplicate bets and double charges happen. If the error flow is unclear, users retry blindly or think a bet went through when it didn't. | 1. Double-click Place Bet quickly<br>2. Send two `place-bet` requests at the same time<br>3. Trigger the error modal (DevTools offline/throttling), check title and text<br>4. Click Rebet, then repeat with Close, then with X | • One bet placed, stake deducted once, second request gets 409<br>• Modal title "Something went wrong" with a retry message<br>• Rebet closes the modal and retries<br>• Close / X close the modal and clear the selection and stake |
| TC&#8209;06 | API requests, auth and reset | Medium | The API can be called without the UI, so it is the last check. Every test starts with a reset, so the reset has to be reliable. | 1. `place-bet` without `x-user-id`<br>2. `place-bet` with `selection: "WIN"`<br>3. `place-bet` with unknown / blank `matchId`<br>4. `place-bet` with body `[]` / broken JSON<br>5. `GET /api/place-bet`<br>6. `POST /api/reset-balance`, then `GET /api/balance` | 1. 401<br>2. 422<br>3. 422<br>4. 400<br>5. 405<br>6. Both return €125.50<br>• No request changes the balance |

I executed the 3 Critical scenarios (TC-01 to TC-03) manually. Results are in [BUG_REPORTS.md](BUG_REPORTS.md).

## Spec ambiguities to clarify with the Product Owner

| # | Topic | Conflict |
|---|---|---|
| 1 | Minimum stake | €1.00 (§3, §4.4) vs €1.01 (§4.1) |
| 2 | Reset-balance docs | Swagger says the reset "response payload may differ from persisted balance". §5.3 says they must match |
| 3 | Odds filter range | The filter only allows 1.00 to 10.00, but valid odds are 1.01 to 1000.00 (§3), so users can't filter for odds above 10 |
| 4 | Kickoff time | §2.1 says each match shows a kickoff date/time, but the API contract in §5.3 only has `kickoffDate` (YYYY-MM-DD). Without a time, it's unclear when betting on a match later today should close (see TC-03) |

## Not covered by the scenarios

| Area | Reason |
|---|---|
| Date and odds filters (§2.6) | No money moves through them, so they're lower risk than the 6 scenarios. Covered by exploratory checks instead (BUG-14 to BUG-16) |
| Live betting, multi-bets, other sports, mobile | Out of scope in the spec |
