from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.config.database.base import Base


class Novelist(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)

    books = relationship("Book", back_populates="novelist")
