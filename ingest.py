# seed_books.py  — run from the project root: python seed_books.py

import sys
from pathlib import Path

# Make sure `rose` package is importable from the project root
sys.path.insert(0, str(Path(__file__).parent))

from rose.database import db
from rose.models import Book, create_tables

BOOKS = [
    {
        "title": "The Green Mile",
        "author": "Stephen King",
        "print_year": 1996,
        "reading_year": None,
        "number_of_pages": 544,
        "original_language": "English",
        "reading_language": "English",
        "cover_photo_url": "https://covers.openlibrary.org/b/id/8231303-L.jpg",
        "summary": (
            "Set on death row at Cold Mountain Penitentiary during the 1930s, "
            "The Green Mile follows Paul Edgecombe, a corrections officer who supervises "
            "the inmates awaiting execution. His world is upended when John Coffey arrives — "
            "a towering, gentle giant convicted of the murder of two young girls, yet possessing "
            "a mysterious supernatural gift of healing. As Paul and his colleagues come to know "
            "Coffey, they are forced to confront profound questions about innocence, guilt, "
            "justice, and the nature of miracles. King blends Southern Gothic atmosphere with "
            "deep moral weight in what many consider one of his most emotionally powerful works."
        ),
    },
    {
        "title": "How to Win Friends and Influence People",
        "author": "Dale Carnegie",
        "print_year": 1936,
        "reading_year": None,
        "number_of_pages": 288,
        "original_language": "English",
        "reading_language": "English",
        "cover_photo_url": "https://covers.openlibrary.org/b/id/8739161-L.jpg",
        "summary": (
            "One of the best-selling self-help books of all time, Carnegie's classic distills "
            "decades of research and real-world observation into practical principles for building "
            "lasting relationships and becoming more effective in personal and professional life. "
            "The book teaches readers how to make people feel genuinely valued, how to win others "
            "over to your point of view without argument, how to be a better listener, and how to "
            "inspire enthusiasm and cooperation. Its advice remains strikingly relevant nearly a "
            "century after it was first published."
        ),
    },
    {
        "title": "Never",
        "author": "Ken Follett",
        "print_year": 2021,
        "reading_year": None,
        "number_of_pages": 784,
        "original_language": "English",
        "reading_language": "English",
        "cover_photo_url": "https://covers.openlibrary.org/b/id/12547862-L.jpg",
        "summary": (
            "A geopolitical thriller of the highest order, Never follows a web of characters "
            "across the globe — a CIA operative in the Sahara, a Chinese intelligence officer, "
            "a US National Security Advisor, and a British diplomat — as a series of small "
            "miscalculations and misunderstandings gradually escalates toward a confrontation "
            "that could trigger a third world war. Follett draws on the logic of real-world "
            "deterrence theory and the fragility of international diplomacy to create a novel "
            "that is simultaneously a page-turning thriller and a sobering meditation on how "
            "easily civilisation can unravel."
        ),
    },
    {
        "title": "The Bourne Identity",
        "author": "Robert Ludlum",
        "print_year": 1980,
        "reading_year": None,
        "number_of_pages": 535,
        "original_language": "English",
        "reading_language": "English",
        "cover_photo_url": "https://covers.openlibrary.org/b/id/240727-L.jpg",
        "summary": (
            "A wounded man is pulled from the Mediterranean Sea with no memory of who he is. "
            "Piece by piece he reconstructs his identity — a name, Jason Bourne, and a set of "
            "lethal skills he cannot explain — while being hunted by intelligence agencies and "
            "assassins on multiple continents. Alongside economist Marie St. Jacques, who is "
            "drawn into his dangerous world against her will, Bourne races to uncover the truth "
            "about his past before his enemies can silence him. Ludlum's breakneck pacing and "
            "intricate plotting launched one of the most iconic espionage franchises in fiction."
        ),
    },
    {
        "title": "The Fifth Profession",
        "author": "David Morrell",
        "print_year": 1990,
        "reading_year": None,
        "number_of_pages": 486,
        "original_language": "English",
        "reading_language": "English",
        "cover_photo_url": "https://covers.openlibrary.org/b/id/336404-L.jpg",
        "summary": (
            "Savage, an American executive protector, and Akira, a Japanese bodyguard, "
            "independently experience the same traumatic memory of failing to save their "
            "clients in a hotel massacre — yet those events happened on opposite sides of the "
            "world. Drawn together by this impossible shared vision, the two elite operators "
            "must confront a labyrinthine conspiracy that challenges everything they believe "
            "about their pasts, their identities, and the nature of reality itself. Morrell — "
            "the creator of Rambo — delivers a tightly wound thriller that blends Eastern "
            "philosophy, Cold War intrigue, and relentless action."
        ),
    },
]


def main():
    db.connect(reuse_if_open=True)
    create_tables()

    inserted = 0
    for data in BOOKS:
        book, created = Book.get_or_create(
            title=data["title"],
            author=data["author"],
            defaults={k: v for k, v in data.items() if k not in ("title", "author")},
        )
        if created:
            print(f"  + Added: {book.title}")
            inserted += 1
        else:
            print(f"  ~ Skipped (already exists): {book.title}")

    db.close()
    print(f"\nDone. {inserted} book(s) added.")


if __name__ == "__main__":
    main()
