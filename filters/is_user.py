from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from data.config import admins
from data.config import db
from data.logging import logger


def check_teachers(tg_id):
    result = db.fetchall("SELECT tg_id FROM teachers WHERE tg_id=%s", (tg_id,))
    if result is None:
        return {"tg_id": None}
    return result["tg_id"]


class IsUser(BoundFilter):

    """Фильтр для проверки на юзера"""

    async def check(self, message: Message):
        return message.from_user.id not in admins and \
               message.from_user.id != check_teachers(message.from_user.id)["tg_id"]

