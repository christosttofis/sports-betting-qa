"""Creates the WebDriver. Selenium Manager downloads a matching chromedriver automatically."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from utils.config import Settings


def create_chrome_driver(settings: Settings) -> WebDriver:
    options = Options()
    if settings.headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)
