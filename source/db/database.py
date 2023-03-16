from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from config import settings


engine = create_engine(settings.get_database_url())
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
