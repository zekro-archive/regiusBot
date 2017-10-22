from utils import perms
from discord import Embed, Color
import requests
from os import mkdir, remove, path
import sys


description = "Execute online python scripts. (Only for zekro)"


async def ex(message, client):

    author = message.author
    channel = message.channel
    if not perms.check_if_zekro(author):
        await client.send_message(author, embed=Embed(color=Color.red(), description="Sorry, this command is only available for zekro ;)"))
        await client.delete_message(message)
        return

    args = message.content.split()[1:]
    if len(args) < 1:
        await client.delete_message(message)
        return

    try:
        if not path.isdir("temp"):
            mkdir("temp")
        with open("temp/execute.py", "w") as f:
            f.write("import discord\n\n\n"
                    "CLIENT = None\n"
                    "MESSAGE = None\n\n\n")
            f.write(requests.get(args[0]).text)
        from temp import execute
        execute.CLIENT = client
        execute.MESSAGE = message
        await execute.ex()
        remove("temp/execute.py")
    except:
        client.send_message(channel, embed=Embed(color=Color.red(), title="Exception", description=sys.exc_info()[0]))
        raise

    await client.delete_message(message)
