from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, func
from ..services.database import Base

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    cif = Column(String(5), ForeignKey("users.cif"), nullable=False)
    payment_type_id = Column(String(5), nullable=False)
    amount = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
