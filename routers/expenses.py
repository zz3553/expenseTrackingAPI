from __future__ import annotations

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

import crud, schemas, db
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/", response_model=schemas.ExpenseResponse)
def create_expense(expense: schemas.ExpenseCreate, database: Session = Depends(db.get_db)):
    return crud.create_expense(database, expense)


@router.get("/", response_model=List[schemas.ExpenseResponse])
def get_expenses(
        limit: int = Query(10, gt=0),
        start_date: str = Query(default=""),
        end_date: str = Query(default=""),
        database: Session = Depends(db.get_db)
):
    start_date = datetime.strptime(start_date, "%m/%d/%Y") if start_date else datetime.min
    end_date = datetime.strptime(end_date, "%m/%d/%Y").replace(hour=23, minute=59, second=59) if end_date else datetime.max

    return crud.get_last_x_expenses(
        database,
        limit=limit,
        start_date=start_date,
        end_date=end_date
    )


@router.get("/category", response_model=List[schemas.ExpenseResponse])
def get_expenses_filtered_by_type(
        category: str = Query(...),
        database: Session = Depends(db.get_db)
):
    return crud.get_expense_by_category(database, category)


@router.get("/{expense_id}", response_model=schemas.ExpenseResponse)
def get_expense_with_id(expense_id: int, database: Session = Depends(db.get_db)):
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
