from datetime import datetime

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants import ModeratorMessageTypes
from bot.constants.buttons import PassengerTrainRoutes
from bot.handlers.moderator import buttons
from bot.handlers.moderator.states import (PassengerTrainStates,
                                           SendMessageStates)
from bot.models.message_template import MessageTemplateType
from bot.services.message_template_service import MessageTemplatesService
from repository import MessageTemplatesRepository

passenger_train_router = Router()

MESSAGE_TEMPLATE = """**ШАБЛОННЫЙ ТЕКСТ С %ДАТОЙ% %ВРЕМЕНЕМ% и %Маршрутом%**"""


@passenger_train_router.message(
    F.text == ModeratorMessageTypes.PASSENGER_TRAIN.value, SendMessageStates.crossing
)
async def passenger_train_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    crossing_id = data["crossing_id"]
    await state.set_state(PassengerTrainStates.time)
    await state.update_data(crossing_id=crossing_id)
    text = "Укажите время отправки пробного пассажирского рейса в формате ЧЧ:ММ"
    await message.answer(text)


@passenger_train_router.message(PassengerTrainStates.time)
async def passenger_train_message_time(message: types.Message, state: FSMContext):
    try:
        datetime.strptime(message.text, "%H:%M")
    except Exception:
        await message.answer("Время указано некорректно")
        return
    await state.set_state(PassengerTrainStates.date)
    await state.update_data(time=message.text)
    await message.answer(
        "Укажите время отправки пробного пассажирского рейса в формате ДД.ММ.ГГГГ"
    )


@passenger_train_router.message(PassengerTrainStates.date)
async def passenger_train_message_date(message: types.Message, state: FSMContext):
    try:
        datetime.strptime(message.text, "%d.%m.%Y")
    except Exception:
        await message.answer("Дата указана некорректно")
        return
    await state.set_state(PassengerTrainStates.route)
    await state.update_data(date=message.text)
    btn = buttons._inline_keyboard(PassengerTrainRoutes)
    await message.answer("Выберите маршрут направления:", reply_markup=btn)


@passenger_train_router.callback_query(PassengerTrainStates.route)
async def passenger_train_message_route(
    callback: types.CallbackQuery, state: FSMContext
):
    await callback.message.delete()
    await state.update_data(route=callback.data)
    await state.set_state(PassengerTrainStates.confirming)
    data = await state.get_data()
    message_template_repository = MessageTemplatesRepository()
    message_templates = (
        await message_template_repository.get_messages_templates_by_type(
            MessageTemplateType.PASSENGER_TRAIN
        )
    )
    message_template_service = MessageTemplatesService(
        message_template_id=message_templates[0].id
    )
    message_text = await message_template_service.get_formated_message(**data)
    new_message = await callback.message.answer(message_text)
    await state.update_data(message_id_to_send=new_message.message_id)
    await callback.message.answer(
        "Подтвердите отправку сообщения", reply_markup=buttons.confirm_keyboard()
    )
