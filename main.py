import asyncio
import discord
import subprocess
from discord import Game
from time import gmtime, strftime
import SECRETS
import STATICS


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
        yield from cmd_start(message)

    if message.content.startswith(STATICS.PREFIX + "restart"):
        yield from cmd_restart(message)

    if message.content.startswith(STATICS.PREFIX + "help"):
        yield from cmd_help(message)

    if message.content.startswith(STATICS.PREFIX + "invite"):
        yield from cmd_invite(message)

    if message.content.startswith(STATICS.PREFIX + "lmgtfy"):
        yield from cmd_google(message)


# COMMANDS

def cmd_start(message):
    if message.server.get_member("272336949841362944").status.__str__() != "offline":
        text = "zekroBot is currently online. Please dont start the bot if its still online.\nIf zekroBot is not reaction to commands, please use `!restart` command."
        yield from client.send_message(message.channel,
                                       embed=discord.Embed(description=text, colour=discord.Color.red()))
    else:
        subprocess.Popen(["bash", "start.sh"])
        yield from client.send_message(message.channel, embed=discord.Embed(description="Starting zekroBot...", colour=discord.Color.green()))


def cmd_restart(message):
    subprocess.Popen(["bash", "restart.sh"])
    yield from client.send_message(message.channel, embed=discord.Embed(description="Restarting zekroBot...",
                                                                        colour=discord.Color.green()))


def cmd_help(message):
    yield from client.send_message(message.author, STATICS.helpText)
    yield from client.delete_message(message)


def cmd_invite(message):
    args = message.content.split(" ")
    if len(args) > 1:
        yield from client.send_message(message.server.get_member("221905671296253953"), embed=discord.Embed(
            title=message.author.name,
            description="https://discordapp.com/oauth2/authorize?client_id=%s&scope=bot" % args[1]))
        yield from client.send_message(message.author, embed=discord.Embed(colour=discord.Color.green(),
                                                                           description="Invite link (*https://discordapp.com/oauth2/authorize?client_id=%s&scope=bot*) send to zekro (Server Owner)." %
                                                                                       args[1]))
        yield from client.delete_message(message)
    else:
        yield from client.send_message(message.channel, "**COMMAND USAGE:**\n"
                                                        "`!invite <botID>`\n\n"
                                                        "*The bot ID you get from there (Client ID: ...): \n"
                                                        "https://discordapp.com/developers/applications/me*")


def cmd_google(message):
    args = message.content.replace(STATICS.PREFIX + "lmgtfy ", "").split("|")
    if len(args) < 2:
        yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description="**USAGE:**\n"
                                                                                                                    "`!lmgtfy <link title>|<search query>`"))
    else:
        url = "http://lmgtfy.com/?q=" + args[1].replace(" ", "+")
        em = discord.Embed(title=args[0], url=url)
        yield from client.send_message(message.channel, embed=em)
        yield from client.delete_message(message)


client.run(SECRETS.token)