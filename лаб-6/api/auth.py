from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.session import SessionLocal
from schemas.user import UserCreate, UserOut, Token
from services.auth_service import (
    register_user, authenticate_user, create_access_token,
    create_refresh_token, decode_token, get_user_by_username
)
from jose import JWTError

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = get_user_by_username(db, user.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    return register_user(db, user.username, user.password)


@router.post("/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = create_access_token({"sub": db_user.username})
    refresh_token = create_refresh_token({"sub": db_user.username})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=Token)
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        username = payload.get("sub")
        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = get_user_by_username(db, username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    new_access_token = create_access_token({"sub": username})
    new_refresh_token = create_refresh_token({"sub": username})
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
