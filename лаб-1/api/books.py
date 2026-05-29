from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from typing import List, Optional
from schemas.book import Book, BookCreate, BookStatus
from services.book_service import get_books, get_book, create_book, remove_book

router = APIRouter()

@router.get("/books", response_model=List[Book], status_code=200)
async def read_books(
    status: Optional[BookStatus] = Query(None),
    author: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None)
):
    return get_books(status, author, sort_by)

@router.get("/books/{book_id}", response_model=Book, status_code=200)
async def read_book(book_id: UUID):
    book = get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/books", response_model=Book, status_code=201)
async def create_new_book(book: BookCreate):
    return create_book(book)

@router.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: UUID):
    remove_book(book_id)
