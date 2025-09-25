from sqlalchemy import Column, Integer, String, Boolean
from app.models.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_company = Column(Boolean, default=False)  # False = candidate, True = HR/company
