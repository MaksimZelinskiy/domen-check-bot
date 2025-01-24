from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.filters.state import StateFilter

from filters import IsPrivate
from loader import bot
from data import main
from database.repo.requests import RequestsRepo

router = Router()

@router.message(CommandStart(), IsPrivate(), StateFilter("*"))
async def command_start(message: Message, repo: RequestsRepo):    
    args = message.text[7:]

    date_reg = str(datetime.now())[:16]
    username = message.from_user.username
    locale = message.from_user.language_code
    name = message.from_user.first_name.replace("'", "")
    
    user_exists = await repo.users.get_user_by_id(message.from_user.id)
    if not user_exists:

        await repo.users.create_user(
            user_id=message.from_user.id,
            utm=args,
            name=name,
            date_reg=date_reg,
            username=username,
            lang=locale,
            role_id=3 # Гость
        )

    role = await repo.roles.get_role_by_id(user_exists.role_id)
    await message.answer(f"Привет, {user_exists.name}!\n\nВаша роль: {role.name}")

    try:
        await message.delete()
    except Exception:
        pass
    
    return True

