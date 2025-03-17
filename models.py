from __future__ import annotations

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer
from db import Base

class ExpenseType(Enum):
    RENT = "rent"


class Expense(Base):
    __tablename__ = "Expenses"

    id = Column(Integer, primary_key=True, index=True)
    description: str
    amount: float
    type: ExpenseType
    created_at: datetime
    updated_at: datetime