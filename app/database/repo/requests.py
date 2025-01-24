from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from database.repo.users import UsersRepo
from database.repo.todos import TodosRepo
from database.repo.roles import RolesRepo

from data.config import STANDARD_ROLES_IDS

@dataclass
class RequestsRepo:
    session: AsyncSession

    @property
    def users(self):
        return UsersRepo(self.session)
    
    @property
    def todos(self):
        return TodosRepo(self.session)
    
    @property
    def roles(self):
        return RolesRepo(self.session)
    
    @property
    def standard_roles(self):
        return STANDARD_ROLES_IDS

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def flush(self):
        await self.session.flush()
