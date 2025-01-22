from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from bot.constants import ModeratorMessageTypes
from bot.handlers.moderator import buttons
from bot.handlers.moderator.states import LimitMessageStates, SendMessageStates
from bot.models.message_template import MessageTemplateType
from bot.services.message_template_service import MessageTemplatesService
from repository import MessageTemplatesRepository

limit_message_router = Router()


MESSAGE_TEMPLATE = """Подтвердите: что дата и сообщение об открытии указано верно:\n\n
**ШАБЛОННЫЙ ТЕКСТ СООБЩЕНИЯ С %ДАТОЙ% %ВРЕМЕНЕМ% и %ПРИЧИНА%**"""


@limit_message_router.message(
    F.text == ModeratorMessageTypes.LIMIT_MESSAGE.value, SendMessageStates.crossing
)
async def open_crossing_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    crossing_id = data["crossing_id"]
    await state.set_state(LimitMessageStates.ferry_count)
    await state.update_data(crossing_id=crossing_id)
    await message.answer(
        "Укажите количество паромов на линии",
        reply_markup=buttons.ferry_count_keyboard(),
    )


@limit_message_router.callback_query(
    F.data.startswith("ferry_count_"), LimitMessageStates.ferry_count
)
async def morning_ferry_count(callback: types.CallbackQuery, state: FSMContext):
    ferry_count = int(callback.data.split("_")[-1])
    await state.update_data(ferry_count=ferry_count)
    await state.set_state(LimitMessageStates.confirming)
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
