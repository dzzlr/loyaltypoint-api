from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

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

class TransactionList(BaseModel):
    # id: int
    payment_type_id: str
    created_at: datetime
    score: int
    # amount: float

    class Config:
        orm_mode = True

class UserTransactionsResponse(BaseModel):
    total_points: int
    transactions: List[TransactionList]