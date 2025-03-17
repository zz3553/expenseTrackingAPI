from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas

def create_expense(db: Session, expense: schemas.ExpenseCreate):
    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_expenses(db: Session, skip: int = 0, limit: int = 10):
    stmt = select(models.Expense).offset(skip).limit(limit)
    return db.execute(stmt).scalars().all()

def get_expense(db: Session, expense_id: int):
    stmt = select(models.Expense).where(models.Expense.id == expense_id)
    return db.execute(stmt).scalar_one_or_none()

def update_expense(db: Session, expense_id: int, updates: schemas.ExpenseUpdate):
    stmt = select(models.Expense).where(models.Expense.id == expense_id)
    db_expense = db.execute(stmt).scalar_one_or_none()

    if not db_expense:
        return None  # Handle not found case

    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(db_expense, key, value)
    db.commit()
    db.refresh(db_expense)
    return db_expense

def delete_expense(db: Session, expense_id: int):
    stmt = select(models.Expense).where(models.Expense.id == expense_id)
    db_expense = db.execute(stmt).scalar_one_or_none()

    if not db_expense:
        return None  # Handle not found case

    db.delete(db_expense)
    db.commit()
    return db_expense