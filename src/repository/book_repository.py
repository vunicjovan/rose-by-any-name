from dataclasses import asdict
from typing import List

from tinydb.table import Table

from src.db.db import books_table
from src.schemas.book import Book


class BookRepository:
    def __init__(self) -> None:
        self.table: Table = books_table

    def create(self, book: Book) -> int:
        return self.table.insert(asdict(book))

    def get(self, book_id: int) -> Book | None:
        result = self.table.get(doc_id=book_id)

        # result may be a Document, a list[Document], or None; normalize to a single Document or None
        if isinstance(result, list):
            document = result[0] if result else None
        else:
            document = result

        return Book(**document) if document else None

    def list(self) -> List[tuple[int, Book]]:
        return [(d.doc_id, Book(**d)) for d in self.table.all()]

    def update(self, book_id: int, book: Book) -> bool:
        return bool(self.table.update(asdict(book), doc_ids=[book_id]))

    def delete(self, book_id: int) -> bool:
        return bool(self.table.remove(doc_ids=[book_id]))
