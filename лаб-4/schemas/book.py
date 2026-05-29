from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    description: str
    status: str
    year: int


class BookOut(BookCreate):
    id: str
