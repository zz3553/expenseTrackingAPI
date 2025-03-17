from __future__ import annotations

from enum import Enum

from sqlalchemy import Column, Integer, String, Float, DateTime, func
from .db import Base

class ExpenseType(Enum):
    RENT = "rent"


class Expense(Base):
    __tablename__ = "Expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    type = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())