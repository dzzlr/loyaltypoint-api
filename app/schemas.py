# app/schemas.py
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    # cif: str
    username: str
    password: str
    # point: int = 0

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    cif: str
    username: str
    point: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None