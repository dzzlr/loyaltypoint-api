# app/models.py
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"
    
    # Use CIF as primary key
    cif = Column(String(5), primary_key=True, index=True, unique=True)
    username = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    point = Column(Integer, default=0)
