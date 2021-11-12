from sqlalchemy.orm import Session

from src.schemas.order import OrderBase, OrderEdit
from src.database.models import Order
from src.database.crud import client as crud_client
from src.database.crud import walker as crud_walker
from src.database.crud import user as crud_user


def create_order_for_client(user_id: int, order_arg: OrderBase, session: Session):
    order = Order(**order_arg.dict())
    order.client_id = user_id
    client = crud_client.get_client(order.client_id, session)
    walker = crud_walker.get_walker(order.walker_id, session)

    if client and walker:
        price = order.numbers_of_hours * walker.price_per_hour
        if client.counter < 5:
            price *= 1.05
        elif client.counter < 10:
            price *= 1.04
        elif client.counter < 15:
            price *= 1.03
        elif client.counter < 20:
            price *= 1.02
        else:
            price *= 1.01
        order.price = price

        session.add(order)
        session.commit()
        return order


def get_order(order_id: int, session: Session):
    return session.query(Order).get(order_id)


def get_all_user_order_for_client(user_id: int, session: Session):
    user = crud_user.get_user(user_id, session)
    if user.client_id:
        return session.query(Order).filter(Order.client_id == user_id).all()
    return 'Ты лох'


def get_all_user_order_for_walker(user_id: int, session: Session):
    user = crud_user.get_user(user_id, session)
    if user.walker_id:
        return session.query(Order).filter(Order.walker_id == user_id).all()


def set_order(order_id: int, order_arg: OrderEdit, session: Session):
    order = session.query(Order).get(order_id)
    if order:
        if order_arg.walker_took_order:
            order.walker_took_order = order_arg.walker_took_order
        if order_arg.client_confirmed_execution:
            order.client_confirmed_execution = order_arg.client_confirmed_execution
        if order_arg.paid:
            order.paid = order_arg.paid
        session.add(order)
        session.commit()
        return order
    return None


def delete_order(order_id, session: Session):
    order = session.query(Order).get(order_id)
    session.delete(order)
    session.commit()
    return order