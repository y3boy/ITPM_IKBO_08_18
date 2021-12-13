from sqlalchemy import Column, Integer, Float, Text, String
from sqlalchemy.dialects.postgresql import ARRAY
from src.db.database import DataBase


class Walker(DataBase):
    __tablename__ = 'walker'
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    counter = Column(Integer, default=0, nullable=False)
    price_per_hour = Column(Integer, nullable=False)
    stations = Column(ARRAY(String), nullable=False)
    min_dog_size_in_kg = Column(Integer, nullable=True)
    max_dog_size_in_kg = Column(Integer, nullable=True)
    min_dog_age_in_years = Column(Integer, nullable=True)
    max_dog_age_in_years = Column(Integer, nullable=True)
    schedule = Column(Text, nullable=True)
    about_walker = Column(Text, nullable=True)
