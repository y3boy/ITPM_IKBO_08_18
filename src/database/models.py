from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, Boolean

from src.database.database import DataBase


class User(DataBase):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
