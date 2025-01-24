import asyncio
import logging

from aiogram import Bot, Dispatcher

from database.setup import create_engine, create_session_pool, create_tables
from middlewares.database import DatabaseMiddleware

from loader import bot, dp
from handlers import router

def register_global_middlewares(dp: Dispatcher, session_pool=None):
    """
    Register global middlewares for the given dispatcher.
    Global middlewares here are the ones that are applied to all the handlers (you specify the type of update)

    :param dp: The dispatcher instance.
    :type dp: Dispatcher
    :param config: The configuration object from the loaded configuration.
    :param session_pool: Optional session pool object for the database using SQLAlchemy.
    :return: None
    """
    middleware_types = [
        DatabaseMiddleware(session_pool),
    ]

    for middleware_type in middleware_types:
        dp.message.outer_middleware(middleware_type)
        dp.callback_query.outer_middleware(middleware_type)
        dp.my_chat_member.outer_middleware(middleware_type)


async def main():
    logger = logging.getLogger(__name__)

    engine = create_engine()
    
    # Ждем пока база данных будет готова
    await asyncio.sleep(5)
    
    # Создаем таблицы если они не существуют
    try:
        await create_tables(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

    session_pool = create_session_pool(engine)

    dp.workflow_data.update(bot=bot)

    dp.include_router(router)
    register_global_middlewares(dp, session_pool)

    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot was stopped!")
