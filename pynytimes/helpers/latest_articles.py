# Import typings dependencies
from __future__ import annotations


def latest_articles_check_types(source: str, section: str):
    if not isinstance(source, str):
        raise TypeError("Source needs to be str")
    if not isinstance(section, str):
        raise TypeError("Section needs to be str")

    # Check if sections options is valid
    source_options = ["all", "nyt", "inyt"]
    if source not in source_options:
        raise ValueError("Source is not a valid option")
