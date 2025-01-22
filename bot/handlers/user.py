from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot import buttons
from bot.constants import UserMenuButtons
from bot.handlers.filter import ModeratorFilter
from bot.models import Crossing, User
from bot.models.messages import AppMessages
from repository import (CrossingRepository, UserCrossingsRepository,
                        UserRepository)

user_router = Router()


class UserCrossingsStates(StatesGroup):
    crossing_choice = State()


class UserCrossingsCamerasStates(StatesGroup):
    crossing_choice = State()


class ModeratorCrossingsStates(StatesGroup):
    crossing_choice = State()


@user_router.message(ModeratorFilter(), F.text.startswith("/start"))
async def start_moderator(message: types.Message, state: FSMContext):
    user_repository = UserRepository()
    await user_repository.create_user(User(chat_id=message.chat.id))
    text, btn = AppMessages.start_user, buttons.manager_menu_keyboard()
    await message.answer(text, reply_markup=btn)
    await state.clear()


@user_router.message(F.text.startswith("/start"))
async def start(message: types.Message, state: FSMContext):
    user_repository = UserRepository()
    await user_repository.create_user(User(chat_id=message.chat.id))
    text, btn = AppMessages.start_user, buttons.user_menu_keyboard()
    text = text.format(user_name=message.from_user.full_name)
    await message.answer(text, reply_markup=btn)
    await state.clear()


@user_router.message(F.text == UserMenuButtons.SETTINGS.value)
async def subscribe_handler(message: types.Message, state: FSMContext, user: User):
    await state.set_state(UserCrossingsStates.crossing_choice)
    text = "Выберите переправы, на которые вы хотите подписаться на уведомления"
    crossings_repository = CrossingRepository()
    crossings = await crossings_repository.get_all_crossings()
    await state.update_data(crossings=crossings)
    btn = buttons.user_crossings_keyboard(crossings)
    await message.answer(text, reply_markup=btn)


@user_router.callback_query(
    F.data.startswith("crossing_"), UserCrossingsStates.crossing_choice
)
async def crossing_choice_handler(callback: types.CallbackQuery, state: FSMContext):
    crossing_id = int(callback.data.split("_")[-1])
    data = await state.get_data()
    crossings = data.get("crossings")
    for crossing in crossings:
        if crossing.id == crossing_id:
            crossing.name = f"✅ {crossing.name}"
            break
    await state.update_data(crossings=crossings)
    btn = buttons.user_crossings_keyboard(crossings)
    await callback.message.edit_reply_markup(reply_markup=btn)


@user_router.callback_query(
    F.data.startswith("save_crossings"), UserCrossingsStates.crossing_choice
)
async def save_crossings_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    crossings: list[Crossing] = data.get("crossings")
    crossings_ids = [
        crossing.id for crossing in crossings if crossing.name.startswith("✅")
    ]
    user_crossings_repository = UserCrossingsRepository()
    await user_crossings_repository.set_user_crossings(
        callback.from_user.id, crossings_ids
    )
    await callback.message.delete()
    text = "Переправы успешно сохранены.\n\nВы можете изменить их в разделе 'Настройки'"
    await callback.message.answer(text, reply_markup=buttons.user_menu_keyboard())
    await state.clear()


@user_router.message(F.text == UserMenuButtons.CROSSING_CAMERAS.value)
async def crossing_cameras_handler(
    message: types.Message, state: FSMContext, user: User
):
    await state.set_state(UserCrossingsCamerasStates.crossing_choice)
    user_crossings_repository = UserCrossingsRepository()
    crossings_ids = await user_crossings_repository.get_user_crossings_ids(
        message.chat.id
    )
    crossings = await CrossingRepository().get_crossings_by_ids(crossings_ids)
    print(crossings)
    if not crossings:
        text = "У вас нет сохраненных переправ. Перейдите в настройки и выберите переправы."
        btn = buttons.user_menu_keyboard()
    else:
        text = "Выберите переправу, чтобы посмотреть камеры"
        btn = buttons.user_camera_crossings_keyboard(crossings)
    await message.answer(text, reply_markup=btn)


@user_router.callback_query(
    F.data.startswith("crossing_"), UserCrossingsCamerasStates.crossing_choice
)
async def crossing_camera_handler(callback: types.CallbackQuery, state: FSMContext):
    crossing_id = int(callback.data.split("_")[-1])
    crossing = await CrossingRepository().get_crossing_by_id(crossing_id)
    if crossing.camera_url:
        await callback.message.answer(crossing.camera_url)
    else:
        await callback.message.answer("У переправы нет камеры")
