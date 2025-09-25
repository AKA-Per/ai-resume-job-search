from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import database, user
from app.models.schemas import UserCreate, UserLogin, Token
from app.core.security import hash_password, verify_password, create_access_token

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
def login(payload: UserLogin, db: Session = Depends(database.get_db)):
    db_user = db.query(user.User).filter(user.User.email == payload.email).first()
    if not db_user or not verify_password(payload.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": db_user.email})
    return {"access_token": token}
