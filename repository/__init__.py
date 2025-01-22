import asyncio

from repository.appeal_repository import AppealRepository
from repository.base import BaseRepository
from repository.crossing_repository import CrossingRepository
from repository.message_templates import MessageTemplatesRepository
from repository.user_crossings import UserCrossingsRepository
from repository.user_repository import UserRepository


async def create_tables():
    for child in BaseRepository.__subclasses__():
        await child().create_table()


asyncio.run(create_tables())
__all__ = [
    "UserRepository",
    "AppealRepository",
    "CrossingRepository",
    "BaseRepository",
    "MessageTemplatesRepository",
    "UserCrossingsRepository",
]
