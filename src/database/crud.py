from datetime import datetime, timedelta
import random
import string
import hashlib

from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.database.models import UserBase, Client, Walker, TokenBase, Dog


def __create_user(user_arg: UserBase):
    salt = "".join(random.choice(string.ascii_letters) for _ in range(12))
    hashed_password = hash_password(salt=salt, password=user_arg.hashed_password)
    user_arg.hashed_password = f"{salt}${hashed_password}"
    return UserBase(**user_arg.dict())


def client_create(user_arg: UserBase, session: Session):
    client = Client()
    session.add(client)
    session.commit()

    user = __create_user(user_arg)
    user.client_id = client.id
    session.add(user)
    session.commit()
    return user


def walker_create(user_arg: UserBase, walker_arg: Walker, session: Session):
    walker = Walker(**walker_arg.dict())
    session.add(walker)
    session.commit()

    user = __create_user(user_arg)
    user.walker_id = walker.id
    session.add(user)
    session.commit()
    return user


def user_read(user_id: int, session: Session):
    return session.query(UserBase).get(user_id)


def walker_read(user_id: int, session: Session):
    user = user_read(user_id, session)
    if user:
        if user.walker_id:
            return session.query(Walker).get(user.walker_id)


def client_read(user_id: int, session: Session):
    user = user_read(user_id, session)
    if user:
        if user.client_id:
            return session.query(Client).get(user.client_id)


def user_read_by_username(session: Session, username):
    return session.query(UserBase).filter(UserBase.username == username).first()


# FIXME: сделать не латентным)))0)
def user_update(user_id: int, user_arg: UserBase, session: Session):
    user = session.query(UserBase).get(user_id)
    salt = "".join(random.choice(string.ascii_letters) for _ in range(12))
    hashed_password = hash_password(salt=salt, password=user_arg.hashed_password)
    if user:
        if user.username:
            user.username = user_arg.username
        if user.hashed_password:
            user.hashed_password = f"{salt}${hashed_password}"
        if user.fullname:
            user.fullname = user_arg.fullname
        if user.phone:
            user.phone = user_arg.phone
        if user.email:
            user.email = user_arg.email
        session.add(user)
        session.commit()
        return user
    return None


def user_delete(user_id, session: Session):
    user = session.query(UserBase).get(user_id)
    session.delete(user)
    session.commit()
    return user


def create_user_token(user_id: int, session: Session, Authorize):
    access_token = Authorize.create_access_token(subject=user_id)
    refresh_token = Authorize.create_refresh_token(subject=user_id)
    return {"access_token": access_token, "refresh_token": refresh_token}


def hash_password(password: str, salt: str = None):
    if salt is None:
        salt = "".join(random.choice(string.ascii_letters) for _ in range(12))
    enc = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return enc.hex()


def validate_password(password: str, hashed_password: str):
    salt, hashed = hashed_password.split("$")
    return hash_password(password, salt) == hashed


def create_dog(user_id: int, dog_arg: Dog, session: Session):
    dog = Dog(user_id=user_id, **dog_arg.dict())
    session.add(dog)
    session.commit()
    return dog


def dog_read(dog_id: int, session: Session):
    return session.query(Dog).get(dog_id)


def get_all_user_dog(user_id: int, session: Session):
    return session.query(Dog).filter(Dog.user_id == user_id).all()


def dog_delete(dog_id, session: Session):
    dog = session.query(Dog).get(dog_id)
    session.delete(dog)
    session.commit()
    return dog
