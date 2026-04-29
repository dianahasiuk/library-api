from fastapi import FastAPI
from api.books import router as books_router
from api.auth import router as auth_router
from db.session import Base, engine
from models.user import User

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(books_router)

@app.get("/")
def root():
    return {"status": "running"}
