"""Movie Reviews helper functions"""
# Import typings dependencies
from __future__ import annotations
from typing import Any, Optional, Union

# Import Python dependencies
import datetime

# Shorten type(None)
NoneType: type = type(None)


def _convert_date_to_datetime(input: datetime.date) -> datetime.datetime:
    return datetime.datetime(input.year, input.month, input.day)


def _movie_reviews_check_types(
    keyword: Optional[str],
    options: Optional[dict[str, Any]],
    dates: Optional[dict[str, Union[datetime.date, datetime.datetime, None]]],
):
    # Raise error if keyword is not a string or NoneType
    if not isinstance(keyword, (str, NoneType)):
        raise TypeError("Keyword needs to be str")

    # Raise error if options or date is not a dict
    if not isinstance(options, dict):
        raise TypeError("Options needs to be dict")

    if not isinstance(dates, dict):
        raise TypeError("Dates needs to be dict")

    # Raise error if critics pick is not a bool
    if not isinstance(options.get("critics_pick", False), bool):
        raise TypeError("Critics Pick needs to be a bool")


def _check_order_option(options: dict):
    # Raise error if order is invalid type
    if not isinstance(options.get("order"), (str, NoneType)):
        raise TypeError("Order needs to be a str or None")

    # Check if order options is correct value
    order_options = [
        None,
        "by-opening-date",
        "by-publication-date",
        "by-title",
    ]

    if options.get("order") not in order_options:
        raise ValueError("Order is not a valid option")


def movie_reviews_check_input(
    keyword: Optional[str],
    options: Optional[dict[str, Any]],
    dates: Optional[dict[str, Union[datetime.date, datetime.datetime, None]]],
):
    _movie_reviews_check_types(keyword, options, dates)
    assert isinstance(dates, dict)
    assert isinstance(options, dict)

    # Loop through all items in dates and check if its a datetime.datetime
    # or a datetime.date object
    for date in dates.values():
        date_types = (datetime.datetime, datetime.date)
        if not isinstance(date, date_types):
            raise TypeError(
                "Date items need to be datetime.date or datetime.datetime"
            )

    _check_order_option(options)


def movie_reviews_parse_dates(
    dates: dict[str, Union[datetime.date, datetime.datetime, None]]
) -> dict:
    # Convert datetime.date to datetime.datetime
    for date in dates.items():
        date_value = date[1]
        if isinstance(date_value, datetime.date):
            dates[date[0]] = _convert_date_to_datetime(date_value)

    params = {}

    # Define a date if neccecary and convert all data to valid data
    # for API request
    undefined_opening_date = (
        dates.get("opening_date_end") is not None
        and dates.get("opening_date_start") is None
    )
    if undefined_opening_date is True:
        dates["opening_date_start"] = datetime.datetime(1900, 1, 1)

    undefined_publication_date = (
        dates.get("publication_date_end") is not None
        and dates.get("publication_date_start") is None
    )
    if undefined_publication_date is True:
        dates["publication_date_start"] = datetime.datetime(1900, 1, 1)

    # Insert the dates in the options dictionary
    _opening_dates = None
    _publication_dates = None

    if dates.get("opening_date_start") is not None:
        assert dates["opening_date_start"]  # Just to stop type checker
        _opening_dates = dates["opening_date_start"].strftime("%Y-%m-%d")
        _opening_dates += ";"

        if dates.get("opening_date_end") is not None:
            assert dates["opening_date_end"]  # Just to stop type checker
            _opening_dates += dates["opening_date_end"].strftime("%Y-%m-%d")

    if dates.get("publication_date_start") is not None:
        assert dates["publication_date_start"]
        _publication_dates = dates["publication_date_start"].strftime(
            "%Y-%m-%d"
        )
        _publication_dates += ";"

        if dates.get("publication_date_end") is not None:
            assert dates["publication_date_end"]
            _publication_dates += dates["publication_date_end"].strftime(
                "%Y-%m-%d"
            )

    params["opening-date"] = _opening_dates
    params["publication-date"] = _publication_dates

    return params


def movie_reviews_parse_params(
    params: dict, keyword: Optional[str], options: dict
):
    # Set keyword if defined
    if keyword is not None:
        params["query"] = keyword
    # Set critics pick to "Y" if true
    if options.get("critics_pick") is True:
        params["critics_pick"] = "Y"
    # Set API request params if defined
    params["reviewer"] = options.get("reviewer")
    params["order"] = options.get("order")
