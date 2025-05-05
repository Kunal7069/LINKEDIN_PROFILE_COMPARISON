import uuid
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from database.models.base import Base



class LinkedInProfile(Base):
    __tablename__ = "linkedin_profile"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    headline = Column(Text, nullable=True)
    follower_count = Column(Integer, default=0)
    connection_count = Column(Integer, default=0)
    industry = Column(String(100), nullable=False) 
    
    