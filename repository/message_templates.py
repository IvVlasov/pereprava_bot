from bot.models.message_template import MessageTemplate, MessageTemplateType
from repository.base import BaseRepository


class MessageTemplatesRepository(BaseRepository):
    table_name = "message_templates"

    async def create_table(self):
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                message_type TEXT NOT NULL,
                template TEXT NOT NULL
            )
        """
        await self.execute(create_table_query)

    async def create_or_update_message_template(
        self, message_template: MessageTemplate
    ):
        await self.insert(
            name=message_template.name,
            template=message_template.template,
            message_type=message_template.message_type.value,
        )
        await self.update(
            set_conditions={"template": message_template.template},
            name=message_template.name,
        )

    async def get_all_message_templates(self) -> list[MessageTemplate]:
        message_templates = await self.select_all()
        return [
            MessageTemplate(**message_template)
            for message_template in message_templates
        ]

    async def get_message_template_by_id(
        self, message_template_id: int
    ) -> MessageTemplate:
        message_template = await self.select_one(id=message_template_id)
        return MessageTemplate(**message_template)

    async def get_messages_templates_by_type(
        self, message_type: MessageTemplateType
    ) -> list[MessageTemplate]:
        message_templates = await self.select_all(message_type=message_type.value)
        return [
            MessageTemplate(**message_template)
            for message_template in message_templates
        ]

    async def delete_message_template(self, message_template_name: str):
        await self.delete(name=message_template_name)
