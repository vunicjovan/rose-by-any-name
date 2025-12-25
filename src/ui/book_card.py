from src.schemas.book import Book


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
