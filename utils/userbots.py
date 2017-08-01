from commands import cmd_invite
import discord


client = None


async def joined(member, clt):
    global client
    client = clt
    
    if not member.bot:
        return

    if cmd_invite.last_invite is None:
        await client.send_message(discord.utils.get(member.server.channels, name="general"), embed=discord.Embed(color=discord.Color.red(), description="The currently joined bot %s can not be assinged a owner!" % member.mention))

    owner = cmd_invite.last_invite.name if cmd_invite.last_invite is not None else "None"

    await client.add_roles(member, discord.utils.get(member.server.roles, name="User Bots"))
    await client.change_nickname(member, "🤖 %s (%s)" % (member.name, owner))
    if cmd_invite.last_invite is not None:
        await client.send_message(cmd_invite.last_invite, embed=discord.Embed(color=discord.Color.orange(), description="**Your bot was successfully added on the server!**\n\nPlease use the command `!prefix` to set the bots prefix.\nPlease check before if your prefix is free with `!prefix list` and then assing to your bot a free prefix."))
