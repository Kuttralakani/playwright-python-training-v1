import re

from playwright.sync_api import Locator, Page, expect


class CartPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.cart_table = page.locator("#cart_info_table")
        self.proceed_checkout_button = page.get_by_text(
            "Proceed To Checkout",
            exact=True,
        )
        self.checkout_modal = page.locator("#checkoutModal")

        self.subscription_heading = page.get_by_text(
            re.compile(r"^Subscription$", re.IGNORECASE)
        )
        self.subscription_email = page.locator("#susbscribe_email")
        self.subscription_button = page.locator("#subscribe")
        self.subscription_success = page.locator("#success-subscribe")

    def verify_loaded(self) -> None:
        expect(self.cart_table).to_be_visible()

    def row(self, product_name: str) -> Locator:
        return self.cart_table.locator("tbody tr").filter(
            has=self.page.get_by_role("link", name=product_name, exact=True)
        ).first

    def product_link(self, product_name: str) -> Locator:
        return self.row(product_name).get_by_role(
            "link",
            name=product_name,
            exact=True,
        )

    def price_text(self, product_name: str) -> str:
        return self.row(product_name).locator(".cart_price p").inner_text().strip()

    def quantity_text(self, product_name: str) -> str:
        return self.row(product_name).locator(".cart_quantity button").inner_text().strip()

    def total_text(self, product_name: str) -> str:
        return self.row(product_name).locator(".cart_total p").inner_text().strip()

    def remove_product(self, product_name: str) -> None:
        self.row(product_name).locator(".cart_quantity_delete").click()

    def verify_product_in_cart(self, product_name: str) -> None:
        expect(self.product_link(product_name)).to_be_visible()

    def verify_product_removed(self, product_name: str) -> None:
        expect(self.page.get_by_role("link", name=product_name, exact=True)).to_have_count(0)

    def proceed_to_checkout(self) -> None:
        self.proceed_checkout_button.click()

    def go_to_register_login_from_checkout(self) -> None:
        self.checkout_modal.get_by_role("link", name="Register / Login").click(no_wait_after=True)
        expect(self.page).to_have_url(re.compile(r".*/login"))

    def subscribe(self, email: str) -> None:
        self.subscription_heading.scroll_into_view_if_needed()
        self.subscription_email.fill(email)
        self.subscription_button.click()

    def verify_subscription_success(self) -> None:
        expect(self.subscription_success).to_contain_text(
            "You have been successfully subscribed!"
        )
