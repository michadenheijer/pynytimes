# Import typings dependencies
from __future__ import annotations


def most_viewed_check_values(days: int):
    days_options = [1, 7, 30]

    # Raise an TypeError if days is not a int
    if not isinstance(days, int):
        raise TypeError("You can only enter an int")
    # Raise an ValueError if number of days is invalid
    if days not in days_options:
        raise ValueError("You can only select 1, 7 or 30 days")
