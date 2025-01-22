from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from settings import get_settings

settings = get_settings()


# Создание диспатчера
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
