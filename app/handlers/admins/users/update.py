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

@router.message(Command("edit-user"), IsPrivate(), IsAdmin())
async def command_edit_user(message: Message, repo: RequestsRepo):
    users = await repo.users.get_all_users()
    
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{user.name} (ID: {user.user_id})", 
            callback_data=f"edit_user_{user.user_id}"
        )]
        for user in users
    ])
    
    await message.answer("Выберите пользователя для редактирования:", reply_markup=markup)

@router.callback_query(F.data.startswith("edit_user_"))
async def process_edit_user(callback: CallbackQuery, repo: RequestsRepo):
    user_id = int(callback.data.split("_")[2])
    
    try:
        user = await repo.users.get_user_by_id(user_id)
        if not user:
            await callback.message.edit_text("Пользователь не найден")
            return
            
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Удалить пользователя", callback_data=f"delete_user_{user_id}"),
                InlineKeyboardButton(text="Изменить роль", callback_data=f"change_role_{user_id}")
            ]
        ])
            
        await callback.message.edit_text(
            f"Пользователь: {user.name}\nID: {user.user_id}\n\nВыберите действие:",
            reply_markup=markup
        )
            
    except Exception as e:
        await callback.message.edit_text(f"Ошибка при редактировании пользователя: {str(e)}")

@router.callback_query(F.data.startswith("change_role_"))
async def process_delete_user(callback: CallbackQuery, repo: RequestsRepo):
    user_id = int(callback.data.split("_")[2])
    
    roles = await repo.roles.get_all_roles()
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=role.name, callback_data=f"role_{role.id}")]
        for role in roles
    ])
    
    await callback.message.edit_text(f"Выберите новую роль для пользователя:\nID: {user_id}", reply_markup=markup)

@router.callback_query(F.data.startswith("change_role_"))
async def process_change_role(callback: CallbackQuery, repo: RequestsRepo):
    role_id = int(callback.data.split("_")[1])
    user_id = int(callback.message.text.split("\n")[1].split(": ")[1])
    
    await repo.users.update_user(user_id=user_id, role_id=role_id)
    await callback.message.edit_text(f"Роль пользователя изменена!\nID: {user_id}")
