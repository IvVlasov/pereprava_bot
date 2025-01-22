from bot.constants.base import AppStringEnum


class ChatMemberStatus(AppStringEnum):
    CREATOR = "creator"
    ADMINISTRATOR = "administrator"
    MEMBER = "member"
    RESTRICTED = "restricted"
    LEFT = "left"
    KICKED = "kicked"
