from uuid import UUID
from typing import List, Dict, Optional
from models.book import books

def get_all_books() -> List[Dict]:
    return books

def get_book_by_id(book_id: UUID) -> Optional[Dict]:
    for book in books:
        if book["id"] == book_id:
            return book
    return None

def add_book(book: Dict) -> Dict:
    books.append(book)
    return book

def delete_book(book_id: UUID) -> None:
    global books
    books = [book for book in books if book["id"] != book_id]
