import re

from playwright.sync_api import Page, expect


class LandingPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logout_link = page.get_by_role("link", name="Logout")
        self.delete_account_link = page.get_by_role("link", name="Delete Account")

    def verify_logged_in(self, username: str) -> None:
        expect(self.page.get_by_text(f"Logged in as {username}")).to_be_visible()

    def logout(self) -> None:
        self.logout_link.click(no_wait_after=True)
        expect(self.page).to_have_url(re.compile(r".*/login"))

    def delete_account(self) -> None:
        self.delete_account_link.click(no_wait_after=True)
