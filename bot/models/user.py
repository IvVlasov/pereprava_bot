from pydantic import BaseModel


class User(BaseModel):
    chat_id: int
    crossings: str = ""
