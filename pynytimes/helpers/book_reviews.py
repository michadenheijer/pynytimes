"""Book Reviews helper functions"""
# Import typings dependencies
from __future__ import annotations
from typing import Optional, Union

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

    # Check if only one of author, isbn, title is defined
    values_defined = int(isbn is not None)
    values_defined += int(title is not None)
    values_defined += int(author is not None)

    if values_defined != 1:
        raise ValueError(
            "You can only define one of the following: ISBN, author or title."
        )

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
