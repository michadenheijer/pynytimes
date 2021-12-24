# Import typings dependencies
from __future__ import annotations
from typing import Any, Literal, Optional, Union

import datetime
import re


def parse_date(
    date_string: str,
    date_type: Literal["rfc3339", "date-only", "date-time"],
) -> Union[datetime.datetime, datetime.date, None]:
    """Parse the date into datetime.datetime object"""
    # If date_string is None return None
    if date_string is None:
        return None

    date: Union[datetime.datetime, datetime.date]

    # FIXME this should probabily be split up
    if date_type == "rfc3339":
        date = datetime.datetime.strptime(
            date_string,
            "%Y-%m-%dT%H:%M:%S%z",
        )
    elif date_type == "date-only":
        if re.match(r"^(\d){4}-00-00$", date_string):
            date = datetime.datetime.strptime(date_string, "%Y-00-00").date()

        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    elif date_type == "date-time":
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")

    return date


def parse_dates(
    articles: list[dict[str, str]],
    date_type: Literal["rfc3339", "date-only", "date-time"],
    locations: Optional[list] = None,
) -> list[dict[str, Any]]:
    """Parse dates to datetime"""
    # Create list locations is None
    if locations is None:
        locations = []

    # Create parsed_articles list
    parsed_articles: list[dict[str, Any]] = []

    # For every article parse date_string into datetime.datetime
    for article in articles:
        parsed_article: dict[str, Any] = article
        for location in locations:
            parsed_article[location] = parse_date(
                parsed_article[location], date_type
            )
        parsed_articles.append(article)

    return parsed_articles
