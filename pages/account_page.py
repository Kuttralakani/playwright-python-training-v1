from playwright.sync_api import Page, expect


class AccountPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.account_created = page.locator('[data-qa="account-created"]')
        self.account_deleted = page.locator('[data-qa="account-deleted"]')
        self.continue_button = page.locator('[data-qa="continue-button"]')

    def verify_created(self) -> None:
        expect(self.account_created).to_be_visible()

    def verify_deleted(self) -> None:
        expect(self.account_deleted).to_be_visible()

    def continue_after_status(self) -> None:
        self.continue_button.click(no_wait_after=True)
