from dataclasses import dataclass
from typing import List

import gradio as gr

# =========================
# Data Model
# =========================


@dataclass(frozen=True)
class Book:
    cover_url: str
    title: str
    author: str
    year: int
    pages: int


# =========================
# Mock Repository
# =========================


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


# =========================
# UI Components
# =========================


class BookCard:
    @staticmethod
    def render(book: Book) -> str:
        return f"""
        <div class="book-card">
            <img src="{book.cover_url}" alt="{book.title} cover" />
            <div class="book-info">
                <h3>{book.title}</h3>
                <p class="author">{book.author}</p>
                <p class="meta">{book.year} • {book.pages} pages</p>
            </div>
        </div>
        """


class BookGrid:
    @staticmethod
    def render(books: List[Book]) -> str:
        cards = "".join(BookCard.render(book) for book in books)
        return f"""
        <div class="book-grid">
            {cards}
        </div>
        """


# =========================
# App
# =========================


class RoseApp:
    CSS = """
    .book-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        padding: 1rem;
    }

    .book-card {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
        overflow: hidden;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .book-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 24px rgba(0, 0, 0, 0.12);
    }

    .book-card img {
        width: 100%;
        height: 280px;
        object-fit: cover;
    }

    .book-info {
        padding: 0.75rem 1rem 1rem;
    }

    .book-info h3 {
        font-size: 1rem;
        color: #555;
        margin: 0;
    }

    .book-info .author {
        font-size: 0.9rem;
        color: #555;
        margin: 0.25rem 0;
    }

    .book-info .meta {
        font-size: 0.8rem;
        color: #777;
    }
    """

    def __init__(self):
        self.books = BookRepository.get_books()

    def build(self) -> gr.Blocks:
        with gr.Blocks() as demo:
            gr.Markdown("## 📚 Book Showcase")
            gr.HTML(BookGrid.render(self.books))
        return demo

    def launch(self):
        self.build().launch(css=self.CSS)


# =========================
# Entry Point
# =========================

if __name__ == "__main__":
    RoseApp().launch()
