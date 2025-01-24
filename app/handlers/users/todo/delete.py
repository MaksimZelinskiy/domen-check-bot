from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters import IsPrivate
from database.repo.requests import RequestsRepo

from utils.states.users import DeleteTodoStates

router = Router()


@router.message(Command("delete-todo"), IsPrivate())
async def command_delete_todo(message: Message, state: FSMContext):
    await message.answer("Введите ID задачи, которую хотите удалить:")
    await state.set_state(DeleteTodoStates.todo_id)

@router.message(DeleteTodoStates.todo_id)
async def process_delete_todo(message: Message, state: FSMContext, repo: RequestsRepo):
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
            
        await repo.todos.delete_todo(todo_id)
        await message.answer(f"Задача успешно удалена!\nID: {todo_id}")
        
    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID задачи (число)")
    except Exception as e:
        await message.answer(f"Ошибка при удалении задачи: {str(e)}")
    finally:
        await state.clear()
