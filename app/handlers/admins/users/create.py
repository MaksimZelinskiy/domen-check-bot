from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters import IsPrivate, IsAdmin
from loader import bot
from database.repo.requests import RequestsRepo
from utils.states import AddUserStates

router = Router()

@router.message(Command("add-user"), IsPrivate(), IsAdmin())
async def command_add_user(message: Message, state: FSMContext):
    await message.answer("Введите <b>Telegram ID</b> пользователя:")
    await state.set_state(AddUserStates.user_id)

@router.message(AddUserStates.user_id)
async def process_user_id(message: Message, state: FSMContext, repo: RequestsRepo):
    try:
        user_id = int(message.text)
        await state.update_data(user_id=user_id)

        user = await repo.users.get_user_by_id(user_id)
        if not user:
            await message.answer("Пользователь не найден в боте. Сперва он должен зайти в бота.")
            return
        
        roles = await repo.roles.get_all_roles()
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=role.name, callback_data=f"role_{role.id}")]
            for role in roles
        ])
        
        await message.answer("Выберите роль для пользователя:", reply_markup=markup)
        await state.set_state(AddUserStates.role)
    except ValueError:
        await message.answer("Пожалуйста, введите корректный <b>Telegram ID</b> (только цифры)")

@router.callback_query(AddUserStates.role, F.data.startswith("role_"))
async def process_role_selection(callback: CallbackQuery, state: FSMContext, repo: RequestsRepo):
    role_id = int(callback.data.split("_")[1])
    user_data = await state.get_data()
    user_id = user_data["user_id"]
        
    try:
        await repo.users.update_user(
            user_id=user_id,
            role_id=role_id
        )
        
        role = await repo.roles.get_role_by_id(role_id)
        await callback.message.edit_text(f"Роль пользователя обновлена!\nID: {user_id}\nРоль: {role.name}")
        await bot.send_message(user_id, f"Ваша роль обновлена: {role.name}")
    except Exception as e:
        await callback.message.edit_text(f"Ошибка при добавлении пользователя: {str(e)}")
    
    await state.clear()
