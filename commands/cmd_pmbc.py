import discord
from discord import Embed

import STATICS
from commands import cmd_github


description = "Null"


def ex(message, client):

    if message.author != message.server.owner:
        yield from client.delete_message(message)
        return

    links = cmd_github.get_links()
    count = 0

    for m in message.server.members:
        count += 1
        if not links.__contains__(m.id) and not m.bot:
            yield from client.send_message(m, message.content.replace(STATICS.PREFIX + "pmbc ", ""))

    yield from client.send_message(message.channel, embed=Embed(color=discord.Color.green(), description=("Send private message to `%s` users." % count)))