# Import typings dependencies
from __future__ import annotations
from typing import Literal


def latest_articles_check_types(
    source: Literal["all", "nyt", "inyt"],
    section: str,
):
    if not isinstance(source, str):
        raise TypeError("Source needs to be str")
    if not isinstance(section, str):
        raise TypeError("Section needs to be str")

    # Check if sections options is valid
    # FIXME maybe not raise error, since additional sources
    # might be added in the future
    source_options = ["all", "nyt", "inyt"]
    if source not in source_options:
        raise ValueError("Source is not a valid option")
