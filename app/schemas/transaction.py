from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    payment_type_id: str
    amount: int
    # score: int

class TransactionResponse(BaseModel):
    id: int
    cif: str
    payment_type_id: str
    amount: int
    score: int
    created_at: datetime

    class Config:
        orm_mode = True
