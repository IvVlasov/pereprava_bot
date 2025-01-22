import json

from pydantic import BaseModel


class Messages(BaseModel):
    start_user: str
    start_moderator: str
    menu_user: str

    message_types: str
    choose_crossings: str
    appeal_message: str
    appeal_message_success: str
    appeal_message_already_answered: str
    appeal_message_answered: str


AppMessages = Messages.model_validate(json.load(open("messages.json")))
