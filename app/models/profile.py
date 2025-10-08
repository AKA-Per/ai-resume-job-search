from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.models.database import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    full_name = Column(String)
    headline = Column(String)
    about = Column(Text, nullable=True)
    resume_path = Column(String, nullable=True)

    user = relationship("User", back_populates="profile")
    educations = relationship("Education", back_populates="profile", cascade="all, delete-orphan")
    experiences = relationship("Experience", back_populates="profile", cascade="all, delete-orphan")
    skills = relationship("Skill", back_populates="profile", cascade="all, delete-orphan")
    

class Education(Base):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    degree = Column(String)
    institution = Column(String)
    start_year = Column(String)
    end_year = Column(String)
    description = Column(Text, nullable=True)

    profile = relationship("Profile", back_populates="educations")


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    title = Column(String)
    company = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    description = Column(Text, nullable=True)

    profile = relationship("Profile", back_populates="experiences")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    name = Column(String, index=True)
    level = Column(String, nullable=True)  # e.g., Beginner / Intermediate / Expert

    profile = relationship("Profile", back_populates="skills")
