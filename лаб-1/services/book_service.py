from uuid import UUID, uuid4
from typing import List, Dict, Optional
from schemas.book import BookCreate, BookStatus
from repository.book_repository import get_all_books, get_book_by_id, add_book, delete_book

def get_books(status: Optional[BookStatus] = None, author: Optional[str] = None, sort_by: Optional[str] = None) -> List[Dict]:
    books = get_all_books()
    if status:
        books = [b for b in books if b["status"] == status]
    if author:
        books = [b for b in books if b["author"].lower() == author.lower()]
    if sort_by == "title":
        books = sorted(books, key=lambda x: x["title"])
    elif sort_by == "year":
        books = sorted(books, key=lambda x: x["year"])
    return books

def get_book(book_id: UUID) -> Optional[Dict]:
    return get_book_by_id(book_id)

def create_book(book_data: BookCreate) -> Dict:
    book = book_data.model_dump()
    book["id"] = uuid4()
    return add_book(book)

def remove_book(book_id: UUID) -> None:
    delete_book(book_id)
