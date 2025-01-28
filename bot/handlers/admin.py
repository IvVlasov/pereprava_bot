from aiogram import F, Router, types
from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext

from bot import buttons
from bot.app import bot
from bot.services.parse_settings_excel import ExcelSettings
from settings import get_settings

admin_router = Router()
settings = get_settings()


class AdminFilter(Filter):
    async def __call__(self, msg: types.Message | types.CallbackQuery) -> bool:
        if isinstance(msg, types.Message):
            return msg.chat.id == settings.ADMIN_CHAT_ID
        if isinstance(msg, types.CallbackQuery):
            return msg.message.chat.id == settings.ADMIN_CHAT_ID


@admin_router.message(AdminFilter(), F.text == "/admin")
async def admin(message: types.Message, state: FSMContext):
    await message.answer(
        "Меню администратора", reply_markup=buttons.admin_menu_keyboard()
    )


@admin_router.callback_query(AdminFilter(), F.data == "settings")
async def get_settings(callback: types.CallbackQuery, state: FSMContext):
    text = "Текущие настройки бота. Измените их в файле и отправьте его мне."
    parse_settings_excel = ExcelSettings()
    document_file = await parse_settings_excel.get_excel_file()
    await callback.message.answer_document(document=document_file, caption=text)


@admin_router.message(AdminFilter(), F.document)
async def get_settings(message: types.Message, state: FSMContext):
    file = await bot.get_file(message.document.file_id)
    await bot.download_file(file.file_path, settings.SETTINGS_FILE_PATH)
    parse_settings_excel = ExcelSettings()
    is_success = await parse_settings_excel.parse_and_save()
    if is_success:
        await message.answer("Настройки успешно обновлены", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Произошла ошибка при обновлении настроек", reply_markup=types.ReplyKeyboardRemove())
