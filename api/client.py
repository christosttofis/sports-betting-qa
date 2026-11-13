"""Thin wrapper around the betting API.

Methods return the raw `requests.Response` so tests can assert on status codes.
"""

from enum import StrEnum
from typing import Any

import requests


class Selection(StrEnum):
    HOME = "HOME"
    DRAW = "DRAW"
    AWAY = "AWAY"


class BettingApiClient:
    def __init__(self, api_url: str, user_id: str, timeout: int = 10) -> None:
        self._api_url = api_url
        self._timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"x-user-id": user_id})

    def get_matches(self) -> requests.Response:
        return self._request("GET", "/matches")

    def get_balance(self) -> requests.Response:
        return self._request("GET", "/balance")

    def reset_balance(self) -> requests.Response:
        return self._request("POST", "/reset-balance")

    def place_bet(self, payload: dict[str, Any]) -> requests.Response:
        """Send any payload as-is, so invalid bodies can be tested too."""
        return self._request("POST", "/place-bet", json=payload)

    def current_balance(self) -> float:
        """Balance stored in the backend."""
        response = self.get_balance()
        response.raise_for_status()
        return response.json()["balance"]

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        return self._session.request(
            method, f"{self._api_url}{path}", timeout=self._timeout, **kwargs
        )
