from .data_models import Book


class Persistence:
    """
    A class to handle operations for books.

    ### Attributes

    `book_items`: The list of `Book` objects.
    """

    def __init__(self) -> None:
        """
        Initializes the Persistence object with a list of `Book` objects.
        """

        self.book_items: list[Book] = self._populate_items()

    def _populate_items(self) -> list[Book]:
        """
        Populates the initial list of `Book` objects.
        """

        return [
            Book("1984", "George Orwell", 1949, 328),
            Book("To Kill a Mockingbird", "Harper Lee", 1960, 281),
            Book("The Great Gatsby", "F. Scott Fitzgerald", 1925, 180),
            Book("Pride and Prejudice", "Jane Austen", 1813, 279),
            Book("The Catcher in the Rye", "J.D. Salinger", 1951, 234),
            Book("The Hobbit", "J.R.R. Tolkien", 1937, 310),
            Book("Fahrenheit 451", "Ray Bradbury", 1953, 194),
            Book("Moby-Dick", "Herman Melville", 1851, 635),
            Book("Brave New World", "Aldous Huxley", 1932, 268),
            Book("Animal Farm", "George Orwell", 1945, 112),
        ]
