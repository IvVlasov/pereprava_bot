from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants import ModeratorMenuButtons
from bot.handlers.filter import ModeratorFilter
from bot.handlers.moderator import buttons
from bot.handlers.moderator.states import SendMessageStates
from repository import CrossingRepository, UserCrossingsRepository
from bot.services.message_service import get_message_service
from bot.app import bot

menu_router = Router()


@menu_router.message(
    ModeratorFilter(), F.text == ModeratorMenuButtons.SEND_MESSAGE.value
)
async def morning_message(message: types.Message, state: FSMContext):
    crossings = await CrossingRepository().get_all_crossings()
    text = "Выберите переправу"
    btn = buttons.send_crossings_keyboard(crossings)
    await message.answer(text, reply_markup=btn)


@menu_router.callback_query(ModeratorFilter(), F.data.startswith("choose_crossing_"))
async def choose_crossing(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    crossing_id = int(callback.data.split("_")[-1])
    await state.set_state(SendMessageStates.crossing)
    await state.update_data(crossing_id=crossing_id)
    app_messages = await get_message_service()
    await callback.message.answer(
        app_messages.message_types,
        reply_markup=buttons.send_message_types_keyboard(),
    )


@menu_router.callback_query(F.data == "confirm_yes")
async def close_crossing_message_confirm(
    callback: types.CallbackQuery, state: FSMContext
):
    data = await state.get_data()
    crossing_id = data.get("crossing_id")
    user_crossings_repository = UserCrossingsRepository()
    user_ids = await user_crossings_repository.get_user_crossings_by_ids(crossing_id)
    for user_id in user_ids:
        await bot.copy_message(user_id, callback.message.chat.id, data.get("message_id_to_send"))
    await callback.message.delete()
    await state.clear()
    await callback.message.answer("Сообщение отправлено")
