from sqlalchemy import Column, String, TIMESTAMP, ForeignKey
from ..services.database import Base

class Voucher(Base):
    __tablename__ = "vouchers"
    
    id = Column(String(10), primary_key=True, index=True, unique=True)
    batch_id = Column(String(10), ForeignKey("voucher_batches.id"), nullable=False)
    status = Column(String(15), nullable=False)
    redeemed_at = Column(TIMESTAMP, nullable=True)