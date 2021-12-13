from sqlalchemy import Column, Integer, String, LargeBinary
from src.db.database import DataBase


class Avatar(DataBase):
    __tablename__ = 'avatar'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    file = Column(LargeBinary, nullable=False)
