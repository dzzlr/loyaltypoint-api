# app/main.py
from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app import models, schemas, auth
from app.database import engine, get_db
from app.utils.generate_cif import generate_random_cif

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Loyalty Points Management API",
    description="This API allows for the management of customer loyalty points within a system",
    version="0.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/token", response_model=schemas.Token)
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

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Generate random CIF
    random_cif = generate_random_cif()

    # Ensure the CIF is unique
    db_cif = db.query(models.User).filter(models.User.cif == random_cif).first()
    if db_cif:
        raise HTTPException(status_code=400, detail="CIF already exists. Please try again.")

    # Hash the password
    hashed_password = auth.get_password_hash(user.password)

    # Create a new user with random CIF, hashed password, and default points
    db_user = models.User(cif=random_cif, username=user.username, hashed_password=hashed_password, point=0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: schemas.UserResponse = Depends(auth.get_current_user)):
    return current_user
