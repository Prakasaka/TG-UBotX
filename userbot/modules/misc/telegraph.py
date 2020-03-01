# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Copyright (C) 2020-2069 The authorship

#This Module Originally Created by @SpecHide https://github.com/SpEcHiDe/UniBorg/blob/master/stdplugins/telegraph.py

from telethon import events
import os
from PIL import Image
from asyncio import sleep
from datetime import datetime
from telegraph import Telegraph, upload_file, exceptions
from userbot import (TELEGRAPH_SHORT_NAME, TEMP_DOWNLOAD_DIRECTORY, BOTLOG_CHATID, bot)
from ..help import add_help_item
from userbot.events import register

telegraph = Telegraph()
r = telegraph.create_account(short_name=TELEGRAPH_SHORT_NAME)
auth_url = r["auth_url"]


@register(outgoing=True, pattern="^.telegraph (media|text)$")
async def telegraphs(graph):
    """ For .telegraph command, upload media & text to telegraph site. ""
    await graph.edit("Uploading... \nPlease wait...")
    await sleep(1.5)
    await graph.delete()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if graph.reply_to_msg_id:
        start = datetime.now()
        r_message = await graph.get_reply_message()
        input_str = graph.pattern_match.group(1)
        if input_str == "media":
            downloaded_file_name = await bot.download_media(
                r_message,
                TEMP_DOWNLOAD_DIRECTORY
            )
            end = datetime.now()
            ms = (end - start).seconds
            await graph.edit("Downloaded to {} in {} seconds.".format(downloaded_file_name, ms))
            if downloaded_file_name.endswith((".webp")):
                resize_image(downloaded_file_name)
            try:
                start = datetime.now()
                media_urls = upload_file(downloaded_file_name)
            except exceptions.TelegraphException as exc:
                await graph.edit("ERROR: " + str(exc))
                os.remove(downloaded_file_name)
            else:
                end = datetime.now()
                ms_two = (end - start).seconds
                os.remove(downloaded_file_name)
                await graph.edit("Uploaded to https://telegra.ph{} in {} seconds.".format(media_urls[0], (ms + ms_two)), link_preview=True)
        elif input_str == "text":
            user_object = await bot.get_entity(r_message.from_id)
            title_of_page = user_object.first_name # + " " + user_object.last_name
            # apparently, all Users do not have last_name field
            page_content = r_message.message
            if r_message.media:
                if page_content != "":
                    title_of_page = page_content
                downloaded_file_name = await bot.download_media(
                    r_message,
                    TEMP_DOWNLOAD_DIRECTORY
                )
                m_list = None
                with open(downloaded_file_name, "rb") as fd:
                    m_list = fd.readlines()
                for m in m_list:
                    page_content += m.decode("UTF-8") + "\n"
                os.remove(downloaded_file_name)
            page_content = page_content.replace("\n", "<br>")
            response = telegraph.create_page(
                title_of_page,
                html_content=page_content
            )
            end = datetime.now()
            ms = (end - start).seconds
            await graph.edit("Pasted to https://telegra.ph/{} in {} seconds.".format(response["path"], ms), link_preview=True)
    else:
        await graph.edit("Reply to a message to get a permanent telegra.ph link. (Inspired by @ControllerBot)")


def resize_image(image):
    im = Image.open(image)
    im.save(image, "PNG")


add_help_item(
    "picture",
    "Misc",
    "upload media & text to telegraph site.",
    """
    `.telegraph (media|text) <with reply any document, image, gif & text>`
    """
)
