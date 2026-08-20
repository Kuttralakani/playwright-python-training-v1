from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.login_heading = page.get_by_role("heading", name="Login to your account")
        self.email_input = page.locator('[data-qa="login-email"]')
        self.password_input = page.locator('[data-qa="login-password"]')
        self.login_button = page.locator('[data-qa="login-button"]')

    def verify_loaded(self) -> None:
        expect(self.login_heading).to_be_visible()

    def login(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def verify_login_success(self, expected_text: str) -> None:
        expect(self.page.locator("b")).to_contain_text(expected_text)

    def verify_login_error(self, expected_message: str) -> None:
        expect(self.page.get_by_text(expected_message, exact=True)).to_be_visible()
