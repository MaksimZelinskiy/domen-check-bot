from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters import IsPrivate, IsAdmin
from loader import bot
from database.repo.requests import RequestsRepo

router = Router()

@router.message(Command("delete-user"), IsPrivate(), IsAdmin())
async def command_delete_user(message: Message, repo: RequestsRepo):
    users = await repo.users.get_all_users()
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{user.name} (ID: {user.user_id})", 
            callback_data=f"delete_user_{user.user_id}"
        )]
        for user in users
    ])
    
    await message.answer("Выберите кого удалить:", reply_markup=markup)

@router.callback_query(F.data.startswith("delete_user_"))
async def process_delete_user(callback: CallbackQuery, repo: RequestsRepo):
    user_id = int(callback.data.split("_")[2])
    
    try:
        user = await repo.users.get_user_by_id(user_id)
        if not user:
            await callback.message.edit_text("Пользователь не найден")
            return
            
        await repo.users.delete_user(user_id)
        await callback.message.edit_text(f"Пользователь удален!\nID: {user_id}\nИмя: {user.name}")
        
        try:
            await bot.send_message(user_id, "Ваш аккаунт был удален администратором")
        except Exception:
            pass
            
    except Exception as e:
        await callback.message.edit_text(f"Ошибка при удалении пользователя: {str(e)}")
