
import logging
from datetime import date

from sqlalchemy import Date, cast, func, insert, select, update

from database.models.roles import Role

from .base import BaseRepo

logger = logging.getLogger(__name__)


class RolesRepo(BaseRepo):

    async def get_role_by_id(self, role_id: int) -> Role | None:
        query = select(Role).where(Role.role_id == role_id)
        res = await self.session.execute(query)
        return res.scalars().one_or_none()
    
    async def create_role(
        self,
        name: str,
    ):
        query = insert(Role).values(
            name=name
        )
        await self.session.execute(query)
        await self.session.commit()

    async def get_all_roles(self) -> list[Role]:
        query = select(Role).order_by(Role.role_id)
        res = await self.session.execute(query)
        return res.scalars().all()

