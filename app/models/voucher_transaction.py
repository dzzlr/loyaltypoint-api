from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func
from ..services.database import Base

class VoucherTransaction(Base):
    __tablename__ = "voucher_transactions"
    
    id = Column(Integer, primary_key=True, index=True, unique=True)
    cif = Column(String(5), ForeignKey("users.cif"), nullable=False)
    batch_id = Column(String(10), ForeignKey("voucher_batches.id"), nullable=False)
    voucher_code = Column(String(10), unique=True, nullable=False)
    redeemed_at = Column(TIMESTAMP, nullable=True)
