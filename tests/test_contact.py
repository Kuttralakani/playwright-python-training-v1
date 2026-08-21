import allure
import pytest

from pages.application import Application
from utilities.file_reader import PROJECT_ROOT, read_csv

CONTACT_DATA = read_csv("contact.csv")[0]


@allure.feature("Contact Us")
@allure.story("Contact Form")
@allure.title("TC06 - Contact Us Form")
@pytest.mark.regression
def test_tc06_contact_us_form(app: Application) -> None:
    upload_path = PROJECT_ROOT / CONTACT_DATA["upload_file"]

    with allure.step("Open application and navigate to Contact Us"):
        app.home_page.open()
        app.home_page.go_to_contact_us()
        app.contact_page.verify_loaded()

    with allure.step("Complete and submit the Contact Us form"):
        app.contact_page.submit(CONTACT_DATA, upload_path)
        app.contact_page.verify_success()

    with allure.step("Return to Home page"):
        app.contact_page.go_home()
        app.home_page.verify_home_visible()
