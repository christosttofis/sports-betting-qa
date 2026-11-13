"""Fixtures shared by both suites (UI and API)."""

from datetime import date
from typing import Any

import pytest

from api import BettingApiClient
from utils.config import Settings, load_settings


@pytest.fixture(scope="session")
def settings() -> Settings:
    return load_settings()


@pytest.fixture(scope="session")
def api(settings: Settings) -> BettingApiClient:
    return BettingApiClient(settings.api_url, settings.user_id, settings.timeout)


@pytest.fixture
def fresh_balance(api: BettingApiClient) -> float:
    """Reset the balance before a test and return the stored starting balance."""
    api.reset_balance().raise_for_status()
    return api.current_balance()


@pytest.fixture(scope="session")
def upcoming_match(api: BettingApiClient) -> dict[str, Any]:
    """First match with a kickoff date after today.

    Chosen dynamically so tests don't break as fixed dates move into the past.
    """
    response = api.get_matches()
    response.raise_for_status()
    today = date.today().isoformat()
    upcoming = [m for m in response.json() if m["kickoffDate"] > today]
    if not upcoming:
        pytest.skip("No upcoming matches available in the catalog")
    return min(upcoming, key=lambda m: m["kickoffDate"])
