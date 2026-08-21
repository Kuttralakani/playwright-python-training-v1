import re

from playwright.sync_api import Locator, Page, expect


class ProductsPage:
    def __init__(self, page: Page) -> None:
        self.page = page
        self.all_products_heading = page.get_by_role(
            "heading",
            name=re.compile(r"ALL PRODUCTS", re.IGNORECASE),
        )
        self.products_list = page.locator(".features_items")
        self.search_input = page.locator("#search_product")
        self.search_button = page.locator("#submit_search")
        self.searched_products_heading = page.get_by_role(
            "heading",
            name=re.compile(r"SEARCHED PRODUCTS", re.IGNORECASE),
        )
        self.brands_heading = page.get_by_text(
            re.compile(r"^Brands$", re.IGNORECASE)
        )
        self.cart_modal = page.locator("#cartModal")

    def verify_loaded(self) -> None:
        expect(self.all_products_heading).to_be_visible()

    def product_card(self, product_name: str) -> Locator:
        return self.page.locator(".product-image-wrapper").filter(
            has_text=product_name
        ).first

    def product_name(self, product_name: str) -> Locator:
        return self.product_card(product_name).locator(".productinfo p").first

    def open_first_product(self) -> str:
        card = self.page.locator(".product-image-wrapper").first
        name = card.locator(".productinfo p").first.inner_text().strip()
        card.get_by_role("link", name="View Product").click(no_wait_after=True)
        expect(self.page).to_have_url(re.compile(r".*/product_details/\d+"))
        return name

    def search(self, search_term: str) -> None:
        self.search_input.fill(search_term)
        self.search_button.click()

    def verify_search_results(self, expected_product: str) -> None:
        expect(self.searched_products_heading).to_be_visible()
        expect(self.product_name(expected_product)).to_be_visible()

    def add_product_to_cart(self, product_name: str) -> None:
        card = self.product_card(product_name)
        card.locator(".productinfo .add-to-cart").first.click()

    def continue_shopping(self) -> None:
        self.cart_modal.get_by_role("button", name="Continue Shopping").click()

    def view_cart_from_modal(self) -> None:
        self.cart_modal.get_by_role("link", name="View Cart").click(no_wait_after=True)
        expect(self.page).to_have_url(re.compile(r".*/view_cart"))

    def verify_brands_visible(self) -> None:
        expect(self.brands_heading).to_be_visible()

    def open_brand(self, brand: str) -> None:
        self.page.locator(".brands-name a").filter(has_text=brand).first.click(no_wait_after=True)

    def verify_category_heading(self, expected_heading: str) -> None:
        expect(
            self.page.get_by_role(
                "heading",
                name=re.compile(re.escape(expected_heading), re.IGNORECASE),
            )
        ).to_be_visible()

    def verify_brand_heading(self, expected_heading: str) -> None:
        expect(
            self.page.get_by_role(
                "heading",
                name=re.compile(re.escape(expected_heading), re.IGNORECASE),
            )
        ).to_be_visible()
