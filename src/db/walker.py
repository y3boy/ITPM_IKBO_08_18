from sqlalchemy import Column, Integer, ForeignKey, Float, Text
from src.db.database import DataBase
from src.db.station import Station


class Walker(DataBase):
    __tablename__ = 'walker'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    rating = Column(Float(precision=10), default=0, nullable=False)
    counter = Column(Integer, default=0, nullable=False)
    price_per_hour = Column(Integer, nullable=False)
    min_dog_size_in_kg = Column(Integer, nullable=True)
    max_dog_size_in_kg = Column(Integer, nullable=True)
    min_dog_age_in_years = Column(Integer, nullable=True)
    max_dog_age_in_years = Column(Integer, nullable=True)
    schedule = Column(Text, nullable=True)
    about_walker = Column(Text, nullable=True)


class WalkerStation(DataBase):
    __tablename__ = 'walker_station'
    walker_id = Column(Integer, ForeignKey(Walker.id), primary_key=True)
    station_id = Column(Integer, ForeignKey(Station.id), primary_key=True)
