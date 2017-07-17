import subprocess
import discord
import perms
import STATICS


description = "Restart zekro bot"


async def ex(message, client):
    if not perms.check(message.author):
        await client.send_message(message.channel, embed=discord.Embed(color=discord.Color.red(), description=("Sorry, but you need to have role `%s` to use this command!" % STATICS.PERMS_ROLE_1)))
    else:
        subprocess.Popen(["bash", "restart.sh"])
        await client.send_message(message.channel, embed=discord.Embed(description="Restarting zekroBot...",
                                                                       colour=discord.Color.green()))
