from typing import Optional

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.database import Base


class UserProfile(Base):
    __tablename__ = "UserProfile"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    google_access_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    yandex_access_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)

    prompts: Mapped[list["UsersPrompts"]] = relationship(back_populates="user")


class UsersPrompts(Base):
    __tablename__ = "UsersPrompts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("UserProfile.id"), nullable=False)
    currently_use: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["UserProfile"] = relationship(back_populates="prompts")
