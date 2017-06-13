import asyncio
from time import gmtime, strftime

import discord
from discord import Game

import SECRETS
import STATICS
from commands import cmd_help, cmd_start, cmd_restart, cmd_invite, cmd_google, cmd_log

client = discord.Client()


# LISTENER

@client.event
@asyncio.coroutine
def on_ready():
    print("BOT STARTED\n-----------------")
    members = discord.utils.get(client.servers, id="307084334198816769").member_count
    yield from client.change_presence(game=Game(name="%s members | !help" % members))


@client.event
@asyncio.coroutine
def on_member_join(member):
    members = discord.utils.get(client.servers, id="307084334198816769").member_count
    yield from client.change_presence(game=Game(name="%s members | !help" % members))


@client.event
@asyncio.coroutine
def on_member_remove(member):
    members = discord.utils.get(client.servers, id="307084334198816769").member_count
    yield from client.change_presence(game=Game(name="%s members | !help" % members))


@client.event
@asyncio.coroutine
def on_message(message):
    if message.content.startswith(STATICS.PREFIX):
        print(strftime("[%d.%m.%Y %H:%M:%S]", gmtime()) + " [COMMAND] \"" + message.content + "\" by " + message.author.name)

    if message.content.startswith(STATICS.PREFIX + "start"):
        yield from cmd_start.ex(message, client)

    if message.content.startswith(STATICS.PREFIX + "restart"):
        yield from cmd_restart.ex(message, client)

    if message.content.startswith(STATICS.PREFIX + "help"):
        yield from cmd_help.ex(message, client)

    if message.content.startswith(STATICS.PREFIX + "invite"):
        yield from cmd_invite.ex(message, client)

    if message.content.startswith(STATICS.PREFIX + "lmgtfy"):
        yield from cmd_google.ex(message, client)

    if message.content.startswith(STATICS.PREFIX + "log"):
        yield from cmd_log.ex(message, client)


client.run(SECRETS.token)