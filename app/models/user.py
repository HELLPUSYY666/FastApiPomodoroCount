from typing import Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped

from app.infrastructure.database.database import Base


class UserProfile(Base):
    __tablename__ = "UserProfile"
    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String, nullable=False)
    password: Mapped[str] = Column(String, nullable=True)
    google_access_token: Mapped[Optional[str]] = Column(String, nullable=True)
    yandex_access_token: Mapped[Optional[str]] = Column(String, nullable=True)
    email: Mapped[Optional[str]] = Column(String, nullable=True)
    name: Mapped[Optional[str]] = Column(String, nullable=True)
