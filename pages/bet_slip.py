"""Right-hand bet slip panel (spec §2.2, §2.3)."""

from decimal import Decimal

from selenium.webdriver.common.by import By

from pages.base_page import BasePage, Locator
from utils.money import parse_money


class BetSlip(BasePage):
    STAKE_INPUT: Locator = (By.ID, "bet-slip-stake-input")
    POTENTIAL_PAYOUT: Locator = (By.ID, "bet-slip-potential-payout")
    PLACE_BET_BUTTON: Locator = (By.ID, "bet-slip-place-bet")
    SELECTION_MATCH: Locator = (By.CSS_SELECTOR, "#bet-slip .betSelectionTeams")
    SELECTION_OUTCOME: Locator = (By.CSS_SELECTOR, "#bet-slip .betSelectionMarket")
    SELECTION_ODDS: Locator = (By.CSS_SELECTOR, "#bet-slip .betSelectionOdds")

    def match_name(self) -> str:
        return self.text_of(self.SELECTION_MATCH)

    def outcome(self) -> str:
        return self.text_of(self.SELECTION_OUTCOME)

    def odds(self) -> Decimal:
        return parse_money(self.text_of(self.SELECTION_ODDS))

    def enter_stake(self, stake: str) -> None:
        self.type(self.STAKE_INPUT, stake)

    def potential_payout(self) -> Decimal:
        return parse_money(self.text_of(self.POTENTIAL_PAYOUT))

    def place_bet(self) -> None:
        self.click(self.PLACE_BET_BUTTON)
