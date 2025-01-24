import logging
from datetime import date

from sqlalchemy import Date, cast, func, insert, select, update, delete

from database.models.users import User

from .base import BaseRepo

logger = logging.getLogger(__name__)


class UsersRepo(BaseRepo):

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.user_id == user_id)
        res = await self.session.execute(query)
        return res.scalars().one_or_none()
    
    async def update_user(self, user_id: int, **kwargs):
        query = update(User).where(User.user_id == user_id).values(kwargs)
        await self.session.execute(query)

    async def create_user(
        self,
        user_id: int,
        username: str,
        name: str,
        language: str,
        utm: str,
        role_id: int,
    ):
        query = insert(User).values(
            user_id=user_id,
            username=username,
            name=name,
            utm=utm,
            lang=language,
            role_id=role_id
        )
        
        await self.session.execute(query)
        await self.session.commit()

    async def delete_user(self, user_id: int) -> bool:
        query = delete(User).where(User.user_id == user_id)
        
        await self.session.execute(query)
        await self.session.commit()

        return True

    async def get_all_users(self) -> list[User]:
        query = select(User)
        res = await self.session.execute(query)
        return res.scalars().all()
