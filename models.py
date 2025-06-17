from __future__ import annotations

from enum import Enum

from sqlalchemy import Column, Integer, String, Float, DateTime, func, ForeignKey
from db import Base
from sqlalchemy.orm import relationship

class ExpenseType(Enum):
    RENT = "rent"
    UTIL = "utils"
    RESTAURANTS = "restaurants"
    GROCERIES = "groceries"
    TEST = "test"
    HEALTH = "health"

class Expense(Base):
    __tablename__ = "Expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=True)
    type = Column(String, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    users = relationship("User", back_populates="Expense")

class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    expense_id = Column(Integer, ForeignKey('Expenses.id'))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    expenses = relationship("Expense", back_populates="Users")
