import logging
import json
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from ..auth import auth 
from ..schemas.transaction import TransactionCreate, TransactionResponse
from ..models import User, Transaction
from ..services.database import get_db
# from ..services.rabbitmq import RabbitMQ

router = APIRouter(
    prefix="/api/transactions",
    tags=["Transactions"],
    # responses={404: {"description": "Not found"}},
)

# rabbitmq = RabbitMQ()
logger = logging.getLogger('uvicorn.error')

TRANSACTION_RULES = {
    "T001": {"min_amount": 25000, "max_transactions": 50, "points": 190},
    "T002": {"min_amount": 25000, "max_transactions": 50, "points": 125},
    "T003": {"min_amount": 25000, "max_transactions": 50, "points": 100},
    "T004": {"min_amount": 25000, "max_transactions": 50, "points": 100},
    "T005": {"min_amount": 25000, "max_transactions": 50, "points": 3},
}

# @router.post("/", response_model=TransactionResponse)
@router.post("/")
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)  # Authenticated user
):
    payment_type_id = transaction.payment_type_id
    amount = transaction.amount

    # Step 1: Check if the payment_type_id is valid and exists in rules
    if payment_type_id not in TRANSACTION_RULES:
        raise HTTPException(status_code=400, detail="Invalid payment type")
    
    # Get the transaction rule for the specific payment_type_id
    rule = TRANSACTION_RULES[payment_type_id]

    # Step 2: Get the current month period (first day of the current month to now)
    start_of_month = datetime(datetime.now().year, datetime.now().month, 1)
    current_time = datetime.now()

    # Step 3: Count the number of transactions for the current user and payment_type_id in the current month
    transaction_count = db.query(func.count(Transaction.id)).filter(
        Transaction.cif == current_user.cif,
        Transaction.payment_type_id == payment_type_id,
        Transaction.created_at >= start_of_month,
        Transaction.created_at <= current_time
    ).scalar()

    # Step 6: Calculate the score based on the rule
    points = rule["points"]

    # Step 4: Check if the number of transactions exceeds the allowed limit for the month
    if transaction_count >= rule["max_transactions"]:
        # raise HTTPException(status_code=400, detail=f"Transaction limit for {payment_type_id} exceeded for this month")
        points = 0

    # Step 5: Check if the amount is greater than or equal to the minimum required amount
    if amount < rule["min_amount"]:
        points = 0
        # raise HTTPException(status_code=400, detail=f"Transaction amount must be at least {rule['min_amount']}")

    # Step 7: Create the new transaction
    new_transaction = Transaction(
        cif=current_user.cif,
        payment_type_id=payment_type_id,
        amount=amount,
        score=points,
        created_at=current_time
    )
    db.add(new_transaction)

    # Step 8: Update the user's points
    current_user.point += points

    # Step 9: Commit the transaction and update user points
    db.commit()
    db.refresh(new_transaction)
    db.refresh(current_user)

    return new_transaction

    # # Create a new transaction with the user's CIF (retrieved from JWT token)
    # db_transaction = Transaction(
    #     cif=current_user.cif,  # The CIF is tied to the logged-in user
    #     payment_type_id=transaction.payment_type_id,
    #     amount=transaction.amount,
    #     score=transaction.score,
    # )
    # db.add(db_transaction)
    # current_user.point += transaction.score
    # db.commit()
    # db.refresh(db_transaction)


    # db_transaction = {
    #     'cif': current_user.cif,  # The CIF is tied to the logged-in user
    #     'payment_type_id': transaction.payment_type_id,
    #     'amount': transaction.amount,
    #     'score': transaction.score,
    # }

    # rabbitmq.publish(queue_name='payment_queue', message=json.dumps(db_transaction))
    # logger.info(f'Send message to payment_queue: {db_transaction}')

    # return f'Send message to payment_queue: {db_transaction}'