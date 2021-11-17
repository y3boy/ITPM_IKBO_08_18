import random
import string
import hashlib
from sqlalchemy.orm import Session

from src.database.models import UserBase
from src.schemas import user as pd_user


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = "".join(random.choice(string.ascii_letters) for _ in range(12))
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


def create_user_obj(user_arg: pd_user.UserBase):
    salt = "".join(random.choice(string.ascii_letters) for _ in range(12))
    hashed_password = hash_password(salt=salt, password=user_arg.hashed_password)
    user_arg.hashed_password = f"{salt}${hashed_password}"
    return UserBase(**user_arg.dict())


def create_user_token(user_id: int, session: Session, Authorize):
    access_token = Authorize.create_access_token(subject=user_id)
    refresh_token = Authorize.create_refresh_token(subject=user_id)
    return {"access_token": access_token, "refresh_token": refresh_token}


def get_user(user_id: int, session: Session):
    return session.query(UserBase).get(user_id)


def get_user_by_username(session: Session, username):
    return session.query(UserBase).filter(UserBase.username == username).first()


def set_user(user_id: int, user_arg: pd_user.UserEdit, session: Session):
    user = session.query(UserBase).get(user_id)
    salt = "".join(random.choice(string.ascii_letters) for _ in range(12))
    hashed_password = hash_password(salt=salt, password=user_arg.hashed_password)
    if user:
        if user_arg.username:
            user.username = user_arg.username
        if user_arg.hashed_password:
            user.hashed_password = f"{salt}${hashed_password}"
        if user_arg.fullname:
            user.fullname = user_arg.fullname
        if user_arg.phone:
            user.phone = user_arg.phone
        if user_arg.email:
            user.email = user_arg.email
        if user_arg.avatar_url:
            user.avatar_url = user_arg.avatar_url
        session.add(user)
        session.commit()
        return user
    return None


def delete_user(user_id, session: Session):
    user = session.query(UserBase).get(user_id)
    session.delete(user)
    session.commit()
    return user

