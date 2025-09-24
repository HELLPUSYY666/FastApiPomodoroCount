from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.database.database import Base


class Task(Base):
    __tablename__ = "Task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    pomodoro_count = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey("Category.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("UserProfile.id"), nullable=False)
    category = relationship("Category")


class Category(Base):
    __tablename__ = "Category"
    id: Mapped[int] = Column(Integer, primary_key=True)
    type: Mapped[str] = Column(String, nullable=True)
    name: Mapped[str] = Column(String, nullable=False)
