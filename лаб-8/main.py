from fastapi import FastAPI
from api.books import router
from db.session import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def root():
    return {"status": "running"}
