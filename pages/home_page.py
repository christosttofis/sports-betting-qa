"""The single page of the app: header, match list, bet slip and modals."""

from decimal import Decimal

from selenium.webdriver.common.by import By

from api import Selection
from pages.base_page import BasePage, Locator
from pages.bet_slip import BetSlip
from pages.receipt_modal import ReceiptModal
from utils.money import parse_money


class HomePage(BasePage):
    HEADER_BALANCE: Locator = (By.ID, "header-balance")
    MATCH_LIST: Locator = (By.ID, "match-list")

    def open(self, url: str) -> "HomePage":
        self.driver.get(url)
        self.find(self.MATCH_LIST)
        return self

    @property
    def bet_slip(self) -> BetSlip:
        return BetSlip(self.driver, self.timeout)

    @property
    def receipt(self) -> ReceiptModal:
        return ReceiptModal(self.driver, self.timeout)

    def header_balance(self) -> Decimal:
        return parse_money(self.text_of(self.HEADER_BALANCE))

    def select_odds(self, match_id: str, selection: Selection) -> None:
        """Click an odds button. Each one has a stable id: odds-<matchId>-<home|draw|away>."""
        self.click((By.ID, f"odds-{match_id}-{selection.lower()}"))
