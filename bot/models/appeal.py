from pydantic import BaseModel


class Appeal(BaseModel):
    id: int | None = None
    chat_id: int
    message_id: int
    is_answered: bool = False
