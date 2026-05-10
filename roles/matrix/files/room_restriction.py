from synapse.module_api import ModuleApi, NOT_SPAM
from synapse.module_api.errors import Codes

class RoomCreationRestriction:
    def __init__(self, config: dict, api: ModuleApi):
        self._api = api
        api.register_spam_checker_callbacks(
            user_may_create_room=self.check,
        )

    async def check(self, user_id: str, room_config: dict | None = None):
        # Allow admins to create any room.
        if await self._api.is_user_admin(user_id):
            return NOT_SPAM

        room_config = room_config or {}

        # `room_config` is a subset of the `/createRoom` body; for direct chats
        # Synapse exposes `is_direct` (and typically `invite`) there.
        creation_content = room_config.get("creation_content") or {}
        if not isinstance(creation_content, dict):
            creation_content = {}

        is_direct = bool(room_config.get("is_direct") or creation_content.get("is_direct"))
        preset = room_config.get("preset") or creation_content.get("preset")
        invite = room_config.get("invite") or creation_content.get("invite")

        # Direct / 1:1 chats should be creatable by everyone.
        if is_direct:
            if isinstance(invite, list) and len(invite) != 1:
                return Codes.FORBIDDEN
            return NOT_SPAM

        # Fallback for older/atypical clients: allow only a single invitee in
        # a "private chat" preset.
        if (
            preset in ("private_chat", "trusted_private_chat")
            and isinstance(invite, list)
            and len(invite) == 1
        ):
            return NOT_SPAM

        return Codes.FORBIDDEN
