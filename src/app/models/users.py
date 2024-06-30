from sqlalchemy import Column, Integer, String

from src.config.database.base import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
