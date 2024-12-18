from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"  # наименование таблицы данных

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)  # логин
    firstname = Column(String)  # имя
    lastname = Column(String)  # фамилия
    age = Column(Integer)  # возраст
    slug = Column(String, unique=True, index=True)

    tasks = relationship("Task", back_populates="user")
