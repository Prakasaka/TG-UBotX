# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# This module originally created by @spechide
# https://github.com/SpEcHiDe/UniBorg/blob/master/stdplugins/create_private_group.py

from telethon.tl import functions, types

from ..help import add_help_item
from userbot.events import register


@register(outgoing=True, pattern="^.create (c|g) (.*)")
async def telegraphs(grop):
    """ For .create command, Creating New Group & Channel """
    type_of_group = grop.pattern_match.group(1)
    group_name = grop.pattern_match.group(2)
    if type_of_group == "g":
        try:
            r = await grop.client(functions.channels.CreateChannelRequest(  # pylint:disable=E0602
                title=group_name,
                about="Welcome",
                megagroup=True
            ))
            created_chat_id = r.chats[0].id
            result = await grop.client(functions.messages.ExportChatInviteRequest(
                peer=created_chat_id,
            ))
            await grop.edit(f"**SuperGroup Created Successfully.\nJoin SuperGroup : ** [{group_name}]({result.link})")
        except Exception as e:  # pylint:disable=C0103,W0703
            await grop.edit(str(e))
    elif type_of_group == "c":
        try:
            r = await grop.client(functions.channels.CreateChannelRequest(  # pylint:disable=E0602
                title=group_name,
                about="Welcome",
                megagroup=False
            ))
            created_chat_id = r.chats[0].id
            result = await grop.client(functions.messages.ExportChatInviteRequest(
                peer=created_chat_id,
            ))
            await grop.edit(f"**Channel Created Successfully.\nJoin Channel : ** [{group_name}]({result.link})")
        except Exception as e:  # pylint:disable=C0103,W0703
            await grop.edit(str(e))
    else:
        await grop.edit("**Wrong Character. Type g for SuperGroup or c for Channel**")

add_help_item(
    "create",
    "Me",
    "Creating new group & channel",
    """
    `.create g`
    **Usage:** Create a private Group.

    `.create c`
    **Usage:** Create a channel.
    """
)
