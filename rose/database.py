import os

from peewee import SqliteDatabase

db = SqliteDatabase(
    os.environ.get("DB_PATH", "books.db"),
    pragmas={"foreign_keys": 1},
)
