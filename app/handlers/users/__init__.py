from aiogram import Router

from .todo import router as todo_router

router = Router()
router.include_router(todo_router)

__all__ = ['router']