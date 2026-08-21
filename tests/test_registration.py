import allure
import pytest

from pages.application import Application
from utilities.file_reader import read_csv

_LOGIN_DATA = read_csv("test_login.csv")
VALID_LOGIN = next(row for row in _LOGIN_DATA if row["type"] == "valid")


@allure.feature("Registration")
@allure.story("Register User")
@allure.title("TC01 - Register User")
@pytest.mark.smoke
@pytest.mark.regression
def test_tc01_register_user(app: Application, new_user: dict[str, str]) -> None:
    with allure.step("Launch application and open Signup / Login"):
        app.home_page.open()
        app.home_page.verify_home_visible()
        app.home_page.go_to_login()
        app.login_page.verify_signup_loaded()

    with allure.step("Enter name and email for new user signup"):
        app.login_page.signup(new_user["name"], new_user["email"])
        app.signup_page.verify_loaded()

    with allure.step("Complete account registration"):
        app.signup_page.register(new_user)
        app.account_page.verify_created()
        app.account_page.continue_after_status()
        app.landing_page.verify_logged_in(new_user["name"])

    with allure.step("Delete the created account"):
        app.landing_page.delete_account()
        app.account_page.verify_deleted()


@allure.feature("Registration")
@allure.story("Existing Email")
@allure.title("TC05 - Register User with existing email")
@pytest.mark.regression
def test_tc05_register_user_with_existing_email(app: Application) -> None:
    with allure.step("Open Signup / Login"):
        app.home_page.open()
        app.home_page.go_to_login()
        app.login_page.verify_signup_loaded()

    with allure.step("Try to register with an existing email"):
        app.login_page.signup(VALID_LOGIN["name"], VALID_LOGIN["email"])
        app.login_page.verify_existing_email_error()
