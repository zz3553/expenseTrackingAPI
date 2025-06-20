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

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # One user -> many expenses
    expenses = relationship("Expense", back_populates="user")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="expenses")