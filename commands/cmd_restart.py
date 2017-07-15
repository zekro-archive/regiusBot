import subprocess
import discord


description = "Restart zekro bot"


async def ex(message, client):
    subprocess.Popen(["bash", "restart.sh"])
    await client.send_message(message.channel, embed=discord.Embed(description="Restarting zekroBot...",
                                                                   colour=discord.Color.green()))
