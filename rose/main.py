from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import db
from .models import create_tables
from .routers.books import router as books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect(reuse_if_open=True)
    create_tables()
    yield
    if not db.is_closed():
        db.close()


app = FastAPI(title="Rose by Any Name", lifespan=lifespan)
app.include_router(books_router)
app.mount("/", StaticFiles(directory="ui", html=True), name="ui")
