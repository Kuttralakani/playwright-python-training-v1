import allure
import pytest

from pages.application import Application
from utilities.file_reader import read_csv

_LOGIN_DATA = read_csv("test_login.csv")
VALID_LOGIN = next(row for row in _LOGIN_DATA if row["type"] == "valid")
INVALID_LOGINS = [row for row in _LOGIN_DATA if row["type"] == "invalid"]


@allure.feature("Authentication")
@allure.story("Valid Login")
@allure.title("TC02 - Login User with correct email and password")
@pytest.mark.smoke
@pytest.mark.regression
def test_tc02_login_user_with_correct_email_and_password(app: Application) -> None:
    with allure.step("Open application and navigate to Login"):
        app.home_page.open()
        app.home_page.go_to_login()
        app.login_page.verify_loaded()

    with allure.step("Login with valid credentials"):
        app.login_page.login(VALID_LOGIN["email"], VALID_LOGIN["password"])
        app.landing_page.verify_logged_in(VALID_LOGIN["name"])


@allure.feature("Authentication")
@allure.story("Invalid Login")
@allure.title("TC03 - Login User with incorrect email and password")
@pytest.mark.regression
@pytest.mark.parametrize("credentials", INVALID_LOGINS)
def test_tc03_login_user_with_incorrect_email_and_password(
    app: Application,
    credentials: dict[str, str],
) -> None:
    with allure.step("Open application and navigate to Login"):
        app.home_page.open()
        app.home_page.go_to_login()
        app.login_page.verify_loaded()

    with allure.step("Submit invalid login credentials"):
        app.login_page.login(credentials["email"], credentials["password"])
        app.login_page.verify_login_error()


@allure.feature("Authentication")
@allure.story("Logout")
@allure.title("TC04 - Logout User")
@pytest.mark.regression
def test_tc04_logout_user(app: Application) -> None:
    with allure.step("Login with valid credentials"):
        app.home_page.open()
        app.home_page.go_to_login()
        app.login_page.login(VALID_LOGIN["email"], VALID_LOGIN["password"])
        app.landing_page.verify_logged_in(VALID_LOGIN["name"])

    with allure.step("Logout and verify Login page"):
        app.landing_page.logout()
        app.login_page.verify_loaded()
