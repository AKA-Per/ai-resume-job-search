from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.models import database, user
from app.models.schemas import UserCreate, UserLogin, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings

router = APIRouter()

@router.post("/signup", response_model=Token)
def signup(payload: UserCreate, db: Session = Depends(database.get_db)):
    # check if user exists
    if db.query(user.User).filter(user.User.email == payload.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = user.User(
        email=payload.email,
        full_name=payload.full_name,
        is_company=payload.is_company,
        hashed_password=hash_password(payload.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token({"sub": new_user.email})
    return {"access_token": token}

@router.post("/login", response_model=Token)
def login(payload: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    print(payload)
    db_user = db.query(user.User).filter(user.User.email == payload.username).first()
    if not db_user or not verify_password(payload.password, str(db_user.hashed_password)):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": str(db_user.id)}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
