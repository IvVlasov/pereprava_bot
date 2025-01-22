from bot.constants.base import AppStringEnum


class UserMenuButtons(AppStringEnum):
    CROSSING_CAMERAS = "Камеры Переправа"
    SETTINGS = "Настройки уведомлений"
    CALLBACK = "Обратная связь"


class ModeratorMenuButtons(AppStringEnum):
    SEND_MESSAGE = "Отправка сообщения"
    SETTINGS = "Настройки уведомлений"
    TECH_SUPPORT = "Тех.поддержка"


class ModeratorMessageTypes(AppStringEnum):
    MORNING_MESSAGE = "Ежедневное утренее сообщение"
    CLOSING_MESSAGE = "Сообщение о закрытии переправы"
    OPENING_MESSAGE = "Сообщение об открытии переправы"
    PASSENGER_TRAIN = "Пробный пассажирский рейс"
    LIMIT_MESSAGE = "Сообщение об ограничении"


class CrossingTimeButtons(AppStringEnum):
    NOW = "Текущее время"
    MANUAL = "Указать время вручную"


class CloseCrossingReasonButtons(AppStringEnum):
    WIND = "Ветер"
    MIST = "Туман / Плохая видимость"
    TECHNICAL = "Технические причины"


class PassengerTrainRoutes(AppStringEnum):
    SALAHRAD_LABYTNANGI = "Салехард - Лабытнанги"
    LABYTNANGI_SALAHRAD = "Лабытнанги - Салехард"
