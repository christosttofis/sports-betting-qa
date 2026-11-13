"""API test: stake validation on POST /api/place-bet (TC-02)."""

from typing import Any

import pytest

from api import BettingApiClient, Selection

INVALID_STAKES = [
    pytest.param(0.99, "invalid_stake_min", id="below-min"),
    pytest.param(0, "invalid_stake_min", id="zero"),
    pytest.param(
        -5,
        "invalid_stake_min",
        id="negative",
        marks=pytest.mark.xfail(reason="BUG-06: negative stake is accepted", strict=True),
    ),
    pytest.param(100.01, "invalid_stake_max", id="above-max"),
    pytest.param(1.234, "invalid_stake_precision", id="three-decimals"),
    pytest.param("abc", "invalid_stake_type", id="not-a-number"),
]


@pytest.mark.api
@pytest.mark.parametrize(("stake", "expected_error"), INVALID_STAKES)
def test_invalid_stake_is_rejected(
    api: BettingApiClient,
    fresh_balance: float,
    upcoming_match: dict[str, Any],
    stake: Any,
    expected_error: str,
) -> None:
    """Invalid stakes must be rejected by the backend and must not update the balance.

    Why this test: the UI checks the stake, but anyone can skip the UI and call the
    API directly (that is how BUG-06 was found). So the backend has to enforce the
    stake rules (§4) itself. One parametrized test covers every limit and format rule.
    """
    response = api.place_bet(
        {"matchId": upcoming_match["id"], "selection": Selection.HOME, "stake": stake}
    )

    assert response.status_code == 422, response.text
    assert response.json()["error"] == expected_error
    assert api.current_balance() == fresh_balance, "balance changed after a rejected bet"
