from commands import cmd_invite
import discord
from os import path, mkdir


client = None

savefile = "SAVES/userbots.txt"


def _get_member(uid, server):
    return discord.utils.get(server.members, id=uid)


def get_botlist(server):
    botlist = {}
    if not path.isdir("SAVES"):
        mkdir("SAVES")
    if path.isfile(savefile):
        with open(savefile) as f:
            for line in f.readlines():
                user = _get_member(line.split(":")[1].replace("\n", ""), server)
                bot = _get_member(line.split(":")[0], server)
                if bot is not None and user is not None:
                    botlist[bot] = user
    return botlist



async def joined(member, clt):
    global client
    client = clt

    if not member.bot:
        return

    botlist = get_botlist(member.server)

    if cmd_invite.last_invite is None:
        await client.send_message(discord.utils.get(member.server.channels, name="general"), embed=discord.Embed(color=discord.Color.red(), description="The currently joined bot %s can not be assinged a owner!" % member.mention))

    owner = cmd_invite.last_invite
    if owner is not None:
        botlist[member] = owner
        with open(savefile, "w") as f:
            for k, v in botlist.items():
                print(k.name, v.name)
                f.write("%s:%s\n" % (k.id, v.id))

    await client.add_roles(member, discord.utils.get(member.server.roles, name="User Bots"))
    await client.change_nickname(member, "🤖 %s (%s)" % (member.name, owner.name if owner is not None else "Null"))
    if owner is not None:
        await client.add_roles(owner, [r for r in member.server.roles if r.name == "Bot Owner"][0])
        await client.send_message(owner, embed=discord.Embed(color=discord.Color.orange(), description="**Your bot was successfully added on the server!**\n\nPlease use the command `!prefix` to set the bots prefix.\nPlease check before if your prefix is free with `!prefix list` and then assing to your bot a free prefix."))
