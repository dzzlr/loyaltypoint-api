from sqlalchemy import Column, Integer, String
from ..services.database import Base

class User(Base):
    __tablename__ = "users"
    
    cif = Column(String(5), primary_key=True, index=True, unique=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True)
    hashed_password = Column(String(100))
    point = Column(Integer, default=0)