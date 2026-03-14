from peewee import SqliteDatabase

db = SqliteDatabase("books.db", pragmas={"foreign_keys": 1})
