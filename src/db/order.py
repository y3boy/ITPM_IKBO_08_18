from sqlalchemy import Column, Integer, ForeignKey, Float, Text, DateTime, Boolean
from src.db.user import User
from src.db.database import DataBase


class Order(DataBase):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    datetime_of_creation = Column(DateTime, nullable=False)
    datetime_of_walking = Column(DateTime, nullable=False)
    numbers_of_hours = Column(Integer, nullable=False)
    price_without_commission = Column(Integer, nullable=False)
    commission = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)

    rating = Column(Float, nullable=True)
    review = Column(Text, nullable=True)

    walker_took_order = Column(Boolean, nullable=True, default=None)
    client_confirmed_execution = Column(Boolean, nullable=True, default=None)
    paid = Column(Boolean, nullable=True, default=None)

    client_id = Column(Integer, ForeignKey(User.id), nullable=False)
    walker_id = Column(Integer, ForeignKey(User.id), nullable=False)
