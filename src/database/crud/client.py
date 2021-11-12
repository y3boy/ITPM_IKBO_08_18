from sqlalchemy.orm import Session

from src.database.models import UserBase, Client
from src.database.crud.user import create_user_obj, get_user, delete_user


def create_client(user_arg: UserBase, client_arg: Client, session: Session):
    client = Client(**client_arg.dict())
    session.add(client)
    session.commit()

    user = create_user_obj(user_arg)
    user.client_id = client.id
    session.add(user)
    session.commit()
    return user


def get_client(user_id: int, session: Session):
    user = get_user(user_id, session)
    if user:
        if user.client_id:
            return session.query(Client).get(user.client_id)


def set_client(user_id: int, client_arg: Client, session: Session):
    user = session.query(UserBase).get(user_id)
    if user:
        client = session.query(Client).get(user.walker_id)
        if client:
            if client_arg.counter:
                client.counter = client_arg.counter
            session.add(client)
            session.commit()
            return client
    return None