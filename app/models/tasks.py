import datetime as dt
import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship

from app.infrastructure.database.database import Base


class TaskPriorityEnum(enum.Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatusEnum(enum.Enum):
    COMPLETE = "complete"
    PENDING = "pending"
    NOT_START = "not_start"


class Task(Base):
    __tablename__ = "Task"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False)

    status: Mapped[TaskStatusEnum] = Column(
        Enum(
            TaskStatusEnum,
            name="task_status_enum",
            create_type=True,
        ),
        nullable=False,
        default=TaskStatusEnum.NOT_START,
    )

    priority: Mapped[TaskPriorityEnum] = Column(
        Enum(TaskPriorityEnum, name="task_priority_enum", create_type=True),
        nullable=False,
        default=TaskPriorityEnum.MEDIUM,
    )
    description: Mapped[str] = Column(Text, nullable=True)
    deadline: Mapped[dt.datetime] = Column(
        DateTime, nullable=False, default=dt.datetime.today
    )
    progress: Mapped[float] = Column(Float, nullable=False, default=0.0)

    category_id: Mapped[int] = Column(
        Integer, ForeignKey("Category.id"), nullable=False
    )
    user_id: Mapped[int] = Column(Integer, ForeignKey("UserProfile.id"), nullable=False)

    category = relationship("Category")


class Category(Base):
    __tablename__ = "Category"

    id: Mapped[int] = Column(Integer, primary_key=True)
    type: Mapped[str] = Column(String, nullable=True)
    name: Mapped[str] = Column(String, nullable=False)


class WeekTaskPlan(Base):
    __tablename__ = "WeekTaskPlan"

    id: Mapped[int] = Column(Integer, primary_key=True)
    task_id: Mapped[int] = Column(Integer, ForeignKey("Task.id"), nullable=False)
    day: Mapped[int] = Column(Integer, nullable=False)

    task = relationship("Task")
