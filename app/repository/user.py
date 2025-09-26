from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models import UserProfile
from app.schema import UserCreateSchema


@dataclass
class UserRepository:
    session_maker: async_sessionmaker[AsyncSession]

    async def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)
        async with self.session_maker() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def create_user(self, user: UserCreateSchema) -> UserProfile:
        query = (
            insert(UserProfile).values(**user.model_dump()).returning(UserProfile.id)
        )
        async with self.session_maker() as session:
            result = await session.execute(query)
            user_id = result.scalar_one()
            await session.commit()
            return await self.get_user(user_id, session=session)

    async def get_user(
        self, user_id: int, session: AsyncSession | None = None
    ) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        if session is None:
            async with self.session_maker() as session:
                result = await session.execute(query)
                return result.scalar_one_or_none()
        else:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.session_maker() as session:
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def update_user(self, user: UserProfile):
        async with self.session_maker() as session:
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user
