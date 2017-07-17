import statistics
from time import gmtime, strftime
import sys

import discord
from discord import Game

import functions
import SECRETS
import STATICS
from commands import cmd_start, cmd_restart, cmd_invite, cmd_google, cmd_log, cmd_dev, cmd_test, cmd_prefix, cmd_dnd, \
    cmd_github, cmd_say, cmd_pmbc, cmd_mute
import level_system


DEVMODE = False
if sys.argv.__contains__("-dev"):
    DEVMODE = True

client = discord.Client()

cmdmap = {
            "lmgtfy": cmd_google,
            "invite": cmd_invite,
            "log": cmd_log,
            "restart": cmd_restart,
            "start": cmd_start,
            "dev": cmd_dev,
            "prefix": cmd_prefix,
            "dnd": cmd_dnd,
            "afk": cmd_dnd,
            "github": cmd_github,
            "git": cmd_github,
            "say": cmd_say,
            "test": cmd_test,
            "pmbc": cmd_pmbc,
            "mute": cmd_mute
        }


# LISTENER

@client.event
async def on_ready():
    print("BOT STARTED\n-----------------")
    await client.change_presence(game=Game(name=functions.get_members_msg(client)))
    statistics.server = list(client.servers)[0]
    if not DEVMODE:
        statistics.start()


@client.event
async def on_member_join(member):
    await client.change_presence(game=Game(name=functions.get_members_msg(client)))
    await functions.send_join_pm(member, client)


@client.event
async def on_member_remove(member):
    await client.change_presence(game=Game(name=functions.get_members_msg(client)))


@client.event
async def on_member_update(before, after):
    await client.change_presence(game=Game(name=functions.get_members_msg(client)))
    if not DEVMODE:
        await cmd_dnd.check_status(before, after, client)
        await functions.supp_add(before, after, client)


@client.event
async def on_message(message):
    await cmd_dnd.test(message, client)
    await cmd_mute.check_mute(message, client)
    if message.content.startswith(STATICS.PREFIX) and not message.author == client.user:
        functions.logcmd(message)
        print(strftime("[%d.%m.%Y %H:%M:%S]", gmtime()) + " [COMMAND] \"" + message.content + "\" by " + message.author.name)
        invoke = message.content.split(" ")[0].replace(STATICS.PREFIX, "", 1)
        command_string = ""
        if invoke == "help":
            for s in cmdmap.keys():
                command_string += ":white_small_square:  **" + s + "**  -  `" + cmdmap.get(s).description + "`\n"
            await client.send_message(message.author, STATICS.helpText + command_string)
        else:
            await cmdmap.get(invoke).ex(message, client)

level_system.client = client

if not DEVMODE:
    client.loop.create_task(level_system.level_to_scoreboard())
    client.loop.create_task(level_system.add_time_xp())

client.run(SECRETS.token)
