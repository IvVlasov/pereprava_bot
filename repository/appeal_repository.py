from bot.models.appeal import Appeal
from repository.base import BaseRepository


class AppealRepository(BaseRepository):
    table_name = "appeals"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                chat_id BIGINT NOT NULL,
                message_id BIGINT NOT NULL,
                is_answered BOOLEAN NOT NULL DEFAULT 0
            )
        """
        await self.execute(create_table_query)

    async def create_appeal(self, appeal: Appeal):
        await self.insert(**appeal.model_dump())

    async def get_appeal(self, message_id: int) -> Appeal | None:
        res = await self.select(message_id=message_id)
        return Appeal(**res[0]) if res else None

    async def update_appeal(self, appeal: Appeal):
        await self.update(
            set_conditions={"is_answered": appeal.is_answered}, id=appeal.id
        )
