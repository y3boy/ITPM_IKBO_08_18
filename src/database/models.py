from sqlalchemy import Column, ForeignKey, Integer, String, Text, Date, Boolean

from src.database.database import DataBase


class User(DataBase):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstname = Column(String(45))
    surname = Column(String(45))
    patronimyc = Column(String(45))
    phone = Column(String(12))
    email = Column(String(45))
    password = Column(String(45))
    username = Column(String(45))
    client = relationship("Client", back_populates="parent")
    walker = relationship("Walker", back_populates="parent")
    

class Client(DataBase):
    __tablename__ = 'client'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    counter = Column(Integer)
    user = relationship("User" , back_populates="children")

class Walker(DataBase):
    __tablename__ = 'walker'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    rating = Column(Float(precision=10,scale=2))
    counter = Column(Integer)
    user = relationship("User" , back_populates="children")
