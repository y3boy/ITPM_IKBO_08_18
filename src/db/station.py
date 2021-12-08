from sqlalchemy import Column, Integer, String
from src.db.database import DataBase


class Station(DataBase):
    __tablename__ = 'station'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    line_name = Column(String, nullable=False)
    line_hex_color = Column(String, nullable=False)
    station_name = Column(String, nullable=False)
