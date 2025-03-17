from fastapi import FastAPI
from .db import engine, Base
from .routers import expenses

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracking API", description="A simple Expense Tracking API")

# Include routers
app.include_router(expenses.router)

# Run with: uvicorn main:app --reload
