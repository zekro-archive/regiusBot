import discord
from os import path, makedirs, remove
import STATICS
import perms


ROLE_NAME = "Supporter"

description = "Mute members on guild in chat"


def get_mutes(server):
    if not path.isdir("SAVES/" + server.id):
        makedirs("SAVES/" + server.id)
    if path.isfile("SAVES/" + server.id + "/mutes"):
        with open("SAVES/" + server.id + "/mutes") as f:
            return [line.replace("\n", "") for line in f.readlines()]
    else:
        return []


def add_mute(member, server):
    mutelist = get_mutes(server)
    mutelist.append(member.id)
    try:
        remove("SAVES/" + server.id + "/mutes")
    except:
        pass
    with open("SAVES/" + server.id + "/mutes", "w") as fw:
        [(lambda x: fw.write(x + "\n"))(line) for line in mutelist]


def rem_mute(member, server):
    mutelist = get_mutes(server)
    mutelist.remove(member.id)
    try:
        remove("SAVES/" + server.id + "/mutes")
    except:
        pass
    with open("SAVES/" + server.id + "/mutes", "w") as fw:
        [(lambda x: fw.write(x))(line) for line in mutelist]


def get_member(id, server):
    return discord.utils.get(server.members, id=id)


async def check_mute(message, client):
    if not message.channel.is_private:
        if get_mutes(message.server).__contains__(message.author.id):
            await client.send_message(message.author, embed=discord.Embed(color=discord.Color.red(), description="Sorry, but you got muted on this server! Contact a supporter to get unmuted."))
            await client.delete_message(message)


async def ex(message, client):
    if not perms.check(message.author):
        await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=("Sorry, but you need to have role `%s` to use this command!" % STATICS.PERMS_ROLE_1)))
    elif message.content.replace(STATICS.PREFIX + "mute ", "") == "list":
        muted_str = "\n".join([get_member(line, message.server).name for line in get_mutes(message.server)]) if len(get_mutes(message.server)) > 0 else "no one"
        await client.send_message(message.channel, embed=discord.Embed(description="**MUTED MEMBERS\n\n**" + muted_str))
    elif len(message.mentions) < 1:
        await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description="Please mention the user you want to mute!"))
    elif get_mutes(message.server).__contains__(message.mentions[0].id):
        rem_mute(message.mentions[0], message.server)
        await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.green(), description=("%s got unmuted by %s." % (message.mentions[0].mention, message.author.mention))))
    else:
        add_mute(message.mentions[0], message.server)
        await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.orange(), description=("%s got muted by %s." % (message.mentions[0].mention, message.author.mention))))
