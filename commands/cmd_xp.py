import discord
from discord import Embed

import level_system


description = ""


async def ex(message, client):
    if len(list(message.mentions)) > 0:
        member = message.mentions[0]
        xp = level_system.get_xp(member)
        await client.send_message(message.channel, embed=Embed(color=discord.Color.gold(),
                                                               description=("**%s:**  **`%s XP`**" % (member.name, xp))))

    else:
        table = level_system.get_table()
        out = ""
        for memb_id in table[:20]:
            out += "**%s:**  **`%s XP`** \n" % (discord.utils.get(message.server.members, id=memb_id).name, table[memb_id])
        await client.send_message(message.channel, "**XP LIST (Top 10)**\n\n" + out)

