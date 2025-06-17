from datetime import datetime

from pydantic import BaseModel

class ExpenseBase(BaseModel):
    description: str = ""
    amount: float = 0.0
    type: str

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    pass

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True