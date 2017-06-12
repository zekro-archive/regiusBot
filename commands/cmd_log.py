import os

import discord
import requests

import SECRETS


def ex(message, client):
    if not os.path.isfile("screenlog.0"):
        yield from client.send_message(message.channel, embed=discord.Embed(colour=discord.Color.red(), description="File `screenlog.0` does not exist!"))
    else:
        with open("screenlog.0") as f:
            lines = f.readlines()
        if len(lines) > 10:
            lines = lines[len(lines)-10:len(lines)]
        log = ""
        for string in lines:
            log += string
        message_send = yield from client.send_message(message.channel, embed=discord.Embed(description="Uploading log to pastebin.com ..."))
        params = {"api_option": "paste", "api_dev_key": SECRETS.PASTEBIN_API_TOKEN, "api_paste_code": log, "api_paste_private": "1", "api_paste_expire_date": "10M"}
        paste = requests.post("https://pastebin.com/api/api_post.php", data=params).text.replace("https://pastebin.com/", "https://pastebin.com/raw/")
        yield from client.delete_message(message_send)
        yield from client.send_message(message.channel, "**Log of `screenlog.0`**\n*Full log file here: " + paste + "*\n\n" + "```" + log + "```")