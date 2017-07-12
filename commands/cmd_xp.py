import discord
from discord import Embed

import level_system


description = ""


def ex(message, client):
    if len(list(message.mentions)) > 0:
        member = message.mentions[0]
        xp = level_system.get_xp(member)
        yield from client.send_message(message.channel, embed=Embed(color=discord.Color.gold(),
                                                                    description=("**%s:**  **`%s XP`**" % (member.name, xp))))

    else:
        table = level_system.get_table()
        out = ""
        for memb_id in table:
            out += "**%s:**  **`%s XP`** \n" % (discord.utils.get(message.server.members, id=memb_id).name, table[memb_id])
        yield from client.send_message(message.channel, "**XP LIST**\n\n" + out)