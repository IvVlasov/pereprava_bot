from repository.base import BaseRepository


class UserCrossingsRepository(BaseRepository):
    table_name = "user_crossings"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_chat_id INTEGER,
                crossings_id INTEGER,
                FOREIGN KEY (user_chat_id) REFERENCES users (chat_id),
                FOREIGN KEY (crossings_id) REFERENCES crossings (id)
            )
        """
        await self.execute(create_table_query)

    async def set_user_crossings(self, chat_id: int, crossings_ids: list[int]):
        await self.delete(user_chat_id=chat_id)
        for crossing_id in crossings_ids:
            await self.insert(user_chat_id=chat_id, crossings_id=crossing_id)

    async def get_user_crossings_ids(self, chat_id: int) -> list[int]:
        query = (
            f"SELECT crossings_id FROM {self.table_name} WHERE user_chat_id = {chat_id}"
        )
        result = await self.execute_fetchall(query)
        return [row["crossings_id"] for row in result]

    async def get_user_crossings_by_ids(self, crossing_id: int) -> list[int]:
        query = f"SELECT DISTINCT user_chat_id FROM {self.table_name} WHERE crossings_id = {crossing_id}"
        result = await self.execute_fetchall(query)
        return [row["user_chat_id"] for row in result]
