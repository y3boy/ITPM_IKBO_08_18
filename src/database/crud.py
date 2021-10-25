from src.database.models import User, Client, Walker
from src.database.database import SessionLocal


def __user_create(username, password, fullname=None, phone=None, email=None):
    return User(
        username=username,
        password=password,
        fullname=fullname,
        phone=phone,
        email=email
    )


def client_create(username, password, fullname=None, phone=None, email=None):
    session = SessionLocal()

    client = Client()
    session.add(client)
    session.commit()

    user = __user_create(username, password, fullname, phone, email)
    user.client_id = client.id
    session.add(user)
    session.commit()
    return user


def walker_create(username, password, fullname=None, phone=None, email=None):
    session = SessionLocal()

    walker = Walker()
    session.add(walker)
    session.commit()

    user = __user_create(username, password, fullname, phone, email)
    user.walker_id = walker.id
    session.add(user)
    session.commit()
    return user


def user_read(user_id):
    session = SessionLocal()
    return session.query(User).get(user_id)


def user_read_by_username(username):
    session = SessionLocal()
    return session.query(User).filter(User.username == username).first()


def user_update(user_id, password=None, fullname=None, phone=None, email=None):
    session = SessionLocal()
    user = session.query(User).get(user_id)
    if password:
        user.password = password
    if fullname:
        user.fullname = fullname
    if phone:
        user.phone = phone
    if email:
        user.email = email
    session.add(user)
    session.commit()
    return user


def user_delete(user_id):
    session = SessionLocal()
    user = session.query(User).get(user_id)
    session.delete(user)
    session.commit()
    return user
