from fastapi import FastAPI
from db import engine, Base
from routers import expenses, users
import logging


# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Tracking API", description="A simple Expense Tracking API")

# Include routers
app.include_router(expenses.router)
app.include_router(users.router)

# Run with: uvicorn main:app --reload
# Grab the root logger used by uvicorn
logger = logging.getLogger("uvicorn")

# Optional: Set level to DEBUG to see everything
logger.setLevel(logging.INFO)
