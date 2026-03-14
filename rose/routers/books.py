from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..models import Book

router = APIRouter(prefix="/api/books", tags=["books"])


class BookIn(BaseModel):
    title: str
    author: str
    print_year: int | None = None
    reading_year: int | None = None
    number_of_pages: int | None = None
    original_language: str | None = None
    reading_language: str | None = None
    summary: str | None = None
    cover_photo_url: str | None = None
    user_rating: float = 0
    user_remarks: str | None = None


def _to_dict(book: Book) -> dict:
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "print_year": book.print_year,
        "reading_year": book.reading_year,
        "number_of_pages": book.number_of_pages,
        "original_language": book.original_language,
        "reading_language": book.reading_language,
        "summary": book.summary,
        "cover_photo_url": book.cover_photo_url,
        "user_rating": book.user_rating,
        "user_remarks": book.user_remarks,
    }


@router.get("/")
def list_books():
    return [_to_dict(b) for b in Book.select()]


@router.get("/{book_id}")
def get_book(book_id: int):
    book = Book.get_or_none(Book.id == book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return _to_dict(book)


@router.post("/", status_code=201)
def create_book(data: BookIn):
    book = Book.create(**data.model_dump())
    return _to_dict(book)


@router.put("/{book_id}")
def update_book(book_id: int, data: BookIn):
    book = Book.get_or_none(Book.id == book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    for field, value in data.model_dump().items():
        setattr(book, field, value)
    book.save()
    return _to_dict(book)


@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int):
    book = Book.get_or_none(Book.id == book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    book.delete_instance()
