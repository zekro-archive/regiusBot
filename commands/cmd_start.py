import subprocess
import discord


description = "Start zekro bot if it went offline"


def ex(message, client):
    if message.server.get_member("272336949841362944").status.__str__() != "offline":
        text = "zekroBot is currently online. Please dont start the bot if its still online.\nIf zekroBot is not reaction to commands, please use `!restart` command."
        yield from client.send_message(message.channel,
                                       embed=discord.Embed(description=text, colour=discord.Color.red()))
    else:
        subprocess.Popen(["bash", "start.sh"])
        yield from client.send_message(message.channel, embed=discord.Embed(description="Starting zekroBot...", colour=discord.Color.green()))