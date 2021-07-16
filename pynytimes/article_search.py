"""Article Search helper functions"""
# Import typings dependencies
from __future__ import annotations
from typing import Any, Optional, Union

# Import Python dependencies
import datetime
import warnings

NoneType = type(None)


def article_search_check_input(
    query: Optional[str],
    dates: dict[str, Union[datetime.date, datetime.datetime]],
    options: dict[str, Any],
    results: int,
) -> None:
    """Check input of article_search"""
    # Check if types are correct
    if not isinstance(query, (str, NoneType)):
        raise TypeError("Query needs to be None or str")

    if not isinstance(dates, dict):
        raise TypeError("Dates needs to be a dict")

    if not isinstance(options, dict):
        raise TypeError("Options needs to be a dict")

    if not isinstance(results, (int, NoneType)):
        raise TypeError("Results needs to be None or int")

    # Get and check if sort option is valid
    sort = options.get("sort")

    if sort not in [None, "newest", "oldest", "relevance"]:
        raise ValueError("Sort option is not valid")

    # Raise error if date is incorrect type
    date_types = (datetime.datetime, datetime.date, NoneType)

    begin_date = dates.get("begin_date")
    if not isinstance(begin_date, date_types):
        raise TypeError(
            "Begin date needs to be datetime.datetime, datetime.date or None"
        )

    end_date = dates.get("end_date")
    if not isinstance(end_date, date_types):
        raise TypeError(
            "End date needs to be datetime.datetime, datetime.date or None"
        )

    # Show warnings when a lot of results are requested
    if results >= 100:
        warnings.warn(
            "Asking for a lot of results, because of rate"
            + " limits it can take a while."
        )

    # Show waring when above maximum amount of results
    if results >= 2010:
        warnings.warn(
            "Asking for more results then the API can provide,"
            + "loading maximum results."
        )


def _convert_date_to_datetime(input: datetime.date) -> datetime.datetime:
    return datetime.datetime(input.year, input.month, input.day)


def article_search_parse_dates(
    dates: dict[str, Union[datetime.datetime, datetime.date, None]]
) -> tuple[Optional[str], Optional[str]]:
    """Parse dates into options"""
    # Get dates if defined
    begin_date = dates.get("begin")
    end_date = dates.get("end")

    # Set dates
    begin_date_str = None
    end_date_str = None

    # Raise error if dates aren't datetime.datetime objects
    if begin_date is not None:
        if isinstance(begin_date, datetime.date):
            begin_date = _convert_date_to_datetime(begin_date)

        begin_date_str = begin_date.strftime("%Y%m%d")

    if end_date is not None:
        if isinstance(end_date, datetime.date):
            end_date = _convert_date_to_datetime(end_date)

        end_date_str = end_date.strftime("%Y%m%d")

    return (begin_date_str, end_date_str)


def _filter_input(values: list) -> str:
    input = ""
    # Add all the data in the list to the filter
    for i, value in enumerate(values):
        input += f'"{value}"'
        if i < len(values) - 1:
            input += " "

    return input


def article_search_parse_options(options: dict[str, Any]) -> dict:
    """Help to create all fq queries"""
    # pylint: disable=invalid-name
    # Get options already defined in fq (filter query)
    fq = options.get("fq", "")

    # Set query options that are currently supported
    current_filter_support = [
        "source",
        "news_desk",
        "section_name",
        "glocation",
        "type_of_material",
    ]

    # Run for every filter
    for _filter in current_filter_support:
        # Get data for filter if it's not defined continue to next filter
        values = options.get(_filter)
        if values is None:
            continue

        # Check if filter query is already defined. If it is then add
        # " AND " to the query
        if len(fq) != 0:
            fq += " AND "

        # Add filter
        filter_input = _filter_input(values)
        fq += f"{_filter}:({filter_input})"

        # Remove the filter from options
        options.pop(_filter)

    # Set fq in options
    options["fq"] = fq

    # Return the options
    return options
