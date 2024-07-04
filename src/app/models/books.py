from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.config.database.base import Base


class Book(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    year = Column(Integer)
    novelist_id = Column(Integer, ForeignKey("novelist.id"))

    novelist = relationship("Novelist", back_populates="books")
