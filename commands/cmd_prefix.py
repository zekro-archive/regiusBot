from pathlib import Path
import discord

import STATICS


description = "Register bot prefixes running in this server"

help = "**USAGE:**\n" \
       ":white_small_square:  `!prefix list`\n" \
       ":white_small_square:  `!prefix register <ID of bot> <prefix>`\n" \
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

        if not bot.bot:
            yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description="Please enter a valid ID of a bots user account."))
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