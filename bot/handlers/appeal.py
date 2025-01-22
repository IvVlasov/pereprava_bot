from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.app import bot
from bot.constants import ModeratorMenuButtons, UserMenuButtons
from bot.handlers.filter import ModeratorFilter
from bot.handlers.states import AppealStates
from bot.models.appeal import Appeal
from bot.models.messages import AppMessages
from repository import AppealRepository
from settings import get_settings

appeal_router = Router()


@appeal_router.message(
    F.text.in_(
        [ModeratorMenuButtons.TECH_SUPPORT.value, UserMenuButtons.CALLBACK.value]
    )
)
async def appeal_message(message: types.Message, state: FSMContext):
    await message.answer(AppMessages.appeal_message)
    await state.set_state(AppealStates.appeal)


@appeal_router.message(AppealStates.appeal)
async def appeal_message_handler(message: types.Message, state: FSMContext):
    await message.answer(AppMessages.appeal_message_success)
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


@appeal_router.channel_post()
async def channel_post(message: types.Message):
    if not message.reply_to_message:
        return

    reply_id = message.reply_to_message.message_id
    appeal_repository = AppealRepository()
    appeal = await appeal_repository.get_appeal(reply_id)
    if appeal.is_answered:
        await message.reply(AppMessages.appeal_message_already_answered)
        return

    appeal.is_answered = True
    await appeal_repository.update_appeal(appeal)
    await bot.send_message(
        appeal.chat_id, "Ответ на ваше обращение:\n\n %s" % message.text
    )
    await message.reply(AppMessages.appeal_message_answered)
