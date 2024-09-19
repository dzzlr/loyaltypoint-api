from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..auth import auth 
from ..models import User, Transaction
from ..schemas import UserCreate, UserResponse, Token, UserTransactionsResponse
from ..services.database import get_db
from ..utils.generate_cif import generate_random_cif

router = APIRouter(
    prefix="/api",
    tags=["Users"],
    # responses={404: {"description": "Not found"}},
)

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Generate random CIF
    random_cif = generate_random_cif()

    # Ensure the CIF is unique
    db_cif = db.query(User).filter(User.cif == random_cif).first()
    if db_cif:
        raise HTTPException(status_code=400, detail="CIF already exists. Please try again.")

    # Hash the password
    hashed_password = auth.get_password_hash(user.password)

    # Create a new user with random CIF, hashed password, and default points
    db_user = User(cif=random_cif, username=user.username, hashed_password=hashed_password, point=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: UserResponse = Depends(auth.get_current_user)):
    return current_user

@router.get("/transactions/me", response_model=UserTransactionsResponse)
def get_user_transactions(db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    transactions = db.query(Transaction).filter(Transaction.cif == current_user.cif).all()
    total_points = sum(t.score for t in transactions)
    return {"total_points": total_points, "transactions": transactions}

@router.get("/transactions/point", response_model=dict)
def get_user_transactions_grouped_by_payment_type(
    db: Session = Depends(get_db), 
    current_user: User = Depends(auth.get_current_user)
):
    # Query to sum the scores grouped by payment_type_id
    grouped_transactions = db.query(
        Transaction.payment_type_id,
        func.sum(Transaction.score)
    ).filter(
        Transaction.cif == current_user.cif
    ).group_by(
        Transaction.payment_type_id
    ).all()

    # Convert result to dictionary where keys are payment_type_ids and values are the total points
    result = {f"{str(payment_type_id).zfill(3)}": int(total_score) for payment_type_id, total_score in grouped_transactions}
    
    return result