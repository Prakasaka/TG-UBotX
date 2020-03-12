# Random RGB Sticklet by @PhycoNinja13b
#Exclusive for My personal Repo
#Requirement of this plugin is very high (Kumbhkaran ki aulad) 

import io
import textwrap
from telethon import events

from PIL import Image, ImageDraw, ImageFont
from random import choice

from userbot.events import register

xd = [
    "/app/userbot/fonts/Aisyah-Demo.otf",
    "/app/userbot/fonts/BeachmanScript.ttf",
    "/app/userbot/fonts/Bella Donna Personal Use.ttf",
    "/app/userbot/fonts/Honeymoon Avenue Script Demo.ttf"
]
    

@register(outgoing=True, pattern="^\.font (.*)")
async def sticklet(event):
    
    R = random.randint(0,256)
    G = random.randint(0,256)
    B = random.randint(0,256)
    
    sticktext = event.pattern_match.group(1)

    if not sticktext:
        await event.edit("`I need text to sticklet!`")
        return

    await event.delete()

    sticktext = textwrap.wrap(sticktext, width=10)
    sticktext = '\n'.join(sticktext)

    image = Image.new("RGBA", (512, 512), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    fontsize = 230
    font = ImageFont.truetype(choice(xd), size=fontsize)

    while draw.multiline_textsize(sticktext, font=font) > (512, 512):
        fontsize -= 3
        font = ImageFont.truetype(choice(xd), size=fontsize)

    width, height = draw.multiline_textsize(sticktext, font=font)
    draw.multiline_text(((512-width)/2,(512-height)/2), sticktext, font=font, fill=(R, G, B))

    image_stream = io.BytesIO()
    image_stream.name = "sticker.webp"
    image.save(image_stream, "WebP")
    image_stream.seek(0)

    await event.client.send_file(event.chat_id, image_stream, reply_to=event.message.reply_to_msg_id)
    await event.delete()
