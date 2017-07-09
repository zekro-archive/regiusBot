import os
from pathlib import Path
import discord
import time
from discord import Server

import STATICS


description = "Register bot prefixes running in this server"

help = "**USAGE:**\n" \
       ":white_small_square:  `!prefix list`\n" \
       ":white_small_square:  `!prefix add <ID of bot> <prefix>`\n" \
       ":white_small_square:  `!prefix edit <ID of bot> <new prefix>`\n" \
       ":white_small_square:  `!prefix remove <ID of bot>`\n" \
       ":white_small_square:  `!prefix test <prefix>`\n"


def ex(message, client):

    args = message.content.replace(STATICS.PREFIX + "prefix", "")[1:].split(" ")

    file = "prefixes.txt"

    if args[0] == "":
        yield from client.send_message(message.channel, embed=discord.Embed(description=help, colour=discord.Color.red()))
        return


    if args[0] == "add":

        if len(args) < 3:
            yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description=help))
            return

        bot = discord.utils.get(message.server.members, id=args[1])

        try:
            if not bot.bot:
                yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description="Please enter a valid ID of a bots user account."))
                return
        except:
            yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(),description="Please enter a valid ID of a bots user account."))
            return

        if Path(file).is_file():
            readout = {}
            for line in open(file).readlines():
                readout[line.split(":")[1].replace("\n", "")] = line.split(":")[0]
            if readout.keys().__contains__(args[2]):
                yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description="Entered prefix is just uses! Please change prefix settings in your bot!"))
                return

        w = open(file, "a")
        w.write(args[1] + ":" + args[2] + "\n")
        w.close()
        yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.green(), description="Assigned prefix `%s` to bot %s." % (args[2], bot.mention)))


    if args[0] == "edit":

        if not message.author == message.server.owner:
            msg = yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description=("Sorry, but only the server owner (%s) is allowed to use this command." % message.server.owner.mention)))
            yield from client.delete_message(message)
            time.sleep(5)
            yield from client.delete_message(msg)
            return


        if len(args) < 3:
            yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description=help))
            return

        bot = discord.utils.get(message.server.members, id=args[1])

        try:
            if not bot.bot:
                yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description="Please enter a valid ID of a bots user account."))
                return
        except:
            yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(),description="Please enter a valid ID of a bots user account."))
            return

        before = ""
        if Path(file).is_file():
            readout = {}
            for line in open(file).readlines():
                readout[line.split(":")[0]] = line.split(":")[1].replace("\n", "")
            if readout.keys().__contains__(args[1]):
                before = readout[args[1]]
                readout[args[1]] = args[2]
                os.remove(file)
                w = open(file, "w")
                for k in readout.keys():
                    w.write(k + ":" + readout[k] + "\n")
                w.close()

        yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.green(), description="Changed prefix from `%s` to `%s` of bot %s." % (before, args[2], bot.mention)))


    if args[0] == "remove":

        if not message.author == message.server.owner:
            msg = yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description=("Sorry, but only the server owner (%s) is allowed to use this command." % message.server.owner.mention)))
            yield from client.delete_message(message)
            time.sleep(5)
            yield from client.delete_message(msg)
            return

        if len(args) < 2:
            yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description=help))
            return

        bot = discord.utils.get(message.server.members, id=args[1])

        try:
            if not bot.bot:
                yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description="Please enter a valid ID of a bots user account."))
                return
        except:
            yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(),description="Please enter a valid ID of a bots user account."))
            return

        if Path(file).is_file():
            readout = {}
            for line in open(file).readlines():
                readout[line.split(":")[0]] = line.split(":")[1].replace("\n", "")
            if readout.keys().__contains__(args[1]):
                del readout[args[1]]
                os.remove(file)
                w = open(file, "w")
                for k in readout.keys():
                    w.write(k + ":" + readout[k] + "\n")
                w.close()

        yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.green(), description="Removed entry of Bot %s." % (bot.mention)))


    if args[0] == "list":

        out = "**Registered bot prefixes:**\n\n"

        for line in open(file).readlines():
            out += ":white_small_square:  **%s** (%s)  -  `%s`\n" % (discord.utils.get(message.server.members, id=line.split(":")[0]).name, discord.utils.get(message.server.members, id=line.split(":")[0]).mention, line.split(":")[1])
        yield from client.send_message(message.channel, embed=discord.Embed(description=out))


    if args[0] == "test":

        if len(args) < 2:
            yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description=help))
            return

        if not Path(file).is_file():
            yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description="There are no prefixes saved yet.\n\nRegister your prefix with\n`!prefix register <ID of bot> <prefix>`"))
            return

        readout = {}
        for line in open(file).readlines():
            readout[line.split(":")[1].replace("\n", "")] = line.split(":")[0]

        if readout.keys().__contains__(args[1]):
            yield from client.send_message(message.channel, embed=discord.Embed(description=("Prefix `%s` ist just used by %s." % (args[1], discord.utils.get(message.server.members, id=readout.get(args[1])).mention))))
        else:
            yield from client.send_message(message.channel, embed=discord.Embed(description=("Prefix `%s` is currently not used by any bot on this server." % args[1])))