import asyncio
import discord
from utils import userbots

description = "Just for zekro for testing purposes."


async def ex(message, client):

    print("TEST")

    if not message.author.id == "221905671296253953":
        await client.send_message(message.author, embed=discord.Embed(colour=discord.Color.red(),
                                                                      description=("Sorry, but this command is only allowed to be executed by %s (my Owner ^^)." % discord.utils.get(message.server.members, id="221905671296253953").mention)))
        return

    em = discord.Embed(description="TEST")
    em.set_author(name="zekro", icon_url="https://images-ext-2.discordapp.net/external/XJ8JyZNEFUR5MCaA_5qNJDUdkJeogr65F3rpg9SYt2g/https/cdn.discordapp.com/avatars/221905671296253953/9e46d5f495a49a088b1f22224357528e.png?width=72&height=72")
    await client.send_message(message.channel, embed=em)
