from sqlalchemy.orm import Session

from app.schemas import *
from app.models import *


def get_user_by_name(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()