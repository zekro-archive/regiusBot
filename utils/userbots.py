from commands import cmd_invite
import discord
from utils import functions, gspread_api


client = None

savefile = "SAVES/userbots.txt"


def _get_member(uid, server):
    return discord.utils.get(server.members, id=uid)


def get_botlist(server):
    g = gspread_api.Settings("dd_saves", 3)
    temp = g.get_dict()
    out = {}

    for k, v in temp.items():
        bot = _get_member(k, server)
        user = _get_member(v, server)
        if bot is not None and user is not None:
            out[bot] = user
    return out


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
        g = gspread_api.Settings("dd_saves", 3)
        botlist[member] = owner
        g.set_dict(
            dict([(k.id, v.id) for k, v in botlist.items()])
        )

    await client.add_roles(member, discord.utils.get(member.server.roles, name="User Bots"))
    await client.change_nickname(member, "🤖 %s (%s)" % (member.name, owner.name if owner is not None else "Null"))
    invite_receivers = [discord.utils.get(member.server.members, id=uid) for uid in functions.get_settings()["roles"]["invite-receivers"]]
    for u in invite_receivers:
        await client.send_message(u, embed=discord.Embed(color=discord.Color.green(), description="Bot %s got accepted on the server." % member.mention))
    if owner is not None:
        await client.add_roles(owner, [r for r in member.server.roles if r.name == "Bot Owner"][0])
        await client.send_message(owner, embed=discord.Embed(color=discord.Color.orange(), description="**Your bot was successfully added on the server!**\n\nPlease use the command `!prefix` to set the bots prefix.\nPlease check before if your prefix is free with `!prefix list` and then assing to your bot a free prefix."))
