from bot.models import User
from repository.base import BaseRepository


class UserRepository(BaseRepository):
    table_name = "users"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                chat_id BIGINT PRIMARY KEY,
                crossings TEXT NOT NULL
            )
        """
        await self.execute(create_table_query)

    async def create_user(self, user: User):
        await self.insert(**user.model_dump())

    async def get_user(self, chat_id: int) -> User | None:
        result = await self.select_one(chat_id=chat_id)
        return User(**result) if result else None
