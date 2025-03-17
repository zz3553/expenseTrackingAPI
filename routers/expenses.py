from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, db

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=schemas.ExpenseResponse)
def create_expense(expense: schemas.ExpenseCreate, database: Session = Depends(db.get_db)):
    return crud.create_expense(database, expense)

@router.get("/", response_model=List[schemas.ExpenseResponse])
def get_expenses(database: Session = Depends(db.get_db)):
    return crud.get_expenses(database)

@router.get("/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense(expense_id: int, database: Session = Depends(db.get_db)):
    expense = crud.get_expense(database, expense_id)
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.put("/{expense_id}", response_model=schemas.ExpenseResponse)
def update_expense(
        expense_id: int,
        updates: schemas.ExpenseUpdate,
        database: Session = Depends(db.get_db)
):
    return crud.update_expense(database, expense_id, updates)

@router.delete("/{expense_id}", response_model=schemas.ExpenseResponse)
def delete_expense(
        expense_id: int,
        database: Session = Depends(db.get_db)
):
    expense = crud.get_expense(database, expense_id)

    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    return crud.delete_expense(database, expense_id)