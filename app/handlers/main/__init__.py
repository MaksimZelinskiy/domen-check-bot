from .start import router as start_router   

from aiogram import Router  

router = Router()
router.include_router(start_router)

__all__ = ['router']
