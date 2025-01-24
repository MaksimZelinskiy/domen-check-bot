import logging
from datetime import date

from sqlalchemy import Date, cast, func, insert, select, update

from database.models.users import User

from .base import BaseRepo

logger = logging.getLogger(__name__)


class UsersRepo(BaseRepo):

    async def get_user_by_id(self, user_id: int) -> str | None:
        query = select(User.user_ip).where(User.user_id == user_id)
        res = await self.session.execute(query)
        return res.scalars().one_or_none()

    async def create_user(
        self,
        user_id: int,
        username: str,
        name: str,
        language: str,
        utm: str
    ):
        logger.info(f"Creating user {user_id} with refferer id {statapp_code}")
        query = insert(User).values(
            user_id=user_id,
            username=username,
            name=name,
            user_ip=user_ip,
            utm=utm,
            lang=language,
        )
        await self.session.execute(query)

