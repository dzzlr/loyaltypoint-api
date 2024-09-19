from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from ..auth import auth   # Assuming you're using JWT to get the current logged-in user
from ..models import User, VoucherBatch, Voucher, VoucherTransaction
from ..schemas.voucher import VoucherTransactionCreate, VoucherTransactionResponse, VoucherRedeem
from ..services.database import get_db

router = APIRouter(
    prefix="/api/vouchers",
    tags=["Vouchers"],
    # responses={404: {"description": "Not found"}},
)

@router.post("/buy", response_model=VoucherTransactionResponse)
def buy_voucher_transaction(
    transaction_data: VoucherTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    # Step 1: Find the voucher batch
    voucher_batch = db.query(VoucherBatch).filter(VoucherBatch.id == transaction_data.batch_id).first()
    if not voucher_batch:
        raise HTTPException(status_code=404, detail="Voucher batch not found")

    # Step 2: Check if the user's points are sufficient
    if current_user.point < voucher_batch.point:
        raise HTTPException(status_code=400, detail="Insufficient points to redeem the voucher")

    # Step 3: Find an available voucher from the batch
    available_voucher = db.query(Voucher).filter(
        Voucher.batch_id == transaction_data.batch_id,
        Voucher.status == 'available'
    ).first()

    if not available_voucher:
        raise HTTPException(status_code=404, detail="No available vouchers in this batch")

    # Step 4: Deduct the points from the user's point balance
    current_user.point -= voucher_batch.point

    # Step 5: Update the voucher status to 'redeemed' and set the redeemed_at field
    available_voucher.status = 'pending'
    available_voucher.redeemed_at = None

    # Step 6: Create the voucher transaction
    new_voucher_transaction = VoucherTransaction(
        cif=current_user.cif,
        batch_id=transaction_data.batch_id,
        voucher_code=available_voucher.id,
        redeemed_at=None
    )
    db.add(new_voucher_transaction)

    # Step 7: Commit the changes to both the user's points and the voucher
    db.commit()

    # Step 8: Return the created transaction
    db.refresh(new_voucher_transaction)
    return new_voucher_transaction

@router.post("/redeem", response_model=VoucherTransactionResponse)
def redeem_voucher(
    transaction_data: VoucherRedeem,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user),
):
    # Step 1: Validate the user's CIF (must match the logged-in user's CIF)
    user_cif = current_user.cif
    
    # Step 2: Check if the user has sufficient voucher code
    voucher_transaction = db.query(VoucherTransaction).filter(
        VoucherTransaction.voucher_code == transaction_data.voucher_code,
        VoucherTransaction.cif == user_cif
    ).first()
    if not voucher_transaction:
        raise HTTPException(status_code=404, detail="Voucher code not found")

    voucher_transaction.redeemed_at = datetime.now()

    # Step 3: Get an pending voucher from the vouchers
    available_voucher = db.query(Voucher).filter(
        Voucher.id == transaction_data.voucher_code,
        Voucher.status == 'pending'
    ).first()

    if not available_voucher:
        raise HTTPException(status_code=404, detail="No available vouchers for this batch")

    # Step 4: Update the voucher's status to 'redeemed'
    available_voucher.status = 'redeemed'
    available_voucher.redeemed_at = datetime.now()

    # Step 5: Commit changes (update voucher, update points, and insert transaction)
    db.commit()

    # Step 6: Return the transaction details including voucher code
    # db.refresh()
    return voucher_transaction
