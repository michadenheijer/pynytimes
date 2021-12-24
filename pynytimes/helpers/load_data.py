# Import typings dependencies
from __future__ import annotations
from typing import Any, Final, Optional

# Import Request type
from requests.models import Response

INVALID_INPUT: Final = 400
INVALID_API_KEY: Final = 401
NO_ACCESS: Final = 403
DOES_NOT_EXIST: Final = 404


def raise_for_status(res: Response):
    if res.status_code == INVALID_INPUT:
        raise ValueError("Error 400: Invalid input")

    if res.status_code == INVALID_API_KEY:
        raise ValueError("Error 401: Invalid API Key")

    if res.status_code == NO_ACCESS:
        raise RuntimeError("Error 403: You don't have access to this page")

    if res.status_code == DOES_NOT_EXIST:
        raise RuntimeError("Error 404: This page does not exist")

    res.raise_for_status()


def get_from_location(
    parsed_res: dict[str, Any],
    location: Optional[list[str]],
) -> list[dict[str, Any]]:

    if location is None:
        return parsed_res["results"]

    # Sometimes the results are in a different location,
    # this location can be defined in a list
    # Then load the data from that location
    else:
        results: Any = parsed_res
        for loc in location:
            results = results[loc]

    return results
