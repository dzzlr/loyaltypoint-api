from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from ..models import VoucherBatch, Voucher
from ..schemas.voucher import VoucherBatchResponse, VoucherBatchCreate
from ..services.database import get_db
from ..utils.generate_vcode import generate_vcode

router = APIRouter(
    prefix="/api/voucher_batches",
    tags=["Vouchers"],
    # responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[VoucherBatchResponse])
def get_voucher_batches(db: Session = Depends(get_db)):
    """Retrieve the list of all voucher batches, including their associated vouchers."""
    voucher_batches = db.query(VoucherBatch).all()
    return voucher_batches

@router.post("/", response_model=VoucherBatchResponse)
def create_voucher_batch(
    batch_data: VoucherBatchCreate,
    db: Session = Depends(get_db),
):
    # Step 1: Create the voucher batch
    new_batch = VoucherBatch(
        id=generate_vcode(),
        name=batch_data.name,
        description=batch_data.description,
        point=batch_data.point,
        quantity=batch_data.quantity,
        expiry_date=batch_data.expiry_date,
    )
    db.add(new_batch)
    db.commit()
    db.refresh(new_batch)

    # Step 2: Generate voucher codes based on quantity
    vouchers = []
    for _ in range(batch_data.quantity):
        voucher_code = generate_vcode()
        new_voucher = Voucher(
            id=voucher_code,
            batch_id=new_batch.id,
            status="available",  # Vouchers start as active
        )
        db.add(new_voucher)
        vouchers.append(new_voucher)

    # Step 3: Save vouchers to the database
    db.commit()
    db.refresh(new_batch)

    return new_batch
