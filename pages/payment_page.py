from pathlib import Path

from playwright.sync_api import Page, expect


class PaymentPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.name_on_card = page.locator('[data-qa="name-on-card"]')
        self.card_number = page.locator('[data-qa="card-number"]')
        self.cvc = page.locator('[data-qa="cvc"]')
        self.expiry_month = page.locator('[data-qa="expiry-month"]')
        self.expiry_year = page.locator('[data-qa="expiry-year"]')
        self.pay_button = page.locator('[data-qa="pay-button"]')
        self.order_placed = page.get_by_role("heading", name="Order Placed!")
        self.download_invoice_link = page.get_by_role(
            "link",
            name="Download Invoice",
        )
        self.continue_button = page.locator('[data-qa="continue-button"]')

    def pay(self, payment: dict[str, str]) -> None:
        self.name_on_card.fill(payment["name_on_card"])
        self.card_number.fill(payment["card_number"])
        self.cvc.fill(payment["cvc"])
        self.expiry_month.fill(payment["expiry_month"])
        self.expiry_year.fill(payment["expiry_year"])
        with self.page.expect_navigation(wait_until="domcontentloaded"):
            self.pay_button.click()

    def verify_order_placed(self) -> None:
        expect(self.order_placed).to_be_visible()

    def download_invoice(self, destination: Path) -> Path:
        with self.page.expect_download() as download_info:
            self.download_invoice_link.click()
        download = download_info.value
        target = destination / download.suggested_filename
        download.save_as(target)
        return target

    def continue_after_order(self) -> None:
        with self.page.expect_navigation(wait_until="domcontentloaded"):
            self.continue_button.click()
