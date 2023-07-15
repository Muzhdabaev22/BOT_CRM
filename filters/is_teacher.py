from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from data.config import db
from data.logging import logger


def check_teachers(tg_id):
    result = db.fetchone("SELECT tg_id FROM teachers WHERE tg_id=%s", (tg_id,))
    if result is None:
        logger.info("Проверку не прошел")
        return {"tg_id": None}
    return result


class IsTeacher(BoundFilter):

    """Фильтр для проверки на учителя"""

    async def check(self, message: Message):
        return message.from_user.id == check_teachers(message.from_user.id)["tg_id"]
