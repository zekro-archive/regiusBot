import discord
import time

from discord import Member, Server

import STATICS

description = "Mark yourself as 'do not disturb' or 'afk'."

map_dnd = []
map_afk = []


def ex(message, client):

    author = message.author

    if message.content.startswith(STATICS.PREFIX + "dnd"):

        if map_afk.__contains__(author):
            msg = yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=("%s, you just set your status to 'afk'." % author.mention)))
            time.sleep(3)
            yield from client.delete_message(msg)

        elif not map_dnd.__contains__(author):
            map_dnd.append(author)
            yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.orange(), description=("%s now does not want to be disturbed." % author.mention)))

        else:
            map_dnd.remove(author)
            yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=("%s is now back again." % author.mention)))


    if message.content.startswith(STATICS.PREFIX + "afk"):

        if map_dnd.__contains__(author):
            msg = yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=("%s, you just set your status to 'do not disturb'." % author.mention)))
            time.sleep(3)
            yield from client.delete_message(msg)

        elif not map_afk.__contains__(author):
            map_afk.append(author)
            yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.orange(), description=("%s is now afk" % author.mention)))

        else:
            map_afk.remove(author)
            yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=("%s is now back again." % author.mention)))

    yield from client.delete_message(message)


def test(message, client):

    if message.author.id == "323587299617275904":
        return

    for m in message.mentions:
        if map_dnd.__contains__(m):
            yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.orange(), description=("%s does not want to be disturbed currently." % m.mention)))
        elif map_afk.__contains__(m):
            yield from client.send_message(message.channel, embed=discord.Embed(color=discord.Color.orange(), description=("%s is currently afk." % m.mention)))


def check_status(before, after, client):

    channel = discord.utils.get(after.server.channels, name="botlog")

    if before.status.__str__() != "dnd" and after.status.__str__() == "dnd":
        if (not map_dnd.__contains__(after)) and (not map_afk.__contains__(after)):
            map_dnd.append(after)
            yield from client.send_message(channel, embed=discord.Embed(color=discord.Color.orange(), description=("%s now does not want to be disturbed." % after.mention)))

    elif before.status.__str__() == "dnd" and after.status.__str__() != "dnd":
        if map_dnd.__contains__(after):
            map_dnd.remove(after)
            yield from client.send_message(channel, embed=discord.Embed(color=discord.Color.green(), description=("%s is now back again." % after.mention)))