from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..database import get_db
from ..models import Book, Feedback, User

router = APIRouter(tags=["views"])
templates = Jinja2Templates(directory="templates")


def _login_redirect(path: str) -> RedirectResponse:
    return RedirectResponse(url=f"/login?next={path}", status_code=302)


def _htmx_login_redirect() -> Response:
    """For htmx partial requests: signal the browser to redirect to login."""
    r = Response(status_code=401)
    r.headers["HX-Redirect"] = "/login"
    return r


# ── Pages ─────────────────────────────────────────────────────────────────────


@router.get("/", response_class=HTMLResponse)
def index(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    books = db.query(Book).order_by(Book.title).all()
    return templates.TemplateResponse(
        request, "index.html", {"books": books, "current_user": current_user}
    )


@router.get("/books", response_class=HTMLResponse)
def books_page(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    if not current_user:
        return _login_redirect("/books")
    books = db.query(Book).order_by(Book.title).all()
    return templates.TemplateResponse(
        request, "books.html", {"books": books, "current_user": current_user}
    )


@router.get("/books/{book_id}", response_class=HTMLResponse)
def book_detail(request: Request, book_id: int, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    book = db.get(Book, book_id)
    if not book:
        return templates.TemplateResponse(
            request, "404.html", {"current_user": current_user}, status_code=404
        )
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
        {
            "book": book,
            "feedbacks": feedbacks,
            "users": users,
            "current_user": current_user,
        },
    )


@router.get("/users", response_class=HTMLResponse)
def users_page(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    if not current_user:
        return _login_redirect("/users")
    if not current_user.is_admin:
        # Non-admins are redirected to their own profile
        return RedirectResponse(url=f"/users/{current_user.id}", status_code=302)
    users = db.query(User).order_by(User.surname, User.name).all()
    return templates.TemplateResponse(
        request, "users.html", {"users": users, "current_user": current_user}
    )


@router.get("/users/{user_id}", response_class=HTMLResponse)
def user_detail(request: Request, user_id: int, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    if not current_user:
        return _login_redirect(f"/users/{user_id}")
    # Non-admins can only view their own profile
    if not current_user.is_admin and current_user.id != user_id:
        return RedirectResponse(url=f"/users/{current_user.id}", status_code=302)
    user = db.get(User, user_id)
    if not user:
        return templates.TemplateResponse(
            request, "404.html", {"current_user": current_user}, status_code=404
        )
    feedbacks = (
        db.query(Feedback)
        .filter(Feedback.user_id == user_id)
        .order_by(Feedback.created_at.desc())
        .all()
    )
    return templates.TemplateResponse(
        request,
        "user_detail.html",
        {"user": user, "feedbacks": feedbacks, "current_user": current_user},
    )


@router.get("/profile", response_class=HTMLResponse)
def own_profile(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    if not current_user:
        return _login_redirect("/profile")
    return RedirectResponse(url=f"/users/{current_user.id}", status_code=302)


@router.get("/feedbacks", response_class=HTMLResponse)
def feedbacks_page(request: Request, db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    if not current_user:
        return _login_redirect("/feedbacks")
    feedbacks = db.query(Feedback).order_by(Feedback.created_at.desc()).all()
    return templates.TemplateResponse(
        request,
        "feedbacks.html",
        {"feedbacks": feedbacks, "current_user": current_user},
    )


# ── HTMX partials ─────────────────────────────────────────────────────────────


@router.get("/partials/books", response_class=HTMLResponse)
def partial_books(request: Request, q: str = "", db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    query = db.query(Book)
    if q:
        like = f"%{q}%"
        query = query.filter(Book.title.ilike(like) | Book.author.ilike(like))
    books = query.order_by(Book.title).all()
    return templates.TemplateResponse(
        request,
        "partials/book_list.html",
        {"books": books, "current_user": current_user},
    )


@router.get("/partials/users", response_class=HTMLResponse)
def partial_users(request: Request, q: str = "", db: Session = Depends(get_db)):
    current_user = get_current_user(request, db)
    if not current_user:
        return _htmx_login_redirect()
    if not current_user.is_admin:
        return Response(status_code=403)
    query = db.query(User)
    if q:
        like = f"%{q}%"
        query = query.filter(
            User.name.ilike(like) | User.surname.ilike(like) | User.email.ilike(like)
        )
    users = query.order_by(User.surname, User.name).all()
    return templates.TemplateResponse(
        request,
        "partials/user_list.html",
        {"users": users, "current_user": current_user},
    )
