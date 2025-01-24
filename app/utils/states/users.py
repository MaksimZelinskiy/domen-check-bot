from aiogram.fsm.state import State, StatesGroup

class CreateTodoStates(StatesGroup):
    name = State()

class DeleteTodoStates(StatesGroup):
    todo_id = State()

class UpdateTodoStates(StatesGroup):
    todo_id = State()
    new_name = State()

class DomainCheckStates(StatesGroup):
    waiting_domains = State()

class GetTodoStates(StatesGroup):
    todo_id = State()
