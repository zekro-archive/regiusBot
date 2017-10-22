import subprocess
import discord


description = "Restart zekro bot"

perm = 3

async def ex(message, client):

    subprocess.Popen(["bash", "restart.sh"])
    await client.send_message(message.channel, embed=discord.Embed(description="Restarting zekroBot...",
                                                                   colour=discord.Color.green()))
