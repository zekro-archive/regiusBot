import os

import discord
import requests

from utils import functions

description = "Show bot log"

perm = 2


async def ex(message, client):
    if not os.path.isfile("screenlog.0"):
        await client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(),
                                                                       description="File `screenlog.0` does not exist!"))
    else:
        with open("screenlog.0") as f:
            lines = f.readlines()

        log_full = ""
        for string in lines:
            log_full += string

        if len(lines) > 10:
            lines = lines[len(lines) - 10:len(lines)]

        log = ""
        for string in lines:
            log += string

        message_send = await client.send_message(message.channel, embed=discord.Embed(
            description="Uploading log to pastebin.com ..."))

        params = {"api_option": "paste", "api_dev_key": functions.get_settings()["secrets"]["pastebin"], "api_paste_code": log_full,
                  "api_paste_private": "1", "api_paste_expire_date": "10M"}
        paste = requests.post("https://pastebin.com/api/api_post.php", data=params).text.replace(
            "https://pastebin.com/", "https://pastebin.com/raw/")

        await client.delete_message(message_send)
        await client.send_message(message.channel,
                                  "**Log of `screenlog.0`**\n*Full log file here: " + paste + "*\n\n" + "```" + log + "```")
