"""Book Reviews helper functions"""
# Import typings dependencies
from __future__ import annotations
from typing import Final, Optional, Union

# Shorten type(None)
NoneType: Final = type(None)


def book_reviews_check_input(
    author: Optional[str] = None,
    isbn: Union[str, int, None] = None,
    title: Optional[str] = None,
) -> None:
    """Check input of book_reviews"""
    # Raise TypeError if input is wrong type
    author_types = (str, NoneType)
    if not isinstance(author, author_types):
        raise TypeError("Author needs to be str")

    isbn_types = (int, str, NoneType)
    if not isinstance(isbn, isbn_types):
        raise TypeError("ISBN needs to be int or str")

    title_types = (str, NoneType)
    if not isinstance(title, title_types):
        raise TypeError("Title needs to be str")


def book_reviews_extract_options(
    author: Optional[str],
    isbn: Union[str, int, None],
    title: Optional[str],
) -> dict[str, str]:

    # FIXME this is just overly complicated
    options = {
        "author": author,
        "isbn": str(isbn) if isbn is not None else None,
        "title": title,
    }

    # Remove None values
    filtered_options = {k: v for k, v in options.items() if v is not None}

    # Check if only one is defined
    if len(filtered_options) != 1:
        raise ValueError(
            "You need to define one of the following: ISBN, author or title."
        )
    return filtered_options
