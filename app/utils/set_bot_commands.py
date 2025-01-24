from aiogram import Bot
from aiogram.types import BotCommand

async def set_default_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Начать'),
        BotCommand(command='search', description='Проверить домены'),
        BotCommand(command='get-all-todo', description='Получить все задачи'),
        BotCommand(command='create-todo', description='Создать задачу'),
        BotCommand(command='update-todo', description='Обновить задачу'),
        BotCommand(command='delete-todo', description='Удалить задачу'),
    ]
    await bot.set_my_commands(commands)