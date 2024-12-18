from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.models import *


class Task(Base):
    __tablename__ = "tasks"  # наименование таблицы данных
    __table_args__ = {"keep_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)  # наименование задачи
    content = Column(String)  # описание задачи
    priority = Column(Integer, default=0)  # приоритет (очередь)
    completed = Column(Boolean, default=False)  # завершена ли задача
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # связь с таблицей users
    slug = Column(String, unique=True, index=True)

    user = relationship("User", back_populates="tasks")
