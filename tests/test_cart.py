import allure
import pytest

from pages.application import Application
from utilities.file_reader import read_csv
from utilities.value_parser import parse_rupees

PRODUCTS = read_csv("products.csv")
BLUE_TOP = PRODUCTS[0]
MEN_TSHIRT = PRODUCTS[1]


@allure.feature("Cart")
@allure.story("Multiple Products")
@allure.title("TC12 - Add Products in Cart")
@pytest.mark.smoke
@pytest.mark.regression
def test_tc12_add_products_in_cart(app: Application) -> None:
    with allure.step("Open Products page"):
        app.home_page.open()
        app.home_page.go_to_products()
        app.products_page.verify_loaded()

    with allure.step("Add first product and continue shopping"):
        app.products_page.add_product_to_cart(BLUE_TOP["expected_product"])
        app.products_page.continue_shopping()

    with allure.step("Add second product and open Cart"):
        app.products_page.add_product_to_cart(MEN_TSHIRT["expected_product"])
        app.products_page.view_cart_from_modal()
        app.cart_page.verify_loaded()

    with allure.step("Verify both products, prices, quantities and totals"):
        for product in (BLUE_TOP, MEN_TSHIRT):
            name = product["expected_product"]
            app.cart_page.verify_product_in_cart(name)

            price = parse_rupees(app.cart_page.price_text(name))
            quantity = int(app.cart_page.quantity_text(name))
            total = parse_rupees(app.cart_page.total_text(name))

            assert quantity == 1
            assert total == price * quantity


@allure.feature("Cart")
@allure.story("Quantity")
@allure.title("TC13 - Verify Product quantity in Cart")
@pytest.mark.regression
def test_tc13_verify_product_quantity_in_cart(app: Application) -> None:
    expected_quantity = 4

    with allure.step("Open a product from the Home page"):
        app.home_page.open()
        app.home_page.open_featured_product(BLUE_TOP["expected_product"])
        app.product_details_page.verify_details_visible( BLUE_TOP["expected_product"] )

    with allure.step(f"Set quantity to {expected_quantity} and add to Cart"):
        app.product_details_page.set_quantity(expected_quantity)
        app.product_details_page.add_to_cart()
        app.product_details_page.view_cart_from_modal()

    with allure.step("Verify quantity in Cart"):
        actual_quantity = int( app.cart_page.quantity_text(BLUE_TOP["expected_product"]) )
        assert actual_quantity == expected_quantity


@allure.feature("Cart")
@allure.story("Remove Product")
@allure.title("TC17 - Remove Products From Cart")
@pytest.mark.regression
def test_tc17_remove_products_from_cart(app: Application) -> None:
    with allure.step("Add a product to Cart"):
        app.home_page.open()
        app.home_page.go_to_products()
        app.products_page.add_product_to_cart(BLUE_TOP["expected_product"])
        app.products_page.view_cart_from_modal()

    with allure.step("Remove the product and verify it is absent"):
        app.cart_page.remove_product(BLUE_TOP["expected_product"])
        app.cart_page.verify_product_removed(BLUE_TOP["expected_product"])


@allure.feature("Cart")
@allure.story("Search Persistence")
@allure.title("TC20 - Search Products and Verify Cart After Login")
@pytest.mark.regression
def test_tc20_search_products_and_verify_cart_after_login(app: Application, registered_user: dict[str, str], ) -> None:
    with allure.step("Search a product"):
        app.home_page.open()
        app.home_page.go_to_products()
        app.products_page.search(BLUE_TOP["search_term"])
        app.products_page.verify_search_results(BLUE_TOP["expected_product"])

    with allure.step("Add searched product and verify Cart"):
        app.products_page.add_product_to_cart(BLUE_TOP["expected_product"])
        app.products_page.view_cart_from_modal()
        app.cart_page.verify_product_in_cart(BLUE_TOP["expected_product"])

    with allure.step("Login and return to Cart"):
        app.home_page.go_to_login()
        app.login_page.login( registered_user["email"], registered_user["password"], )
        app.landing_page.verify_logged_in(registered_user["name"])
        app.home_page.go_to_cart()

    with allure.step("Verify the product remains in Cart after Login"):
        app.cart_page.verify_product_in_cart(BLUE_TOP["expected_product"])

    with allure.step("Cleanup the pre-created account"):
        app.landing_page.delete_account()
        app.account_page.verify_deleted()


@allure.feature("Cart")
@allure.story("Recommended Items")
@allure.title("TC22 - Add to cart from Recommended items")
@pytest.mark.regression
def test_tc22_add_to_cart_from_recommended_items(app: Application) -> None:
    with allure.step("Open Home page and add a Recommended item"):
        app.home_page.open()
        product_name = app.home_page.add_first_recommended_product()

    with allure.step("Open Cart and verify the Recommended item"):
        app.home_page.view_cart_from_modal()
        app.cart_page.verify_product_in_cart(product_name)
