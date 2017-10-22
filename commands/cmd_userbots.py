import asyncio
import discord
from utils import userbots, gspread_api
from discord import Embed
from commands import cmd_prefix

description = "Just for zekro for testing purposes."


async def ex(message, client):

    server = message.server

    sendmsg = await client.send_message(message.channel, "Collecting data...\n\nYou could take a small coffe that while ;) :coffee:")

    bots = userbots.get_botlist(server)
    pres = gspread_api.Settings("dd_saves", 2).get_dict()

    msg = ""
    print(pres)
    for b, o in bots.items():
        prefix = pres[b.id] if b.id in pres.keys() else "[NOT REGISTERED!]"
        msg += "%s\nby %s\n```Prefix:  %s```\n\n" % (b.mention, o.mention, prefix)

    print(len(msg))
    await client.delete_message(sendmsg)
    await client.send_message(message.channel, "*On mobile devices, this view will be really bugy. Please use a desktop device for this command!*\n\n" + msg)