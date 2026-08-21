import allure
import pytest

from pages.application import Application
from utilities.file_reader import read_csv

SUBSCRIPTION = read_csv("subscription.csv")[0]


@allure.feature("Subscription")
@allure.story("Home Page")
@allure.title("TC10 - Verify Subscription in home page")
@pytest.mark.regression
def test_tc10_verify_subscription_in_home_page(app: Application) -> None:
    with allure.step("Open application and subscribe"):
        app.home_page.open()
        app.home_page.subscribe(SUBSCRIPTION["email"])
        app.home_page.verify_subscription_success()


@allure.feature("Subscription")
@allure.story("Cart Page")
@allure.title("TC11 - Verify Subscription in Cart page")
@pytest.mark.regression
def test_tc11_verify_subscription_in_cart_page(app: Application) -> None:
    with allure.step("Open application and navigate to Cart"):
        app.home_page.open()
        app.home_page.go_to_cart()

    with allure.step("Subscribe from the Cart page"):
        app.cart_page.subscribe(SUBSCRIPTION["email"])
        app.cart_page.verify_subscription_success()
