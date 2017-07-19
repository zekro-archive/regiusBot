import discord
import os

description = "Blacklist people that they aren't allowed to use this bot"


def set_list(blacklist):
    if not os.path.isdir("SAVES"):
        os.mkdir("SAVES")
    with open("SAVES/blacklist", "w") as f:
        for m in blacklist:
            f.write(m.id + "\n")


def get_list(server):
    blacklist = []
    if os.path.isfile("SAVES/blacklist"):
        with open("SAVES/blacklist") as f:
            for line in f.readlines():
                memb = discord.utils.get(server.members, id=line.replace("\n", ""))
                blacklist.append(memb)
    return blacklist


def check(member):
    return get_list(member.server).__contains__(member)


async def ex(message, client):
    blacklist = get_list(message.server)
    try:
        victim = message.mentions[0]
    except:
        out = "**BLACKLISTED MEMBERS**\n\n"
        for m in blacklist:
            out += ":white_small_square:   %s\n" % m.name
        await client.send_message(message.channel, embed=discord.Embed(description=out))
        return
    if blacklist.__contains__(victim):
        blacklist.remove(victim)
        await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.orange(), description="%s removed %s from blacklist." % (message.author.mention, victim.mention)))
    else:
        blacklist.append(victim)
        await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description="%s added %s to blacklist." % (message.author.mention, victim.mention)))
    set_list(blacklist)
