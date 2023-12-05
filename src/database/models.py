from sqlalchemy import Column, Integer,Boolean, String, DateTime, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String, index=True)
    secondname = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phonenumber = Column(String)
    birthday = Column(DateTime)
    refresh_token = Column(String(280), nullable=True)
    password = Column(String(280), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    confirmed = Column(Boolean, default=False)







