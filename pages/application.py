from playwright.sync_api import Page

from pages.home_page import HomePage
from pages.landing_page import LandingPage
from pages.login_page import LoginPage


class Application:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page

        self.home_page = HomePage(page, base_url)
        self.login_page = LoginPage(page)
        self.landing_page = LandingPage(page)
