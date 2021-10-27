from src.database.models import User, Client, Walker
from sqlalchemy.orm import Session


def __user_create(user: User):
    return User(user)


def user_authorization(user: str, session: Session):
    return "Fake token"


def client_create(user: User, session: Session):
    client = Client()
    session.add(client)
    session.commit()

    user = __user_create(user)
    user.client_id = client.id
    session.add(user)
    session.commit()
    return user


def walker_create(user: User, session: Session):
    walker = Walker()
    session.add(walker)
    session.commit()

    user = __user_create(user)
    user.walker_id = walker.id
    session.add(user)
    session.commit()
    return user


def user_read(user_id, session: Session):
    return session.query(User).get(user_id)


def user_read_by_username(session: Session, username):
    return session.query(User).filter(User.username == username).first()

# FIXME: сделать не латентным)))0)
def user_update(user: User, session: Session):
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


def user_delete(user_id, session: Session):
    user = session.query(User).get(user_id)
    session.delete(user)
    session.commit()
    return user
