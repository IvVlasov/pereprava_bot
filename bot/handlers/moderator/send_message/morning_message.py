from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants import ModeratorMessageTypes
from bot.handlers.moderator import buttons
from bot.handlers.moderator.states import (MorningMessageStates,
                                           SendMessageStates)
from bot.models.message_template import MessageTemplateType
from bot.services.message_template_service import MessageTemplatesService
from repository import MessageTemplatesRepository

morning_message_router = Router()


@morning_message_router.message(
    F.text == ModeratorMessageTypes.MORNING_MESSAGE.value, SendMessageStates.crossing
)
async def morning_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(MorningMessageStates.message_type)
    await state.update_data(crossing_id=data["crossing_id"])
    message_templates = (
        await MessageTemplatesRepository().get_messages_templates_by_type(
            MessageTemplateType.MORNING
        )
    )
    text = "Выберите тип приветственного собщения"
    btn = buttons.send_hello_types_keyboard(message_templates)
    await message.answer(text, reply_markup=btn)


@morning_message_router.callback_query(
    F.data.startswith("type_"), MorningMessageStates.message_type
)
async def morning_message_type(callback: types.CallbackQuery, state: FSMContext):
    message_template_id = callback.data.split("_")[1]
    await state.update_data(message_template_id=message_template_id)
    await state.set_state(MorningMessageStates.ferry_count)
    text = "Укажите количество паромов на линии"
    btn = buttons.ferry_count_keyboard()
    await callback.message.edit_text(text, reply_markup=btn)


@morning_message_router.callback_query(
    F.data.startswith("ferry_count_"), MorningMessageStates.ferry_count
)
async def morning_ferry_count(callback: types.CallbackQuery, state: FSMContext):
    ferry_count = int(callback.data.split("_")[-1])
    await state.update_data(ferry_count=ferry_count)
    await state.set_state(MorningMessageStates.confirming)
    data = await state.get_data()
    message_template_service = MessageTemplatesService(int(data["message_template_id"]))
    message_text = await message_template_service.get_formated_message(**data)
    new_message = await callback.message.answer(message_text)
    await state.update_data(message_id_to_send=new_message.message_id)
    await callback.message.answer(
        "Подтвердите отправку сообщения", reply_markup=buttons.confirm_keyboard()
    )
