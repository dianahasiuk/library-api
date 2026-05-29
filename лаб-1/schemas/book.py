from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import Optional
from enum import Enum

class BookStatus(str, Enum):
    available = "available"
    issued = "issued"

class BookBase(BaseModel):
    title: str
    author: str
    description: str
    status: BookStatus
    year: int

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: UUID = Field(default_factory=uuid4)

    class Config:
        from_attributes = True
