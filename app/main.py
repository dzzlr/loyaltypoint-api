from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .models import User, Transaction, Voucher, VoucherBatch, VoucherTransaction
from .services.database import engine
from .routers import user, transaction, voucher_batch, voucher

User.metadata.create_all(bind=engine)
Transaction.metadata.create_all(bind=engine)
VoucherBatch.metadata.create_all(bind=engine)
Voucher.metadata.create_all(bind=engine)
VoucherTransaction.metadata.create_all(bind=engine)

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

app.include_router(user.router)
app.include_router(transaction.router)
app.include_router(voucher_batch.router)
app.include_router(voucher.router)

# Root endpoint
@app.get("/")
def read_root():
    return JSONResponse(
        status_code = status.HTTP_200_OK, 
        content = {
            "message": "Welcome to Loyalty Points Management API"
        })