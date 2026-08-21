import re

from playwright.sync_api import Page, expect


class ProductDetailsPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.product_information = page.locator(".product-information")
        self.product_name = self.product_information.locator("h2")
        self.price = self.product_information.locator("span span").first
        self.quantity = page.locator("#quantity")
        self.add_to_cart_button = page.get_by_role("button", name="Add to cart")
        self.cart_modal = page.locator("#cartModal")

        self.review_heading = page.get_by_text(re.compile(r"WRITE YOUR REVIEW", re.IGNORECASE))
        self.review_name = page.locator("#name")
        self.review_email = page.locator("#email")
        self.review_text = page.locator("#review")
        self.review_button = page.locator("#button-review")
        self.review_success = page.get_by_text(
            "Thank you for your review.",
            exact=True,
        )

    def verify_details_visible(self, expected_name: str | None = None) -> None:
        expect(self.product_information).to_be_visible()
        if expected_name:
            expect(self.product_name).to_have_text(expected_name)

        for label in ("Category:", "Availability:", "Condition:", "Brand:"):
            expect(
                self.product_information.get_by_text(re.compile(rf"^{re.escape(label)}"))
            ).to_be_visible()
        expect(self.price).to_be_visible()

    def set_quantity(self, quantity: int) -> None:
        self.quantity.fill(str(quantity))

    def add_to_cart(self) -> None:
        self.add_to_cart_button.click()

    def view_cart_from_modal(self) -> None:
        self.cart_modal.get_by_role("link", name="View Cart").click()

    def verify_review_section_visible(self) -> None:
        expect(self.review_heading).to_be_visible()

    def submit_review(self, review: dict[str, str]) -> None:
        self.review_name.fill(review["name"])
        self.review_email.fill(review["email"])
        self.review_text.fill(review["message"])
        self.review_button.click()

    def verify_review_success(self) -> None:
        expect(self.review_success).to_be_visible()
