from pydantic import BaseModel


class Message(BaseModel):
    key: str
    name: str
    text: str
