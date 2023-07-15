from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from data.config import admins
from data.logging import logger


class IsAdmin(BoundFilter):

    """Фильтр для проверки на админа"""

    async def check(self, message: Message):
        return message.from_user.id in admins
