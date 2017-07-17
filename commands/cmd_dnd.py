import discord
import time

import STATICS

description = "Mark yourself as 'do not disturb' or 'afk'."

map_dnd = []
map_afk = []


async def ex(message, client):

    author = message.author
    if message.content.startswith(STATICS.PREFIX + "dnd"):

        if map_afk.__contains__(author):
            msg = await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=("%s, you just set your status to 'afk'." % author.mention)))
            time.sleep(3)
            await client.delete_message(msg)

        elif not map_dnd.__contains__(author):
            map_dnd.append(author)
            await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.orange(), description=("%s now does not want to be disturbed." % author.mention)))

        else:
            map_dnd.remove(author)
            await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=("%s is now back again." % author.mention)))


    if message.content.startswith(STATICS.PREFIX + "afk"):

        if map_dnd.__contains__(author):
            msg = await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=("%s, you just set your status to 'do not disturb'." % author.mention)))
            time.sleep(3)
            await client.delete_message(msg)

        elif not map_afk.__contains__(author):
            map_afk.append(author)
            await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.orange(), description=("%s is now afk" % author.mention)))

        else:
            map_afk.remove(author)
            await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=("%s is now back again." % author.mention)))

    await client.delete_message(message)


async def test(message, client):

    if message.author.id == "323587299617275904":
        return

    for m in message.mentions:
        if map_dnd.__contains__(m):
            await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.orange(), description=("%s does not want to be disturbed currently." % m.mention)))
        elif map_afk.__contains__(m):
            await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.orange(), description=("%s is currently afk." % m.mention)))


async def check_status(before, after, client):

    channel = discord.utils.get(after.server.channels, name="botlog")

    if before.status.__str__() != "dnd" and after.status.__str__() == "dnd":
        if (not map_dnd.__contains__(after)) and (not map_afk.__contains__(after)):
            map_dnd.append(after)
            await client.send_message(channel, embed=discord.Embed(color=discord.Color.orange(), description=("%s now does not want to be disturbed." % after.mention)))

    elif before.status.__str__() == "dnd" and after.status.__str__() != "dnd":
        if map_dnd.__contains__(after):
            map_dnd.remove(after)
            await client.send_message(channel, embed=discord.Embed(color=discord.Color.green(), description=("%s is now back again." % after.mention)))

