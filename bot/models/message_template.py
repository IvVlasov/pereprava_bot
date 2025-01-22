from enum import Enum

from pydantic import BaseModel


class MessageTemplateType(Enum):
    MORNING = "morning"
    CLOSING = "closing"
    OPENING = "opening"
    PASSENGER_TRAIN = "passenger_train"
    LIMIT = "limit"


class MessageTemplate(BaseModel):
    id: int | None = None
    name: str
    template: str
    message_type: MessageTemplateType
