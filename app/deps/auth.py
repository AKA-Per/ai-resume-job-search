from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.models import database, user
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    db_user = db.query(user.User).filter(user.User.id == user_id).first()
    if db_user is None:
        raise credentials_exception
    return db_user

def require_company(current_user: user.User = Depends(get_current_user)):
    if not current_user.is_company:
        raise HTTPException(status_code=403, detail="Only company accounts can perform this action")
    return current_user

def require_candidate(current_user: user.User = Depends(get_current_user)):
    if current_user.is_company:
        raise HTTPException(status_code=403, detail="Only candidate accounts can perform this action")
    return current_user
