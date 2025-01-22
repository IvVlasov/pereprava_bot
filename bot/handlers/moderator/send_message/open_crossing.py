from datetime import datetime

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants import ModeratorMessageTypes
from bot.constants.buttons import CrossingTimeButtons
from bot.handlers.moderator import buttons
from bot.handlers.moderator.states import OpenCrossingStates, SendMessageStates
from bot.models.message_template import MessageTemplateType
from bot.services.message_template_service import MessageTemplatesService
from repository import MessageTemplatesRepository

open_crossing_router = Router()


MESSAGE_TEMPLATE = """Подтвердите: что дата и сообщение об открытии указано верно:\n\n
**ШАБЛОННЫЙ ТЕКСТ СООБЩЕНИЯ С %ДАТОЙ% %ВРЕМЕНЕМ% и %ПРИЧИНА%**"""


@open_crossing_router.message(
    F.text == ModeratorMessageTypes.OPENING_MESSAGE.value, SendMessageStates.crossing
)
async def open_crossing_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    crossing_id = data["crossing_id"]
    await state.set_state(OpenCrossingStates.datetime)
    await state.update_data(crossing_id=crossing_id)
    text = "Укажите время открытия переправы"
    btn = buttons._keyboard(CrossingTimeButtons)
    await message.answer(text, reply_markup=btn)


@open_crossing_router.message(
    F.text == CrossingTimeButtons.NOW.value, OpenCrossingStates.datetime
)
async def open_crossing_message_now(message: types.Message, state: FSMContext):
    _datetime = datetime.now()
    date, time = _datetime.date().strftime("%d.%m.%Y"), _datetime.time().strftime(
        "%H:%M"
    )
    await state.update_data(time=time, date=date)
    await state.set_state(OpenCrossingStates.ferry_count)
    await message.answer(
        "Укажите количество паромов на линии",
        reply_markup=buttons.ferry_count_keyboard(),
    )


@open_crossing_router.message(
    F.text == CrossingTimeButtons.MANUAL.value, OpenCrossingStates.datetime
)
async def open_crossing_message_manual(message: types.Message, state: FSMContext):
    await state.set_state(OpenCrossingStates.time)
    await message.answer("Укажите время открытия переправы в формате ЧЧ:ММ")


@open_crossing_router.message(OpenCrossingStates.time)
async def open_crossing_message_time(message: types.Message, state: FSMContext):
    try:
        datetime.strptime(message.text, "%H:%M")
    except Exception:
        await message.answer("Время указано некорректно")
        return
    await state.set_state(OpenCrossingStates.date)
    await state.update_data(time=message.text)
    await message.answer("Укажите дату открытия переправы в формате ДД.ММ.ГГГГ")


@open_crossing_router.message(OpenCrossingStates.date)
async def open_crossing_message_date(message: types.Message, state: FSMContext):
    try:
        datetime.strptime(message.text, "%d.%m.%Y")
    except Exception:
        await message.answer("Дата указана некорректно")
        return
    await state.set_state(OpenCrossingStates.ferry_count)
    await state.update_data(date=message.text)
    await message.answer(
        "Укажите количество паромов на линии",
        reply_markup=buttons.ferry_count_keyboard(),
    )


@open_crossing_router.callback_query(
    F.data.startswith("ferry_count_"), OpenCrossingStates.ferry_count
)
async def morning_ferry_count(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    ferry_count = int(callback.data.split("_")[-1])
    await state.update_data(ferry_count=ferry_count)
    await state.set_state(OpenCrossingStates.confirming)

    data = await state.get_data()
    message_template_repository = MessageTemplatesRepository()
    message_templates = (
        await message_template_repository.get_messages_templates_by_type(
            MessageTemplateType.OPENING
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
