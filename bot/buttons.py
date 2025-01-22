from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.constants import ModeratorMenuButtons, UserMenuButtons
from bot.models import Crossing


def admin_menu_keyboard():
    builder = InlineKeyboardBuilder()
    # builder.button(text='Создать ссылку модератора', callback_data='create_link')
    # builder.button(text='Добавить переправу', callback_data='add_crossing')
    builder.button(text="Настройки", callback_data="settings")

    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Начать", callback_data="start")
    keyboard = builder.as_markup()
    return keyboard


def user_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    for button in UserMenuButtons:
        builder.button(text=button.value)
    builder.adjust(1)
    keyboard = builder.as_markup()
    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True
    return keyboard


def manager_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    for button in ModeratorMenuButtons:
        builder.button(text=button.value)
    builder.adjust(1)
    keyboard = builder.as_markup()
    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True
    return keyboard


def user_crossings_keyboard(crossings: list[Crossing]):
    builder = InlineKeyboardBuilder()
    for crossing in crossings:
        builder.button(text=crossing.name, callback_data=f"crossing_{crossing.id}")
    builder.button(text="Сохранить", callback_data="save_crossings")
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def user_camera_crossings_keyboard(crossings: list[Crossing]):
    builder = InlineKeyboardBuilder()
    for crossing in crossings:
        builder.button(text=crossing.name, callback_data=f"crossing_{crossing.id}")
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard
