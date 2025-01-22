from repository import CrossingRepository, MessageTemplatesRepository


class MessageTemplatesService:
    replacements = {
        "crossing_name": "{имя переправы}",
        "ferry_count": "{число паромов}",
        "date": "{дата}",
        "time": "{время}",
        "route": "{маршрут}",
        "reason": "{причина}",
    }

    def __init__(self, message_template_id: int):
        self.crossing_repository = CrossingRepository()
        self.message_templates_repository = MessageTemplatesRepository()
        self.message_template_id = message_template_id

    async def get_formated_message(self, **kwargs) -> str:
        """
        kwargs: crossing_id, ferry_count, date, time, route
        """
        message_template = (
            await self.message_templates_repository.get_message_template_by_id(
                self.message_template_id
            )
        )
        if "crossing_id" in kwargs:
            crossing = await self.crossing_repository.get_crossing_by_id(
                kwargs["crossing_id"]
            )
            kwargs["crossing_name"] = crossing.name
            del kwargs["crossing_id"]
        text = message_template.template
        return self._reformat_all(text, **kwargs)

    def _reformat_all(self, text: str, **kwargs) -> str:
        for key, value in kwargs.items():
            if key in self.replacements:
                text = text.replace(self.replacements[key], str(value))
        return text
