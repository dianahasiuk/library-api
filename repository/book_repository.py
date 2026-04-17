from sqlalchemy.orm import Session
from models.book import Book

def get_books(db: Session, limit: int, offset: int):
    return db.query(Book).offset(offset).limit(limit).all()


def get_book(db: Session, book_id: str):
    return db.query(Book).filter(Book.id == book_id).first()


def create_book(db: Session, book: Book):
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book: Book):
    db.delete(book)
    db.commit()
