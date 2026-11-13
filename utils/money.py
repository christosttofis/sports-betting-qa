"""Helpers for working with money values shown in the UI."""

import re
from decimal import ROUND_HALF_UP, Decimal

_CENT = Decimal("0.01")


def parse_money(text: str) -> Decimal:
    """Convert a UI amount such as '€1,234.50' or 'Balance: €120.00' to Decimal('1234.50')."""
    match = re.search(r"-?[\d,]+(?:\.\d+)?", text)
    if not match:
        raise ValueError(f"No amount found in {text!r}")
    return Decimal(match.group().replace(",", ""))


def expected_payout(stake: Decimal, odds: Decimal) -> Decimal:
    """Payout = stake × odds, rounded to cents (spec: 'Payout')."""
    return (stake * odds).quantize(_CENT, rounding=ROUND_HALF_UP)
