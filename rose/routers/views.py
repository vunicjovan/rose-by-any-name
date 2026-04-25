from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Book, Feedback, User

router = APIRouter(tags=["views"])
templates = Jinja2Templates(directory="templates")


# ── Pages ─────────────────────────────────────────────────────────────────────


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).order_by(Book.title).all()
    return templates.TemplateResponse(request, "index.html", {"books": books})


@router.get("/books", response_class=HTMLResponse)
def books_page(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).order_by(Book.title).all()
    return templates.TemplateResponse(request, "books.html", {"books": books})


@router.get("/books/{book_id}", response_class=HTMLResponse)
def book_detail(request: Request, book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        return templates.TemplateResponse(request, "404.html", status_code=404)
    feedbacks = (
        db.query(Feedback)
        .filter(Feedback.book_id == book_id)
        .order_by(Feedback.created_at.desc())
        .all()
    )
    users = db.query(User).order_by(User.surname, User.name).all()
    return templates.TemplateResponse(
        request,
        "book_detail.html",
        {"book": book, "feedbacks": feedbacks, "users": users},
    )


@router.get("/users", response_class=HTMLResponse)
def users_page(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.surname, User.name).all()
    return templates.TemplateResponse(request, "users.html", {"users": users})


@router.get("/users/{user_id}", response_class=HTMLResponse)
def user_detail(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        return templates.TemplateResponse(request, "404.html", status_code=404)
    feedbacks = (
        db.query(Feedback)
        .filter(Feedback.user_id == user_id)
        .order_by(Feedback.created_at.desc())
        .all()
    )
    return templates.TemplateResponse(
        request,
        "user_detail.html",
        {"user": user, "feedbacks": feedbacks},
    )


@router.get("/feedbacks", response_class=HTMLResponse)
def feedbacks_page(request: Request, db: Session = Depends(get_db)):
    feedbacks = db.query(Feedback).order_by(Feedback.created_at.desc()).all()
    return templates.TemplateResponse(
        request, "feedbacks.html", {"feedbacks": feedbacks}
    )


# ── HTMX partial: book list ───────────────────────────────────────────────────


@router.get("/partials/books", response_class=HTMLResponse)
def partial_books(request: Request, q: str = "", db: Session = Depends(get_db)):
    query = db.query(Book)
    if q:
        like = f"%{q}%"
        query = query.filter(Book.title.ilike(like) | Book.author.ilike(like))
    books = query.order_by(Book.title).all()
    return templates.TemplateResponse(
        request, "partials/book_list.html", {"books": books}
    )


@router.get("/partials/users", response_class=HTMLResponse)
def partial_users(request: Request, q: str = "", db: Session = Depends(get_db)):
    query = db.query(User)
    if q:
        like = f"%{q}%"
        query = query.filter(
            User.name.ilike(like) | User.surname.ilike(like) | User.email.ilike(like)
        )
    users = query.order_by(User.surname, User.name).all()
    return templates.TemplateResponse(
        request, "partials/user_list.html", {"users": users}
    )
