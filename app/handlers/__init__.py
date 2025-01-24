from .admins import router as admins_router
from .main import router as main_router

from aiogram import Router

router = Router()   
router.include_router(admins_router)
router.include_router(main_router)

__all__ = ['router']
