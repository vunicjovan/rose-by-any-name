from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import engine
from .models import create_tables
from .routers import books, feedbacks, users, views


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables(engine)
    yield


app = FastAPI(title="Rose by Any Name", lifespan=lifespan)

# API routers
app.include_router(users.router)
app.include_router(books.router)
app.include_router(feedbacks.router)

# UI pages (htmx + Jinja2)
app.include_router(views.router)

# Static assets
app.mount("/static", StaticFiles(directory="static"), name="static")
