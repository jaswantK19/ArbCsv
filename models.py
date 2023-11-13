from sqlalchemy import String, Integer, Boolean, DateTime, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id=Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String, nullable=False)

    uploads = relationship('Uploads', back_populates='user')

class TokenTable(Base):
    __tablename__= "token"
    user_id = Column(Integer)
    access_token = Column(String, primary_key= True)
    refresh_token = Column(String, nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)


class Uploads(Base):
    __tablename__ = "uploads"
    upload_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    src = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship('User', back_populates='uploads')

