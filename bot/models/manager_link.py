import uuid

from pydantic import BaseModel, Field


class ManagerLink(BaseModel):
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()))
    is_used: bool = Field(default=False)
