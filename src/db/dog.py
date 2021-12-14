from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from src.db.user import User
from src.db.avatar import Avatar
from src.db.database import DataBase


class Dog(DataBase):
    __tablename__ = 'dog'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    breed = Column(String(100), nullable=False)
    nickname = Column(String(100), nullable=False)
    size_in_kg = Column(Integer, nullable=True)
    date_of_birth = Column(DateTime, nullable=True)

    user_id = Column(Integer, ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    avatar_id = Column(Integer, ForeignKey(Avatar.id, ondelete='CASCADE'), nullable=True)
