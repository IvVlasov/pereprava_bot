from datetime import datetime

from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants import ModeratorMessageTypes
from bot.constants.buttons import (CloseCrossingReasonButtons,
                                   CrossingTimeButtons)
from bot.handlers.moderator import buttons
from bot.handlers.moderator.states import (CloseCrossingStates,
                                           SendMessageStates)
from bot.models.message_template import MessageTemplateType
from bot.services.message_template_service import MessageTemplatesService
from repository import MessageTemplatesRepository

close_crossing_router = Router()


@close_crossing_router.message(
    F.text == ModeratorMessageTypes.CLOSING_MESSAGE.value, SendMessageStates.crossing
)
async def close_crossing_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    crossing_id = data["crossing_id"]
    await state.set_state(CloseCrossingStates.datetime)
    await state.update_data(crossing_id=crossing_id)
    text = "Укажите время закрытия переправы"
    btn = buttons._keyboard(CrossingTimeButtons)
    await message.answer(text, reply_markup=btn)


@close_crossing_router.message(
    F.text == CrossingTimeButtons.NOW.value, CloseCrossingStates.datetime
)
async def close_crossing_message_now(message: types.Message, state: FSMContext):
    _datetime = datetime.now()
    date, time = _datetime.date().strftime("%d.%m.%Y"), _datetime.time().strftime(
        "%H:%M"
    )
    await state.update_data(time=time, date=date)
    await state.set_state(CloseCrossingStates.reason)
    btn = buttons._keyboard(CloseCrossingReasonButtons)
    await message.answer("Укажите причину закрытия переправы", reply_markup=btn)


@close_crossing_router.message(
    F.text == CrossingTimeButtons.MANUAL.value, CloseCrossingStates.datetime
)
async def close_crossing_message_manual(message: types.Message, state: FSMContext):
    await state.set_state(CloseCrossingStates.time)
    await message.answer("Укажите время закрытия переправы в формате ЧЧ:ММ")


@close_crossing_router.message(CloseCrossingStates.time)
async def close_crossing_message_time(message: types.Message, state: FSMContext):
    try:
        datetime.strptime(message.text, "%H:%M")
    except Exception:
        await message.answer("Время указано некорректно")
        return
    await state.set_state(CloseCrossingStates.date)
    await state.update_data(time=message.text)
    await message.answer("Укажите дату закрытия переправы в формате ДД.ММ.ГГГГ")


@close_crossing_router.message(CloseCrossingStates.date)
async def close_crossing_message_date(message: types.Message, state: FSMContext):
    try:
        datetime.strptime(message.text, "%d.%m.%Y")
    except Exception:
        await message.answer("Дата указана некорректно")
        return
    await state.set_state(CloseCrossingStates.reason)
    await state.update_data(date=message.text)
    btn = buttons._keyboard(CloseCrossingReasonButtons)
    await message.answer("Укажите причину закрытия переправы", reply_markup=btn)


@close_crossing_router.message(CloseCrossingStates.reason)
async def close_crossing_message_reason(message: types.Message, state: FSMContext):
    await state.update_data(reason=message.text)
    await state.set_state(CloseCrossingStates.confirming)

    data = await state.get_data()
    message_template_repository = MessageTemplatesRepository()
    message_templates = (
        await message_template_repository.get_messages_templates_by_type(
            MessageTemplateType.CLOSING
        )
    )
    message_template_service = MessageTemplatesService(
        message_template_id=message_templates[0].id
    )
    message_text = await message_template_service.get_formated_message(**data)
    new_message = await message.answer(message_text)
    await state.update_data(message_id_to_send=new_message.message_id)
    await message.answer(
        "Подтвердите отправку сообщения", reply_markup=buttons.confirm_keyboard()
    )
