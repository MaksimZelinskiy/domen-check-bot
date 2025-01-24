import asyncio
from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext

from filters import IsPrivate
from loader import bot
from data import main
from fast_api.database.repo.requests import RequestsRepo

router = Router()

@router.message(CommandStart(), IsPrivate())
async def command_start(message: Message, repo: RequestsRepo):    
    args = message.text[7:]

    date_reg = str(datetime.now())[:16]
    username = message.from_user.username
    locale = message.from_user.language_code
    name = message.from_user.first_name.replace("'", "")
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Запросить доступ", callback_data="get_access")],
    ])

    caption = (f"{name}, добро пожаловать!\n\n"
              f"Чтобы получить доступ к данному боту, нужно запросить доступ у администратора")
    
    user_exists = await repo.users.get_user(message.from_user.id)
    if not user_exists:

        await repo.users.add_user(
            user_id=message.from_user.id,
            utm=referrer_id,
            status="active",
            name=name,
            date_reg=date_reg,
            username=username,
            lang=locale
        )

    else:
        user_status = await repo.users.get_user_status(message.from_user.id)
        if user_status != "active":
            await repo.users.update_user(message.from_user.id, status="active")

    try:
        await message.delete()
    except Exception:
        pass
    
    return True

