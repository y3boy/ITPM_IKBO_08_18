from sqlalchemy import Column, Integer, String, ForeignKey
from src.db.walker import Walker
from src.db.avatar import Avatar
from src.db.database import DataBase


class User(DataBase):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    client_order_count = Column(Integer, nullable=False, default=0)

    walker_id = Column(Integer, ForeignKey(Walker.id), nullable=True, unique=True)
    avatar_id = Column(Integer, ForeignKey(Avatar.id), nullable=True)

