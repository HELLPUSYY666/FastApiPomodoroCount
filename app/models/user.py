from typing import Optional

from database import Base
from sqlalchemy.orm import Mapped
from sqlalchemy import Column, Integer, String


class UserProfile(Base):
    __tablename__ = 'UserProfile'
    id: Mapped[int] = Column(Integer, primary_key=True)
    username: Mapped[str] = Column(String, nullable=False)
    password: Mapped[str] = Column(String, nullable=True)
    google_access_token: Mapped[Optional[str]] = Column(String, nullable=True)
    yandex_access_token: Mapped[Optional[str]] = Column(String, nullable=True)
    email: Mapped[Optional[str]] = Column(String, nullable=True)
    name: Mapped[Optional[str]] = Column(String, nullable=True)
