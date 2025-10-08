from pydantic import BaseModel, EmailStr
from typing import Optional, List

class EducationBase(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    start_year: Optional[str] = None
    end_year: Optional[str] = None
    description: Optional[str] = None

class EducationCreate(EducationBase):
    pass

class EducationOut(EducationBase):
    id: int
    class Config:
        from_attributes = True
        


class ExperienceBase(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None

class ExperienceCreate(ExperienceBase):
    pass

class ExperienceOut(ExperienceBase):
    id: int
    class Config:
        from_attributes = True

class SkillBase(BaseModel):
    name: str
    level: Optional[str] = None

class SkillCreate(SkillBase):
    pass

class SkillOut(SkillBase):
    id: int
    class Config:
        from_attributes = True

class ProfileBase(BaseModel):
    full_name: Optional[str] = None
    headline: Optional[str] = None
    about: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileOut(ProfileBase):
    id: int
    resume_path: Optional[str]
    educations: List[EducationOut] = []
    experiences: List[ExperienceOut] = []
    skills: List[SkillOut] = []
    class Config:
        from_attributes = True