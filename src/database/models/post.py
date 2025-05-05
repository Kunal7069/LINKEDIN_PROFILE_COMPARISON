import uuid
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from database.models.base import Base



class LinkedInPost(Base):
    __tablename__ = "linkedin_posts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(100), nullable=False)
    text = Column(Text, nullable=True)
    original_post_text = Column(Text, nullable=True)
    totalreactions = Column(Integer, default=0)
    totalcomments = Column(Integer, default=0)
    posted_date = Column(String(100), nullable=False)

    images = relationship("PostImage", back_populates="post", cascade="all, delete-orphan")
    videos = relationship("PostVideo", back_populates="post", cascade="all, delete-orphan")


class PostImage(Base):
    __tablename__ = "post_images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("linkedin_posts.id"), nullable=False)
    url = Column(Text, nullable=False)
    width = Column(Integer)
    height = Column(Integer)

    post = relationship("LinkedInPost", back_populates="images")


class PostVideo(Base):
    __tablename__ = "post_videos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    post_id = Column(UUID(as_uuid=True), ForeignKey("linkedin_posts.id"), nullable=False)
    url = Column(Text, nullable=False)
    width = Column(Integer)
    height = Column(Integer)

    post = relationship("LinkedInPost", back_populates="videos")
