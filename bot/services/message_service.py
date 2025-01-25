from repository.messages import MessagesRepository


class MessageService:
    start_user: str
    start_moderator: str
    message_types: str
    appeal_message: str
    appeal_message_success: str

    async def init_messages(self):
        messages = await MessagesRepository().get_messages()
        for message in messages:
            setattr(self, message.key, message.text)


async def get_message_service() -> MessageService:
    messages = MessageService()
    await messages.init_messages()
    return messages
