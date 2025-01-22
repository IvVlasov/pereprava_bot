from aiogram.fsm.state import State, StatesGroup


class SendMessageStates(StatesGroup):
    crossing = State()
    # message_type = State()


class MorningMessageStates(StatesGroup):
    crossing = State()
    message_type = State()
    ferry_count = State()
    confirming = State()


class CloseCrossingStates(StatesGroup):
    crossing = State()
    datetime = State()
    time = State()
    date = State()
    reason = State()
    confirming = State()


class OpenCrossingStates(StatesGroup):
    crossing = State()
    datetime = State()
    time = State()
    date = State()
    ferry_count = State()
    confirming = State()


class PassengerTrainStates(StatesGroup):
    crossing = State()
    time = State()
    date = State()
    route = State()
    confirming = State()


class LimitMessageStates(StatesGroup):
    crossing = State()
    ferry_count = State()
    confirming = State()
