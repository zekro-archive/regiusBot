import threading

import discord
from discord import Server

description = "Just for zekro for testing purposes."


def ex(message, client):

    print("TEST")

    if not message.author.id == "221905671296253953":
        yield from client.send_message(message.author, embed=discord.Embed(colour=discord.Color.red(),
                                                                           description=("Sorry, but this command is only allowed to be executed by %s (my Owner ^^)." % discord.utils.get(message.server.members, id="221905671296253953").mention)))
        return

