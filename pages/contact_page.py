import re
from pathlib import Path

from playwright.sync_api import Page, expect


class ContactPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.heading = page.get_by_text(re.compile(r"GET IN TOUCH", re.IGNORECASE))
        self.name = page.locator('[data-qa="name"]')
        self.email = page.locator('[data-qa="email"]')
        self.subject = page.locator('[data-qa="subject"]')
        self.message = page.locator('[data-qa="message"]')
        self.upload_file = page.locator('input[name="upload_file"]')
        self.submit_button = page.locator('[data-qa="submit-button"]')
        self.success_message = page.locator("#contact-page").get_by_text(
            "Success! Your details have been submitted successfully.",
            exact=True,
        )
        self.home_button = page.get_by_role("link", name="Home")

    def verify_loaded(self) -> None:
        expect(self.heading).to_be_visible()

    def submit(self, data: dict[str, str], upload_path: Path) -> None:
        self.name.fill(data["name"])
        self.email.fill(data["email"])
        self.subject.fill(data["subject"])
        self.message.fill(data["message"])
        self.upload_file.set_input_files(str(upload_path))

        self.page.once("dialog", lambda dialog: dialog.accept())
        self.submit_button.click()

    def verify_success(self) -> None:
        expect(self.success_message).to_be_visible()

    def go_home(self) -> None:
        self.home_button.click()
