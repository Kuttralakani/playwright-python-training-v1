import re

from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page) -> None:
        self.page = page

        self.login_heading = page.get_by_role("heading", name="Login to your account")
        self.email_input = page.locator('[data-qa="login-email"]')
        self.password_input = page.locator('[data-qa="login-password"]')
        self.login_button = page.locator('[data-qa="login-button"]')
        self.login_error = page.get_by_text(
            "Your email or password is incorrect!",
            exact=True,
        )

        self.signup_heading = page.get_by_role("heading", name="New User Signup!")
        self.signup_name = page.locator('[data-qa="signup-name"]')
        self.signup_email = page.locator('[data-qa="signup-email"]')
        self.signup_button = page.locator('[data-qa="signup-button"]')
        self.existing_email_error = page.get_by_text(
            "Email Address already exist!",
            exact=True,
        )

    def verify_loaded(self) -> None:
        expect(self.login_heading).to_be_visible()

    def verify_signup_loaded(self) -> None:
        expect(self.signup_heading).to_be_visible()

    def login(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click(no_wait_after=True)

    def signup(self, name: str, email: str) -> None:
        self.signup_name.fill(name)
        self.signup_email.fill(email)
        self.signup_button.click(no_wait_after=True)
        expect(self.page).to_have_url(re.compile(r".*/signup"))

    def verify_login_error(self) -> None:
        expect(self.login_error).to_be_visible()

    def verify_existing_email_error(self) -> None:
        expect(self.existing_email_error).to_be_visible()
