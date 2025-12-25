from typing import List

from src.schemas.book import Book


class BookRepository:
    @staticmethod
    def get_books() -> List[Book]:
        return [
            Book(
                cover_url="https://covers.openlibrary.org/b/id/10523366-L.jpg",
                title="1984",
                author="George Orwell",
                year=1949,
                pages=328,
            ),
            Book(
                cover_url="https://covers.openlibrary.org/b/id/11153258-L.jpg",
                title="Brave New World",
                author="Aldous Huxley",
                year=1932,
                pages=288,
            ),
            Book(
                cover_url="https://covers.openlibrary.org/b/id/10594754-L.jpg",
                title="Fahrenheit 451",
                author="Ray Bradbury",
                year=1953,
                pages=194,
            ),
            Book(
                cover_url="https://covers.openlibrary.org/b/id/10469362-L.jpg",
                title="The Hobbit",
                author="J.R.R. Tolkien",
                year=1937,
                pages=310,
            ),
            Book(
                cover_url="https://covers.openlibrary.org/b/id/10958350-L.jpg",
                title="Dune",
                author="Frank Herbert",
                year=1965,
                pages=412,
            ),
            Book(
                cover_url="https://covers.openlibrary.org/b/id/10580435-L.jpg",
                title="The Catcher in the Rye",
                author="J.D. Salinger",
                year=1951,
                pages=277,
            ),
            Book(
                cover_url="https://covers.openlibrary.org/b/id/10207889-L.jpg",
                title="To Kill a Mockingbird",
                author="Harper Lee",
                year=1960,
                pages=281,
            ),
            Book(
                cover_url="https://covers.openlibrary.org/b/id/10519127-L.jpg",
                title="The Great Gatsby",
                author="F. Scott Fitzgerald",
                year=1925,
                pages=180,
            ),
        ]
