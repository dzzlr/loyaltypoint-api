from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class VoucherBatchCreate(BaseModel):
    name: str
    description: str
    point: int
    quantity: int
    expiry_date: datetime

class VoucherBatchResponse(BaseModel):
    id: str
    name: str
    description: str
    point: int
    quantity: int
    expiry_date: datetime
    created_at: datetime
    # vouchers: List[VoucherBatchCreate] = []

    class Config:
        orm_mode = True

class VoucherCreate(BaseModel):
    batch_id: str
    status: str  # e.g., "active", "redeemed", "expired"

class VoucherResponse(BaseModel):
    id: str
    batch_id: str
    status: str
    redeemed_at: datetime

    class Config:
        orm_mode = True

class VoucherTransactionCreate(BaseModel):
    batch_id: str

class VoucherTransactionResponse(BaseModel):
    id: int
    cif: str
    batch_id: str
    voucher_code: str
    redeemed_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class VoucherRedeem(BaseModel):
    voucher_code: str