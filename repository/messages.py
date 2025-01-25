from repository.base import BaseRepository
from bot.models.messages import Message


class MessagesRepository(BaseRepository):
    table_name = "messages"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL UNIQUE,
                text TEXT NOT NULL
            )
        """
        await self.execute(create_table_query)

    async def create_message(self, message: Message):
        await self.insert(
            key=message.key,
            name=message.name,
            text=message.text,
        )
        await self.update(
            set_conditions={
                "name": message.name,
                "text": message.text,
            },
            key=message.key,
        )

    async def get_messages(self) -> list[Message]:
        messages = await self.select_all()
        return [Message(**message) for message in messages]
