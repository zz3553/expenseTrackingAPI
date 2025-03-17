from __future__ import annotations

from datetime import datetime
from enum import Enum

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Database setup
DATABASE_URL = "sqlite:///./expense.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class ExpenseType(Enum):
    RENT = "rent"


class Expense(BaseModel):
    id = Column(Integer, primary_key=True, index=True)
    description: str
    amount: float
    type: ExpenseType
    created_at: datetime
    updated_at: datetime


# Create database tables
Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# FastAPI app
app = FastAPI()


# Get all expenses
@app.get("/expenses/")
def read_expenses(db: Session = Depends(get_db)):
    return db.query(Expense).all()


# Read Single Expense
@app.get("/expenses/{expense_id}")
def read_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


# Update Expense
@app.put("/expenses/{expense_id}")
def update_expense(
        expense_id: int,
        amount: int = None,
        description: str = None,
        expenseType: ExpenseType = None,
        db: Session = Depends(get_db)
):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    if amount:
        expense.amount = amount
    if description:
        expense.description = description
    if expenseType:
        expense.expenseType = expenseType
    db.commit()
    db.refresh(expense)
    return {"message": "Expense updated", "Expense": expense}


# Delete Expense
@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="To-Do item not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted"}