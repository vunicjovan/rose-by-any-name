from pydantic import BaseModel, EmailStr, field_validator

# ── User ──────────────────────────────────────────────────────────────────────


class UserCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    is_admin: bool = False

    @field_validator("name", "surname")
    @classmethod
    def not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Field must not be empty")
        return v


class UserUpdate(BaseModel):
    name: str
    surname: str
    email: EmailStr

    @field_validator("name", "surname")
    @classmethod
    def not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Field must not be empty")
        return v


class UserOut(BaseModel):
    id: int
    name: str
    surname: str
    email: str
    is_admin: bool

    model_config = {"from_attributes": True}


# ── Book ──────────────────────────────────────────────────────────────────────


class BookCreate(BaseModel):
    title: str
    author: str
    publishing_year: int | None = None
    number_of_pages: int | None = None

    @field_validator("title", "author")
    @classmethod
    def not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Field must not be empty")
        return v


class BookUpdate(BookCreate):
    pass


class BookOut(BaseModel):
    id: int
    title: str
    author: str
    publishing_year: int | None
    number_of_pages: int | None

    model_config = {"from_attributes": True}


# ── Feedback ──────────────────────────────────────────────────────────────────


class FeedbackCreate(BaseModel):
    user_id: int
    book_id: int
    rating: float | None = None
    review: str | None = None
    year_of_reading: int | None = None

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v: float | None) -> float | None:
        if v is not None and not (0.0 <= v <= 10.0):
            raise ValueError("Rating must be between 0 and 10")
        return v


class FeedbackUpdate(BaseModel):
    rating: float | None = None
    review: str | None = None
    year_of_reading: int | None = None

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v: float | None) -> float | None:
        if v is not None and not (0.0 <= v <= 10.0):
            raise ValueError("Rating must be between 0 and 10")
        return v


class FeedbackOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    rating: float | None
    review: str | None
    year_of_reading: int | None
    user: UserOut
    book: BookOut

    model_config = {"from_attributes": True}
