"""Article Search helper functions"""
# Import typings dependencies
from __future__ import annotations
from typing import Any, Optional, Union

# Import Python dependencies
import datetime
import warnings


def article_search_check_input(
    query: Optional[str],
    dates: dict[str, Union[datetime.date, datetime.datetime]],
    options: dict[str, Any],
    results: int,
) -> None:
    """Check input of article_search"""
    # Check if types are correct
    if not isinstance(query, (str, type(None))):
        raise TypeError("Query needs to be None or str")

    if not isinstance(dates, dict):
        raise TypeError("Dates needs to be a dict")

    if not isinstance(options, dict):
        raise TypeError("Options needs to be a dict")

    if not isinstance(results, (int, type(None))):
        raise TypeError("Results needs to be None or int")

    # Get and check if sort option is valid
    sort = options.get("sort")

    if sort not in [None, "newest", "oldest", "relevance"]:
        raise ValueError("Sort option is not valid")

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
            begin_date = datetime.datetime(
                begin_date.year, begin_date.month, begin_date.day
            )
        elif not isinstance(begin_date, datetime.datetime):
            raise TypeError(
                "Begin date has to be datetime.datetime or datetime.date"
            )

        begin_date_str = begin_date.strftime("%Y%m%d")

    if end_date is not None:
        if isinstance(end_date, datetime.date):
            end_date = datetime.datetime(
                end_date.year, end_date.month, end_date.day
            )
        elif not isinstance(end_date, datetime.datetime):
            raise TypeError(
                "End date has to be datetime.datetime or datetime.date"
            )

        end_date_str = end_date.strftime("%Y%m%d")

    return (begin_date_str, end_date_str)


def article_search_parse_options(options: dict[str, Any]) -> dict:
    """Help to create all fq queries"""
    # pylint: disable=invalid-name
    # Get options already defined in fq (filter query)
    fq = options.get("fq")

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
        # " AND " to the query, otherwise create fq
        if isinstance(fq, str):
            fq += " AND "
        else:
            fq = ""

        # Add filter
        fq += _filter + ":("

        # Add all the data in the list to the filter
        for i, value in enumerate(values):
            fq += '"'
            fq += value
            fq += '"'
            if i < len(values) - 1:
                fq += " "
        fq += ")"

        # Remove the filter from options
        del options[_filter]

    # If filter query was defined set fq
    if fq is not None:
        options["fq"] = fq

    # Return the options
    return options
