# Import typings dependencies
from __future__ import annotations
from typing import Literal


def most_shared_check_method(method: str):
    method_options = ["email", "facebook"]
    # Raise error if method isn't a str
    if not isinstance(method, str):
        raise TypeError("Method needs to be str")

        # Raise error if days, or method aren't in options
    if method not in method_options:
        raise ValueError("Shared option does not exist")


def most_shared_check_days(days: int):
    # Check if options are valid
    days_options = [1, 7, 30]

    # Raise error if days isn't an int
    if not isinstance(days, int):
        raise TypeError("Days needs to be int")

    if days not in days_options:
        raise ValueError("You can only select 1, 7 or 30 days")


def most_shared_get_url(
    base_url: str,
    method: Literal["email", "facebook"],
    days: Literal[1, 7, 30],
):
    # FIXME checking for none, while it is not a valid option
    if method is None:
        return f"{base_url}shared/{days}.json"
    elif method == "email":
        return f"{base_url}emailed/{days}.json"
    else:
        return f"{base_url}shared/{days}/{method}.json"
