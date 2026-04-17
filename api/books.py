from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.book import BookCreate, BookOut
from services.book_service import *

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/books", response_model=list[BookOut])
def list_all(limit: int = 10, offset: int = 0, db: Session = Depends(get_db)):
    return list_books(db, limit, offset)


@router.post("/books", response_model=BookOut)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    return create(db, book)


@router.get("/books/{book_id}", response_model=BookOut)
def get_by_id(book_id: str, db: Session = Depends(get_db)):
    return get_one(db, book_id)


@router.delete("/books/{book_id}")
def delete_book(book_id: str, db: Session = Depends(get_db)):
    delete(db, book_id)
    return {"status": "deleted"}
