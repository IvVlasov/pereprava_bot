from bot.handlers.admin import admin_router
from bot.handlers.appeal import appeal_router
from bot.handlers.moderator import moderator_router
from bot.handlers.user import user_router

__all__ = ["user_router", "admin_router", "moderator_router", "appeal_router"]
