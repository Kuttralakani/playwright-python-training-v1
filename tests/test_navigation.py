import allure
import pytest

from pages.application import Application


@allure.feature("Navigation")
@allure.story("Test Cases Page")
@allure.title("TC07 - Verify Test Cases Page")
@pytest.mark.regression
def test_tc07_verify_test_cases_page(app: Application) -> None:
    with allure.step("Open application and navigate to Test Cases"):
        app.home_page.open()
        app.home_page.go_to_test_cases()


@allure.feature("Navigation")
@allure.story("Scroll")
@allure.title("TC25 - Verify Scroll Up using Arrow button and Scroll Down functionality")
@pytest.mark.regression
def test_tc25_scroll_up_using_arrow_and_scroll_down(app: Application) -> None:
    with allure.step("Open application and scroll down to Subscription"):
        app.home_page.open()
        app.home_page.scroll_to_subscription()

    with allure.step("Use the Scroll Up arrow"):
        app.home_page.click_scroll_up()
        app.home_page.verify_home_visible()


@allure.feature("Navigation")
@allure.story("Scroll")
@allure.title("TC26 - Verify Scroll Up without Arrow button and Scroll Down functionality")
@pytest.mark.regression
def test_tc26_scroll_up_without_arrow_and_scroll_down(app: Application) -> None:
    with allure.step("Open application and scroll down to Subscription"):
        app.home_page.open()
        app.home_page.scroll_to_subscription()

    with allure.step("Scroll back to the top without using the arrow"):
        app.home_page.scroll_to_top_without_arrow()
        app.home_page.verify_home_visible()
