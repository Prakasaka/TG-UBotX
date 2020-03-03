# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" UserBot module to welcome the new members """

from ..help import add_help_item
from telethon.utils import pack_bot_file_id
from userbot.modules.sql_helper.welcome_sql import get_current_welcome_settings, add_welcome_setting, rm_welcome_setting
from userbot.events import register
from userbot import bot, LOGS
from telethon.events import ChatAction



@bot.on(ChatAction)
async def welcome_to_chat(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        """user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,"""
        if event.user_joined or event.user_added:
            if cws.should_clean_welcome:
                try:
                    await event.client.delete_messages(
                        event.chat_id,
                        cws.previous_welcome
                    )
                except Exception as e:
                    LOGS.warn(str(e))
                    
            a_user = await event.get_user()
            chat = await event.get_chat()
            me = await event.client.get_me()

            title = chat.title if chat.title else "this chat"
            
            participants = await event.client.get_participants(chat)
            count = len(participants)
            
            current_saved_welcome_message = cws.custom_welcome_message
            
            mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
            my_mention = "[{}](tg://user?id={})".format(me.first_name, me.id)
            
            first = a_user.first_name
            last = a_user.last_name
            if last:
                fullname = f"{first} {last}"
            else:
                fullname = first
                
            username = f"@{a_user.username}" if a_user.username else mention
            
            userid = a_user.id
            
            my_first = me.first_name
            my_last = me.last_name
            if my_last:
                my_fullname = f"{my_first} {my_last}"
            else:
                my_fullname = my_first
            
            my_username = f"@{me.username}" if me.username else my_mention

            current_message = await event.reply(
                current_saved_welcome_message.format(mention=mention, 
                                                     title=title, 
                                                     count=count, 
                                                     first=first, 
                                                     last=last, 
                                                     fullname=fullname, 
                                                     username=username, 
                                                     userid=userid, 
                                                     my_first=my_first, 
                                                     my_last=my_last, 
                                                     my_fullname=my_fullname, 
                                                     my_username=my_username, 
                                                     my_mention=my_mention),
                file=cws.media_file_id
            )


@register(outgoing=True, pattern=r"^.welcome(?: |$)(.*)")
async def save_welcome(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if event.fwd_from:
            return
        msg = await event.get_reply_message()
        input_str = event.pattern_match.group(1)
        if input_str:
            if add_welcome_setting(event.chat_id, input_str, True, 0) is True:
                await event.edit("`Welcome note saved !!`")
            else:
                await event.edit("`I can only have one welcome note per chat !!`")
        elif msg and msg.media:
            bot_api_file_id = pack_bot_file_id(msg.media)
            if add_welcome_setting(event.chat_id, msg.message, True, 0, bot_api_file_id) is True:
                await event.edit("`Welcome note saved !!`")
            else:
                await event.edit("`I can only have one welcome note per chat !!`")
        elif msg.message is not None:
            if add_welcome_setting(event.chat_id, msg.message, True, 0) is True:
                await event.edit("`Welcome note saved !!`")
            else:
                await event.edit("`I can only have one welcome note per chat !!`")


@register(outgoing=True, pattern="^.checkwelcome$")
async def show_welcome(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if event.fwd_from:
            return
        cws = get_current_welcome_settings(event.chat_id)
        if cws:
            await event.edit(f"`The current welcome message is:`\n{cws.custom_welcome_message}")
        else:
            await event.edit("`No welcome note saved here !!`")

@register(outgoing=True, pattern="^.rmwelcome")
async def del_welcome(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        if event.fwd_from:
            return
        if rm_welcome_setting(event.chat_id) is True:
            await event.edit("`Welcome note deleted for this chat.`")
        else:
            await event.edit("`Do I even have a welcome note here ?`")


add_help_item(
    "welcomes",
    "Admin",
    "Welcome the new members.",
    """
`.welcome` <welcome message> or reply to a message with .setwelcome
**Usage:** Saves the message as a welcome note in the chat.

**Available variables for formatting welcome messages:**
`{mention}, {title}, {count}, {first}, {last}, {fullname}, {userid}, {username}, {my_first}, {my_fullname}, {my_last}, {my_mention}, {my_username}`

`.checkwelcome`
**Usage:** Check whether you have a welcome note in the chat.

`.rmwelcome`
**Usage:** Deletes the welcome note for the current chat.
    """
)
