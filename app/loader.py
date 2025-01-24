from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode

from data import config

bot = Bot(
    token=config.BOT_TOKEN,
)

storage = MemoryStorage()

dp = Dispatcher(storage=storage)

__all__ = ['bot', 'storage', 'dp']
