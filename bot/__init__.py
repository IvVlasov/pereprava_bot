from bot.app import dp
from bot.handlers import (admin_router, appeal_router, moderator_router,
                          user_router)
from bot.middlewares import DatabaseMiddleware

# Регистрация middlewares
dp.message.middleware(DatabaseMiddleware())
dp.callback_query.middleware(DatabaseMiddleware())


# Регистрация роутеров
dp.include_router(user_router)
dp.include_router(admin_router)
dp.include_router(moderator_router)
dp.include_router(appeal_router)
