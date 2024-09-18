import logging
import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..auth import auth 
from ..schemas.transaction import TransactionCreate, TransactionResponse
from ..models import User, Transaction
from ..services.database import get_db
from ..services.rabbitmq import RabbitMQ

router = APIRouter(
    prefix="/api/transactions",
    tags=["transactions"],
    # responses={404: {"description": "Not found"}},
)

rabbitmq = RabbitMQ()
logger = logging.getLogger('uvicorn.error')

# @router.post("/", response_model=TransactionResponse)
@router.post("/")
def create_transaction(
    transaction: TransactionCreate,
    # db: Session = Depends(get_db),
    current_user: User = Depends(auth.get_current_user)  # Authenticated user
):
    # Create a new transaction with the user's CIF (retrieved from JWT token)
    # db_transaction = Transaction(
    #     cif=current_user.cif,  # The CIF is tied to the logged-in user
    #     payment_type_id=transaction.payment_type_id,
    #     amount=transaction.amount,
    #     score=transaction.score,
    # )
    # db.add(db_transaction)
    # db.commit()
    # db.refresh(db_transaction)

    db_transaction = {
        'cif': current_user.cif,  # The CIF is tied to the logged-in user
        'payment_type_id': transaction.payment_type_id,
        'amount': transaction.amount,
        'score': transaction.score,
    }

    rabbitmq.publish(queue_name='payment_queue', message=json.dumps(db_transaction))
    logger.info(f'Send message to payment_queue: {db_transaction}')

    return f'Send message to payment_queue: {db_transaction}'