from pydantic import BaseModel


class Crossing(BaseModel):
    id: int | None = None
    name: str
    camera_url: str | None = None
