import re

from playwright.sync_api import Page, expect


class SignupPage:
    def __init__(self, page: Page) -> None:
        self.page = page

        self.account_info_heading = page.get_by_text(
            re.compile(r"ENTER ACCOUNT INFORMATION", re.IGNORECASE)
        )
        self.password = page.locator("#password")
        self.days = page.locator("#days")
        self.months = page.locator("#months")
        self.years = page.locator("#years")
        self.newsletter = page.locator("#newsletter")
        self.offers = page.locator("#optin")
        self.first_name = page.locator("#first_name")
        self.last_name = page.locator("#last_name")
        self.company = page.locator("#company")
        self.address1 = page.locator("#address1")
        self.address2 = page.locator("#address2")
        self.country = page.locator("#country")
        self.state = page.locator("#state")
        self.city = page.locator("#city")
        self.zipcode = page.locator("#zipcode")
        self.mobile_number = page.locator("#mobile_number")
        self.create_account_button = page.locator('[data-qa="create-account"]')

    def verify_loaded(self) -> None:
        expect(self.account_info_heading).to_be_visible()

    def register(self, user: dict[str, str]) -> None:
        title = user["title"].strip().lower()
        if title in {"mr", "male"}:
            self.page.locator("#id_gender1").check()
        else:
            self.page.locator("#id_gender2").check()

        self.password.fill(user["password"])
        self.days.select_option(user["birth_day"])
        self.months.select_option(user["birth_month"])
        self.years.select_option(user["birth_year"])

        if user.get("newsletter", "").lower() == "yes":
            self.newsletter.check()
        if user.get("offers", "").lower() == "yes":
            self.offers.check()

        self.first_name.fill(user["first_name"])
        self.last_name.fill(user["last_name"])
        self.company.fill(user["company"])
        self.address1.fill(user["address1"])
        self.address2.fill(user["address2"])
        self.country.select_option(label=user["country"])
        self.state.fill(user["state"])
        self.city.fill(user["city"])
        self.zipcode.fill(user["zipcode"])
        self.mobile_number.fill(user["mobile_number"])
        self.create_account_button.click()
