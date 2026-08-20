from playwright.sync_api import Page, expect


class LandingPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.logged_in_text = page.get_by_text("Logged in as")
        self.logout_link = page.get_by_role("link", name="Logout")
        self.delete_account_link = page.get_by_role("link", name="Delete Account")

    def verify_logged_in(self, username: str) -> None:
        expect(self.page.get_by_text(f"Logged in as {username}")).to_be_visible()

    def logout(self) -> None:
        self.logout_link.click()
