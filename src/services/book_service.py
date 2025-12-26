from typing import List

from src.repository.book_repository import BookRepository
from src.schemas.book import Book


class BookService:
    def __init__(self) -> None:
        self.repository: BookRepository = BookRepository()

    def list(self) -> List[tuple[int, Book]]:
        return self.repository.list()
