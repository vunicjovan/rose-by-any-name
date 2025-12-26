from typing import List

from src.schemas.book import Book
from src.ui.book_card import BookCard


class BookGrid:
    @staticmethod
    def render(books: List[tuple[int, Book]]) -> str:
        cards = "".join(BookCard.render(book) for book_id, book in books)
        return f"""
        <div class="book-grid">
            {cards}
        </div>
        """
