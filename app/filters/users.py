from typing import Union

from aiogram import types
from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from database.repo.requests import RequestsRepo

class IsPrivate(BaseFilter):
    async def __call__(self, event: Union[Message, CallbackQuery]) -> bool:
        if isinstance(event, CallbackQuery):
            return event.message.chat.type == "private"
        return event.chat.type == "private"
    
class IsAdmin(BaseFilter):
    async def __call__(self, event: Union[Message, CallbackQuery], repo: RequestsRepo) -> bool:
        user_id = event.from_user.id
        user = await repo.users.get_user_by_id(user_id)
        if user.role_id == 1:
            return True
        
        await event.answer("У вас нет доступа к этому функционалу")
        return False

class IsUser(BaseFilter):
    async def __call__(self, event: Union[Message, CallbackQuery], repo: RequestsRepo) -> bool:
        user_id = event.from_user.id
        user = await repo.users.get_user_by_id(user_id)
        if user.role_id == 2:
            return True
        
        await event.answer("У вас нет доступа к этому функционалу")
        return False