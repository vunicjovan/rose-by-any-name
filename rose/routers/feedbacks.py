from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Book, Feedback, User
from ..schemas import FeedbackCreate, FeedbackOut, FeedbackUpdate

router = APIRouter(prefix="/api/feedbacks", tags=["feedbacks"])


@router.get("/", response_model=list[FeedbackOut])
def list_feedbacks(db: Session = Depends(get_db)):
    return db.query(Feedback).order_by(Feedback.created_at.desc()).all()


@router.get("/{feedback_id}", response_model=FeedbackOut)
def get_feedback(feedback_id: int, db: Session = Depends(get_db)):
    fb = db.get(Feedback, feedback_id)
    if not fb:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return fb


@router.post("/", response_model=FeedbackOut, status_code=201)
def create_feedback(data: FeedbackCreate, db: Session = Depends(get_db)):
    if not db.get(User, data.user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if not db.get(Book, data.book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    fb = Feedback(**data.model_dump())
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb


@router.put("/{feedback_id}", response_model=FeedbackOut)
def update_feedback(
    feedback_id: int, data: FeedbackUpdate, db: Session = Depends(get_db)
):
    fb = db.get(Feedback, feedback_id)
    if not fb:
        raise HTTPException(status_code=404, detail="Feedback not found")
    for field, value in data.model_dump().items():
        setattr(fb, field, value)
    db.commit()
    db.refresh(fb)
    return fb


@router.delete("/{feedback_id}", status_code=204)
def delete_feedback(feedback_id: int, db: Session = Depends(get_db)):
    fb = db.get(Feedback, feedback_id)
    if not fb:
        raise HTTPException(status_code=404, detail="Feedback not found")
    db.delete(fb)
    db.commit()
