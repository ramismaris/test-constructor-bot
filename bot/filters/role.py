from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.dals import UserDAL


class RoleFilter(BaseFilter):
    def __init__(self, role: Union[str, list]):
        self.role = role

    async def __call__(self, message: Message, session: AsyncSession) -> bool:
        user = await UserDAL.get_user(session, tg_id=str(message.chat.id))

        if not user:
            return False
        if isinstance(self.role, str):
            return user.role == self.role
        else:
            return user.role in self.role
