# Import typings dependencies
from __future__ import annotations
from typing import Union

import datetime


def best_sellers_parse_date(
    date: Union[datetime.date, datetime.datetime, None]
) -> str:
    # Set current if none
    if date is None:
        return "current"

    # Raise error if date is not a datetime.datetime object
    if not isinstance(date, (datetime.datetime, datetime.date)):
        raise TypeError("Date has to be a datetime or date object")

    # Set date if defined
    return datetime.datetime(date.year, date.month, date.day).strftime(
        "%Y-%m-%d"
    )
