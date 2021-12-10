import datetime

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.order import OrderCreate, OrderUpdate

from src.db.order import Order
from src.db.user import User
from src.db.dog import Dog
from src.repositories.walker import get_walker_by_id
from src.repositories.user import get_user_by_id


def create_order(o: OrderCreate, client_user_id: int, walker_user_id: int, dog_id: int, s: Session):
    walker = get_walker_by_id(get_user_by_id(walker_user_id, s).walker_id, s)
    client = get_user_by_id(client_user_id, s)
    order = Order()

    order.datetime_of_creation = datetime.datetime.utcnow()
    order.datetime_of_walking = o.datetime_of_walking
    order.numbers_of_hours = o.numbers_of_hours
    order.price_without_commission = walker.price_per_hour * o.numbers_of_hours
    count = client.client_order_count
    if count > 100:
        count = 100
    order.commission = order.price_without_commission * ((15 - (count // 10)) / 100)
    order.description = o.description

    order.client_id = client_user_id
    order.walker_id = walker_user_id
    order.dog_id = dog_id

    s.add(order)
    try:
        s.commit()
        return order
    except IntegrityError:
        return None


def get_order_by_id(id: int, s: Session):
    return s.query(Order).filter(Order.id == id).first()


def get_all_client_order(client_user_id: int, s: Session):
    return s.query(Order, User, Dog).filter(Order.client_id == client_user_id,
                                            User.id == Order.walker_id,
                                            Dog.id == Order.dog_id).all()


def get_all_walker_order(walker_user_id: int, s: Session):
    return s.query(Order, User, Dog).filter(Order.walker_id == walker_user_id,
                                            User.id == Order.client_id,
                                            Dog.id == Order.dog_id).all()


def edit_order(o: OrderUpdate, id: int, user_id: int, s: Session):
    order = s.query(Order).filter(Order.id == id).first()
    if order.walker_id == user_id or order.client_id == user_id:
        order.rating = o.rating
        order.review = o.review
        order.walker_took_order = o.walker_took_order
        order.client_confirmed_execution = o.client_confirmed_execution
        order.paid = o.paid

        s.add(order)
        s.commit()
        return order


def get_all_rating_and_reviews_walker(walker_user_id: int, s: Session):
    return s.query(Order.rating, Order.review, Order.client_id).filter(Order.walker_id == walker_user_id).all()
