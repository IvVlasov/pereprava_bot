from aiogram import types
from aiogram.filters import Filter

from bot.app import bot
from bot.constants.chat_members import ChatMemberStatus
from settings import get_settings


class ModeratorFilter(Filter):
    async def __call__(self, msg: types.Message | types.CallbackQuery) -> bool:
        settings = get_settings()
        chat_member = await bot.get_chat_member(settings.CHANNEL_ID, msg.from_user.id)
        return chat_member.status in [
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.CREATOR,
            ChatMemberStatus.MEMBER,
        ]
