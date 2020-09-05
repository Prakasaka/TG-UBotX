from random import choice
from userbot.events import register
from ..help import add_help_item


@register(outgoing=True, pattern=r"^\.sp (.*)")
async def sp_char(e):
    char = e.pattern_match.group(1).lower()
    
    if char:
        char_a = ['@', '4']
        char_rplc = char.replace('a', choice(char_a))
        char_rplc = char_rplc.replace('c', '<')
        char_rplc = char_rplc.replace('e', '3')
        char_rplc = char_rplc.replace('h', '#')
        char_rplc = char_rplc.replace('i', '!')
        char_rplc = char_rplc.replace('o', '0')
        char_rplc = char_rplc.replace('s', '$')
        char_rplc = char_rplc.replace('t', '7')
    
    await e.edit(f"`{char_rplc}`")
    

add_help_item(
    "spcl_char",
    "Fun",
    "u$3rb07",
    """
    `.sp userbot`
    """
)
