import re

from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url

    def open(self) -> None:
        self.page.goto(self.base_url, wait_until="domcontentloaded")
        expect(self.page).to_have_title(re.compile(r"Automation Exercise"))

    def go_to_products(self) -> None:
        self.page.get_by_role("link", name="Products").click()

    def go_to_login(self) -> None:
        self.page.get_by_role("link", name="Signup / Login").click()
