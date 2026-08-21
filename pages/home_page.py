import re

from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page
        self.base_url = base_url

        self.products_link = page.get_by_role("link", name="Products")
        self.signup_login_link = page.get_by_role("link", name="Signup / Login")
        self.cart_link = page.get_by_role("link", name="Cart")
        self.contact_link = page.get_by_role(
            "link", name=re.compile(r"Contact us", re.IGNORECASE)
        ).first
        self.test_cases_link = page.get_by_role("link", name="Test Cases").first

        self.subscription_heading = page.get_by_text(re.compile(r"^Subscription$", re.IGNORECASE))
        self.subscription_email = page.locator("#susbscribe_email")
        self.subscription_button = page.locator("#subscribe")
        self.subscription_success = page.locator("#success-subscribe")

        self.category_heading = page.get_by_text(re.compile(r"^Category$", re.IGNORECASE))
        self.recommended_items = page.locator(".recommended_items")
        self.scroll_up_button = page.locator("#scrollUp")
        self.hero_text = page.locator(".carousel-inner .item.active").get_by_text(
            "Full-Fledged practice website for Automation Engineers",
            exact=True,
        )

    def open(self) -> None:
        self.page.goto(self.base_url, wait_until="commit")
        expect(self.page).to_have_title(re.compile(r"Automation Exercise"))

    def verify_home_visible(self) -> None:
        expect(self.hero_text).to_be_visible()

    def go_to_products(self) -> None:
        self.products_link.click(no_wait_after=True)
        expect(self.page).to_have_url(re.compile(r".*/products"))

    def go_to_login(self) -> None:
        self.signup_login_link.click(no_wait_after=True)
        expect(self.page).to_have_url(re.compile(r".*/login"))

    def go_to_cart(self) -> None:
        self.cart_link.click(no_wait_after=True)
        expect(self.page).to_have_url(re.compile(r".*/view_cart"))

    def go_to_contact_us(self) -> None:
        self.contact_link.click(no_wait_after=True)
        expect(self.page).to_have_url(re.compile(r".*/contact_us"))

    def go_to_test_cases(self) -> None:
        self.test_cases_link.click(no_wait_after=True)
        expect(self.page).to_have_url(re.compile(r".*/test_cases"))
        expect(self.page.get_by_text("Test Cases", exact=True).first).to_be_visible()

    def verify_category_visible(self) -> None:
        expect(self.category_heading).to_be_visible()

    def subscribe(self, email: str) -> None:
        self.subscription_heading.scroll_into_view_if_needed()
        self.subscription_email.fill(email)
        self.subscription_button.click()

    def verify_subscription_success(self) -> None:
        expect(self.subscription_success).to_contain_text("You have been successfully subscribed!")

    def expand_category(self, category: str) -> None:
        self.page.locator(f'a[href="#{category}"]').click()

    def open_subcategory(self, category: str, subcategory: str) -> None:
        self.page.locator(f"#{category}").get_by_role("link", name=subcategory, exact=True).click(
            no_wait_after=True
        )
        expect(self.page).to_have_url(re.compile(r".*/category_products/\d+"))

    def open_featured_product(self, product_name: str) -> None:
        card = (
            self.page.locator(".features_items .product-image-wrapper")
            .filter(has_text=product_name)
            .first
        )
        card.get_by_role("link", name="View Product").click(no_wait_after=True)
        expect(self.page).to_have_url(re.compile(r".*/product_details/\d+"))

    def add_first_recommended_product(self) -> str:
        self.recommended_items.scroll_into_view_if_needed()
        active_item = self.recommended_items.locator(".item.active").first
        product_name = active_item.locator(".productinfo p").first.inner_text().strip()
        active_item.locator(".productinfo .add-to-cart").first.click()
        return product_name

    def view_cart_from_modal(self) -> None:
        self.page.get_by_role("link", name="View Cart", exact=True).click(no_wait_after=True)
        expect(self.page).to_have_url(re.compile(r".*/view_cart"))

    def scroll_to_subscription(self) -> None:
        self.subscription_heading.scroll_into_view_if_needed()
        expect(self.subscription_heading).to_be_visible()

    def click_scroll_up(self) -> None:
        self.scroll_up_button.click()

    def scroll_to_top_without_arrow(self) -> None:
        self.page.evaluate("window.scrollTo(0, 0)")
