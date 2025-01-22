from aiogram import Router

from bot.handlers.moderator.menu import menu_router
from bot.handlers.moderator.send_message import (close_crossing_router,
                                                 limit_message_router,
                                                 morning_message_router,
                                                 open_crossing_router,
                                                 passenger_train_router)

moderator_router = Router()


moderator_router.include_router(menu_router)
moderator_router.include_router(morning_message_router)
moderator_router.include_router(close_crossing_router)
moderator_router.include_router(open_crossing_router)
moderator_router.include_router(passenger_train_router)
moderator_router.include_router(limit_message_router)

__all__ = ["moderator_router"]
