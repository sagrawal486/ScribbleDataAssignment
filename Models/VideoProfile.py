from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date
from datetime import date, datetime
from enum import Enum

metadata = declarative_base()

class Regions(str, Enum):
    US = "US"
    IN = "IN"
    CA = "CA"
    FR = "FR"
    DE = "DE"

class VideoProfile(BaseModel):
    video_id: str
    trending_date: date
    title: str
    channel_title: str
    category_id: int
    #publish_time: datetime
    tags: str
    region: str
    views: int
    likes: int
    dislikes: int
    comment_count: int
    category_title: str
    description: str

class VideoProfileDB(metadata):
    __tablename__ = "video_profiles"

    video_id = Column(String, primary_key=True, index=True)
    trending_date = Column(Date, primary_key=True, index=True)
    title = Column(String)
    channel_title = Column(String)
    category_id = Column(Integer)
    tags = Column(String)
    region = Column(String, primary_key=True, index=True)
    views = Column(Integer)
    likes = Column(Integer)
    dislikes = Column(Integer)
    comment_count = Column(Integer)
    #category_id = Column(Integer)
    category_title = Column(String)
    description = Column(String)
    