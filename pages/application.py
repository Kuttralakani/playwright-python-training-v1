from playwright.sync_api import Page

from pages.account_page import AccountPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.contact_page import ContactPage
from pages.home_page import HomePage
from pages.landing_page import LandingPage
from pages.login_page import LoginPage
from pages.payment_page import PaymentPage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage
from pages.signup_page import SignupPage


class Application:
    def __init__(self, page: Page, base_url: str) -> None:
        self.page = page

        self.home_page = HomePage(page, base_url)
        self.login_page = LoginPage(page)
        self.signup_page = SignupPage(page)
        self.account_page = AccountPage(page)
        self.landing_page = LandingPage(page)
        self.contact_page = ContactPage(page)
        self.products_page = ProductsPage(page)
        self.product_details_page = ProductDetailsPage(page)
        self.cart_page = CartPage(page)
        self.checkout_page = CheckoutPage(page)
        self.payment_page = PaymentPage(page)

    def register(self, user: dict[str, str]) -> None:
        self.login_page.verify_signup_loaded()
        self.login_page.signup(user["name"], user["email"])
        self.signup_page.verify_loaded()
        self.signup_page.register(user)
        self.account_page.verify_created()
        self.account_page.continue_after_status()
        self.landing_page.verify_logged_in(user["name"])

    def add_product_and_open_cart(self, product_name: str) -> None:
        self.home_page.go_to_products()
        self.products_page.verify_loaded()
        self.products_page.add_product_to_cart(product_name)
        self.products_page.view_cart_from_modal()
        self.cart_page.verify_loaded()

    def checkout(self, user: dict[str, str], comment: str) -> None:
        self.cart_page.proceed_to_checkout()
        self.checkout_page.verify_loaded()
        self.checkout_page.verify_delivery_and_billing_addresses(user)
        self.checkout_page.enter_comment(comment)
        self.checkout_page.place_order()

    def pay(self, payment: dict[str, str]) -> None:
        self.payment_page.pay(payment)
        self.payment_page.verify_order_placed()
