from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, Boolean, Float, text, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4

from src.database.database import DataBase


class User(DataBase):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(45))
    hashed_password = Column(String())
    fullname = Column(String(135))
    phone = Column(String(12))
    email = Column(String(45))
    client_id = Column(Integer, ForeignKey("client.id"))
    client = relationship("Client", backref=backref("user", uselist=False, cascade="all,delete"))
    walker_id = Column(Integer, ForeignKey("walker.id"))
    walker = relationship("Walker", backref=backref("user", uselist=False, cascade="all,delete"))
    

class Client(DataBase):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    counter = Column(Integer, default=0)


class Walker(DataBase):
    __tablename__ = 'walker'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rating = Column(Float(precision=10), default=0)
    counter = Column(Integer)


class Token(DataBase):
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    token = Column(UUID(as_uuid=False),
                   default=uuid4,
                   unique=True,
                   nullable=False,
                   index=True)
    expires = Column(DateTime())
    user_id = Column(Integer, ForeignKey("user.id"))
