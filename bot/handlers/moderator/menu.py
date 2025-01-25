from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants import ModeratorMenuButtons
from bot.handlers.filter import ModeratorFilter
from bot.handlers.moderator import buttons
from bot.handlers.moderator.states import SendMessageStates
from bot.services.message_service import get_message_service
from repository import CrossingRepository

menu_router = Router()


@menu_router.message(
    ModeratorFilter(), F.text == ModeratorMenuButtons.SEND_MESSAGE.value
)
async def morning_message(message: types.Message, state: FSMContext):
    crossings = await CrossingRepository().get_all_crossings()
    text = "Выберите переправу"
    btn = buttons.send_crossings_keyboard(crossings)
    await message.answer(text, reply_markup=btn)


@menu_router.callback_query(ModeratorFilter(), F.data.startswith("crossing_"))
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
    # TODO: send message
    data = await state.get_data()
    print("Result data", data)
    await callback.message.delete()
    await state.clear()
    await callback.message.answer("Сообщение отправлено")


@menu_router.message(ModeratorFilter(), F.text == ModeratorMenuButtons.SETTINGS.value)
async def settings(message: types.Message, state: FSMContext):
    app_messages = await get_message_service()
    await message.answer(
        app_messages.message_types,
        reply_markup=buttons.send_message_types_keyboard()
    )
