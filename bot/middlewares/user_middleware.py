from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from repository import UserRepository


class DatabaseMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user_repository = UserRepository()
        user = await user_repository.get_user(chat_id=event.from_user.id)
        data["user"] = user
        return await handler(event, data)
