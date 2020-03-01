# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Ported from SpEcHiDe UniBorg

from telethon import functions

from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern=r"^\.invite(?: |$)(.*)")
async def _(event):
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await event.edit("`.invite` users to a chat, not to a Private Message.")
    elif:
        if not event.is_channel and event.is_group:
            # https://lonamiwebs.github.io/Telethon/methods/messages/add_chat_user.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(functions.messages.AddChatUserRequest(
                        chat_id=event.chat_id,
                        user_id=user_id,
                        fwd_limit=1000000
                    ))
                    await event.edit(f"{user_id} **Invited Successfully!**")
                except Exception:
                    await event.edit(f"{user_id} Does't Want Anyone Add Him To This Group")
        else:
            # https://lonamiwebs.github.io/Telethon/methods/channels/invite_to_channel.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(functions.channels.InviteToChannelRequest(
                        channel=event.chat_id,
                        users=[user_id]
                    ))
                    await event.edit(f"{user_id} **Invited Successfully!**")
                except Exception:
                    await event.edit(f"{user_id} Does't Want Anyone Add Him To This Group")


add_help_item(
    "invite",
    "Admin",
    "Invite users to a chat, not to a private message.",
    """
    `.invite`
    """
)
