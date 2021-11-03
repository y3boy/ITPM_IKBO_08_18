from datetime import datetime, timedelta
import random
import string
import hashlib

from sqlalchemy.orm import Session

import src.database.models as models
from src.schemas.user import User as class_user


def client_create(user_arg: class_user, session: Session):
    client = models.Client()
    session.add(client)
    session.commit()
    user = models.User(**user_arg.dict())
    user.client_id = client.id
    session.add(user)
    session.commit()
    return user


def walker_create(user: class_user, session: Session):
    walker = models.Walker()
    session.add(walker)
    session.commit()

    user = models.User(user)
    user.walker_id = walker.id
    session.add(user)
    session.commit()
    return user


def user_read(user_id, session: Session):
    return session.query(models.User).get(user_id)


def user_read_by_username(session: Session, username):
    return session.query(models.User).filter(models.User.username == username).first()


# FIXME: сделать не латентным)))0)
def user_update(user: class_user, session: Session):
    user = session.query(models.User).get(models.User.id)
    if user.password:
        user.password = user.password
    if user.fullname:
        user.fullname = user.fullname
    if user.phone:
        user.phone = user.phone
    if user.email:
        user.email = user.email
    session.add(user)
    session.commit()
    return user


def user_delete(user_id, session: Session):
    user = session.query(models.User).get(user_id)
    session.delete(user)
    session.commit()
    return user


def create_user_token(user_id: int, session: Session):
    token = models.Token(expires=datetime.now() + timedelta(weeks=2), user_id=user_id)
    session.add(token)
    return token


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = "".join(random.choice(string.ascii_letters) for _ in range(12))
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed
