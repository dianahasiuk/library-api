from repository.book_repository import *
from models.book import Book

def list_books(db, limit, offset):
    return get_books(db, limit, offset)


def get_one(db, book_id):
    return get_book(db, book_id)


def create(db, data):
    book = Book(**data.dict())
    return create_book(db, book)


def delete(db, book_id):
    book = get_book(db, book_id)
    if book:
        delete_book(db, book)
    return True
