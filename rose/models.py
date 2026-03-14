from peewee import CharField, FloatField, IntegerField, Model, TextField

from .database import db


class Book(Model):
    title = CharField()
    author = CharField()
    print_year = IntegerField(null=True)
    reading_year = IntegerField(null=True)
    number_of_pages = IntegerField(null=True)
    original_language = CharField(null=True)
    reading_language = CharField(null=True)
    summary = TextField(null=True)
    cover_photo_url = CharField(null=True)
    user_rating = FloatField(default=0)
    user_remarks = TextField(null=True)

    class Meta:
        database = db


def create_tables():
    with db:
        db.create_tables([Book], safe=True)
