from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.dog import DogCreate, DogUpdate

from src.db.avatar import Avatar


def create_avatar(file, s: Session):
    avatar = Avatar()
    avatar.file = file

    s.add(avatar)
    s.commit()
    return avatar


def get_avatar(id: int, s: Session):
    return s.query(Avatar).filter(Avatar.id == id).first()


def delete_avatar(id: int, s: Session):
    avatar = s.query(Avatar).filter(Avatar.id == id).first()
    s.delete(avatar)
    s.commit()
    return avatar

