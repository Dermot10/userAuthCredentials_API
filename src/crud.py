from sqlalchemy.orm import Session
from . import models,  schemas
from .schemas import UserCreate
from .utils import get_password_hash


def get_user(db: Session, username: str):
    try:
        return db.query(models.Credentials).filter(models.Credentials.username == username).first()
    except:
        return None


def get_user_by_id(db: Session, id: int):
    return db.query(models.Credentials).filter(models.Credentials.id == id).first()


def create_user(db: Session, user: UserCreate):
    db_user = models.Credentials(
        username=user.username, email=user.email, fullname=user.fullname, password=get_password_hash(
            user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user_to_delete = db.query(models.Credentials).filter(
        models.Credentials.id == user_id).first()
    try:
        if not db_user_to_delete:
            return "album ID does not exist"
    except:
        db.delete(db_user_to_delete)
        db.commit()
        return {"User Deleted": True}
