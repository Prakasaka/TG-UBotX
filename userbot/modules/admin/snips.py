# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands for keeping global notes. """

from ..help import add_help_item
from telethon import utils
from telethon.tl import types
from userbot.events import register
from userbot import BOTLOG_CHATID


TYPE_TEXT = 0
TYPE_PHOTO = 1
TYPE_DOCUMENT = 2


@register(outgoing=True, pattern=r"\₹\w*", disable_errors=True)
async def on_snip(event):
    """ Snips logic. """
    try:
        from userbot.modules.sql_helper.snips_sql import get_snip
    except AttributeError:
        return
    name = event.text[1:]
    snip = get_snip(name)
    if snip:
        if snip.snip_type == TYPE_PHOTO:
            media = types.InputPhoto(int(snip.media_id),
                                     int(snip.media_access_hash),
                                     snip.media_file_reference)
        elif snip.snip_type == TYPE_DOCUMENT:
            media = types.InputDocument(int(snip.media_id),
                                        int(snip.media_access_hash),
                                        snip.media_file_reference)
        else:
            media = None

        message_id_to_reply = event.message.reply_to_msg_id

        if not message_id_to_reply:
            message_id_to_reply = None

        await event.client.send_message(event.chat_id,
                                        snip.reply,
                                        reply_to=message_id_to_reply,
                                        file=media)
        await event.delete()


@register(outgoing=True, pattern=r"^\.snip (\w*)")
async def on_snip_save(event):
    """ For .snip command, saves snips for future use. """
    try:
        from userbot.modules.sql_helper.snips_sql import add_snip
    except AtrributeError:
        await event.edit("`Running on Non-SQL mode!`")
        return
    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if not msg:
        await event.edit("`I need something to save as a snip.`")
        return
    else:
        snip = {'type': TYPE_TEXT, 'text': msg.message or ''}
        if msg.media:
            media = None
            if isinstance(msg.media, types.MessageMediaPhoto):
                media = utils.get_input_photo(msg.media.photo)
                snip['type'] = TYPE_PHOTO
            elif isinstance(msg.media, types.MessageMediaDocument):
                media = utils.get_input_document(msg.media.document)
                snip['type'] = TYPE_DOCUMENT
            if media:
                snip['id'] = media.id
                snip['hash'] = media.access_hash
                snip['fr'] = media.file_reference

        success = "**Snip {} successfully. Use** `₹{}` **anywhere to get it**"

        if add_snip(name, snip['text'], snip['type'], snip.get('id'),
                    snip.get('hash'), snip.get('fr')) is False:
            await event.edit(success.format('updated', name))
        else:
            await event.edit(success.format('saved', name))


@register(outgoing=True, pattern=r"^\.snips$")
async def on_snip_list(event):
    """ For .snips command, lists snips saved by you. """
    try:
        from userbot.modules.sql_helper.snips_sql import get_snips
    except AttributeError:
        await event.edit("`Running on Non-SQL mode!`")
        return

    message = "`No snips available right now.`"
    all_snips = get_snips()
    for a_snip in all_snips:
        if message == "`No snips available right now.`":
            message = "**Available snips:**\n"
            message += f" • `₹{a_snip.snip}`\n"
        else:
            message += f" • `₹{a_snip.snip}`\n"

    await event.edit(message)


@register(outgoing=True, pattern=r"^\.remsnip (\w*)")
async def on_snip_delete(event):
    """ For .remsnip command, deletes a snip. """
    try:
        from userbot.modules.sql_helper.snips_sql import remove_snip
    except AttributeError:
        await event.edit("`Running on Non-SQL mode!`")
        return
    name = event.pattern_match.group(1)
    if remove_snip(name) is True:
        await event.edit(f"**Successfully deleted snip:** `{name}`")
    else:
        await event.edit(f"**Couldn't find snip:** `{name}`")


add_help_item(
    "snips",
    "Admin",
    "Similar to notes but global and only you can use",
    """
    `.₹<snip_name>`
    Usage: Gets the specified snip, anywhere.

    `.snip` <name> <data> or reply to a message with .snip <name>
    **Usage:** Saves the message as a snip (global note) with the name. (Works with pics, docs, and stickers too!)

    `.snips`
    **Usage: Gets all saved snips.

    `.remsnip` <snip_name>
    **Usage:** Deletes the specified snip.
    """
)
