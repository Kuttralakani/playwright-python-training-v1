import allure
import pytest

from pages.application import Application
from utilities.file_reader import read_csv

PRODUCTS = read_csv("products.csv")
BLUE_TOP = PRODUCTS[0]
CATALOG = read_csv("catalog.csv")[0]
REVIEW = read_csv("review.csv")[0]


@allure.feature("Products")
@allure.story("Product Details")
@allure.title("TC08 - Verify All Products and product detail page")
@pytest.mark.regression
def test_tc08_verify_all_products_and_product_detail_page(app: Application) -> None:
    with allure.step("Open Products page"):
        app.home_page.open()
        app.home_page.go_to_products()
        app.products_page.verify_loaded()

    with allure.step("Open the first product"):
        product_name = app.products_page.open_first_product()

    with allure.step("Verify product details"):
        app.product_details_page.verify_details_visible(product_name)


@allure.feature("Products")
@allure.story("Search")
@allure.title("TC09 - Search Product")
@pytest.mark.smoke
@pytest.mark.regression
def test_tc09_search_product(app: Application) -> None:
    with allure.step("Open Products page"):
        app.home_page.open()
        app.home_page.go_to_products()
        app.products_page.verify_loaded()

    with allure.step(f"Search for {BLUE_TOP['search_term']}"):
        app.products_page.search(BLUE_TOP["search_term"])
        app.products_page.verify_search_results(BLUE_TOP["expected_product"])


@allure.feature("Products")
@allure.story("Categories")
@allure.title("TC18 - View Category Products")
@pytest.mark.regression
def test_tc18_view_category_products(app: Application) -> None:
    with allure.step("Open application and verify Category section"):
        app.home_page.open()
        app.home_page.verify_category_visible()

    with allure.step("Open a Women subcategory"):
        app.home_page.expand_category(CATALOG["women_category"])
        app.home_page.open_subcategory(CATALOG["women_category"], CATALOG["women_subcategory"])
        app.products_page.verify_category_heading(CATALOG["women_heading"])

    with allure.step("Open a Men subcategory"):
        app.home_page.expand_category(CATALOG["men_category"])
        app.home_page.open_subcategory(
            CATALOG["men_category"],
            CATALOG["men_subcategory"],
        )
        app.products_page.verify_category_heading(CATALOG["men_heading"])


@allure.feature("Products")
@allure.story("Brands")
@allure.title("TC19 - View & Cart Brand Products")
@pytest.mark.regression
def test_tc19_view_and_cart_brand_products(app: Application) -> None:
    with allure.step("Open Products and verify Brands"):
        app.home_page.open()
        app.home_page.go_to_products()
        app.products_page.verify_brands_visible()

    with allure.step(f"Open brand {CATALOG['first_brand']}"):
        app.products_page.open_brand(CATALOG["first_brand"])
        app.products_page.verify_brand_heading(CATALOG["first_brand_heading"])

    with allure.step(f"Open brand {CATALOG['second_brand']}"):
        app.products_page.open_brand(CATALOG["second_brand"])
        app.products_page.verify_brand_heading(CATALOG["second_brand_heading"])


@allure.feature("Products")
@allure.story("Reviews")
@allure.title("TC21 - Add review on product")
@pytest.mark.regression
def test_tc21_add_review_on_product(app: Application) -> None:
    with allure.step("Open Products and select first product"):
        app.home_page.open()
        app.home_page.go_to_products()
        app.products_page.verify_loaded()
        app.products_page.open_first_product()

    with allure.step("Verify review section and submit review"):
        app.product_details_page.verify_review_section_visible()
        app.product_details_page.submit_review(REVIEW)
        app.product_details_page.verify_review_success()
