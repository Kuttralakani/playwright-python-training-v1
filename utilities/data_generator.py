from uuid import uuid4


def build_unique_user(template: dict[str, str]) -> dict[str, str]:
    user = dict(template)
    token = uuid4().hex[:10]

    prefix = user.pop("name_prefix")
    user["name"] = f"{prefix}_{token[:6]}"
    user["email"] = f"ae_{token}@example.com"

    return user
