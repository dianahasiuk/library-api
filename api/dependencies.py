from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from db.session import SessionLocal
from services.auth_service import decode_token, get_user_by_username
from services.rate_limiter import is_rate_limited
from jose import JWTError

bearer_scheme = HTTPBearer(auto_error=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    if not credentials:
        return None
    token = credentials.credentials
    try:
        payload = decode_token(token)
        if payload.get("type") != "access":
            return None
        username = payload.get("sub")
        if not username:
            return None
    except JWTError:
        return None
    return get_user_by_username(db, username)


def rate_limit(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db)
):
    user = None
    if credentials:
        try:
            payload = decode_token(credentials.credentials)
            if payload.get("type") == "access":
                username = payload.get("sub")
                if username:
                    user = get_user_by_username(db, username)
        except JWTError:
            pass

    is_authenticated = user is not None
    identifier = user.username if is_authenticated else request.client.host

    if is_rate_limited(identifier, is_authenticated):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Try again later."
        )
    return user
