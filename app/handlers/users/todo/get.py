from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters import IsPrivate
from database.repo.requests import RequestsRepo

from utils.states import GetTodoStates

router = Router()

class GetTodoStates(StatesGroup):
    todo_id = State()

@router.message(Command("get-todo"), IsPrivate())
async def command_get_todo(message: Message, state: FSMContext):
    await message.answer("Введите ID задачи:")
    await state.set_state(GetTodoStates.todo_id)

@router.message(GetTodoStates.todo_id)
async def process_get_todo(message: Message, state: FSMContext, repo: RequestsRepo):
    try:
        todo_id = int(message.text)
        todo = await repo.todos.get_todo_by_id(todo_id, message.from_user.id)
        
        if todo:
            await message.answer(f"<b>Задача #{todo.id}</b>\n"
                               f"<b>Описание:</b> {todo.name}\n"
                               f"<b>Статус:</b> {'Выполнено' if todo.is_completed else 'Не выполнено'}")
        else:
            await message.answer("Задача с таким ID не найдена")
            
    except ValueError:
        await message.answer("Пожалуйста, введите корректный ID задачи (число)")
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")
    
    await state.clear()

@router.message(Command("get-all-todo"), IsPrivate())
async def command_get_all_todos(message: Message, repo: RequestsRepo):
    try:
        todos = await repo.todos.get_all_todos(message.from_user.id)
        
        if todos:
            response = "Ваши задачи:\n\n"
            for todo in todos:
                response += f"#{todo.id} - {todo.name} "
            await message.answer(response)
        else:
            await message.answer("Список задач пуст, чтобы создать задачу, используйте команду /create-todo")
            
    except Exception as e:
        await message.answer(f"Ошибка при получении списка задач: {str(e)}")
