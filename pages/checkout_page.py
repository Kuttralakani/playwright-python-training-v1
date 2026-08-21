from playwright.sync_api import Locator, Page, expect


class CheckoutPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.address_details_heading = page.get_by_text(
            "Address Details",
            exact=True,
        )
        self.review_order_heading = page.get_by_text(
            "Review Your Order",
            exact=True,
        )
        self.delivery_address = page.locator("#address_delivery")
        self.billing_address = page.locator("#address_invoice")
        self.comment = page.locator('textarea[name="message"]')
        self.place_order_link = page.get_by_role("link", name="Place Order")

    def verify_loaded(self) -> None:
        expect(self.address_details_heading).to_be_visible()
        expect(self.review_order_heading).to_be_visible()

    def verify_address(self, address: Locator, user: dict[str, str]) -> None:
        address_text = address.inner_text()
        expected_values = [
            user["first_name"],
            user["last_name"],
            user["address1"],
            user["city"],
            user["state"],
            user["zipcode"],
            user["country"],
            user["mobile_number"],
        ]
        for value in expected_values:
            assert value in address_text, f"Expected address value not found: {value}"

    def verify_delivery_and_billing_addresses(self, user: dict[str, str]) -> None:
        self.verify_address(self.delivery_address, user)
        self.verify_address(self.billing_address, user)

    def enter_comment(self, comment: str) -> None:
        self.comment.fill(comment)

    def place_order(self) -> None:
        with self.page.expect_navigation(wait_until="domcontentloaded"):
            self.place_order_link.click()
