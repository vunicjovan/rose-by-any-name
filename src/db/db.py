from tinydb import TinyDB
from tinydb.table import Table

db = TinyDB("data/books.json")
books_table: Table = db.table("books")
