import re


def parse_rupees(value: str) -> int:
    match = re.search(r"(\d[\d,]*)", value)
    if not match:
        raise ValueError(f"Unable to parse rupee amount from: {value}")
    return int(match.group(1).replace(",", ""))
