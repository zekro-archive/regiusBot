from time import gmtime, strftime
import sys

import discord
from discord import Game

import STATICS
from commands import cmd_start, cmd_restart, cmd_invite, cmd_google, cmd_log, cmd_dev, cmd_test, cmd_prefix, cmd_dnd, \
    cmd_github, cmd_say, cmd_pmbc, cmd_mute, cmd_xp, cmd_blacklist, cmd_stream, cmd_info, cmd_video, cmd_botkick, \
    cmd_stats, cmd_user, cmd_exec, cmd_botmsg, cmd_update
from utils import functions, level_system, statistics, userbots, report, perms, rolechange


# Setting up devmode when argument "-dev" entered
DEVMODE = False
if sys.argv.__contains__("-dev"):
    DEVMODE = True
cmd_stream.DEVMODE = DEVMODE
cmd_video.DEVMODE = DEVMODE
STATICS.set_prefix(DEVMODE)
STATICS.set_version()


# Create discord client
client = discord.Client()

# Register command classes with invokes
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
        "mute": cmd_mute,
        "xp": cmd_xp,
        "blacklist": cmd_blacklist,
        "stream": cmd_stream,
        "info": cmd_info,
        "video": cmd_video,
        "botkick": cmd_botkick,
        "stats": cmd_stats,
        "user": cmd_user,
        "userinfo": cmd_user,
        "exec": cmd_exec,
        "botmsg": cmd_botmsg,
        "update": cmd_update,
}


# LISTENER

@client.event
async def on_ready():
    servers = "\n   - ".join([s.name + " (" + s.id + ")" for s in client.servers])
    print("\n-------------------------------------\n"
          "Knecht Bot v.%s\n"
          "discord.py version: %s\n"
          "Prefix: '%s'\n"
          "Devmode: %s\n"
          "Running on servers:\n"
          "   - %s\n"
          "-------------------------------------\n\n" % (STATICS.VERSION, discord.__version__, STATICS.PREFIX, "active" if DEVMODE else "inactive", servers))
    await client.change_presence(game=Game(name=functions.get_members_msg(client)))
    statistics.server = list(client.servers)[0]
    if not DEVMODE:
        statistics.run()


@client.event
async def on_member_join(member):
    await client.change_presence(game=Game(name=functions.get_members_msg(client)))
    await functions.send_join_pm(member, client)
    await userbots.joined(member, client)

@client.event
async def on_member_remove(member):
    await client.change_presence(game=Game(name=functions.get_members_msg(client)))


@client.event
async def on_member_update(before, after):
    if not cmd_botmsg.customenabled:
        await client.change_presence(game=Game(name=functions.get_members_msg(client)))
        rolechange.client = client
        await rolechange.onchange(before, after)

    if not DEVMODE:
        await cmd_dnd.check_status(before, after, client)
        await functions.supp_add(before, after, client)


@client.event
async def on_message(message):
    # await cmd_dnd.test(message, client)
    await cmd_mute.check_mute(message, client)

    if message.channel.is_private and not message.author == client.user:
        report.client = client
        await report.handle(message)

    if message.content.startswith(STATICS.PREFIX) and not message.author == client.user:
        if cmd_blacklist.check(message.author):
            await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description="Sorry, %s, you are blacklisted for this bot so you are not allowed to use this bots commands!" % message.author.mention))
            return
        functions.logcmd(message)
        print(strftime("[%d.%m.%Y %H:%M:%S]", gmtime()) + " [COMMAND] \"" + message.content + "\" by " + message.author.name)
        invoke = message.content.split(" ")[0].replace(STATICS.PREFIX, "", 1)
        command_string = ""
        if invoke == "help":
            for s in cmdmap.keys():
                command_string += ":white_small_square:  **" + s + "**  -  `" + cmdmap.get(s).description + "`\n"
            await client.send_message(message.author, STATICS.helpText + command_string)
        else:
            cmd = cmdmap[invoke]
            try:
                if not perms.checklvl(message.author, cmd.perm):
                    await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(),
                                                                                   description="You are not permitted to use this command!\n\nRequired permission level: **%s** *(yours is %s)*" % (cmd.perm, perms.get(message.author))))
                    return
                else:
                    await cmd.ex(message, client)
            except:
                await cmd.ex(message, client)
                pass


cmd_info.cmdcount = len(cmdmap)

level_system.client = client

if not DEVMODE:
    client.loop.create_task(level_system.level_to_scoreboard())
    client.loop.create_task(level_system.add_time_xp())
    client.loop.create_task(statistics.setServerStats())

level_system.client = client
statistics.client = client

token = functions.get_settings()["secrets"]["discord-dev"] if DEVMODE else functions.get_settings()["secrets"]["discord"]

client.run(token)
