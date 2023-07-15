from aiogram import executor

from data.logging import logger
from data.config import dp
from data.config import db

from handlers.admin import admin
from handlers.teacher import teacher
from handlers.user import user


async def on_startup(_):
    db.create_tables()


if __name__ == '__main__':
    try:
        logger.info("Бот запущен")
        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
    except Exception as error:
        logger.error(f"Произошла ошибка: {error}")
