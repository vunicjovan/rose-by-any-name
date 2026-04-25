import logging
import os
import secrets
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from .auth import hash_password
from .database import SessionLocal, engine
from .models import User, create_tables
from .routers import auth as auth_router
from .routers import books, feedbacks, users, views

logger = logging.getLogger("rose")


def _seed_admin() -> None:
    """Create the first admin user if the users table is empty."""
    db = SessionLocal()
    try:
        if db.query(User).count() == 0:
            email = os.environ.get("ADMIN_EMAIL", "admin@rose.local")
            password = os.environ.get("ADMIN_PASSWORD", "changeme")
            if password == "changeme":
                logger.warning(
                    "Using default admin password 'changeme'. "
                    "Set ADMIN_PASSWORD environment variable before deploying."
                )
            admin = User(
                name="Admin",
                surname="User",
                email=email,
                password=hash_password(password),
                is_admin=True,
            )
            db.add(admin)
            db.commit()
            logger.info("Created default admin user: %s", email)
    finally:
        db.close()


def _migrate(engine) -> None:
    """Apply any schema changes that create_all cannot handle (e.g. new columns)."""
    with engine.connect() as conn:
        # Add is_admin column to users if it doesn't exist yet (SQLite has no
        # IF NOT EXISTS for ALTER TABLE ADD COLUMN, so inspect first).
        cols = {row[1] for row in conn.exec_driver_sql("PRAGMA table_info(users)")}
        if "is_admin" in cols:
            return
        conn.exec_driver_sql(
            "ALTER TABLE users ADD COLUMN is_admin INTEGER NOT NULL DEFAULT 0"
        )
        conn.commit()
        logger.info("Migration applied: added users.is_admin column")


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables(engine)
    _migrate(engine)
    _seed_admin()
    yield


SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = secrets.token_hex(32)
    logger.warning(
        "SECRET_KEY not set — using a random key. "
        "Sessions will not survive a restart. Set SECRET_KEY in production."
    )

app = FastAPI(title="Rose by Any Name", lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, https_only=False)

# Auth
app.include_router(auth_router.router)

# API routers
app.include_router(users.router)
app.include_router(books.router)
app.include_router(feedbacks.router)

# UI pages (htmx + Jinja2)
app.include_router(views.router)

# Static assets
app.mount("/static", StaticFiles(directory="static"), name="static")
