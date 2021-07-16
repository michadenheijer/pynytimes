"""Book Reviews helper functions"""
# Import typings dependencies
from __future__ import annotations
from typing import Any, Optional, Union

# Shorten type(None)
NoneType: type = type(None)


def book_reviews_check_input(
    author: Optional[str] = None,
    isbn: Union[str, int, None] = None,
    title: Optional[str] = None,
) -> None:
    """Check input of book_reviews"""
    # Check if request is valid
    if author and isbn and title is None:
        raise ValueError("Not all fields in reviews can be empty")

    values_defined = int(isbn is not None)
    values_defined += int(title is not None)
    values_defined += int(author is not None)

    if values_defined != 1:
        raise ValueError(
            "You can only define one of the following: ISBN, author or title."
        )

    # Raise TypeError if input is wrong type
    if not isinstance(author, (str, NoneType)):
        raise TypeError("Author needs to be str")

    if not isinstance(isbn, (int, str, NoneType)):
        raise TypeError("ISBN needs to be int or str")

    if not isinstance(title, (str, NoneType)):
        raise TypeError("Title needs to be str")
