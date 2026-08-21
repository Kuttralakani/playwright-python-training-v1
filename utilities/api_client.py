import requests

_BASE = "https://automationexercise.com/api"


def create_user(user: dict[str, str]) -> None:
    response = requests.post(
        f"{_BASE}/createAccount",
        data={
            "name": user["name"],
            "email": user["email"],
            "password": user["password"],
            "title": user["title"],
            "birth_date": user["birth_day"],
            "birth_month": user["birth_month"],
            "birth_year": user["birth_year"],
            "firstname": user["first_name"],
            "lastname": user["last_name"],
            "company": user["company"],
            "address1": user["address1"],
            "address2": user["address2"],
            "country": user["country"],
            "zipcode": user["zipcode"],
            "state": user["state"],
            "city": user["city"],
            "mobile_number": user["mobile_number"],
        },
        timeout=30,
    )
    data = response.json()
    assert data.get("responseCode") == 201, f"Failed to create user via API: {data}"


def delete_user(email: str, password: str) -> None:
    requests.delete(
        f"{_BASE}/deleteAccount",
        data={"email": email, "password": password},
        timeout=30,
    )
