from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters import IsPrivate
from database.repo.requests import RequestsRepo
from utils.states.users import UpdateTodoStates 

router = Router()

@router.message(Command("update-todo"), IsPrivate())
async def command_update_todo(message: Message, state: FSMContext):
    await message.answer("Введите ID задачи, которую хотите обновить:")
    await state.set_state(UpdateTodoStates.todo_id)

@router.message(UpdateTodoStates.todo_id)
async def process_todo_id(message: Message, state: FSMContext, repo: RequestsRepo):
    try:
        todo_id = int(message.text)
        todo = await repo.todos.get_todo_by_id(todo_id)
        
        if not todo:
            await message.answer("Задача не найдена")
            await state.clear()
            return
            
        if todo.user_id != message.from_user.id:
            await message.answer("Это не ваша задача")
            await state.clear()
            return
            
        await state.update_data(todo_id=todo_id)
        await message.answer("Введите новое описание задачи:")
        await state.set_state(UpdateTodoStates.new_name)
        
    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID задачи (число)")
        await state.clear()
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")
        await state.clear()

@router.message(UpdateTodoStates.new_name)
async def process_update_todo(message: Message, state: FSMContext, repo: RequestsRepo):
    try:
        data = await state.get_data()
        todo_id = data['todo_id']
        
        await repo.todos.update_todo(todo_id, name=message.text)
        await message.answer(f"Задача успешно обновлена!\nID: {todo_id}\nНовое описание: {message.text}")
        
    except Exception as e:
        await message.answer(f"Ошибка при обновлении задачи: {str(e)}")
    finally:
        await state.clear()
