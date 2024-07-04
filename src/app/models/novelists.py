from sqlalchemy import Column, Integer, String

from src.config.database.base import Base


class Novelist(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
