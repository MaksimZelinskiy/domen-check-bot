from .users import router as users_router

from aiogram import Router
router = Router()

router.include_router(users_router)

__all__ = [
    "router"
]