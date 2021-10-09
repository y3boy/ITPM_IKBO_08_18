from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.app.dependencies import get_settings


settings = get_settings()

SQLALCHEMY_DATABASE_URL = settings.postgres_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

DataBase = declarative_base()
