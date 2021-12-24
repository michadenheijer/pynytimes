# Import typings dependencies
from __future__ import annotations
from typing import Any


def article_metadata_set_url(url: str) -> dict[str, str]:
    # Raise error if url is not an str
    if not isinstance(url, str):
        raise TypeError("URL needs to be str")
    # Set metadata in requests params and define URL
    options = {"url": url}

    return options


def article_metadata_check_valid(result: list[dict[str, Any]]):
    # Check if result is valid
    if result[0].get("published_date") == "0000-12-31T19:03:58-04:56":
        raise ValueError(
            "Invalid URL, the API cannot parse metadata from live articles"
        )
