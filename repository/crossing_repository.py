from bot.models.crossing import Crossing
from repository.base import BaseRepository


class CrossingRepository(BaseRepository):
    table_name = "crossings"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                camera_url TEXT
            )
        """
        await self.execute(create_table_query)

    async def create_or_update_crossing(self, crossing: Crossing):
        await self.insert(name=crossing.name, camera_url=crossing.camera_url)
        await self.update(
            set_conditions={"camera_url": crossing.camera_url}, name=crossing.name
        )

    async def get_all_crossings(self) -> list[Crossing]:
        crossings = await self.select_all()
        return [Crossing(**crossing) for crossing in crossings]

    async def get_crossing_by_id(self, crossing_id: int) -> Crossing:
        crossing = await self.select_one(id=crossing_id)
        return Crossing(**crossing)

    async def delete_crossing(self, crossing_name: str):
        await self.delete(name=crossing_name)

    async def get_crossings_by_ids(
        self, crossings_ids: list[int] | None
    ) -> list[Crossing]:
        if not crossings_ids:
            return []
        query = f"SELECT {self.table_name}.* FROM {self.table_name} WHERE id IN ({', '.join(map(str, crossings_ids))})"
        result = await self.execute_fetchall(query)
        return [Crossing(**crossing) for crossing in result]

    # async def get_users_by_crossing_id(self, crossing_id: int) -> list[User]:
    #     query = f"SELECT {self.table_name}.* FROM {self.table_name} WHERE id IN ({', '.join(map(str, crossings_ids))})"
    #     result = await self.execute_fetchall(query)
    #     return [Crossing(**crossing) for crossing in result]
