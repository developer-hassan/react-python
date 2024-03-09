from fastapi import FastAPI, HTTPException, Depends
from schemas import *
import models
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from seed import db_dependency

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/transactions/", response_model=TransactionModel)
async def create_transaction(
        transaction: TransactionBase,
        db: db_dependency
):
    db_transaction = models.Transaction(**transaction.dict()) # based on everything in the transactionbase, map all of the variables from our transaction base to our table "Transaction" to be saved into our mysql database.
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction


@app.get("/transactions/", response_model=List[TransactionModel])
async def read_transactions(db: db_dependency, skip: int = 0, limit: int = 100):
    transactions = db.query(models.Transaction).offset(skip).limit(limit).all()
    return transactions
