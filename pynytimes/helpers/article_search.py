"""Article Search helper functions"""
# Import typings dependencies
from __future__ import annotations
from typing import Any, Final, Optional, Union

# Import Python dependencies
import datetime
import warnings

NoneType: Final = type(None)

LARGE_RESULTS_WARN = 100
MAXIMUM_RESULTS = 2010

# FIXME not all filters are implemented

# Set query options that are currently supported
CURRENT_FILTER_SUPPORT: list[str] = [
    "source",
    "news_desk",
    "section_name",
    "glocation",
    "type_of_material",
    "subject",
    "body",
    "headline",
]


def _article_search_result_warnings(results: int):
    # Show warnings when a lot of results are requested
    if results >= LARGE_RESULTS_WARN:
        warnings.warn(
            "Asking for a lot of results, because of rate"
            + " limits it can take a while."
        )

    # Show waring when above maximum amount of results
    if results >= MAXIMUM_RESULTS:
        warnings.warn(
            "Asking for more results then the API can provide,"
            + "loading maximum results."
        )


def _article_search_check_type(
    query: Optional[str],
    dates: dict[str, Union[datetime.date, datetime.datetime, None]],
    options: dict[str, Any],
    results: int,
):
    # Check if types are correct
    if not isinstance(query, (str, NoneType)):
        raise TypeError("Query needs to be None or str")

    if not isinstance(dates, dict):
        raise TypeError("Dates needs to be a dict")

    if not isinstance(options, dict):
        raise TypeError("Options needs to be a dict")

    if not isinstance(results, (int, NoneType)):
        raise TypeError("Results needs to be None or int")


def _article_search_check_sort_options(options: dict[str, str]):
    # Get and check if sort option is valid
    sort = options.get("sort")

    if sort not in [None, "newest", "oldest", "relevance"]:
        raise ValueError("Sort option is not valid")


def _article_search_check_date_types(dates: dict[str, Any]):
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


def article_search_check_input(
    query: Optional[str],
    dates: dict[str, Union[datetime.date, datetime.datetime, None]],
    options: dict[str, Any],
    results: int,
) -> None:
    """Check input of article_search"""
    _article_search_check_type(query, dates, options, results)
    _article_search_check_sort_options(options)
    _article_search_check_date_types(dates)
    _article_search_result_warnings(results)


def _convert_date_to_str(
    date: Union[datetime.datetime, datetime.date, None]
) -> Optional[str]:
    if date is not None:
        return datetime.datetime(date.year, date.month, date.day).strftime(
            "%Y%m%d"
        )

    return None


def article_search_parse_dates(
    dates: dict[str, Union[datetime.datetime, datetime.date, None]]
) -> tuple[Optional[str], Optional[str]]:
    """Parse dates into options"""
    # Get dates if defined
    begin_date = dates.get("begin")
    end_date = dates.get("end")
    return (_convert_date_to_str(begin_date), _convert_date_to_str(end_date))


def _filter_input(values: list) -> str:
    if not isinstance(values, list):
        raise TypeError(
            "One of the parameters in the Article Search function,"
            " is not a list while it should be"
        )

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

    # Run for every filter
    for _filter in CURRENT_FILTER_SUPPORT:
        # Get data for filter if it's not defined continue to next filter
        values = options.get(_filter)
        if values is None:
            continue

        # Notice that this does not support OR statements, however
        # implementing would complicate this function a lot.
        # This may be worth it in the future, but not now.

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
