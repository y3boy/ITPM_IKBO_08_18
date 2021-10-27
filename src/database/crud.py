from src.database.models import User, Client, Walker
from sqlalchemy.orm import Session


def __user_create(user: User):
    return User(user)


def user_authorization(user: User, session: Session):
    return "Fake token"


def client_create(session: Session, user: User):
    client = Client()
    session.add(client)
    session.commit()

    user = __user_create(user)
    user.client_id = client.id
    session.add(user)
    session.commit()
    return user


def walker_create(session: Session, user: User):
    walker = Walker()
    session.add(walker)
    session.commit()

    user = __user_create(user)
    user.walker_id = walker.id
    session.add(user)
    session.commit()
    return user


def user_read(session: Session, user_id):
    return session.query(User).get(user_id)


def user_read_by_username(session: Session, username):
    return session.query(User).filter(User.username == username).first()

# FIXME: сделать не латентным)))0)
def user_update(session: Session, user: User):
    user = session.query(User).get(user.id)
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


def user_delete(session: Session, user_id):
    user = session.query(User).get(user_id)
    session.delete(user)
    session.commit()
    return user
