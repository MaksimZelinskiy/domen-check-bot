from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters import IsPrivate
from database.repo.requests import RequestsRepo

from utils.states import CreateTodoStates

router = Router()



@router.message(Command("create-todo"), IsPrivate())
async def command_create_todo(message: Message, state: FSMContext):
    await message.answer("Введите описание задачи:")
    await state.set_state(CreateTodoStates.name)

@router.message(CreateTodoStates.name)
async def process_todo_description(message: Message, state: FSMContext, repo: RequestsRepo):
    name = message.text
    user_id = message.from_user.id
    
    try:
        await repo.todos.create_todo(
            user_id=user_id,
            name=name
        )
        await message.answer("Задача успешно создана!")
    except Exception as e:
        await message.answer(f"Ошибка при создании задачи: {str(e)}")
    
    await state.clear()
