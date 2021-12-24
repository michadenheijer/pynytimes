# Import typings dependencies
from __future__ import annotations
from typing import Optional


def tag_query_check_types(query: str, max_results: Optional[int]):
    if not isinstance(query, str):
        raise TypeError("Query needs to be str")
    if not isinstance(max_results, (type(None), int)):
        raise TypeError("Max results needs to be int")


def tag_query_get_filter_options(filter_options) -> Optional[str]:
    # Add filter options
    _filter_options = ""
    if filter_options is not None:
        for filter_opt in filter_options:
            if _filter_options is not None:
                _filter_options += ","
            _filter_options += filter_opt

        return filter_options
