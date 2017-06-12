import asyncio
import discord
import subprocess
from discord import Game
from time import gmtime, strftime
import SECRETS


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
    if message.content.startswith("!start"):
        print(strftime("[%d.%m.%Y %H:%M:%S]", gmtime()) + " [COMMAND] \"" + message.content + "\" by " + message.author.name)
        if message.server.get_member("272336949841362944").status.__str__() != "offline":
            text = "zekroBot is currently online. Please dont start the bot if its still online.\nIf zekroBot is not reaction to commands, please use `!restart` command."
            yield from client.send_message(message.channel, embed=discord.Embed(description=text, colour=discord.Color.red()))
        else:
            subprocess.Popen(["bash", "start.sh"])
            yield from client.send_message(message.channel, embed=discord.Embed(description="Starting zekroBot...", colour=discord.Color.green()))

    if message.content.startswith("!restart"):
        print(strftime("[%d.%m.%Y %H:%M:%S]", gmtime()) + " [COMMAND] \"" + message.content + "\" by " + message.author.name)
        subprocess.Popen(["bash", "restart.sh"])
        yield from client.send_message(message.channel, embed=discord.Embed(description="Restarting zekroBot...", colour=discord.Color.green()))

    if message.content.startswith("!help"):
        print(strftime("[%d.%m.%Y %H:%M:%S]", gmtime()) + " [COMMAND] \"" + message.content + "\" by " + message.author.name)
        text = "**This bot is just here for assistance for zekroBot.**\n\n" \
               "Is the zekroBot is gone **offline**, use command `!start` to get him back alive.\n\n" \
               "Is there a bug, music bot is not running nominal or something else is stuck, use command `!restart` to restart zekroBot.\n" \
               "*In case of abuse, users will be excluded from usage of this bot!*\n\n\n" \
               "__**Extra commands:**__\n\n" \
               ":white_small_square:  `!invite <BotID>`  -  Send zekro a invite link for your own discord bot"
        yield from client.send_message(message.author, text)
        yield from client.delete_message(message)

    if message.content.startswith("!invite"):
        args = message.content.split(" ")
        if len(args) > 1:
            yield from client.send_message(message.server.get_member("221905671296253953"), embed=discord.Embed(
                title=message.author.name, description="https://discordapp.com/oauth2/authorize?client_id=%s&scope=bot" % args[1]))
            yield from client.send_message(message.author, embed=discord.Embed(colour=discord.Color.green(),
                description="Invite link (*https://discordapp.com/oauth2/authorize?client_id=%s&scope=bot*) send to zekro (Server Owner)." % args[1]))
            yield from client.delete_message(message)
        else:
            yield from client.send_message(message.channel, "**COMMAND USAGE:**\n"
                                                            "`!invite <botID>`\n\n"
                                                            "*The bot ID you get from there (Client ID: ...): \n"
                                                            "https://discordapp.com/developers/applications/me*")


client.run(SECRETS.token)