from sqlalchemy import Column, String, Integer
from db.session import Base
import uuid

class Book(Base):
    __tablename__ = "books"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    description = Column(String)
    status = Column(String)
    year = Column(Integer)
