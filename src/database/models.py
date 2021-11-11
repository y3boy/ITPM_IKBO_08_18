from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, Boolean, Float, text, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from src.database.database import DataBase


class UserBase(DataBase):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(45), nullable=False)
    hashed_password = Column(String(), nullable=False)
    fullname = Column(String(135))
    phone = Column(String(12))
    email = Column(String(45))
    client_id = Column(Integer, ForeignKey("client.id"))  # One to One
    client = relationship("Client", backref=backref("user", uselist=False, cascade="all,delete"))
    walker_id = Column(Integer, ForeignKey("walker.id"))  # One to One
    walker = relationship("Walker", backref=backref("user", uselist=False, cascade="all,delete"))
    animal = relationship("Dog")


class TokenBase(DataBase):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    token = Column(UUID(as_uuid=True),
                   default=uuid4,
                   unique=True,
                   nullable=False,
                   index=True)
    expires = Column(DateTime())
    user_id = Column(Integer, ForeignKey("user.id"))
    

class User(UserBase):
    token: TokenBase = {}


class Client(DataBase):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    counter = Column(Integer, default=0, nullable=False)


class Walker(DataBase):
    __tablename__ = 'walker'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rating = Column(Float(precision=10), default=0)
    counter = Column(Integer, nullable=False)

    # For search filter
    region_code = Column(Integer, nullable=False)
    price_per_hour = Column(Integer, nullable=False)
    practice_in_year = Column(Integer, nullable=False)
    min_dog_size_in_kg = Column(Integer)
    max_dog_size_in_kg = Column(Integer)
    min_dog_age_in_years = Column(Integer)
    max_dog_age_in_years = Column(Integer)
    # Walker dogs via user table

    schedule = Column(Text)
    about_walker = Column(Text)


class Dog(DataBase):
    __tablename__ = 'Dog'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    breed = Column(String(100), nullable=False)
    nickname = Column(String(100), nullable=False)

