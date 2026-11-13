"""UI suite: browser fixtures and screenshot on failure."""

from collections.abc import Generator, Iterator
from pathlib import Path

import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from pages import HomePage
from utils.config import Settings
from utils.driver_factory import create_chrome_driver

SCREENSHOT_DIR = Path("artifacts/screenshots")


@pytest.fixture
def driver(settings: Settings) -> Iterator[WebDriver]:
    driver = create_chrome_driver(settings)
    yield driver
    driver.quit()


@pytest.fixture
def home_page(driver: WebDriver, settings: Settings) -> HomePage:
    return HomePage(driver, settings.timeout).open(settings.app_url)


@pytest.hookimpl(wrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[None]
) -> Generator[None, pytest.TestReport, pytest.TestReport]:
    """Save a screenshot when a UI test fails, to artifacts/screenshots/<test>.png."""
    report = yield
    driver = item.funcargs.get("driver") if hasattr(item, "funcargs") else None
    if report.when == "call" and report.failed and driver is not None:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        driver.save_screenshot(str(SCREENSHOT_DIR / f"{item.name}.png"))
    return report
