from abc import abstractmethod

import aiosqlite

from settings import get_settings


def dict_factory(cursor, row):
    return {cursor.description[idx][0]: value for idx, value in enumerate(row)}


class BaseRepository:
    table_name: str

    def __init__(self):
        self.settings = get_settings()
        self.db_path = self.settings.DB_PATH

    async def execute(self, query: str, params: tuple = ()):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(query, params)
            await db.commit()

    async def execute_fetchall(self, query: str):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = dict_factory
            result = await db.execute_fetchall(query)
            return result

    async def insert(self, **kwargs):
        async with aiosqlite.connect(self.db_path) as db:
            keys = ", ".join([key for key in kwargs])
            params = ", ".join(["?" for _ in range(len(kwargs))])
            values = [kwargs[key] for key in kwargs]
            result = await db.execute_insert(
                f"INSERT OR IGNORE INTO {self.table_name} ({keys}) VALUES ({params})",
                values,
            )
            await db.commit()
            return result

    async def select_all(self, **kwargs):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = dict_factory
            if kwargs:
                where_conditions = " AND ".join(
                    [f"{key} = '{value}'" for key, value in kwargs.items()]
                )
                result = await db.execute_fetchall(
                    f"SELECT * FROM {self.table_name} WHERE {where_conditions}"
                )
            else:
                result = await db.execute_fetchall(f"SELECT * FROM {self.table_name}")
            return result

    async def select(self, **kwargs):
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = dict_factory
            where_conditions = " AND ".join(
                [f"{key} = '{value}'" for key, value in kwargs.items()]
            )
            result = await db.execute_fetchall(
                f"SELECT * FROM {self.table_name} WHERE {where_conditions}"
            )
            return result

    async def select_one(self, **kwargs):
        all_result = await self.select(**kwargs)
        if all_result:
            return all_result[0]
        return None

    async def update(self, set_conditions: dict, **kwargs):
        async with aiosqlite.connect(self.db_path) as db:
            where_conditions = " AND ".join(
                [f"{key} = '{value}'" for key, value in kwargs.items()]
            )
            set_conditions = ", ".join(
                [f"{key} = '{value}'" for key, value in set_conditions.items()]
            )
            await db.execute(
                f"UPDATE {self.table_name} SET {set_conditions} WHERE {where_conditions}"
            )
            await db.commit()

    async def delete(self, **kwargs):
        async with aiosqlite.connect(self.db_path) as db:
            where_conditions = " AND ".join(
                [f"{key} = '{value}'" for key, value in kwargs.items()]
            )
            await db.execute(f"DELETE FROM {self.table_name} WHERE {where_conditions}")
            await db.commit()

    @abstractmethod
    async def create_table(self):
        """
        Create table if not exists
        """
        pass
