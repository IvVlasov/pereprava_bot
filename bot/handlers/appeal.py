from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.app import bot
from bot.constants import ModeratorMenuButtons, UserMenuButtons
from bot.handlers.filter import ModeratorFilter
from bot.handlers.states import AppealStates
from bot.models.appeal import Appeal
from bot.services.message_service import get_message_service
from repository import AppealRepository
from settings import get_settings
from aiogram.enums.chat_type import ChatType

appeal_router = Router()


@appeal_router.message(
    F.text.in_(
        [ModeratorMenuButtons.TECH_SUPPORT.value, UserMenuButtons.CALLBACK.value]
    )
)
async def appeal_message(message: types.Message, state: FSMContext):
    app_messages = await get_message_service()
    await message.answer(app_messages.appeal_message)
    await state.set_state(AppealStates.appeal)


@appeal_router.message(AppealStates.appeal)
async def appeal_message_handler(message: types.Message, state: FSMContext):
    app_messages = await get_message_service()
    await message.answer(app_messages.appeal_message_success)
    await send_appeal_message(message)
    await state.clear()


async def send_appeal_message(message: types.Message):
    settings = get_settings()
    moderator_filter = ModeratorFilter()
    is_moderator = await moderator_filter(message)
    status = "модератора" if is_moderator else "пользователя"
    text = (
        f"Новое обращение от {status} {message.from_user.full_name}\n\n{message.text}"
    )
    channel_message = await bot.send_message(settings.CHANNEL_ID, text)
    appeal = Appeal(chat_id=message.from_user.id, message_id=channel_message.message_id)
    appeal_repository = AppealRepository()
    await appeal_repository.create_appeal(appeal)


@appeal_router.message()
async def channel_post(message: types.Message):
    if not message.reply_to_message and message.chat.type == ChatType.CHANNEL:
        return

    reply_id = message.reply_to_message.message_id
    appeal_repository = AppealRepository()
    appeal = await appeal_repository.get_appeal(reply_id)
    if appeal.is_answered:
        await message.reply("Обращение уже отвечено.")
        return

    appeal.is_answered = True
    await appeal_repository.update_appeal(appeal)
    await bot.send_message(
        appeal.chat_id, "Ответ на ваше обращение:\n\n %s" % message.text
    )
    await message.reply("Обращение отвечено.")
