from __future__ import annotations

import copy
from dataclasses import dataclass


@dataclass
class Book:
    """
    Book data model.

    ### Attributes

    `title`: The title of the book.

    `author`: The author of the book.

    `publishing_year`: The publishing year of the book.

    `number_of_pages`: The number of pages in the book.
    """

    title: str
    author: str
    publishing_year: int
    number_of_pages: int

    @staticmethod
    def new_empty() -> Book:
        """
        Creates a new empty `Book` object.
        """

        return Book(
            title="",
            author="",
            publishing_year=0,
            number_of_pages=0,
        )

    def copy(self) -> Book:
        """
        Creates a copy of the `Book` object.
        """

        return copy.copy(self)
