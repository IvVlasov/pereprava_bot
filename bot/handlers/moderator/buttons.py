from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot.constants import ModeratorMessageTypes
from bot.constants.base import AppStringEnum
from bot.models.crossing import Crossing
from bot.models.message_template import MessageTemplate


def send_hello_types_keyboard(message_templates: list[MessageTemplate]):
    builder = InlineKeyboardBuilder()
    for message_template in message_templates:
        builder.button(
            text=message_template.name, callback_data=f"type_{message_template.id}"
        )
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def send_crossings_keyboard(crossings: list[Crossing]):
    builder = InlineKeyboardBuilder()
    for crossing in crossings:
        builder.button(text=crossing.name, callback_data=f"crossing_{crossing.id}")
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def ferry_count_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="1", callback_data="ferry_count_1")
    builder.button(text="2", callback_data="ferry_count_2")
    builder.button(text="3", callback_data="ferry_count_3")
    builder.button(text="4", callback_data="ferry_count_4")
    builder.button(text="5", callback_data="ferry_count_5")
    builder.button(text="6", callback_data="ferry_count_6")
    builder.adjust(3)
    keyboard = builder.as_markup()
    return keyboard


def confirm_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Подтвердить", callback_data="confirm_yes")
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard


def send_message_types_keyboard():
    builder = ReplyKeyboardBuilder()
    for button in ModeratorMessageTypes:
        builder.button(text=button.value)
    builder.adjust(1)
    keyboard = builder.as_markup()
    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True
    return keyboard


def _keyboard(keys: AppStringEnum):
    builder = ReplyKeyboardBuilder()
    for key in keys:
        builder.button(text=key.value)
    builder.adjust(1)
    keyboard = builder.as_markup()
    keyboard.resize_keyboard = True
    keyboard.one_time_keyboard = True
    return keyboard


def _inline_keyboard(keys: AppStringEnum):
    builder = InlineKeyboardBuilder()
    for key in keys:
        builder.button(text=key.value, callback_data=f"{key.name}")
    builder.adjust(1)
    keyboard = builder.as_markup()
    return keyboard
