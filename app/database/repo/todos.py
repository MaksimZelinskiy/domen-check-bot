import logging
from datetime import date

from sqlalchemy import Date, cast, func, insert, select, update, delete

from database.models.todo import Todo

from .base import BaseRepo

logger = logging.getLogger(__name__)


class TodosRepo(BaseRepo):

    async def get_todo_by_id(self, todo_id: int) -> Todo | None:
        query = select(Todo).where(Todo.id == todo_id)
        res = await self.session.execute(query)
        return res.scalars().one_or_none()
    
    async def get_user_todo_by_id(self, todo_id: int, user_id: int) -> Todo | None:
        query = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        res = await self.session.execute(query)
        return res.scalars().one_or_none()
    
    async def update_todo(self, todo_id: int, **kwargs):
        query = update(Todo).where(Todo.id == todo_id).values(**kwargs)
        await self.session.execute(query)

    async def create_todo(
        self,
        user_id: int,
        name: str,
    ):
        query = insert(Todo).values(
            user_id=user_id,
            name=name
        )
        await self.session.execute(query)
        await self.session.commit()

    async def get_todos(self, user_id: int):
        query = select(Todo).where(Todo.user_id == user_id)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def delete_todo(self, todo_id: int):
        query = delete(Todo).where(Todo.id == todo_id)
        await self.session.execute(query)
        await self.session.commit()
    