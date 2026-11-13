"""E2E UI test: place a single bet and verify the receipt and balance (TC-01)."""

import re
from decimal import Decimal
from typing import Any

import pytest

from api import BettingApiClient, Selection
from pages import HomePage
from utils.config import Settings
from utils.money import expected_payout


@pytest.mark.ui
@pytest.mark.xfail(
    reason="BUG-01: receipt shows the teams reversed; BUG-03: receipt payout is wrong",
    strict=True,
)
def test_place_single_bet(
    fresh_balance: float,  # first, so the balance is reset before the page loads
    home_page: HomePage,
    api: BettingApiClient,
    settings: Settings,
    upcoming_match: dict[str, Any],
) -> None:
    """A user places a valid single bet: slip, receipt and balance must all be correct.

    Why this test: it is the main money flow of the feature (TC-01) and it covers
    the whole journey, from the match list to the balance. Bugs on the receipt
    (BUG-01, BUG-03) only show up in the UI, so an API test can't catch them.
    """
    stake = Decimal("10.00")
    odds = Decimal(str(upcoming_match["odds"]["away"]))
    match_name = f"{upcoming_match['homeTeam']} vs {upcoming_match['awayTeam']}"
    payout = expected_payout(stake, odds)

    # Bet slip shows the selection and the correct potential payout
    home_page.select_odds(upcoming_match["id"], Selection.AWAY)
    bet_slip = home_page.bet_slip
    assert bet_slip.match_name() == match_name
    assert bet_slip.outcome() == "Match Winner: Away"
    assert bet_slip.odds() == odds

    bet_slip.enter_stake(str(stake))
    assert bet_slip.potential_payout() == payout

    bet_slip.place_bet()

    # Money first: the backend must debit exactly the stake
    receipt = home_page.receipt.wait_until_visible()
    assert Decimal(str(api.current_balance())) == Decimal(str(fresh_balance)) - stake

    # Receipt
    assert re.fullmatch(r"#B-\d+", receipt.bet_id())
    assert receipt.stake() == stake
    assert receipt.odds() == odds
    assert receipt.payout() == payout  # BUG-03
    assert receipt.match_name() == match_name  # BUG-01

    # Header balance after closing the receipt. It only updates after a reload (BUG-04).
    receipt.close()
    home_page.open(settings.app_url)
    assert home_page.header_balance() == Decimal(str(fresh_balance)) - stake
