from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Book

router = APIRouter()

@router.get("/")
def get_books(db: Session = Depends(get_db)):
    return db.query(Book).all()