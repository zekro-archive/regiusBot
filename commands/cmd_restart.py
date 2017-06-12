import subprocess
import discord


def ex(message, client):
    subprocess.Popen(["bash", "restart.sh"])
    yield from client.send_message(message.channel, embed=discord.Embed(description="Restarting zekroBot...",
                                                                        colour=discord.Color.green()))