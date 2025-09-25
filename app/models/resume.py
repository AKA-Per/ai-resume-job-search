from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.models.database import Base

class Resume(Base):
    __tablename__ = "resumes"
    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String)   # store file path or blob later
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User")
