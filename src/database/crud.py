# Реализовать добавление удаление для Client и Walker'a
# Не забывайте что у нас связаны таблицы сверху с User'ом
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Client, Walker
from database import SessionLocal


def client_add(**kwargs):
    s = SessionLocal()
    client = Client()
    s.add(client)
    s.commit()
    user = User(
        firstname=kwargs['firstname'],
        surname=kwargs['surname'],
        patronimyc=kwargs['patronimyc'],
        phone=kwargs['phone'],
        email=kwargs['email'],
        password=kwargs['password'],
        username=kwargs['username'],
        client_id=client.id,
    )
    s.add(user)
    s.commit()


def walker_add(**kwargs):
    s = SessionLocal()
    walker = Walker()
    s.add(walker)
    s.commit()
    user = User(
        firstname=kwargs['firstname'],
        surname=kwargs['surname'],
        patronimyc=kwargs['patronimyc'],
        phone=kwargs['phone'],
        email=kwargs['email'],
        password=kwargs['password'],
        username=kwargs['username'],
        walker_id=walker.id,
    )
    s.add(user)
    s.commit()


def user_delete(user_id):
    s = SessionLocal()
    s.delete(s.query(User).filter(User.name == user_id))
    s.commit()