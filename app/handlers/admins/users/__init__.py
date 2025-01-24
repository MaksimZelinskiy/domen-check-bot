from aiogram import Router

from .create import router as create_router
from .delete import router as delete_router
from .update import router as update_router

router = Router()
router.include_router(create_router)
router.include_router(delete_router)
router.include_router(update_router)

__all__ = ['router']