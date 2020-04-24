#This module originally created by @SpecHide https://github.com/SpEcHiDe/UniBorg

# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module for Forwarding PM to BotLog Group. """


import asyncio
from telethon import events
from telethon.tl import functions, types
from userbot.events import register
from userbot import BOTLOG, BOTLOG_CHATID, LOGS


NO_PM_LOG_USERS = []
GROUP = -1001150051137


@register(incoming=True, disable_edited=True)
async def monito_p_m_s(event):
    sender = await event.get_sender()
    if event.is_private and not (await event.get_sender(GROUP)).bot:
        chat = await event.get_chat()
        if chat.id not in NO_PM_LOG_USERS and chat.id:
            try:
                e = await event.client.get_entity(int(BOTLOG_CHATID))
                fwd_message = await event.client.forward_messages(
                    e,
                    event.message,
                    silent=True
                )
            except Exception as e:
                LOGS.warn(str(e))
