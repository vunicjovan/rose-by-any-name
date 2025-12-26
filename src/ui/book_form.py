from typing import Optional

from src.schemas.book import Book


class BookForm:
    @staticmethod
    def render(
        action: str,
        book: Optional[Book] = None,
        book_id: Optional[int] = None,
        submit_label: str = "Save Book",
    ) -> str:
        return f"""
        <form class="book-card book-form" method="post" action="{action}">
            {f'<input type="hidden" name="id" value="{book_id}">' if book_id is not None else ""}

            <div class="book-info">
                <div class="form-group">
                    <label class="form-label">
                        Cover URL
                        <input
                            class="form-input"
                            type="url"
                            name="cover_url"
                            required
                            value="{book.cover_url if book else ""}"
                        />
                    </label>
                </div>

                <div class="form-group">
                    <label class="form-label">
                        Title
                        <input
                            class="form-input"
                            type="text"
                            name="title"
                            required
                            value="{book.title if book else ""}"
                        />
                    </label>
                </div>

                <div class="form-group">
                    <label class="form-label">
                        Author
                        <input
                            class="form-input"
                            type="text"
                            name="author"
                            required
                            value="{book.author if book else ""}"
                        />
                    </label>
                </div>

                <div class="form-group form-row">
                    <label class="form-label">
                        Year
                        <input
                            class="form-input"
                            type="number"
                            name="year"
                            min="0"
                            required
                            value="{book.year if book else ""}"
                        />
                    </label>

                    <label class="form-label">
                        Pages
                        <input
                            class="form-input"
                            type="number"
                            name="pages"
                            min="1"
                            required
                            value="{book.pages if book else ""}"
                        />
                    </label>
                </div>

                <div class="form-actions">
                    <button class="form-submit" type="submit">
                        {submit_label}
                    </button>
                </div>
            </div>
        </form>
        """
