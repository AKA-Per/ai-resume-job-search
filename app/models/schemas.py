from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Auth
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None
    is_company: bool = False

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Company
class CompanyCreate(BaseModel):
    name: str
    description: Optional[str]
    website: Optional[str]

# Job
class JobCreate(BaseModel):
    title: str
    description: str
    education: str
    company_id: int
