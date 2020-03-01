# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import sys
import io

from random import randint
from asyncio import sleep
from os import execl

from ..help import add_help_item
from userbot import BOTLOG, BOTLOG_CHATID, MAX_MESSAGE_SIZE_LIMIT, bot
from userbot.events import register


@register(outgoing=True, pattern="^.creator$")
async def creator(e):
    await e.edit(r"Here is TG-UBotX's Creator : [Hitalo](https://t.me/HitaloSama)")


@register(outgoing=True, pattern="^\.repo$")
async def repo_is_here(wannasee):
    """ For .repo command, just returns the repo URL. """
    await wannasee.edit(
        "Click [Here](https://github.com/HitaloKun/TG-UBotX) To Open TG-UBotX's Repository.")


@register(outgoing=True, pattern="^.uwiki$")
async def reedme(e):
    await e.edit(
        "**Our wiki and other useful links::**\n"
        "\n[TG-UBotX - Wiki](https://tg-ubotx.github.io/#/)"
        "\n[Setup Guide - GDive](https://telegra.ph/How-To-Setup-GDrive-11-02)"
        "\n[News Channel](https://t.me/TGUBotX)")


@register(outgoing=True, pattern="^\.random")
async def randomise(items):
    """ For .random command, get a random item from the list of items. """
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        await items.edit(
            "`2 or more items are required! Check .help random for more info.`"
        )
        return
    index = randint(1, len(itemo) - 1)
    await items.edit("**Query: **\n`" + items.text[8:] + "`\n**Output: **\n`" +
                     itemo[index] + "`")


@register(outgoing=True, pattern="^\.sleep( [0-9]+)?$")
async def sleepybot(time):
    """ For .sleep command, let the userbot snooze for a few second. """
    message = time.text
    if " " not in time.pattern_match.group(1):
        await time.reply("Syntax: `.sleep [seconds]`")
    else:
        counter = int(time.pattern_match.group(1))
        await time.edit("`I am sulking and snoozing....`")
        await sleep(2)
        if BOTLOG:
            await time.client.send_message(
                BOTLOG_CHATID,
                "You put the bot to sleep for " + str(counter) + " seconds",
            )
        await sleep(counter)
        await time.edit("`OK, I'm awake now.`")


@register(outgoing=True, pattern="^\.shutdown$")
async def killdabot(event):
    """ For .shutdown command, shut the bot down."""
    await event.edit("`Goodbye *Windows XP shutdown sound*....`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                        "Bot shut down")
    await bot.disconnect()


@register(outgoing=True, pattern="^\.restart$")
async def killdabot(event):
    await event.edit("`Hold tight! I just need a second to be back up....`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                                       "Bot Restarted")
    await event.client.disconnect()
    # Spin a new instance of bot
    execl(sys.executable, sys.executable, *sys.argv)
    # Shut the existing one down
    exit()


# Copyright (c) Gegham Zakaryan | 2019
@register(outgoing=True, pattern="^\.repeat (.*)")
async def repeat(rep):
    cnt, txt = rep.pattern_match.group(1).split(' ', 1)
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)


@register(outgoing=True, pattern="^\.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    if len(the_real_message) > MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(the_real_message)) as out_file:
            out_file.name = "json.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                reply_to=reply_to_id
            )
            await event.delete()
    else:
        await event.edit(f"`{the_real_message}`")


add_help_item(
    "misc",
    "Misc",
    "Some misc commands.",
    """
    `.raw`
    **Usage:** Get detailed JSON-like formatted data about replied message.

    `.random` <item1> <item2> ... <itemN>
    **Usage:** Get a random item from the list of items.

    `.repeat` <no.> <text>
    **Usage:** Repeats the text for a number of times. Don't confuse this with spam tho.

    `.restart`
    **Usage:** Restarts the bot!

    `.uwiki`
    **Usage:** Provides the UBotX wiki

    `.creator`
    **Usage:** Know who created this awesome userbot!

    `.repo`
    **Usage:** If you are curious what makes the userbot work, this is what you need.

    `.shutdown`
    **Usage:** Sometimes you need to shut down your bot. Sometimes you just hope to
    hear Windows XP shutdown sound... but you don't.

    `.sleep` <seconds>
    **Usage:** Userbots get tired too. Let yours snooze for a few seconds.
    """
)
