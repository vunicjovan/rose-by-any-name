from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    surname = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    feedbacks = relationship(
        "Feedback", back_populates="user", cascade="all, delete-orphan"
    )


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    publishing_year = Column(Integer, nullable=True)
    number_of_pages = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    feedbacks = relationship(
        "Feedback", back_populates="book", cascade="all, delete-orphan"
    )


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    rating = Column(Float, nullable=True)
    review = Column(Text, nullable=True)
    year_of_reading = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="feedbacks")
    book = relationship("Book", back_populates="feedbacks")


def create_tables(engine):
    Base.metadata.create_all(bind=engine)
