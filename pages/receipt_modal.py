"""Success receipt modal shown after a bet is placed (spec §2.4)."""

from decimal import Decimal

from selenium.webdriver.common.by import By

from pages.base_page import BasePage, Locator
from utils.money import parse_money


class ReceiptModal(BasePage):
    CONTAINER: Locator = (By.ID, "modal-success")
    BET_ID: Locator = (By.ID, "modal-success-bet-id")
    MATCH: Locator = (By.ID, "modal-success-match")
    STAKE: Locator = (By.ID, "modal-success-stake")
    ODDS: Locator = (By.ID, "modal-success-odds")
    PAYOUT: Locator = (By.ID, "modal-success-payout")
    CLOSE_BUTTON: Locator = (By.ID, "modal-success-close")

    def wait_until_visible(self) -> "ReceiptModal":
        self.find(self.CONTAINER)
        return self

    def bet_id(self) -> str:
        return self.text_of(self.BET_ID)

    def match_name(self) -> str:
        return self.text_of(self.MATCH)

    def stake(self) -> Decimal:
        return parse_money(self.text_of(self.STAKE))

    def odds(self) -> Decimal:
        return parse_money(self.text_of(self.ODDS))

    def payout(self) -> Decimal:
        return parse_money(self.text_of(self.PAYOUT))

    def close(self) -> None:
        self.click(self.CLOSE_BUTTON)
        self.wait_until_gone(self.CONTAINER)
