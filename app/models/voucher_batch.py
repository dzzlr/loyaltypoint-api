from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from ..services.database import Base

class VoucherBatch(Base):
    __tablename__ = "voucher_batches"
    
    id = Column(String(10), primary_key=True, index=True, unique=True)
    name = Column(String(100))
    description = Column(String(100))
    point = Column(Integer, default=0)
    quantity = Column(Integer, default=0)
    expiry_date = Column(TIMESTAMP, server_default=func.now())
    created_at = Column(TIMESTAMP, server_default=func.now())