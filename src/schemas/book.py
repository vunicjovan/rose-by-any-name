from dataclasses import dataclass


@dataclass(frozen=True)
class Book:
    cover_url: str
    title: str
    author: str
    year: int
    pages: int
