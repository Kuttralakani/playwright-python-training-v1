import allure
import pytest

from pages.application import Application
from utilities.file_reader import read_csv


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Authentication")
@allure.story("Login Page")
@allure.title("Verify login page loads successfully")
@allure.description(
    "Verify that the user can navigate to the login page and the login form is displayed."
)
def test_login_page_loads(app: Application) -> None:
    with allure.step("Open the application"):
        app.home_page.open()

    with allure.step("Navigate to the login page"):
        app.home_page.go_to_login()

    with allure.step("Verify the login page is displayed"):
        app.login_page.verify_loaded()


@pytest.mark.smoke
@pytest.mark.regression
@allure.feature("Authentication")
@allure.story("Login Validation")
@allure.title("Validate login with different credentials")
@allure.description(
    "Verify login behaviour using valid and invalid credentials from external test data."
)
@pytest.mark.parametrize("credentials", read_csv("test_login.csv"))
def test_login_validation(app: Application, credentials: dict) -> None:
    allure.dynamic.parameter("Login Type", credentials["type"])

    with allure.step("Open the application"):
        app.home_page.open()

    with allure.step("Navigate to the login page"):
        app.home_page.go_to_login()
        app.login_page.verify_loaded()

    with allure.step("Enter credentials and submit login"):
        app.login_page.login(credentials["email"], credentials["password"])

    if credentials["type"] == "valid":
        with allure.step("Verify successful login"):
            app.landing_page.verify_logged_in(credentials["expected_message"])
    else:
        with allure.step("Verify login error message"):
            app.login_page.verify_login_error(credentials["expected_message"])
