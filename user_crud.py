from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select, desc
import models, schemas
import logging
# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,  # or DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    stmt = (
        select(models.User)
        .order_by(desc(models.User.updated_at))
    )
    return db.execute(stmt).scalars().all()