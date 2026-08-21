import allure
import pytest

from pages.application import Application
from utilities.file_reader import read_csv

PRODUCT = read_csv("products.csv")[0]
PAYMENT = read_csv("checkout.csv")[0]


@allure.feature("Checkout")
@allure.story("Register During Checkout")
@allure.title("TC14 - Place Order: Register while Checkout")
@pytest.mark.regression
def test_tc14_place_order_register_while_checkout(app: Application, new_user: dict[str, str]) -> None:
    with allure.step("Open application, add product and open Cart"):
        app.home_page.open()
        app.add_product_and_open_cart(PRODUCT["expected_product"])

    with allure.step("Proceed to Checkout and choose Register / Login"):
        app.cart_page.proceed_to_checkout()
        app.cart_page.go_to_register_login_from_checkout()

    with allure.step("Register the new user"):
        app.register(new_user)

    with allure.step("Return to Cart and complete Checkout"):
        app.home_page.go_to_cart()
        app.checkout(new_user, PAYMENT["comment"])

    with allure.step("Enter payment details and place order"):
        app.pay(PAYMENT)

    with allure.step("Delete the account"):
        app.landing_page.delete_account()
        app.account_page.verify_deleted()


@allure.feature("Checkout")
@allure.story("Register Before Checkout")
@allure.title("TC15 - Place Order: Register before Checkout")
@pytest.mark.regression
def test_tc15_place_order_register_before_checkout(app: Application, new_user: dict[str, str]) -> None:
    with allure.step("Open application and register before shopping"):
        app.home_page.open()
        app.home_page.go_to_login()
        app.register(new_user)

    with allure.step("Add product and open Cart"):
        app.add_product_and_open_cart(PRODUCT["expected_product"])

    with allure.step("Complete Checkout"):
        app.checkout(new_user, PAYMENT["comment"])

    with allure.step("Enter payment details and place order"):
        app.pay(PAYMENT)

    with allure.step("Delete the account"):
        app.landing_page.delete_account()
        app.account_page.verify_deleted()


@allure.feature("Checkout")
@allure.story("Login Before Checkout")
@allure.title("TC16 - Place Order: Login before Checkout")
@pytest.mark.smoke
@pytest.mark.regression
def test_tc16_place_order_login_before_checkout(app: Application, registered_user: dict[str, str]) -> None:
    with allure.step("Login before shopping"):
        app.home_page.open()
        app.home_page.go_to_login()
        app.login_page.login(registered_user["email"], registered_user["password"])
        app.landing_page.verify_logged_in(registered_user["name"])

    with allure.step("Add product and open Cart"):
        app.add_product_and_open_cart(PRODUCT["expected_product"])

    with allure.step("Complete Checkout"):
        app.checkout(registered_user, PAYMENT["comment"])

    with allure.step("Enter payment details and place order"):
        app.pay(PAYMENT)

    with allure.step("Delete the account"):
        app.landing_page.delete_account()
        app.account_page.verify_deleted()


@allure.feature("Checkout")
@allure.story("Address Details")
@allure.title("TC23 - Verify address details in checkout page")
@pytest.mark.regression
def test_tc23_verify_address_details_in_checkout_page(app: Application, new_user: dict[str, str]) -> None:
    with allure.step("Register a new user"):
        app.home_page.open()
        app.home_page.go_to_login()
        app.register(new_user)

    with allure.step("Add product and open Cart"):
        app.add_product_and_open_cart(PRODUCT["expected_product"])

    with allure.step("Verify delivery and billing address details"):
        app.cart_page.proceed_to_checkout()
        app.checkout_page.verify_loaded()
        app.checkout_page.verify_delivery_and_billing_addresses(new_user)

    with allure.step("Delete the account"):
        app.landing_page.delete_account()
        app.account_page.verify_deleted()


@allure.feature("Checkout")
@allure.story("Invoice")
@allure.title("TC24 - Download Invoice after purchase order")
@pytest.mark.regression
def test_tc24_download_invoice_after_purchase_order(app: Application, new_user: dict[str, str], tmp_path) -> None:
    with allure.step("Open application, add product and open Cart"):
        app.home_page.open()
        app.add_product_and_open_cart(PRODUCT["expected_product"])

    with allure.step("Proceed to Checkout and register"):
        app.cart_page.proceed_to_checkout()
        app.cart_page.go_to_register_login_from_checkout()
        app.register(new_user)

    with allure.step("Return to Cart and complete Checkout"):
        app.home_page.go_to_cart()
        app.checkout(new_user, PAYMENT["comment"])

    with allure.step("Enter payment details and place order"):
        app.pay(PAYMENT)

    with allure.step("Download and verify invoice"):
        invoice_path = app.payment_page.download_invoice(tmp_path)
        assert invoice_path.exists()
        assert invoice_path.stat().st_size > 0
        app.payment_page.continue_after_order()

    with allure.step("Delete the account"):
        app.landing_page.delete_account()
        app.account_page.verify_deleted()
